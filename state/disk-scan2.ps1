$ErrorActionPreference = 'SilentlyContinue'
function Measure-Dir($path) {
  $out = robocopy $path 'C:\__NULL__' /L /E /XJ /R:0 /W:0 /NFL /NDL /NJH /BYTES /NP 2>$null | Select-String 'Bytes :'
  if ($out) { [long](($out -split '\s+')[3]) } else { 0 }
}
Write-Output '== kinetic-scale breakdown'
Get-ChildItem 'C:\Users\User\Desktop\kinetic-scale' -Directory -Force | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 100MB) { '{0,15:N0}  {1}' -f $b, $_.Name }
}
Write-Output '-- kinetic-scale files > 100MB'
Get-ChildItem 'C:\Users\User\Desktop\kinetic-scale' -File -Force | Where-Object Length -gt 100MB | ForEach-Object { '{0,15:N0}  {1}' -f $_.Length, $_.Name }
Write-Output '== node_modules anywhere under user profile (top 15)'
Get-ChildItem 'C:\Users\User\Desktop' -Directory -Recurse -Force -Filter 'node_modules' -Depth 4 | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 100MB) { '{0,15:N0}  {1}' -f $b, $_.FullName }
} | Sort-Object -Descending
Write-Output '== .venv / venv folders'
Get-ChildItem 'C:\Users\User\Desktop' -Directory -Recurse -Force -Depth 4 | Where-Object Name -in '.venv','venv' | ForEach-Object {
  $b = Measure-Dir $_.FullName
  if ($b -gt 100MB) { '{0,15:N0}  {1}' -f $b, $_.FullName }
}
Write-Output '== Ruflo family on Desktop'
Get-ChildItem 'C:\Users\User\Desktop' -Directory -Force | Where-Object Name -like '*ruflo*' | ForEach-Object { '{0,15:N0}  {1}' -f (Measure-Dir $_.FullName), $_.Name }
