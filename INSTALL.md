# Detailed Installation Guide - Tanya UserBot

## Requirements
- Python 3.10+
- Telegram account
- API_ID + API_HASH from https://my.telegram.org
- Git

## Method 1: Render (Recommended - Free)

### Step 1: Get API Credentials
1. Open https://my.telegram.org
2. Login with phone number
3. Click API Development Tools
4. Create app (title: TanyaUserBot)
5. Copy api_id and api_hash

### Step 2: Generate String Session
```bash
git clone https://github.com/Kartiknishad36/Tanya-user-bot.git
cd Tanya-user-bot
pip install telethon
python string_session.py
```
Enter API_ID, API_HASH, phone number, login code. Copy the STRING_SESSION.

### Step 3: Deploy on Render
1. Go to https://dashboard.render.com
2. New + → Web Service
3. Connect repo Kartiknishad36/Tanya-user-bot
4. Build: `pip install -r requirements.txt`
5. Start: `python main.py`
6. Instance: Free
7. Add Environment Variables:

| Key | Required |
|-----|----------|
| API_ID | Yes |
| API_HASH | Yes |
| STRING_SESSION | Yes |
| OWNER_ID | Recommended |
| PORT | 10000 |
| CMD_PREFIX | . |
| GEMINI_API_KEY | Optional |
| OPENAI_API_KEY | Optional |

8. Create Web Service and wait for deploy.
9. Open the Render URL once.

### Step 4: Keep Alive
Use https://cron-job.org → ping your Render URL every 10 minutes.

## Method 2: Local / VPS
```bash
git clone https://github.com/Kartiknishad36/Tanya-user-bot.git
cd Tanya-user-bot
pip install -r requirements.txt
cp .env.example .env
# Edit .env
python main.py
```

## How to get OWNER_ID
Message @userinfobot on Telegram.

## After Start
Send `.alive` in Saved Messages. Type `.help` for commands.
