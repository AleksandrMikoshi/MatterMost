# 🛡️ Mattermost Moderator Bot
Бот-модератор для Mattermost, который ограничивает возможность писать новые сообщения в каналах.  
Пользователи вне списка разрешённых:
- ❌ Не могут писать новые сообщения в канале
- ✅ Могут отвечать в тредах — только в каналах, указанных в THREAD_ALLOWLIST,
- 📩 Получают уведомления в Direct Message о причине блокировки.

---
## 📜 Логика работы
Бот загружает список каналов в указанной команде.  
В каждом канале:
- проверяет отправителя сообщения
- если пользователь в allowlist — сообщение остаётся
- если пользователь не в списке и пишет в канал → сообщение удаляется
- если пользователь не в списке и пишет в тред:
    - канал есть в THREAD_ALLOWLIST → сообщение остаётся,
    - канала нет в THREAD_ALLOWLIST → сообщение удаляется.
- Если включено DM_NOTIFY=yes, бот отправляет пользователю ЛС с текстом DM_TEXT.

---
## 🔧 Зависимости
- mattermostdriver==7.3.2
- requests==2.28.2
- python-dotenv==1.0.1

---
## ⚠️ Примечания
Если Mattermost использует самоподписанный сертификат, бот работает с verify=False (будут предупреждения InsecureRequestWarning в логах, это не критично).  
Боту необходимо быть добавленным в каналы, которые он будет модерировать.  
Все настройки выполняются через .env.

---
## ⚙️ Настройка окружения
Создай файл .env (на основе .env.example):
```
MM_URL=mm.example.com
MM_SCHEME=https
MM_PORT=443
MM_TOKEN=your-bot-token
TEAM_NAME=your-team

CHANNEL_ALLOWLIST=test:@admin1,@admin2;general:@moderator
GLOBAL_ALLOWLIST=@superadmin
THREAD_ALLOWLIST=test,dev-chat

DM_NOTIFY=yes
DM_TEXT=В этом канале писать могут только допущенные пользователи. Канал: {channel}
```

---
## 🗒️ Каналы и разрешённые пользователи
**Формат: channel1:@user1,@user2;channel2:@user3**  
CHANNEL_ALLOWLIST=test:@admin1,@admin2;general:@moderator
**Глобальные пользователи, которым везде разрешено**  
GLOBAL_ALLOWLIST=@superadmin
**Каналы, где пользователи могут отвечать в треды**  
THREAD_ALLOWLIST=test,dev-chat
**Уведомления в ЛС**  
DM_NOTIFY=yes  
DM_TEXT=В этом канале писать могут только допущенные пользователи. Канал: {channel}  

---
## 🚀 Запуск
1. Сборка и запуск в Docker
```bash
docker build -t mm-moderator-bot .
docker run -d --restart=always --env-file .env mm-moderator-bot
```

---
## 👤 Автор
**Микоши Александр**  
Экосистема недвижимости **М2**