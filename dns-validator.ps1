# DNS Validator - PowerShell Script
# Easy launcher for Windows PowerShell users

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptPath "dns_validator_cli.py"

if (Test-Path $PythonScript) {
    python $PythonScript @Arguments
} else {
    Write-Error "dns_validator_cli.py not found in $ScriptPath"
    exit 1
}