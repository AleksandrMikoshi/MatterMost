# Mattermost Ansible Role
[Русский язык](https://github.com/AleksandrMikoshi/MatterMost/blob/main/Ansible-role/Readme_ru.md)  
Ansible role for automating **Mattermost** updates.  
Supports the following operations:  
1. Update the Mattermost service  
2. Update the configuration file and reload it  
3. Update the SSL certificate 

---
## 📋 Requirements
- **Ansible**: version 2.9+  
- **OS**: Ubuntu 20.04 or higher  
- **Configuration**: you need to fill in the `ansible.conf` file  
Example `ansible.conf`:  
```ini
[defaults]
inventory = hosts
remote_user = username
private_key_file = ~/.ssh/id_rsa
```

---
## 🚀 Usage
You need a valid Vault access token. Before running, export it as an environment variable:
```bash
export VAULT_TOKEN="your-token"
```
> 🔑 Use the --limit key to select the target host group:
> - "mattermost"
> - "mattermosttest"
## Run commands
🔄 Update the service
```bash
ansible-playbook mm.yml --tags "update_service" --limit "hosts:mattermosttest"
```
⚙️ Update the configuration
```bash
ansible-playbook mm.yml --tags "update_conf" --limit "hosts:mattermosttest"
```
🔐 Update the SSL certificate
```bash
ansible-playbook mm.yml --tags "update_cert" --limit "hosts:mattermosttest"
```

---
## ⚙️ Role Variables
| Variable | Description | Example Value | Default Value |
|---|---|---|---|
| vault_url | Vault server address | https://vault.domain.com:8200 | - |
| path_data | Path to the Vault storing Mattermost config data | certificates/data/mattermost | - |
| path_cert | Path to the Vault storing the certificate | certificates/data/mattermost | - |
| mattermost_version | Mattermost version | 10.7.0 | - |
| mattermost_user | System user for the service | mattermost | - |
| alloweduntrustedinternalconnections | Whitelist of internal network addresses that Mattermost server can access on behalf of the client | site.domain.com, site_2.domain.com, site_3.domain.com, etc. | - |

---
## 🔒 Vault Secrets
| Variable | Description | Example Value | Default Value |
|---|---|---|---|
| POSTGRESQL_USER | PostgreSQL user | postgres | - |
| POSTGRESQL_PASSWORD | DB user password | Str0ngP@ss | - |
| POSTGRESQL_HOST | Database host | postgresql.domain.com | - |
| POSTGRESQL_PORT | PostgreSQL port | 5432 | - |
| POSTGRESQL_NAME | Database name | mattermost | - |
| POSTGRESQL_ALTRESTENCRYPTKEY | Encryption key for protecting data at rest | gXp...123 | - |
| DRIVER_NAME | Storage driver | amazons3 | - |
| S3_REGION | S3 region | ru-central1 | - |
| S3_ENDPOINT | S3 API endpoint | storage.yandexcloud.net | - |
| S3_KEY | Access Key ID | YCAJ...ABC | - |
| S3_SECRET | Secret Access Key | YCP...xyz | - |
| S3_BUCKET | Bucket name | mattermost | - |
| GITLAB_SECRET | GitLab OAuth app secret | gXp...123 | - |
| GITLAB_ID | GitLab OAuth app ID | 12345 | - |
| AUTH_ENDPOINT | OAuth auth endpoint | https://auth.domain.com/oauth/authorize.php | - |
| TOKEN_ENDPOINT | OAuth token endpoint | https://auth.domain.com/oauth/token.php | - |
| USER_APIENDPOINT | User data API endpoint | https://auth.domain.com/oauth/resource.php | - |
| URL | Base Mattermost URL | https://domain.com | - |
| CERTIFICATE_CRT | Path to SSL certificate | /etc/ssl/mattermost.crt | - |
| CERTIFICATE_KEY | Path to private key | /etc/ssl/mattermost.key | - |

---
## 👤 Author
**Aleksandr Mikoshi**  
Real Estate Ecosystem **M2**