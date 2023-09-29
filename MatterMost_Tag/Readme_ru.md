# MatterMost_Tag

Добавление тегов осуществляется в зависимости от членства в группах Active Directory.

Сначала происходит сбор почтовых адресов пользователей, потом происходит добавление тегов.
На сервере где будет работать данный функционал необходимо установить:
- Python3
- pip
- Модули: psycopg2 argparse json playhouse   

Для добавления тегов необходимо в скрипте "Add_Tag.ps1" в переменной $Tag_All указать необходимые теги.

Для того что бы использовать разделение по группам, необходимо добавить в скрипт свои переменные и запуск скрипта mm-mentions-add.py

Пример:
## Добавление тегов всем членам группы "Domain Users"
```
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
## Добавление тегов всем членам группы "New_Group"
```
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