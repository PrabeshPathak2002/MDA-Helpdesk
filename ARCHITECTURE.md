# System Architecture

## Core Design Principles
This Proof of Concept (PoC) strictly adheres to the architectural best practices outlined by the Mississippi AI Innovation Hub:
1. **Serverless First:** Utilizing AWS Lambda, Amazon Bedrock, and S3 to minimize operational overhead, manage costs effectively, and scale automatically.
2. **Data Governance (RAG):** The system uses a strict Retrieval-Augmented Generation pattern. The LLM cannot use its general training data to answer questions; it is constrained entirely to the provided MDA SOPs and documentation.
3. **Zero Privileged Execution:** The AI cannot execute system changes (e.g., it cannot actively reset an Active Directory password or provision accounts). It acts as a knowledgeable guide and routing agent.

## AWS Infrastructure Components

* **Frontend Interface:** A web-based chat interface where MDA employees interact with the assistant.
* **Amazon API Gateway:** Exposes secure RESTful HTTP endpoints for the frontend to communicate with the backend logic.
* **AWS Lambda (Orchestrator):** The central serverless compute layer. It receives the user's message from the API Gateway, processes it, enforces guardrails, and orchestrates the calls to Amazon Bedrock and the external ticketing system.
* **Amazon Bedrock (Generative AI):** The core intelligence engine. 
    * **Foundation Model:** Utilizes an Amazon Nova model for natural language understanding and generation.
    * **Knowledge Bases:** Manages the RAG pipeline, converting user queries into embeddings and searching the vector store for the correct documentation.
* **Amazon S3 (Data Storage):** Stores the cleaned, Markdown-formatted Standard Operating Procedures (SOPs) and historical FAQs. This serves as the single source of truth for the Bedrock Knowledge Base.
* **Amazon S3 Vectors (Vector Store):** A fully managed vector database within Bedrock used to store the embedded document chunks for fast semantic retrieval.
* **Amazon CloudWatch:** Handles all interaction logging, error tracking, and performance monitoring for auditability and quality assurance.

## Data Flow (The User Journey)

1. **User Input:** An employee types a question (e.g., *"My camera isn't working on Teams"*) into the frontend chat interface.
2. **API Request:** The frontend sends the query via Amazon API Gateway to the orchestration AWS Lambda function.
3. **Retrieval (RAG):** The Lambda function passes the query to the Amazon Bedrock Knowledge Base. Bedrock searches the S3 Vector store for the most relevant Markdown SOPs (e.g., the Teams Troubleshooting guide).
4. **Generation:** Bedrock passes the retrieved documentation and the user's original question to the Foundation Model (Amazon Nova). The model generates a conversational, step-by-step response based *only* on the retrieved text.
5. **Guardrail Check:** If the user's request triggers an escalation rule (e.g., *"Reset my ACE password"* or a desk phone issue), the Lambda function bypasses the RAG generation and returns a hardcoded escalation path to the appropriate human department.
6. **Response:** The Lambda function returns the generated text or escalation instructions back through the API Gateway to the frontend UI.
7. **Ticketing (Optional Flow):** If the user indicates the AI did not solve their problem, the Lambda function executes an API call to the open-source ticketing system to generate a support ticket, attaching the chat transcript for the human IT staff.
