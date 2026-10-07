# 🤖 Tanya UserBot

**Advanced • Powerful • Modular Telegram UserBot**  
Fully optimized for **Render** free tier (Web Service)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Telethon](https://img.shields.io/badge/Telethon-1.36-green)
![Render](https://img.shields.io/badge/Deploy-Render-purple)

---

## ✨ Features

| Module | Commands | Description |
|--------|----------|-------------|
| **Alive** | `.alive` `.ping` `.stats` | Bot status & system info |
| **Admin** | `.ban` `.kick` `.mute` `.promote` `.purge` `.pin` | Full group moderation |
| **Utils** | `.id` `.info` `.qr` `.tts` | Useful tools |
| **AI** | `.ai` `.gemini` `.gpt` | Gemini + ChatGPT support |
| **Media** | `.dl` `.yt` `.song` | Download media & YouTube |
| **Fun** | `.quote` `.joke` `.meme` `.truth` `.dare` | Entertainment |
| **PM Permit** | `.approve` `.block` | Protect your inbox |
| **System** | `.eval` `.exec` `.restart` | Owner-only tools |

**50+ commands** • Plugin based • Easy to extend

---

## 🚀 Deploy on Render (Recommended)

### Step 1: Generate String Session (Local)

1. Go to [my.telegram.org](https://my.telegram.org) → Login → API Development Tools
2. Create app → Copy **API_ID** and **API_HASH**
3. On your PC run:

```bash
git clone https://github.com/Kartiknishad36/Tanya-user-bot.git
cd Tanya-user-bot
pip install telethon
python string_session.py
```

4. Enter API_ID + API_HASH → Login with phone → Copy the **STRING_SESSION**

### Step 2: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repo: `Kartiknishad36/Tanya-user-bot`
4. Settings:
   - **Name**: `tanya-userbot`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: Free

5. Add Environment Variables:

| Key | Value | Required |
|-----|-------|----------|
| `API_ID` | Your API ID | ✅ |
| `API_HASH` | Your API Hash | ✅ |
| `STRING_SESSION` | The long string you generated | ✅ |
| `OWNER_ID` | Your Telegram User ID | Recommended |
| `CMD_PREFIX` | `.` (default) | Optional |
| `PORT` | `10000` | Optional |
| `GEMINI_API_KEY` | For AI features | Optional |
| `OPENAI_API_KEY` | For ChatGPT | Optional |
| `PM_PERMIT` | `True` | Optional |

6. Click **Create Web Service** → Wait for deploy

7. After deploy, open the Render URL once (to wake it up)

---

## 🏠 Local Run

```bash
git clone https://github.com/Kartiknishad36/Tanya-user-bot.git
cd Tanya-user-bot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
python main.py
```

---

## 📖 Commands

Type `.help` after starting the bot for full menu.

**Quick Start:**
- `.alive` → Check bot status
- `.ping` → Check speed
- `.help` → Full help menu

---

## ⚠️ Important Notes

1. **UserBot = Your Account**  
   This runs as **your Telegram account**, not a bot. Be careful with admin commands.

2. **Session Security**  
   Never share your `STRING_SESSION`. Anyone with it can control your account.

3. **Render Free Tier**  
   - Sleeps after 15 min inactivity  
   - Use [cron-job.org](https://cron-job.org) to ping your Render URL every 10 minutes  

4. **Banned Risk**  
   Don't spam, mass DM, or abuse features. Use responsibly.

---

## 🛠️ Project Structure

```
Tanya-user-bot/
├── main.py              # Entry point + Keep-alive server
├── config.py            # Configuration
├── string_session.py    # Session generator
├── requirements.txt
├── render.yaml          # Render blueprint
├── plugins/
│   ├── alive.py
│   ├── admin.py
│   ├── ai.py
│   ├── fun.py
│   ├── help.py
│   ├── media.py
│   ├── pmpermit.py
│   ├── system.py
│   └── utils.py
├── utils/
│   └── helpers.py
└── data/                # Runtime data
```

---

**Star ⭐ the repo if you like it!**

Made with ❤️ for Telegram community
