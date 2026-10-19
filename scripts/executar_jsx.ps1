param(
    [Parameter(Mandatory=$true)] [string]$ScriptPath
)
$ErrorActionPreference = 'Stop'
$resolvedScript = (Resolve-Path -LiteralPath $ScriptPath).Path
if ([System.IO.Path]::GetExtension($resolvedScript) -ne '.jsx') {
    throw 'Informe um arquivo JSX.'
}
$photoshop = New-Object -ComObject Photoshop.Application
$result = $photoshop.DoJavaScriptFile($resolvedScript)
Write-Output $result
Write-Output 'JSX retornou. Confira log, PSD e todas as provas antes de aprovar a APN.'
