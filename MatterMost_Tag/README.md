# MatterMost_Tag
[Русский язык](https://github.com/AleksandrMikoshi/MatterMost/blob/main/MatterMost_Tag/Readme_ru.md)  
This project automates the process of assigning tags to Mattermost users based on their **Active Directory (AD) group membership**.  
The workflow is as follows:
1. Collect users’ email addresses from Active Directory.  
2. Assign tags to those users in Mattermost.  

---
## 📋 Requirements
On the server where this functionality will run, install the following:
- **Python 3**  
- **pip**  
- Python modules:  
  - `psycopg2`  
  - `argparse`  
  - `json`  
  - `playhouse`  

---
## ⚙️ Configuration
To add tags, edit the script **`Add_Tag.ps1`** and specify the required tags in the variable:  
```powershell
$Tag_All = @('@tag1','@tag2','@tag3')
```
If you want to assign tags based on AD groups, you will need to:
1. Add your own group-specific variables in the PowerShell script.
2. Run the Python script mm-mentions-add.py with the appropriate arguments.

---
## 🚀 Usage Examples
Add tags to all members of the Domain Users group
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


**Add tags to all members of the New_Group group**
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
## 📝 Notes
- Ensure that all users in Active Directory have valid email addresses.
- Errors and skipped users are logged to the file defined by the $Log variable.
- Multiple groups can be managed by defining additional variables and reusing the Python script.

---
## 👤 Author
**Aleksandr Mikoshi**  
Real Estate Ecosystem **M2**