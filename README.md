# MDA AI-Enabled IT Helpdesk Assistant 

**A Proof of Concept (PoC) developed for the Mississippi AI Innovation Hub.**

## Project Overview
IT Helpdesks receive a high volume of routine and repetitive support requests (e.g., password resets, Wi-Fi access, basic troubleshooting). This project is an internal, natural-language AI-powered chatbot designed to serve as a knowledgeable, first-line support tool for Mississippi state government employees. 

By guiding users toward existing self-service resources and answering common questions with high accuracy, this assistant reduces routine ticket volume and allows human IT staff to focus on mission-critical issues.

## Key Features
* **Conversational AI Interface:** Natural-language processing to understand non-technical user queries.
* **Retrieval-Augmented Generation (RAG):** Answers are strictly sourced from approved MDA IT documentation and Standard Operating Procedures (SOPs).
* **Strict Escalation Guardrails:** The AI is programmed to recognize out-of-scope requests (e.g., Active Directory unlocks, physical desk phone issues, ACE/MAGIC logins) and immediately route the user to the correct human department.
* **Ticketing System Integration:** Interoperability with an open-source IT ticketing system to automatically log unresolved issues.
* **Audit Logging:** Full interaction logging for quality assurance and compliance.

## The Team (University of Southern Mississippi)
* **Prabesh Pathak:** AI & Backend Lead (LLM Exploration, Conversational Logic)
* **Dikesh Shrestha:** Systems Integration & DevOps Lead (Environment Setup, API Integration)
* **Aavash Tiwari:** Frontend & Data Engineering Lead (Knowledge Base Ingestion, UI/UX)

## Getting Started

### Prerequisites
* AWS Account with access to `us-east-1` (N. Virginia)
* AWS CLI installed and configured
* Node.js / Python (Depending on final frontend/API stack)
* Docker (For local API integration testing)

### Initial Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/PrabeshPathak2002/mda-helpdesk.git](https://github.com/PrabeshPathak2002/mda-helpdesk.git)
   cd mda-helpdesk
