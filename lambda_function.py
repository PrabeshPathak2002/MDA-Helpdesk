import json
import boto3
import os

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Connect to the new DynamoDB table
table = dynamodb.Table('MDA-Chat-Sessions')

def lambda_handler(event, context):
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
            
        user_query = body.get('query', '')
        image_base64 = body.get('image_base64')
        user_id = body.get('user_id', 'anonymous-user') # Get the user ID from the frontend
        
        if not user_query and not image_base64:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'No input provided.'})
            }
            
        user_query_lower = user_query.lower().strip()
        
        # --- Guardrails ---
        greetings = ['hi', 'hello', 'hey', 'good morning', 'test']
        if user_query_lower in greetings and not image_base64:
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'response': 'Hello! How can I help you with your IT needs today?', 'escalated': False})
            }

        escalation_keywords = ['ace', 'magic', 'desk phone', 'unlock account', 'locked out']
        if any(keyword in user_query_lower for keyword in escalation_keywords):
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'response': 'It looks like you need help with a system that requires specialized administrative access. Please contact IT Operations at 601-359-2909.', 'escalated': True})
            }

        # --- MEMORY: Lookup previous session in DynamoDB ---
        bedrock_session_id = None
        try:
            db_response = table.get_item(Key={'UserId': user_id})
            if 'Item' in db_response:
                bedrock_session_id = db_response['Item'].get('SessionId')
        except Exception as e:
            print(f"DynamoDB Read Error: {e}")

        # --- Vision Processing ---
        enhanced_query = user_query
        if image_base64:
            vision_response = bedrock_runtime.converse(
                modelId='amazon.nova-lite-v1:0',
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"text": "You are an IT assistant. Please read any error messages, software names, or technical details visible in this screenshot. Be brief."},
                            {"image": {"format": "jpeg", "source": {"bytes": image_base64}}}
                        ]
                    }
                ]
            )
            extracted_image_text = vision_response['output']['message']['content'][0]['text']
            enhanced_query = f"User Question: {user_query}. Screenshot Details: {extracted_image_text}"

        # --- Bedrock RAG Pipeline ---
        knowledge_base_id = os.environ.get('KNOWLEDGE_BASE_ID') 
        model_arn = os.environ.get('MODEL_ARN', 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0')
        
        strict_prompt = """You are the official IT Helpdesk Assistant for the Mississippi Development Authority. 
        Answer using ONLY the search results. Write naturally and conversationally.
        CRITICAL: DO NOT include internal search metadata, tags like "Passage", "Intent", or citation numbers like "[1]" in your final response.
        If a rule requires escalation, state it clearly.
        If a user states they do not have the required credentials, access, or equipment to follow a procedure, DO NOT list the procedure steps. Immediately stop and tell them to contact the Helpdesk.
        If a user mentions an error but does not provide the actual error message or context, DO NOT guess or provide random troubleshooting steps. Ask them to type the specific error message or paste a screenshot.
        NEVER guess or hallucinate steps or passwords. If the user's issue is completely missing from the documents, reply exactly: "I apologize, but I do not have approved documentation for that specific issue. Please contact the IT Operations Helpdesk at 601-359-2909."
        
        Finally, at the very end of your response, you MUST provide exactly two logical follow-up questions the user might want to ask next based on their current issue. Format them exactly like this on a new line:
        SUGGESTIONS: ["First question?", "Second question?"]
        
        Search results: $search_results$
        User query/context: $query$"""
        
        # Build the API payload
        api_kwargs = {
            'input': {'text': enhanced_query},
            'retrieveAndGenerateConfiguration': {
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn,
                    'generationConfiguration': {
                        'promptTemplate': {'textPromptTemplate': strict_prompt}
                    }
                }
            }
        }
        
        # If we found an old session ID, inject it into the payload so Bedrock remembers!
        if bedrock_session_id:
            api_kwargs['sessionId'] = bedrock_session_id
            
        response = bedrock_agent_runtime.retrieve_and_generate(**api_kwargs)
        
        # --- MEMORY: Save the updated session ID back to DynamoDB ---
        new_session_id = response.get('sessionId')
        if new_session_id:
            try:
                table.put_item(Item={'UserId': user_id, 'SessionId': new_session_id})
            except Exception as e:
                print(f"DynamoDB Write Error: {e}")

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'response': response['output']['text'], 'escalated': False})
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error processing the query.'})
        }
