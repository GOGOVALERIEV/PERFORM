$ErrorActionPreference = 'SilentlyContinue'
function Measure-Dir($path) {
  $out = robocopy $path 'C:\__NULL__' /L /E /XJ /R:0 /W:0 /NFL /NDL /NJH /BYTES /NP 2>$null | Select-String 'Bytes :'
  if ($out) { [long](($out -split '\s+')[3]) } else { 0 }
}
Write-Output '== AppData total re-check'
'{0,15:N0}  AppData TOTAL' -f (Measure-Dir 'C:\Users\User\AppData')
Write-Output '== AppData\Local FULL breakdown (no filter)'
Get-ChildItem 'C:\Users\User\AppData\Local' -Directory -Force | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 50MB) { '{0,15:N0}  {1}' -f $b, $_.Name }
} | Sort-Object -Descending
Write-Output '-- files at Local root > 50MB'
Get-ChildItem 'C:\Users\User\AppData\Local' -File -Force | Where-Object Length -gt 50MB | ForEach-Object { '{0,15:N0}  {1}' -f $_.Length, $_.Name }
Write-Output '== AppData\Roaming full'
Get-ChildItem 'C:\Users\User\AppData\Roaming' -Directory -Force | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 50MB) { '{0,15:N0}  {1}' -f $b, $_.Name }
} | Sort-Object -Descending
Write-Output '== Programs folder (installed apps) breakdown'
Get-ChildItem 'C:\Users\User\AppData\Local\Programs' -Directory -Force | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 50MB) { '{0,15:N0}  {1}' -f $b, $_.Name }
} | Sort-Object -Descending
