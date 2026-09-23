$ErrorActionPreference = 'SilentlyContinue'
function Measure-Dir($path) {
  $out = robocopy $path 'C:\__NULL__' /L /E /XJ /R:0 /W:0 /NFL /NDL /NJH /BYTES /NP 2>$null | Select-String 'Bytes :'
  if ($out) { [long](($out -split '\s+')[3]) } else { 0 }
}
Write-Output '== research-corpus A (Users\User) vs B (kinetic-scale)'
Get-ChildItem 'C:\Users\User\research-corpus' -Force | Select-Object -First 8 -ExpandProperty Name
Write-Output '--- B:'
Get-ChildItem 'C:\Users\User\Desktop\kinetic-scale\research-corpus' -Force | Select-Object -First 8 -ExpandProperty Name
Write-Output '== .cache breakdown'
Get-ChildItem 'C:\Users\User\.cache' -Directory -Force | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 50MB) { '{0,15:N0}  {1}' -f $b, $_.Name }
}
Write-Output '== Temp (Users) breakdown'
Get-ChildItem 'C:\Users\User\AppData\Local\Temp' -Force | Sort-Object -Descending { if ($_.PSIsContainer) { (Measure-Dir $_.FullName) } else { $_.Length } } | Select-Object -First 8 | ForEach-Object {
  if ($_.PSIsContainer) { '{0,15:N0}  {1}/' -f (Measure-Dir $_.FullName), $_.Name } else { '{0,15:N0}  {1}' -f $_.Length, $_.Name }
}
Write-Output '== drive-backup-staging'
Get-ChildItem 'C:\Users\User\Desktop\drive-backup-staging' -Force | Select-Object -First 10 -ExpandProperty Name
Write-Output '== AppData\Local\Python + npm-cache + ms-playwright quick look'
Get-ChildItem 'C:\Users\User\AppData\Local\Python' -Directory -Force | ForEach-Object { '{0,10:N0} MB  {1}' -f ((Measure-Dir $_.FullName)/1MB), $_.Name }
Get-ChildItem 'C:\Users\User\AppData\Local\ms-playwright' -Directory -Force | ForEach-Object { '{0,10:N0} MB  {1}' -f ((Measure-Dir $_.FullName)/1MB), $_.Name }
Get-ChildItem 'C:\Users\User\.local' -Directory -Force | ForEach-Object { '{0,10:N0} MB  {1}' -f ((Measure-Dir $_.FullName)/1MB), $_.Name }
Get-ChildItem 'C:\Users\User\.codex' -Force | Sort-Object -Descending { if ($_.PSIsContainer) { (Measure-Dir $_.FullName) } else { $_.Length } } | Select-Object -First 5 | ForEach-Object {
  if ($_.PSIsContainer) { '{0,15:N0}  {1}/' -f (Measure-Dir $_.FullName), $_.Name } else { '{0,15:N0}  {1}' -f $_.Length, $_.Name }
}
Get-ChildItem 'C:\Users\User\.u2net' -Force | ForEach-Object { '{0,15:N0}  {1}' -f $_.Length, $_.Name }
