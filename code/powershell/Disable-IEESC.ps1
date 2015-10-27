foreach($Computer in $ComputerName) {
if(!(Test-Connection -Computer $Computer -count 1 -ea 0)) {
Write-Host "$Computer NOT REACHABLE"
$FailedComps += $Computer
continue
}
Write-Host "Working on $Computer"
try {
$BaseKey = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey("LocalMachine",$Computer)
$SubKey = $BaseKey.OpenSubKey($AdministratorsKey,$true)
$SubKey.SetValue("IsInstalled",0,[Microsoft.Win32.RegistryValueKind]::DWORD)
$SubKey = $BaseKey.OpenSubKey($UsersKey,$true)
$SubKey.SetValue("IsInstalled",0,[Microsoft.Win32.RegistryValueKind]::DWORD)
Write-Host "Successfully disabled IE ESC on $Computer"
$SuccessComps += $Computer
}
catch {
Write-Host "Failed to disable IE ESC on $Computer"
$FailedComps += $Computer
}
}
