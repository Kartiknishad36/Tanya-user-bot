<div align="center">

# \U0001f311 TANYA USERBOT

```
\u2591\u2580\u2588\u2580\u2591\u2588\u2580\u2588\u2591\u2588\u2580\u2588\u2591\u2588\u2591\u2588\u2591\u2588\u2580\u2588
\u2591\u2591\u2588\u2591\u2591\u2588\u2580\u2588\u2591\u2588\u2591\u2588\u2591\u2591\u2588\u2591\u2591\u2588\u2580\u2588
\u2591\u2591\u2580\u2591\u2591\u2580\u2591\u2580\u2591\u2580\u2591\u2580\u2591\u2591\u2580\u2591\u2591\u2580\u2591\u2580
```

### Dark \u2022 Premium \u2022 Powerful

[![Version](https://img.shields.io/badge/Version-2.0.0-black?style=for-the-badge&logo=github)](https://github.com/Kartiknishad36/Tanya-user-bot)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Telethon](https://img.shields.io/badge/Telethon-1.36-green?style=for-the-badge&logo=telegram&logoColor=white)](https://github.com/LonamiWebs/Telethon)
[![Render](https://img.shields.io/badge/Deploy-Render-purple?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

---

### \U0001f680 Quick Deploy

[![Deploy to Render](https://img.shields.io/badge/Deploy%20to%20Render-0A0A0A?style=for-the-badge&logo=render&logoColor=white)](https://dashboard.render.com/select-repo?type=web)
[![Generate Session](https://img.shields.io/badge/Generate%20String%20Session-0088CC?style=for-the-badge&logo=telegram&logoColor=white)](https://github.com/Kartiknishad36/Tanya-user-bot/blob/main/string_session.py)
[![Full Install Guide](https://img.shields.io/badge/Install%20Guide-INSTALL.md-2EA44F?style=for-the-badge&logo=readme&logoColor=white)](INSTALL.md)

---

### \U0001f4d6 Documentation

[![All Commands](https://img.shields.io/badge/All%20Commands-100%2B-black?style=for-the-badge)](ALL_COMMANDS.md)
[![Commands List](https://img.shields.io/badge/Commands-COMMANDS.md-0D1117?style=for-the-badge)](COMMANDS.md)
[![Changelog](https://img.shields.io/badge/Changelog-CHANGELOG.md-6F42C1?style=for-the-badge)](CHANGELOG.md)
[![Contributing](https://img.shields.io/badge/Contributing-CONTRIBUTING.md-F78166?style=for-the-badge)](CONTRIBUTING.md)

</div>

---

## \u26a1 Features

<div align="center">

| \U0001f6e1\ufe0f Admin | \U0001f4e2 Tagall | \U0001f4a3 Spam | \u2694\ufe0f Raid |
|:---:|:---:|:---:|:---:|
| Ban \u2022 Mute \u2022 Promote | Tag All / Admins | Delay Spam | Reply Raid |

| \U0001f916 Auto | \U0001f4a4 AFK | \U0001f4dd Notes | \U0001f44b Welcome |
|:---:|:---:|:---:|:---:|
| AutoReply \u2022 Filters | Away Mode | Save Notes | Join Messages |

| \U0001f528 GBan | \U0001f464 UserInfo | \U0001f3a8 Art | \U0001f9e0 AI |
|:---:|:---:|:---:|:---:|
| Global Ban + Sudo | **110+ Fields** | Fonts \u2022 ASCII | Gemini \u2022 GPT |

| \U0001f4e5 Media | \U0001f4e1 Broadcast | \U0001f512 Moderation | \u2699\ufe0f System |
|:---:|:---:|:---:|:---:|
| YT \u2022 Song \u2022 DL | Mass Message | Flood \u2022 Blacklist | Eval \u2022 Clone |

</div>

---

## \U0001f527 Environment Variables

<div align="center">

| Variable | Required | Description |
|:--------:|:--------:|-------------|
| `API_ID` | \u2705 | Telegram API ID |
| `API_HASH` | \u2705 | Telegram API Hash |
| `STRING_SESSION` | \u2705 | Telethon String Session |
| `OWNER_ID` | \u2b50 | Your Telegram User ID |
| `PORT` | \u2705 | `10000` (Render) |
| `CMD_PREFIX` | \u274c | Default `.` |
| `GEMINI_API_KEY` | \u274c | For AI commands |
| `OPENAI_API_KEY` | \u274c | For GPT |

</div>

---

## \U0001f680 Deploy Steps

<div align="center">

### \u2460 Generate Session

```bash
git clone https://github.com/Kartiknishad36/Tanya-user-bot.git
cd Tanya-user-bot
pip install telethon
python string_session.py
```

### \u2461 Create Web Service on Render

| Setting | Value |
|:-------:|:-----:|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python main.py` |

### \u2462 Add Environment Variables

Add all required vars from the table above \u2192 **Deploy**

</div>

---

## \U0001f4f1 Telegram Commands

<div align="center">

| Command | Action |
|:-------:|--------|
| `.help` | Premium dark help menu |
| `.help admin` | Admin module help |
| `.alive` | Dark status card |
| `.info` | **110+ user details** |
| `.tagall Hello` | Tag everyone |
| `.ping` | Check speed |

[![View All Commands](https://img.shields.io/badge/View%20All%20100%2B%20Commands-ALL_COMMANDS.md-black?style=for-the-badge)](ALL_COMMANDS.md)

</div>

---

## \U0001f4c1 Project Structure

```
Tanya-user-bot/
\u251c\u2500\u2500 \U0001f4c4 main.py                 # Entry + Keep-alive
\u251c\u2500\u2500 \u2699\ufe0f config.py
\u251c\u2500\u2500 \U0001f311 core/
\u2502   \u251c\u2500\u2500 theme.py               # Dark Premium Theme
\u2502   \u251c\u2500\u2500 database.py
\u2502   \u251c\u2500\u2500 decorators.py
\u2502   \u2514\u2500\u2500 ...
\u251c\u2500\u2500 \U0001f50c plugins/                # 40+ plugins
\u251c\u2500\u2500 \U0001f6e0\ufe0f utils/
\u251c\u2500\u2500 \U0001f4d6 ALL_COMMANDS.md         # Every command
\u251c\u2500\u2500 \U0001f4d8 INSTALL.md
\u2514\u2500\u2500 \U0001f7e3 render.yaml
```

---

## \u26a0\ufe0f Warning

<div align="center">

| \u26a0\ufe0f | Note |
|:--:|------|
| \U0001f510 | Never share `STRING_SESSION` |
| \U0001f464 | This is a **UserBot** (runs on your account) |
| \U0001f4a3 | Spam / Raid = Owner only \u2014 misuse can ban account |
| \U0001f634 | Free Render sleeps \u2192 use [cron-job.org](https://cron-job.org) to ping |

</div>

---

<div align="center">

### \U0001f311 Dark \u2022 Premium \u2022 Powerful

**Tanya UserBot v2.0**

[![GitHub](https://img.shields.io/badge/GitHub-Kartiknishad36-181717?style=for-the-badge&logo=github)](https://github.com/Kartiknishad36/Tanya-user-bot)
[![Stars](https://img.shields.io/github/stars/Kartiknishad36/Tanya-user-bot?style=for-the-badge&logo=github)](https://github.com/Kartiknishad36/Tanya-user-bot/stargazers)
[![Forks](https://img.shields.io/github/forks/Kartiknishad36/Tanya-user-bot?style=for-the-badge&logo=github)](https://github.com/Kartiknishad36/Tanya-user-bot/network/members)

</div>
