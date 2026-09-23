$ErrorActionPreference = 'SilentlyContinue'
function Measure-Dir($path) {
  $out = robocopy $path 'C:\__NULL__' /L /E /XJ /R:0 /W:0 /NFL /NDL /NJH /BYTES /NP 2>$null | Select-String 'Bytes :'
  if ($out) { [long](($out -split '\s+')[3]) } else { 0 }
}
Write-Output '== Desktop (folders > 100MB)'
Get-ChildItem 'C:\Users\User\Desktop' -Directory -Force | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 100MB) { '{0,15:N0}  {1}' -f $b, $_.Name }
}
Write-Output '== Desktop (files > 100MB)'
Get-ChildItem 'C:\Users\User\Desktop' -File -Force | Where-Object Length -gt 100MB | ForEach-Object { '{0,15:N0}  {1}' -f $_.Length, $_.Name }
Write-Output '== Downloads (files > 100MB)'
Get-ChildItem 'C:\Users\User\Downloads' -File -Force | Where-Object Length -gt 100MB | ForEach-Object { '{0,15:N0}  {1}' -f $_.Length, $_.Name }
Write-Output '== Downloads total + top folders'
Get-ChildItem 'C:\Users\User\Downloads' -Directory -Force | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 100MB) { '{0,15:N0}  {1}' -f $b, $_.Name }
}
Write-Output '== Program Files > 100MB'
Get-ChildItem 'C:\Program Files' -Directory -Force | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 100MB) { '{0,15:N0}  {1}' -f $b, $_.Name }
}
Write-Output '== Program Files (x86) > 100MB'
Get-ChildItem 'C:\Program Files (x86)' -Directory -Force | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 100MB) { '{0,15:N0}  {1}' -f $b, $_.Name }
}
