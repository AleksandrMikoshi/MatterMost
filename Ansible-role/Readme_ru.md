# Mattermost

Ansible-роль для обновления Mattermost

Повзоляет выполнить три действия:
1. Обновить сервис Mattermost
2. Обновить конфигурационный файл и перечитать его
3. Обновить SSL-сертификат


## Требования

Ansible 2.9+  
Сервер на базе Ubuntu 20.04 или выше  
Для работы необходимо заполнить файл ansible.conf

*Пример*  
```
[defaults]
inventory = hosts
remote_user = username
private_key_file = ~/.ssh/id_rsa
```

## Использование

Убедитесь, что у вас есть действующий токен для доступа к Vault, который можно передать через переменную окружения VAULT_TOKEN. 

```bash
export VAULT_TOKEN="ваш-токен"
```

*Ключ --limit необходим для указания нужной группы хостов - mattermost или mattermosttest*  

Для обновления сервиса необходимо выполнить

```bash
ansible-playbook mm.yml --tags "update_service" --limit "hosts: mattermosttest"
```

Для обновления конфигурационного файла необходимо выполнить 

```bash
ansible-playbook mm.yml --tags "update_conf" --limit "hosts: mattermosttest"
```

Для обновления SSL-сертификата необходимо выполнить

```bash
ansible-playbook mm.yml --tags "update_cert" --limit "hosts: mattermosttest"
```

## Используемые переменные

| Переменная | Описание | Пример значения | Значение по умолчанию |
|---|---|---|---|
| vault_url | Адрес сайта Vault | https://vault.domain.com:8200 | - |
| path_data | Путь до сейфа содержащего данные конфига mattermost | certificates/data/mattermost | - |
| path_cert | Путь до сейфа содержащего сертификат | certificates/data/mattermost | - |
| mattermost_version | Версия Mattermost | 10.7.0 | - |
| mattermost_user | Системный пользователь для сервиса | mattermost | - |
| alloweduntrustedinternalconnections | Белый список адресов локальной сети, которые могут быть запрошены сервером Mattermost от имени клиента | site.domain.com, site_2.domain.com, site_3.domain.com, etc. | - |


## Секреты VAULT
| Переменная | Описание | Пример значения | Значение по умолчанию |
|---|---|---|---|
| POSTGRESQL_USER | Пользователь PostgreSQL | postgres | - |
| POSTGRESQL_PASSWORD | Пароль пользователя БД | Str0ngP@ss | - |
| POSTGRESQL_HOST | Хост СУБД | postgresql.domain.com | - |
| POSTGRESQL_PORT | Порт PostgreSQL	| 5432 | - |
| POSTGRESQL_NAME | Имя базы данных | mattermost | - |
| POSTGRESQL_ALTRESTENCRYPTKEY | ключ шифрования, используемый для защиты данных "at rest" | gXp...123 | - |
| DRIVER_NAME | Драйвер хранилища | amazons3 | - |
| S3_REGION | Регион S3 | ru-central1 | - |
| S3_ENDPOINT | S3 API endpoint | storage.yandexcloud.net | - |
| S3_KEY | Access Key ID | YCAJ...ABC | - |
| S3_SECRET | Secret Access Key | YCP...xyz | - |
| S3_BUCKET | Имя бакета | mattermost | - |
| GITLAB_SECRET | Секрет OAuth-приложения GitLab | gXp...123 | - |
| GITLAB_ID | ID OAuth-приложения | 12345 | - |
| AUTH_ENDPOINT | auth endpoint | https://auth.m2.ru/oauth/authorize.php | - |
| TOKEN_ENDPOINT | Токен OAuth | https://auth.m2.ru/oauth/token.php | - |
| USER_APIENDPOINT | API для получения данных пользователя | https://auth.m2.ru/oauth/resource.php | - |
| URL | Базовый URL Mattermost | https://mm.m2.ru | - |
| CERTIFICATE_CRT | Путь к SSL-сертификату | /etc/ssl/mattermost.crt | - |
| CERTIFICATE_KEY | Путь к приватному ключу | /etc/ssl/mattermost.key | - |





## Информация об авторе
Микоши Александр  
Экосистема недвижимости М2