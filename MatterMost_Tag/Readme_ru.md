# MatterMost_Tag
Проект автоматизирует процесс назначения тегов пользователям Mattermost в зависимости от их **членства в группах Active Directory (AD)**.  
Алгоритм работы:  
1. Получение адресов электронной почты пользователей из Active Directory.  
2. Назначение тегов этим пользователям в Mattermost.  

---
## 📋 Требования
На сервере, где будет запускаться функционал, необходимо установить:  
- **Python 3**  
- **pip**  
- Модули Python:  
  - `psycopg2`  
  - `argparse`  
  - `json`  
  - `playhouse`  

---
## ⚙️ Настройка
Для добавления тегов отредактируйте скрипт **`Add_Tag.ps1`** и укажите нужные теги в переменной:  
```powershell
$Tag_All = @('@tag1','@tag2','@tag3')
```
Если требуется назначение тегов по группам AD, нужно:
1. Добавить свои переменные для групп в PowerShell-скрипт.
2. Запустить Python-скрипт mm-mentions-add.py с нужными аргументами.

---
## 🚀 Примеры использования
Добавление тегов всем членам группы Domain Users
```powershell
$Group_All = Get-ADGroupMember -Identity "Domain Users" | Where-Object -FilterScript {$_.distinguishedName -match $OU_Users} | ForEach-Object -Process {Get-ADUser -Identity $_ -properties mail}
$Tag_All = @('@tag1','@tag2','@tag3')

foreach ($user_All in $Group_All){
    if ($user_All.mail){
        try {
            foreach ($Alltag in $Tag_All){
                python $PSScriptRoot\mm-mentions-add.py $user_All --tag $Alltag
            }
        }
        catch {
            $user_All.samaccountname | Out-File -FilePath $Log -Append
            $_.Exception | Out-File -FilePath $Log -Append
        }
    }
    else {
        "$($user_All.samaccountname) has not mail" | Out-File -FilePath $Log -Append
    }
}
```

**Добавление тегов всем членам группы New_Group**
```powershell
$Group_New = Get-ADGroupMember -Identity "New_Group" | Where-Object -FilterScript {$_.distinguishedName -match $OU_Users} | ForEach-Object -Process {Get-ADUser -Identity $_ -properties mail}
$Tag_New = @('@tag4','@tag5')

foreach ($user_New in $Group_New){
    if ($user_New.mail){
        try {
            foreach ($Newtag in $Tag_New){
                python $PSScriptRoot\mm-mentions-add.py $user_New --tag $Newtag
            }
        }
        catch {
            $user_New.samaccountname | Out-File -FilePath $Log -Append
            $_.Exception | Out-File -FilePath $Log -Append
        }
    }
    else {
        "$($user_New.samaccountname) has not mail" | Out-File -FilePath $Log -Append
    }
}
```

---
## 📝 Примечания
- Убедитесь, что у всех пользователей в Active Directory есть корректные адреса электронной почты.
- Ошибки и пропущенные пользователи записываются в файл, указанный в переменной $Log.
- Можно обрабатывать несколько групп, задав дополнительные переменные и повторно используя Python-скрипт.

---
## 👤 Автор
**Микоши Александр**  
Экосистема недвижимости **М2**