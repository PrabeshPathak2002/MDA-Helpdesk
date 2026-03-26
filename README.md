# MDA AI-Enabled IT Helpdesk Assistant 

**A Proof of Concept (PoC) developed for the Mississippi AI Innovation Hub.**

## Project Overview
IT Helpdesks receive a high volume of routine and repetitive support requests (e.g., password resets, Wi-Fi access, basic troubleshooting). This project is an internal, natural-language AI-powered chatbot designed to serve as a knowledgeable, first-line support tool for Mississippi state government employees. 

By guiding users toward existing self-service resources and answering common questions with high accuracy, this assistant reduces routine ticket volume and allows human IT staff to focus on mission-critical issues.

## Architecture & Tech Stack
This application is completely serverless, ensuring high availability, zero idle server costs, and enterprise-grade security.

* **Frontend:** Vanilla HTML/CSS/JS (Lightweight, single-file deployment).
* **API Layer:** Amazon API Gateway (HTTP API with strict CORS policies).
* **Compute Orchestration:** AWS Lambda (Python 3.12).
* **AI / Generative Foundation:** Amazon Bedrock (Amazon Nova Lite model).
* **Knowledge Base (Vector DB):** Amazon OpenSearch Serverless.
* **Document Storage:** Amazon S3 (Hosting the unified Markdown SOPs).

## Key Enterprise Features
Unlike standard, open-ended LLMs, this Helpdesk Assistant is heavily sandboxed to meet government and enterprise IT security standards:

1.  **Strict RAG Grounding:** The AI operates under a rigid system prompt. It is forbidden from using outside internet knowledge or hallucinating answers. If an issue is not explicitly covered in the MDA documentation, it refuses to answer and routes the user to human IT operations.
2.  **Hardcoded Escalation Routing:** Sensitive requests (e.g., ACE system access, MAGIC, Active Directory account unlocks) trigger an instant, hardcoded guardrail that immediately provides the user with the DFA or Operations phone numbers without consulting the AI.
3.  **Cost-Saving Chit-Chat Interceptor:** Simple pleasantries ("hello", "thank you") are caught by the Lambda function and answered instantly, bypassing Amazon Bedrock to save on token costs and database query latency.
4.  **Markdown Rendering:** The UI natively parses LLM-generated Markdown to provide users with clear, readable, step-by-step lists and bolded text.

## Phase 2 Roadmap
While the core RAG pipeline is functional, future iterations of this product will include:
* **Ticketing System Integration:** Interoperability with IT ticketing systems (like ServiceNow or Jira) to automatically log unresolved issues and return ticket numbers to the chat UI.
* **Audit Logging:** Full interaction logging to DynamoDB for quality assurance and compliance tracking.
* **SSO Authentication:** Locking down the API endpoint using Amazon Cognito to ensure only authenticated state employees can access the assistant.

## Repository Structure
* `index.html`: The complete frontend user interface and API connection logic.
* `lambda_function.py`: The core backend routing, AI prompting, and guardrail logic.
* `data/`: Contains the master Markdown file consisting of the unified MDA Helpdesk SOPs.

## Local Testing & Deployment
To test the frontend locally without triggering CORS policy blocks:
1. Clone this repository to your local machine:
   `git clone https://github.com/PrabeshPathak2002/mda-helpdesk.git`
2. Open the project folder in your preferred IDE.
3. Launch `index.html` using a local web server (e.g., the "Live Server" extension in VS Code, or by running `python -m http.server 8000` in your terminal).
4. Navigate to the local port (e.g., `http://localhost:8000`) in your browser.

## The Team (University of Southern Mississippi)
* **Prabesh Pathak:** AI Orchestration, Backend Development, AWS implementation *(AWS Lambda, Amazon Bedrock System Prompting, API creation, )*
* **Dikesh Shrestha:** Systems Integration *(Environmental Setupt, API integration)*
* **Aavash Tiwari:** Frontend Development *(UI/UX Design)*
