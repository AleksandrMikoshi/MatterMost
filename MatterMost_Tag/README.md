#MatterMost_Tag

Tagging is added based on Active Directory group membership.

First, user email addresses are collected, then tags are added.
On the server where this functionality will work, you must install:
- Python3
- pip
- Modules: psycopg2 argparse json playhouse

To add tags, you need to specify the required tags in the $Tag_All variable in the "Add_Tag.ps1" script.

In order to use group separation, you need to add your variables to the script and run the mm-mentions-add.py script

Example:
## Adding tags to all members of the "Domain Users" group
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

## Adding tags to all members of the "New_Group" group
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