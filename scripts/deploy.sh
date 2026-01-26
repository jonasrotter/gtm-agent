#!/bin/bash
# =============================================================================
# GTM Agent - Azure App Service Deployment Script (Bash)
# =============================================================================
# Usage: ./deploy.sh --endpoint "https://myopenai.openai.azure.com"
# =============================================================================

set -e

# =============================================================================
# Configuration
# =============================================================================

APP_NAME="gtm-agent"
ENVIRONMENT="${ENVIRONMENT:-dev}"
LOCATION="${LOCATION:-westeurope}"
SKU="${SKU:-B1}"
RESOURCE_GROUP="${RESOURCE_GROUP:-rg-$APP_NAME-$ENVIRONMENT}"
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_DEPLOYMENT="${AZURE_OPENAI_DEPLOYMENT:-gpt-4o}"
API_KEY=""
SKIP_INFRA=false

# =============================================================================
# Parse Arguments
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            RESOURCE_GROUP="rg-$APP_NAME-$ENVIRONMENT"
            shift 2
            ;;
        -l|--location)
            LOCATION="$2"
            shift 2
            ;;
        -s|--sku)
            SKU="$2"
            shift 2
            ;;
        -g|--resource-group)
            RESOURCE_GROUP="$2"
            shift 2
            ;;
        --endpoint)
            AZURE_OPENAI_ENDPOINT="$2"
            shift 2
            ;;
        --deployment)
            AZURE_OPENAI_DEPLOYMENT="$2"
            shift 2
            ;;
        --api-key)
            API_KEY="$2"
            shift 2
            ;;
        --skip-infra)
            SKIP_INFRA=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 --endpoint <azure-openai-endpoint> [options]"
            echo ""
            echo "Options:"
            echo "  -e, --environment    Environment (dev, staging, prod). Default: dev"
            echo "  -l, --location       Azure region. Default: westeurope"
            echo "  -s, --sku            App Service SKU. Default: B1"
            echo "  -g, --resource-group Resource group name"
            echo "  --endpoint           Azure OpenAI endpoint (required)"
            echo "  --deployment         Azure OpenAI deployment name. Default: gpt-4o"
            echo "  --api-key            API key for authentication"
            echo "  --skip-infra         Skip infrastructure deployment"
            echo "  -h, --help           Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$AZURE_OPENAI_ENDPOINT" ]; then
    echo "Error: --endpoint is required"
    echo "Usage: $0 --endpoint <azure-openai-endpoint>"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "GTM Agent - Azure Deployment"
echo "=========================================="
echo "Environment:    $ENVIRONMENT"
echo "Resource Group: $RESOURCE_GROUP"
echo "Location:       $LOCATION"
echo "SKU:            $SKU"
echo "=========================================="

# =============================================================================
# Prerequisites Check
# =============================================================================

echo -e "\n[1/5] Checking prerequisites..."

# Check Azure CLI
if ! command -v az &> /dev/null; then
    echo "Error: Azure CLI is not installed"
    echo "Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi
echo "  ✅ Azure CLI installed"

# Check Azure login
if ! az account show &> /dev/null; then
    echo "  ⚠️ Not logged into Azure. Running 'az login'..."
    az login
fi
ACCOUNT=$(az account show --output json)
echo "  ✅ Logged in: $(echo $ACCOUNT | jq -r '.user.name')"
echo "  ✅ Subscription: $(echo $ACCOUNT | jq -r '.name')"

# =============================================================================
# Create Resource Group
# =============================================================================

echo -e "\n[2/5] Creating resource group..."

az group create \
    --name "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --tags Application=$APP_NAME Environment=$ENVIRONMENT ManagedBy=Script \
    --output none

echo "  ✅ Resource group: $RESOURCE_GROUP"

# =============================================================================
# Deploy Infrastructure
# =============================================================================

if [ "$SKIP_INFRA" = false ]; then
    echo -e "\n[3/5] Deploying infrastructure (Bicep)..."

    DEPLOYMENT_NAME="gtm-agent-$(date +%Y%m%d-%H%M%S)"
    
    DEPLOYMENT=$(az deployment group create \
        --name "$DEPLOYMENT_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --template-file "$PROJECT_ROOT/infra/main.bicep" \
        --parameters \
            appName=$APP_NAME \
            environment=$ENVIRONMENT \
            appServicePlanSku=$SKU \
            azureOpenAiEndpoint="$AZURE_OPENAI_ENDPOINT" \
            azureOpenAiDeployment="$AZURE_OPENAI_DEPLOYMENT" \
            apiKey="$API_KEY" \
            logLevel=INFO \
        --output json)

    WEB_APP_NAME=$(echo $DEPLOYMENT | jq -r '.properties.outputs.webAppName.value')
    WEB_APP_URL=$(echo $DEPLOYMENT | jq -r '.properties.outputs.webAppUrl.value')
    MCP_ENDPOINT=$(echo $DEPLOYMENT | jq -r '.properties.outputs.mcpServerEndpoint.value')

    echo "  ✅ Infrastructure deployed"
    echo "     Web App: $WEB_APP_NAME"
else
    echo -e "\n[3/5] Skipping infrastructure deployment..."
    WEB_APP_NAME="$APP_NAME-$ENVIRONMENT-app"
    WEB_APP_URL="https://$WEB_APP_NAME.azurewebsites.net"
    MCP_ENDPOINT="$WEB_APP_URL/mcp/mcp"
fi

# =============================================================================
# Create Deployment Package
# =============================================================================

echo -e "\n[4/5] Creating deployment package..."

TEMP_DIR=$(mktemp -d)
ZIP_PATH="$TEMP_DIR/deploy.zip"

cd "$PROJECT_ROOT"

# Create ZIP excluding unnecessary files
zip -r "$ZIP_PATH" . \
    -x ".git/*" \
    -x ".github/*" \
    -x ".venv/*" \
    -x ".vscode/*" \
    -x "__pycache__/*" \
    -x "*.pyc" \
    -x ".pytest_cache/*" \
    -x ".ruff_cache/*" \
    -x "tests/*" \
    -x "docs/*" \
    -x ".env" \
    -x ".env.local" \
    -x ".specify/*" \
    > /dev/null

ZIP_SIZE=$(du -h "$ZIP_PATH" | cut -f1)
echo "  ✅ Package created: $ZIP_SIZE"

# =============================================================================
# Deploy Application
# =============================================================================

echo -e "\n[5/5] Deploying application..."

az webapp deploy \
    --resource-group "$RESOURCE_GROUP" \
    --name "$WEB_APP_NAME" \
    --src-path "$ZIP_PATH" \
    --type zip \
    --output none

echo "  ✅ Application deployed"

# Clean up
rm -rf "$TEMP_DIR"

# =============================================================================
# Verify Deployment
# =============================================================================

echo -e "\n[Verification] Checking deployment health..."

MAX_ATTEMPTS=10
ATTEMPT=0
HEALTHY=false

while [ $ATTEMPT -lt $MAX_ATTEMPTS ] && [ "$HEALTHY" = false ]; do
    ATTEMPT=$((ATTEMPT + 1))
    echo "  Attempt $ATTEMPT of $MAX_ATTEMPTS..."
    
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$WEB_APP_URL/health" 2>/dev/null || echo "000")
    
    if [ "$RESPONSE" = "200" ]; then
        HEALTHY=true
        echo "  ✅ Health check passed!"
    else
        echo "  ⚠️ Got $RESPONSE, waiting 15 seconds..."
        sleep 15
    fi
done

if [ "$HEALTHY" = false ]; then
    echo "  ⚠️ Health check did not pass after $MAX_ATTEMPTS attempts"
fi

# =============================================================================
# Output Summary
# =============================================================================

echo ""
echo "=========================================="
echo "🚀 Deployment Complete!"
echo "=========================================="
echo "Web App URL:    $WEB_APP_URL"
echo "MCP Server:     $MCP_ENDPOINT"
echo "Health Check:   $WEB_APP_URL/health"
echo "API Docs:       $WEB_APP_URL/docs"
echo "=========================================="
echo ""
echo "To view logs:"
echo "  az webapp log tail --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
echo ""
