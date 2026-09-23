$ErrorActionPreference = 'SilentlyContinue'
function Measure-Dir($path) {
  $out = robocopy $path 'C:\__NULL__' /L /E /XJ /R:0 /W:0 /NFL /NDL /NJH /BYTES /NP 2>$null | Select-String 'Bytes :'
  if ($out) { [long](($out -split '\s+')[3]) } else { 0 }
}
Write-Output '== lfs-7-clean-cutover A (Users\User) top items'
Get-ChildItem 'C:\Users\User\lfs-7-clean-cutover' -Force | ForEach-Object {
  if ($_.PSIsContainer) { $b = Measure-Dir $_.FullName } else { $b = $_.Length }
  '{0,15:N0}  {1}' -f $b, $_.Name
}
Write-Output '== lfs-7-clean-cutover B (kinetic-scale) top items'
Get-ChildItem 'C:\Users\User\Desktop\kinetic-scale\lfs-7-clean-cutover' -Force | ForEach-Object {
  if ($_.PSIsContainer) { $b = Measure-Dir $_.FullName } else { $b = $_.Length }
  '{0,15:N0}  {1}' -f $b, $_.Name }
Write-Output '== Recycle Bin size'
'{0,15:N0}  RecycleBin' -f (Measure-Dir 'C:\$Recycle.Bin')
Write-Output '== C:\Windows total (may underreport)'
'{0,15:N0}  Windows' -f (Measure-Dir 'C:\Windows')
Write-Output '== Windows.old? Installer caches?'
Get-ChildItem 'C:\' -Directory -Force | Where-Object Name -match 'old|Windows' | Select-Object -ExpandProperty Name
'{0,15:N0}  C:\Windows\Installer' -f (Measure-Dir 'C:\Windows\Installer')
'{0,15:N0}  C:\Windows\SoftwareDistribution' -f (Measure-Dir 'C:\Windows\SoftwareDistribution')
'{0,15:N0}  C:\Windows\WinSxS' -f (Measure-Dir 'C:\Windows\WinSxS')
'{0,15:N0}  C:\Windows\Temp' -f (Measure-Dir 'C:\Windows\Temp')
'{0,15:N0}  C:\Windows\System32\LogFiles' -f (Measure-Dir 'C:\Windows\System32\LogFiles')
'{0,15:N0}  C:\ProgramData\Package Cache' -f (Measure-Dir 'C:\ProgramData\Package Cache')
