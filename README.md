🚀 AI Software Architecture Engine

An AI-powered multi-agent system that simulates a real-world SDLC workflow to convert product ideas into optimized database schemas using structured reasoning and iterative validation.

🧠 Key Features

* Multi-Agent Architecture (PRD → HLD → LLD → Schema → Review)
* Strategy Pattern for LLM selection
* Supports OpenAI & Ollama
* Alignment scoring mechanism
* Iterative schema refinement
* Human-in-the-loop PRD confirmation


🏗 Architecture Flow

    Client Input
        ↓
    Business Analyst (PRD)
        ↓
    Human in the loop
        ↓
    Schema Anlyzer
        ↓
    Schema Generator
        ↓
    Human in the Loop
        ↓
    Create Collection on DB



🔌 LLM Strategy Pattern

The system uses the Strategy Pattern to dynamically switch between:

    *   OpenAI

    *   Ollama (local models)

    *   Groq

llm = get_llm_strategy()
response = llm.chat(system_prompt, user_prompt)

This enables:

1. Clean abstraction
2. Easy provider switching
3. No code modification needed when changing models


⚙️ Installation :

1️⃣ Clone Repository

git clone https://github.com/charanbj10/DB-Schema-Designer-AI.git
cd DB-Schema-Designer-AI

2️⃣ Install Required Packages

pip install -r requirements.txt

Example requirements.txt:

> openai
> ollama
> python-dotenv

3️⃣ Configure Environment Variables

Create a .env file in the root directory:

For OpenAI :

🔐 STEP 1 — Get OpenAI API Key

On : https://platform.openai.com

1. Create account
2. Go to API Keys
3. Create new secret key

Windows (PowerShell):
$env:OPENAI_API_KEY="your_actual_key_here"

Mac/Linux:
export OPENAI_API_KEY="your_actual_key_here"

LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here

For Ollama :

LLM_PROVIDER=ollama

Make sure Ollama is installed.

4️⃣ Run the Application

python run.py


📊 What It Does

1. Generates PRD from product idea
2. Requires user confirmation before proceeding
3. Schema Analyzer agents starts analyzing
4. Schema Generates Schema
5. Requires human in the loop to confirm schema


🧩 Tech Stack

1. Python
2. Strategy Pattern
3. OpenAI API
4. Ollama Local LLM
5. Groq LLM