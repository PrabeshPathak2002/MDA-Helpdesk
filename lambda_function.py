import json
import boto3
import os

bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    try:
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
            
        user_query_lower = user_query.lower().strip()
        
        # --- Chit-Chat Guardrail ---
        # Instantly reply to pleasantries without charging your Bedrock budget
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'test']
        thanks = ['thanks', 'thank you', 'appreciate it', 'ok', 'okay', 'got it']
        
        if user_query_lower in greetings:
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({
                    'response': 'Hello! How can I help you with your IT needs today?',
                    'escalated': False
                })
            }
            
        if user_query_lower in thanks:
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({
                    'response': "You're welcome! Let me know if you need help with anything else.",
                    'escalated': False
                })
            }

        # --- Escalation Guardrail ---
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

        # --- Bedrock RAG Pipeline ---
        knowledge_base_id = os.environ.get('KNOWLEDGE_BASE_ID') 
        model_arn = os.environ.get('MODEL_ARN', 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0')
        
        # This forces the AI to stay within the bounds of your SOPs
        strict_prompt = """You are the official IT Helpdesk Assistant for the Mississippi Development Authority (MDA). 
        You must answer the user's question using ONLY the information provided in the search results. 
        If the search results mention a rule, requirement, or escalation path related to the user's issue (such as needing administrative privileges to reinstall software), state that clearly.
        However, you must NEVER guess or hallucinate troubleshooting steps that are not explicitly written in the search results.
        If the search results contain absolutely zero relevant information to address the user's request, reply exactly with: "I apologize, but I do not have approved documentation for that specific issue. Please contact the IT Operations Helpdesk at 601-359-2909 for further assistance."
        
        Search results: $search_results$
        User question: $query$"""
        
        response = bedrock_agent_runtime.retrieve_and_generate(
            input={
                'text': user_query
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn,
                    'generationConfiguration': {
                        'promptTemplate': {
                            'textPromptTemplate': strict_prompt
                        }
                    }
                }
            }
        )
        
        generated_text = response['output']['text']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
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
