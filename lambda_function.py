import json
import boto3
import os

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
            
        user_query = body.get('query', '')
        image_base64 = body.get('image_base64') # Get the image if it exists
        
        if not user_query and not image_base64:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'No input provided.'})
            }
            
        user_query_lower = user_query.lower().strip()
        
        # --- Chit-Chat & Escalation Guardrails (Unchanged) ---
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

        # --- NEW: Step 1 - Multimodal Vision Processing ---
        # If an image is provided, ask Nova to read the error text off the screen
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
            # Combine the user's typed question with the text extracted from their screenshot
            enhanced_query = f"User Question: {user_query}. Screenshot Details: {extracted_image_text}"


        # --- Step 2: Bedrock RAG Pipeline ---
        knowledge_base_id = os.environ.get('KNOWLEDGE_BASE_ID') 
        model_arn = os.environ.get('MODEL_ARN', 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0')
        
        strict_prompt = """You are the official IT Helpdesk Assistant for the Mississippi Development Authority. 
        Answer using ONLY the search results. If a rule requires escalation, state it clearly.
        NEVER guess or hallucinate steps. If there is no relevant info, reply exactly: "I apologize, but I do not have approved documentation for that specific issue. Please contact the IT Operations Helpdesk at 601-359-2909."
        
        Search results: $search_results$
        User query/screenshot details: $query$"""
        
        response = bedrock_agent_runtime.retrieve_and_generate(
            input={'text': enhanced_query},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn,
                    'generationConfiguration': {
                        'promptTemplate': {'textPromptTemplate': strict_prompt}
                    }
                }
            }
        )
        
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
            'body': json.dumps({'error': 'Internal server error processing the image or connecting to the KB.'})
        }
