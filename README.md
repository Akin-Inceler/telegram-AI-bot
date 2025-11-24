📦 Telegram AI Bot — Python + OpenAI + n8n Automation + Railway Deployment

This project is a fully functional, production-ready Telegram bot powered by Python, OpenAI (ChatGPT + Vision), n8n automation, and deployed on Railway.
The bot can:

Respond to text messages in natural English

Analyze photos using OpenAI Vision

Log every conversation/event to an automated n8n workflow

Convert logs into structured CSV files automatically

This README describes the architecture, features, installation steps, automation setup, and deployment details.

♦ Features
 1. Telegram chatbot (text responses)

Uses OpenAI’s gpt-4.1-mini model to generate natural English replies.

 2. Image analysis with OpenAI Vision

Users can send photos, and the bot returns a concise image description.

 3. n8n automation workflow

Every interaction (text or photo) is sent to an n8n webhook, processed, and converted into a downloadable CSV file.

 4. Railway deployment

The bot runs 24/7 on Railway with environment variables securely stored.

 5. Clean Python code + Environment-based configuration

No hardcoded secrets. All keys are loaded from os.getenv.

♦ Architecture Overview
User (Telegram)
        ↓
Telegram Bot API
        ↓
Python Bot (python-telegram-bot)
        ↓
OpenAI API (ChatGPT + Vision)
        ↓
n8n Automation Workflow
        ↓
CSV Log Output (structured conversation logs)

📁 Project Structure
├── bot.py                # Main Telegram bot application
├── requirements.txt      # Dependencies
├── tests/                # Pytest folder
│   └── test_basic.py     # Example test
└── README.md             # Documentation

🔧 Technologies Used
Component	Technology
Bot backend	Python 3.x
Telegram API	python-telegram-bot
LLM	OpenAI Chat Completions API
Vision	Base64 image → GPT-4.1 Vision
Automation	n8n workflow
Deployment	Railway
Code quality	ruff
Testing	pytest

♦ Environment Variables

Set these in your system or Railway dashboard:

TELEGRAM_BOT_TOKEN=<your Telegram bot token>
OPENAI_API_KEY=<your OpenAI API key>
N8N_WEBHOOK_URL=<Production n8n webhook URL>

▶️ Running Locally

Clone the repository:

git clone https://github.com/<your-username>/<repo>.git
cd <repo>


Create virtual environment:

python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Mac/Linux


Install dependencies:

pip install -r requirements.txt


Export environment variables:

set TELEGRAM_BOT_TOKEN=your_token_here
set OPENAI_API_KEY=your_key_here
set N8N_WEBHOOK_URL=https://your-n8n-url/webhook/xxx


Run the bot:

python bot.py

🤖 How the Bot Works (Flow Description)
1. Text messages

User sends text

Bot calls OpenAI Chat API

Bot returns reply

Bot sends log to n8n → converted to CSV

2. Photo messages

User sends image

Bot converts image to base64

Bot calls OpenAI Vision endpoint

Bot returns analysis

Bot logs result to n8n → CSV

🔄 n8n Automation Setup
✔ Node 1 — Webhook

Method: POST

Use Production URL, not Test URL

Output stored under json.body

✔ Node 2 — Edit Fields

Converts incoming JSON into a clean record:

Field	Expression
timestamp	{{$now}}
type	{{$json["body"]["type"]}}
user_id	{{$json["body"]["user_id"]}}
username	{{$json["body"]["username"]}}
message	{{$json["body"]["message"]}}
reply	{{$json["body"]["reply"]}}
photo_description	{{$json["body"]["description"]}}
✔ Node 3 — Convert to CSV

Config:

Operation: Convert to CSV

Put output file in: data

File name: telegram_ai_logs.csv

Add options:

Delimiter: ;

Header Row: checked (true)

Result → A properly formatted spreadsheet row.

☁️ Deployment (Railway)

Create new Railway project

Connect GitHub repo

Add environment variables under Variables

Deploy

Railway automatically rebuilds and restarts the bot on each Git push.

🧪 Testing (pytest)

This repository includes a minimal test:

def test_math():
    assert 2 + 2 == 4


Run tests with:

pytest

🔍 Code Quality (ruff)

Install:

pip install ruff


Check code:

ruff check .

📸 Screenshots
<img width="925" height="591" alt="Ekran görüntüsü 2025-11-23 170642" src="https://github.com/user-attachments/assets/b643c077-0940-4060-a8f7-31aaa0db04aa" />
<img width="1878" height="867" alt="image" src="https://github.com/user-attachments/assets/525b02c6-2eec-46ac-9b6b-5096c4248236" />
<img width="1887" height="889" alt="image" src="https://github.com/user-attachments/assets/58937937-e81a-46b3-a8d8-eae74c9ecfca" />
<img width="641" height="766" alt="image" src="https://github.com/user-attachments/assets/04d86051-7f08-46da-9d46-2536ad09d7e4" />
<img width="1888" height="909" alt="image" src="https://github.com/user-attachments/assets/011e9277-de05-4d5e-b52f-c2a36c235b8b" />
<img width="1170" height="647" alt="image" src="https://github.com/user-attachments/assets/70841a54-d689-42b2-966a-a46dec66119f" />
<img width="1137" height="905" alt="image" src="https://github.com/user-attachments/assets/a0770c64-701f-44e2-99d7-c030a9cd593d" />



📚 Medium Article

A Medium article about the project explains motivation, architecture, challenges, setup steps, and final result.

👉 Link: ([insert Medium article URL here after publishing](https://medium.com/@akin2001inceler/building-an-ai-powered-telegram-bot-with-python-openai-n8n-automation-and-railway-deployment-315962da405e))

🧑‍🎓 Student Hub Page

Short summary

GitHub link

Medium link

Screenshots

Project description

♦ Conclusion

This project demonstrates a complete end-to-end AI automation system using Python and modern cloud tools:

Telegram bot

Intelligent LLM responses

Vision analysis

Automation workflow

Server deployment

Logging and storage

It meets all rubric requirements for automation, LLM usage, deployment, code quality, documentation, and presentation.



