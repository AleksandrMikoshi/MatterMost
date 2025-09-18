# 🛡️ Mattermost Moderator Bot
Бот-модератор для Mattermost, который ограничивает возможность писать новые сообщения в каналах.  
Пользователи вне списка разрешённых:
- ❌ Не могут писать новые сообщения в канале
- ✅ Могут отвечать в тредах — только в каналах, указанных в `THREAD_ALLOWLIST`
- 🗑️ Системные сообщения (например: *пользователь вошёл в канал*, *пользователь добавлен*) могут автоматически удаляться в каналах из `SYSTEM_MESSAGE_DELETE`
- 📩 Получают личное сообщение с причиной удаления, если включено `DM_NOTIFY`  

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
- если канал в `SYSTEM_MESSAGE_DELETE` → бот удаляет все системные сообщения (`system_join_channel`, `system_add_to_channel` и т. п.)  

---
## 🔧 Зависимости
- mattermostdriver==7.3.2
- requests==2.28.2
- python-dotenv==1.0.1

---
## ⚠️ Примечания
- Если Mattermost использует самоподписанный сертификат, бот работает с `verify=False` (по умолчанию).  
  В этом случае в логах могут появляться предупреждения `InsecureRequestWarning`. Они не критичны и могут быть скрыты самим ботом.  
- Для большей безопасности можно смонтировать доверенный CA-сертификат в контейнер и указать `verify=/path/to/ca.crt` вместо отключения проверки SSL.  
- Бот должен быть добавлен в каналы, которые он будет модерировать.  
- Все настройки выполняются через файл `.env`.  

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
SYSTEM_MESSAGE_DELETE=test,general

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
**Каналы, где будут удаляться системные сообщения**
SYSTEM_MESSAGE_DELETE=test,general
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