# AI Agent for Lead Generation

This project implements an AI-powered sales lead generation pipeline using web scraping, large language models, and a Streamlit dashboard. It accepts a high-level client query and outputs a curated prospect with rationale and an outreach message.

## Features

- Query-based lead discovery using Firecrawl (search + scrape)
- Agent workflow built with LangGraph for modular control flow
- Structured state management using a Pydantic `ResearchState` model
- Streamlit dashboard for interactive result viewing
- Command-line interface for iterative testing and debugging

## How It Works

1. The user provides a client description via the terminal
2. Firecrawl fetches and parses relevant content from the web
3. OpenAI generates a sales lead, supporting description, and outreach content
4. A Streamlit dashboard displays the generated results

## Setup Instructions

1. Clone the repository
2. Create and activate venv
3. Install requirements.txt
4. Create an env file with OpenAI and Firecrawl APIs
5. Run from main.py

   
