# MatterMost
[Русский язык](https://github.com/AleksandrMikoshi/MatterMost/blob/main/Readme_ru.md)

A collection of tools and extensions that improve the functionality of the **free (Community) edition of Mattermost**.  
The goal of this repository is to make Mattermost more convenient for corporate use by adding integrations and automation.  

---
## 📋 Requirements
- **Mattermost** (Community Edition)  
- **Active Directory** (for integration and tagging)  
- **Python 3 / Ansible** (depending on the subproject)  

---
## 📂 Repository Structure
- [**Ansible-role**](https://github.com/AleksandrMikoshi/MatterMost/tree/main/Ansible-role) 
  Role for Mattermost service update and configuration management
- [**MM_Gitlab_Auth**](https://github.com/AleksandrMikoshi/MatterMost/tree/main/MM_Gitlab_Auth)  
  Extension that enables **Active Directory authentication** in Mattermost.  
- [**MatterMost_Tag**](https://github.com/AleksandrMikoshi/MatterMost/tree/main/MatterMost_Tag)  
  Service for centralized and automated user tagging in Mattermost based on AD group membership.  
- [**moderator_bot**](https://github.com/AleksandrMikoshi/MatterMost/tree/main/moderator-bot)  
  A moderation bot that restricts the ability to post new messages in channels (e.g., only admins can post).  

---
## 🚀 Getting Started
Each subproject contains its own README with installation and usage instructions:  
1. Navigate to the project folder.  
2. Read its documentation.  
3. Install dependencies and configure integration.  

---
## 👤 Author
**Aleksandr Mikoshi**  
Real Estate Ecosystem **M2**
