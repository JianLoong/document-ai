# Schemes Mandate Analyzer

This project provides an AI agent for reading, processing, and analyzing official Visa payment processing mandate documents (e.g., Visa Core Rules, Visa Product and Service Rules, technical specifications, compliance requirements, or merchant/acquirer/issuer guidelines issued by Visa).

## Features
- Accepts Visa payment processing mandate documents as input (text, PDF extract, tables, XML, etc.)
- Extracts, summarizes, and analyzes compliance requirements, transaction rules, security standards, and more
- Answers user queries with precise, document-cited responses
- Handles ambiguities and flags missing or unclear information
- Always references the current date in its analysis

## Usage
1. **Setup**
   - Clone this repository
   - Install dependencies (see `requirements.txt`)
   - Set up your `.env` file with required environment variables (see `.env.example`)

2. **Running the Agent**
   - Use Docker Compose to start all services:
     ```sh
     docker-compose up --build
     ```
   - Or run the agent locally with your preferred Python environment

3. **Interacting**
   - Provide a Visa mandate document or query to the agent
   - The agent will respond with a structured, cited analysis based on the document content

## Environment Variables
- `CONFLUENCE_BASE_URL` - Base URL for your Confluence instance (if using Confluence tools)
- `CONFLUENCE_API_TOKEN` - API token for Confluence access
- `GOOGLE_GENAI_USE_VERTEXAI=FALSE` - Settings for Gemini
- `GOOGLE_API_KEY=YOUR_KEY` - Your API Key

## Example Query
```
What are the merchant requirements for accepting Visa contactless payments from this document: [paste document text]?
```

## Disclaimer
This analysis is based on the document provided as of the current date. Verify with official Visa resources (e.g., visa.com) for updates or further details. This is not legal or financial advice.

---

For more details, see the agent instructions in `adk-agents/agent.py`.
