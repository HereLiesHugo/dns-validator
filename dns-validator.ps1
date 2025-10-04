# DNS Validator - PowerShell Script
# Easy launcher for Windows PowerShell users

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptPath "dns_validator.py"

if (Test-Path $PythonScript) {
    python $PythonScript @Arguments
} else {
    Write-Error "dns_validator.py not found in $ScriptPath"
    exit 1
}