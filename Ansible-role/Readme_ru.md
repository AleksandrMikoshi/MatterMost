# Mattermost Ansible Role
Ansible-роль для автоматизации обновлений **Mattermost**.  
Поддерживает следующие операции:
1. Обновление сервиса Mattermost
2. Обновление конфигурационного файла и его перечитывание
3. Обновление SSL-сертификата

---
## 📋 Требования
- Ansible: версия 2.9+
- ОС сервера: Ubuntu 20.04 или выше
- Конфигурация: необходимо заполнить файл ansible.conf
Пример ansible.conf:
```ini
[defaults]
inventory = hosts
remote_user = username
private_key_file = ~/.ssh/id_rsa
```

---
## 🚀 Использование
Для работы нужен токен доступа к Vault. Перед запуском его необходимо передать через переменную окружения:
```bash
export VAULT_TOKEN="ваш-токен"
```
> 🔑 Используйте ключ --limit для выбора группы хостов:
> mattermost
> mattermosttest
## Команды запуска
🔄 Обновление сервиса
```bash
ansible-playbook mm.yml --tags "update_service" --limit "hosts:mattermosttest"
```
⚙️ Обновление конфигурации
```bash
ansible-playbook mm.yml --tags "update_conf" --limit "hosts:mattermosttest"
```
🔐 Обновление SSL-сертификата
```bash
ansible-playbook mm.yml --tags "update_cert" --limit "hosts:mattermosttest"
```

---
## ⚙️ Переменные роли
| Переменная | Описание | Пример | По умолчанию |
|---|---|---|---|
| vault_url | URL Vault | https://vault.domain.com:8200 | - |
| path_data | Путь до сейфа с конфигом Mattermost | certificates/data/mattermost | - |
| path_cert | Путь до сейфа с сертификатом | certificates/data/mattermost | - |
| mattermost_version | Версия Mattermost | 10.7.0 | - |
| mattermost_user | Системный пользователь сервиса | mattermost | - |
| alloweduntrustedinternalconnections | Белый список локальных адресов, доступных Mattermost | site.domain.com, site_2.domain.com | - |

---
## 🔒 Секреты Vault
|Переменная | Описание | Пример | По умолчанию |
|---|---|---|---|
| POSTGRESQL_USER | Пользователь БД | postgres | - |
| POSTGRESQL_PASSWORD | Пароль БД | Str0ngP@ss | - |
| POSTGRESQL_HOST | Хост PostgreSQL | postgresql.domain.com | - |
| POSTGRESQL_PORT | Порт PostgreSQL | 5432 | - |
| POSTGRESQL_NAME | Имя БД | mattermost | - |
| POSTGRESQL_ALTRESTENCRYPTKEY | Ключ шифрования "at rest" | gXp...123 | - |
| DRIVER_NAME | Драйвер хранилища | amazons3 | - |
| S3_REGION | Регион S3 | ru-central1 | - |
| S3_ENDPOINT | Endpoint S3 | storage.yandexcloud.net | - |
| S3_KEY | Access Key ID | YCAJ...ABC | - |
| S3_SECRET | Secret Access Key | YCP...xyz | - |
| S3_BUCKET | Имя бакета | mattermost | - |
| GITLAB_SECRET | Секрет OAuth-приложения GitLab | gXp...123 | - |
| GITLAB_ID | ID OAuth-приложения | 12345 | - |
| AUTH_ENDPOINT | OAuth auth endpoint | https://auth.domain.com/oauth/authorize.php | - |
| TOKEN_ENDPOINT | OAuth token endpoint | https://auth.domain.com/oauth/token.php | - |
| USER_APIENDPOINT | API для данных пользователя | https://auth.domain.com/oauth/resource.php | - |
| URL | Базовый URL Mattermost | https://domain.com | - |
| CERTIFICATE_CRT | Путь к SSL-сертификату | /etc/ssl/mattermost.crt | - |
| CERTIFICATE_KEY | Путь к приватному ключу | /etc/ssl/mattermost.key | - |

---
## 👤 Автор
**Микоши Александр**  
Экосистема недвижимости **М2**