<#
.SYNOPSIS
    Deploy GTM Agent to Azure App Service

.DESCRIPTION
    This script deploys the GTM Agent infrastructure and application to Azure App Service.
    It uses Bicep templates for infrastructure and ZIP deployment for the application.

.PARAMETER Environment
    Target environment (dev, staging, prod). Default: dev

.PARAMETER ResourceGroup
    Azure Resource Group name. Default: rg-gtm-agent-{environment}

.PARAMETER Location
    Azure region. Default: westeurope

.PARAMETER Sku
    App Service Plan SKU. Default: B1

.PARAMETER AzureOpenAiEndpoint
    Azure OpenAI endpoint URL (required)

.PARAMETER AzureOpenAiDeployment
    Azure OpenAI deployment name. Default: gpt-4o

.PARAMETER ApiKey
    Optional API key for authentication

.PARAMETER SkipInfra
    Skip infrastructure deployment (only deploy app)

.EXAMPLE
    .\deploy.ps1 -AzureOpenAiEndpoint "https://myopenai.openai.azure.com"

.EXAMPLE
    .\deploy.ps1 -Environment prod -Sku P1V3 -AzureOpenAiEndpoint "https://myopenai.openai.azure.com"
#>

[CmdletBinding()]
param(
    [ValidateSet("dev", "staging", "prod")]
    [string]$Environment = "dev",

    [string]$ResourceGroup,

    [string]$Location = "swedencentral",

    [ValidateSet("B1", "B2", "B3", "P1V3", "P2V3", "P3V3")]
    [string]$Sku = "B1",

    [Parameter(Mandatory = $true)]
    [string]$AzureOpenAiEndpoint,

    [string]$AzureOpenAiDeployment = "gpt-4o",

    [string]$ApiKey = "",

    [switch]$SkipInfra
)

# =============================================================================
# Configuration
# =============================================================================

$ErrorActionPreference = "Stop"
$AppName = "gtm-agent"

if (-not $ResourceGroup) {
    $ResourceGroup = "rg-$AppName-$Environment"
}

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptRoot

Write-Host "=========================================="
Write-Host "GTM Agent - Azure Deployment"
Write-Host "=========================================="
Write-Host "Environment:  $Environment"
Write-Host "Resource Group: $ResourceGroup"
Write-Host "Location:     $Location"
Write-Host "SKU:          $Sku"
Write-Host "=========================================="

# =============================================================================
# Prerequisites Check
# =============================================================================

Write-Host "`n[1/5] Checking prerequisites..."

# Check Azure CLI
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "  ✅ Azure CLI: $($azVersion.'azure-cli')"
} catch {
    Write-Error "Azure CLI is not installed. Please install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Check Azure login
$account = az account show --output json 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Host "  ⚠️ Not logged into Azure. Running 'az login'..."
    az login
    $account = az account show --output json | ConvertFrom-Json
}
Write-Host "  ✅ Logged in as: $($account.user.name)"
Write-Host "  ✅ Subscription: $($account.name)"

# =============================================================================
# Create Resource Group
# =============================================================================

Write-Host "`n[2/5] Creating resource group..."

az group create `
    --name $ResourceGroup `
    --location $Location `
    --tags Application=$AppName Environment=$Environment ManagedBy=Script `
    --output none

Write-Host "  ✅ Resource group: $ResourceGroup"

# =============================================================================
# Deploy Infrastructure
# =============================================================================

if (-not $SkipInfra) {
    Write-Host "`n[3/5] Deploying infrastructure (Bicep)..."

    $deploymentName = "gtm-agent-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    
    try {
        $deployment = az deployment group create `
            --name $deploymentName `
            --resource-group $ResourceGroup `
            --template-file "$ProjectRoot\infra\main.bicep" `
            --parameters `
                appName=$AppName `
                environment=$Environment `
                appServicePlanSku=$Sku `
                azureOpenAiEndpoint=$AzureOpenAiEndpoint `
                azureOpenAiDeployment=$AzureOpenAiDeployment `
                apiKey=$ApiKey `
                logLevel=INFO `
            --output json 2>&1

        if ($LASTEXITCODE -ne 0) {
            Write-Error "Infrastructure deployment failed. Error: $deployment"
            exit 1
        }

        $deploymentJson = $deployment | ConvertFrom-Json
        $webAppName = $deploymentJson.properties.outputs.webAppName.value
        $webAppUrl = $deploymentJson.properties.outputs.webAppUrl.value
        $mcpEndpoint = $deploymentJson.properties.outputs.mcpServerEndpoint.value

        if (-not $webAppName) {
            Write-Error "Failed to get Web App name from deployment output"
            exit 1
        }

        Write-Host "  ✅ Infrastructure deployed"
        Write-Host "     Web App: $webAppName"
    } catch {
        Write-Error "Infrastructure deployment failed: $_"
        exit 1
    }
} else {
    Write-Host "`n[3/5] Skipping infrastructure deployment..."
    $webAppName = "$AppName-$Environment-app"
    $webAppUrl = "https://$webAppName.azurewebsites.net"
    $mcpEndpoint = "$webAppUrl/mcp/mcp"
}

# =============================================================================
# Create Deployment Package
# =============================================================================

Write-Host "`n[4/5] Creating deployment package..."

$tempDir = Join-Path $env:TEMP "gtm-agent-deploy-$(Get-Date -Format 'yyyyMMddHHmmss')"
$zipPath = Join-Path $tempDir "deploy.zip"

New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

# Copy files excluding unnecessary ones
$excludeDirs = @(".git", ".github", ".venv", ".vscode", "__pycache__", ".pytest_cache", ".ruff_cache", "tests", "docs", ".specify")
$excludeFiles = @(".env", ".env.local", "*.pyc")

Push-Location $ProjectRoot
try {
    # Get all files to include
    $filesToInclude = Get-ChildItem -Recurse -File | Where-Object {
        $path = $_.FullName.Replace($ProjectRoot, "").TrimStart("\", "/")
        $include = $true
        
        foreach ($dir in $excludeDirs) {
            if ($path -like "$dir\*" -or $path -like "$dir/*") {
                $include = $false
                break
            }
        }
        
        foreach ($pattern in $excludeFiles) {
            if ($_.Name -like $pattern) {
                $include = $false
                break
            }
        }
        
        $include
    }

    # Create ZIP with Unix-style paths (required for Linux containers)
    # PowerShell's Compress-Archive creates Windows-style paths that don't work on Linux
    $pythonScript = @"
import zipfile
import os

zip_path = r'$zipPath'
project_root = r'$ProjectRoot'

# Files to include
include_patterns = ['src/', 'app.py', 'requirements.txt', 'startup.sh', 'gunicorn.conf.py']

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_root):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.github', '.venv', '.vscode', 
                                                   '.pytest_cache', '.ruff_cache', 'tests', 'docs', 
                                                   '.specify', 'node_modules', 'infra', 'scripts', 'specs']]
        
        for file in files:
            if file.endswith('.pyc') or file.startswith('.env'):
                continue
            
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, project_root)
            
            # Only include specific patterns
            include = False
            for pattern in include_patterns:
                if relpath.startswith(pattern) or relpath == pattern.rstrip('/'):
                    include = True
                    break
            
            if include:
                # Use forward slashes for Linux compatibility
                arcname = relpath.replace('\\\\', '/')
                zipf.write(filepath, arcname)

print(f'Created {zip_path}')
"@

    $pythonScript | python -
    
    $zipSize = (Get-Item $zipPath).Length / 1MB
    Write-Host "  ✅ Package created: $([math]::Round($zipSize, 2)) MB"
} finally {
    Pop-Location
}

# =============================================================================
# Deploy Application
# =============================================================================

Write-Host "`n[5/5] Deploying application..."

az webapp deploy `
    --resource-group $ResourceGroup `
    --name $webAppName `
    --src-path $zipPath `
    --type zip `
    --output none

Write-Host "  ✅ Application deployed"

# Clean up temp files
Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue

# =============================================================================
# Verify Deployment
# =============================================================================

Write-Host "`n[Verification] Checking deployment health..."

$maxAttempts = 10
$attempt = 0
$healthy = $false

while ($attempt -lt $maxAttempts -and -not $healthy) {
    $attempt++
    Write-Host "  Attempt $attempt of $maxAttempts..."
    
    try {
        $response = Invoke-RestMethod -Uri "$webAppUrl/health" -Method Get -TimeoutSec 30
        if ($response.status -eq "healthy") {
            $healthy = $true
            Write-Host "  ✅ Health check passed!"
        }
    } catch {
        Write-Host "  ⚠️ Health check failed, waiting 15 seconds..."
        Start-Sleep -Seconds 15
    }
}

if (-not $healthy) {
    Write-Warning "Health check did not pass after $maxAttempts attempts. Check logs for details."
}

# =============================================================================
# Output Summary
# =============================================================================

Write-Host "`n=========================================="
Write-Host "🚀 Deployment Complete!"
Write-Host "=========================================="
Write-Host "Web App URL:    $webAppUrl"
Write-Host "MCP Server:     $mcpEndpoint"
Write-Host "Health Check:   $webAppUrl/health"
Write-Host "API Docs:       $webAppUrl/docs"
Write-Host "==========================================`n"

Write-Host "To view logs:"
Write-Host "  az webapp log tail --resource-group $ResourceGroup --name $webAppName`n"

Write-Host "To test MCP server:"
Write-Host "  `$headers = @{ 'Accept' = 'application/json, text/event-stream' }"
Write-Host "  `$body = '{""jsonrpc"":""2.0"",""id"":1,""method"":""tools/list"",""params""{}}'"
Write-Host "  Invoke-WebRequest -Uri '$mcpEndpoint' -Method Post -Headers `$headers -Body `$body`n"
