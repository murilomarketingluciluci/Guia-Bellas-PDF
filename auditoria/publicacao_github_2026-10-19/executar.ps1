param(
    [Parameter(Mandatory=$true)][string]$ActionId,
    [Parameter(Mandatory=$true)][string]$Objective,
    [Parameter(Mandatory=$true)][string]$Command
)
$ErrorActionPreference = 'Stop'
$auditRoot = $PSScriptRoot
$diary = Join-Path $auditRoot 'principal.jsonl'
$scriptHash = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash
$eventBase = @{
    action_id = $ActionId
    agent = 'principal'
    objective = $Objective
    tool = 'exec_command/PowerShell'
    parameters_exact = @{ command = $Command }
    script_version_file = 'auditoria/publicacao_github_2026-10-19/executar.ps1'
    sha256 = @{ executor = $scriptHash }
}
$before = $eventBase.Clone()
$before.timestamp = [DateTimeOffset]::UtcNow.ToString('o')
$before.event = 'started'
$before.status = 'running'
Add-Content -LiteralPath $diary -Value ($before | ConvertTo-Json -Depth 12 -Compress) -Encoding utf8
$global:LASTEXITCODE = 0
$actionOutput = ''
$resultCode = 0
try {
    $actionOutput = (& ([ScriptBlock]::Create($Command)) 2>&1 | Out-String -Width 260)
    $resultCode = $global:LASTEXITCODE
} catch {
    $actionOutput += $_.Exception.Message
    $resultCode = 1
}
$after = $eventBase.Clone()
$after.timestamp = [DateTimeOffset]::UtcNow.ToString('o')
$after.event = 'result'
$after.status = $(if ($resultCode -eq 0) { 'succeeded' } else { 'failed' })
$after.exit_code = $resultCode
$after.result = $actionOutput
Add-Content -LiteralPath $diary -Value ($after | ConvertTo-Json -Depth 12 -Compress) -Encoding utf8
Write-Output $actionOutput
exit $resultCode
