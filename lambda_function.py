import json
import boto3
import os

# Initialize the Bedrock Agent Runtime client
# Ensure the region matches where you built the Knowledge Base
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        # 1. Parse the user input from the API Gateway HTTP request
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
            
        user_query = body.get('query', '')
        
        if not user_query:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'No query provided in the request.'})
            }
            
        # 2. Hardcoded Guardrails / Escalation Check
        # If the user asks about these specific restricted systems, route them to a human immediately.
        user_query_lower = user_query.lower()
        escalation_keywords = ['ace', 'magic', 'desk phone', 'unlock account', 'locked out']
        
        if any(keyword in user_query_lower for keyword in escalation_keywords):
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({
                    'response': 'It looks like you need help with a system that requires specialized administrative access (like ACE, MAGIC, a desk phone, or an Active Directory unlock). Please contact the DFA at 601-359-1343 or Operations at 601-359-2909.',
                    'escalated': True
                })
            }

        # 3. Connect to Bedrock Knowledge Base (The RAG Pipeline)
        # Pulling the specific IDs from your Lambda Environment Variables
        knowledge_base_id = os.environ.get('KNOWLEDGE_BASE_ID') 
        model_arn = os.environ.get('MODEL_ARN', 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0')
        
        # Call the RetrieveAndGenerate API
        response = bedrock_agent_runtime.retrieve_and_generate(
            input={
                'text': user_query
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn
                }
            }
        )
        
        # Extract the generated response text
        generated_text = response['output']['text']
        
        # 4. Return the answer to the Frontend
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # Required for CORS so the frontend can communicate with the backend
            },
            'body': json.dumps({
                'response': generated_text,
                'escalated': False
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error while connecting to the AI Knowledge Base.'})
        }
