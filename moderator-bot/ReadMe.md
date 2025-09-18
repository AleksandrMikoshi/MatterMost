# 🛡️ Mattermost Moderator Bot
[Русский язык](https://github.com/AleksandrMikoshi/MatterMost/blob/main/moderator-bot/ReadMe_ru.md)
A moderation bot for Mattermost that restricts the ability to post new messages in channels.  
Users outside the allowlist:
- ❌ Cannot post new messages in the channel
- ✅ Can reply in threads — only in channels listed in THREAD_ALLOWLIST
- 🗑️ System messages (e.g. *user joined channel*, *user added*) can be automatically deleted in channels listed in SYSTEM_MESSAGE_DELETE
- 📩 Receive a Direct Message notification with the reason for blocking

---
## 📜 How it works
The bot loads the list of channels in the specified team.
For each channel:
- checks the message sender
- if the user is in the allowlist → the message remains
- if the user is not in the list and posts in the channel → the message is deleted
- if the user is not in the list and posts in a thread:
    - if the channel is in THREAD_ALLOWLIST → the message remains
    - if the channel is not in THREAD_ALLOWLIST → the message is deleted
- If DM_NOTIFY=yes is enabled, the bot sends the user a direct message with the text from DM_TEXT
- if the channel is in SYSTEM_MESSAGE_DELETE, any system messages (`system_join_channel`, `system_add_to_channel`, etc.) are deleted automatically


---
## 🔧 Dependencies
- mattermostdriver==7.3.2
- requests==2.28.2
- python-dotenv==1.0.1

---
## ⚠️ Notes
- If Mattermost uses a self-signed certificate, the bot runs with `verify=False` (by default).  
  In this case, `InsecureRequestWarning` may appear in logs. They are not critical and can be suppressed by the bot.  
- To improve security, you can mount a trusted CA certificate inside the container and set `verify=/path/to/ca.crt` instead of disabling SSL verification.  
- The bot must be added to the channels it moderates.  
- All configuration is done through `.env`.

---
## ⚙️ Environment Setup
Create a .env file (based on .env.example):
```
MM_URL=mm.example.com
MM_SCHEME=https
MM_PORT=443
MM_TOKEN=your-bot-token
TEAM_NAME=your-team

CHANNEL_ALLOWLIST=test:@admin1,@admin2;general:@moderator
GLOBAL_ALLOWLIST=@superadmin
THREAD_ALLOWLIST=test,dev-chat
SYSTEM_MESSAGE_DELETE=test,general

DM_NOTIFY=yes
DM_TEXT=Only allowed users can post in this channel. Channel: {channel}
```

---
## 🗒️ Channels and Allowed Users  

**Format: channel1:@user1,@user2;channel2:@user3**  
CHANNEL_ALLOWLIST=test:@admin1,@admin2;general:@moderator  
**Global users allowed everywhere**  
GLOBAL_ALLOWLIST=@superadmin  
**Channels where users can reply in threads**  
THREAD_ALLOWLIST=test,dev-chat  
**Channels where system messages will be deleted**
SYSTEM_MESSAGE_DELETE=test,general
**Direct Message notifications**  
DM_NOTIFY=yes  
DM_TEXT=Only allowed users can post in this channel. Channel: {channel}  

---
## 🚀 Run
1. Build and start in Docker:
```bash
docker build -t mm-moderator-bot .
docker run -d --restart=always --env-file .env mm-moderator-bot
```

---
## 👤 Author
**Aleksandr Mikoshi**  
Real Estate Ecosystem **M2**