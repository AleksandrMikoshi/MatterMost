$ErrorActionPreference = "Stop"

#Creating the necessary variables
$Log = "$($PSScriptRoot)/Logs/History.log"
$OU_Users = "OU=User,DC=company,DC=com"
$Group_All = Get-ADGroupMember -Identity "Domain Users" | Where-Object -FilterScript {$_.distinguishedName -match $OU_Users} | ForEach-Object -Process {Get-ADUser -Identity $_ -properties mail}
$Tag_All = @('@tag1','@tag2','@tag3')

#Start VENV
. $PSScriptRoot\tutorial-env\Scripts\Activate.ps1

#Create Log File
"`n==============================" | Out-File -FilePath $Log -Append
Get-Date -Format s | Out-File -FilePath $Log -Append
"All Users: $($Users_All.Count)" | Out-File -FilePath $Log -Append

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

Get-Date -Format s | Out-File -FilePath $Log -Append



deactivate

"------Finish------" | Out-File -FilePath $Log -Append