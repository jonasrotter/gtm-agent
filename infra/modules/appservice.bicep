// =============================================================================
// App Service Module
// =============================================================================
// Creates:
// - App Service Plan (Linux, Python)
// - Web App with configured environment variables
// - System-assigned managed identity
// =============================================================================

// =============================================================================
// Parameters
// =============================================================================

@description('Resource name prefix')
param resourcePrefix string

@description('Azure region')
param location string

@description('Resource tags')
param tags object

@description('App Service Plan SKU')
param appServicePlanSku string

@description('Application Insights connection string')
@secure()
param applicationInsightsConnectionString string

@description('Application Insights instrumentation key')
@secure()
param applicationInsightsInstrumentationKey string

@description('Azure OpenAI endpoint')
@secure()
param azureOpenAiEndpoint string

@description('Azure OpenAI deployment name')
param azureOpenAiDeployment string

@description('Azure OpenAI API version')
param azureOpenAiApiVersion string

@description('API key for authentication')
@secure()
param apiKey string

@description('Log level')
param logLevel string

// GitHub Copilot SDK Configuration
@description('Enable Copilot CLI for SDK code tool')
param copilotCliEnabled bool = false

@description('Copilot CLI server port')
param copilotCliPort int = 4321

@description('Use Azure OpenAI for Copilot SDK (BYOK mode)')
param copilotUseAzureOpenAi bool = true

@description('Azure OpenAI endpoint for Copilot SDK')
@secure()
param copilotAzureOpenAiEndpoint string = ''

@description('Azure OpenAI API key for Copilot SDK')
@secure()
param copilotAzureOpenAiApiKey string = ''

@description('Model name for Copilot SDK')
param copilotModel string = 'gpt-4o'

// =============================================================================
// Variables
// =============================================================================

// Build Copilot CLI URL only if enabled
var copilotCliUrl = copilotCliEnabled ? 'localhost:${copilotCliPort}' : ''

// =============================================================================
// Resources
// =============================================================================

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: '${resourcePrefix}-plan'
  location: location
  tags: tags
  kind: 'linux'
  sku: {
    name: appServicePlanSku
  }
  properties: {
    reserved: true // Required for Linux
  }
}

// Web App
resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: '${resourcePrefix}-app'
  location: location
  tags: union(tags, {
    'azd-service-name': 'web'
  })
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      alwaysOn: true
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      http20Enabled: true
      // Startup command for FastAPI with Gunicorn
      // Note: Copilot SDK code tool requires local Copilot CLI - not available in Azure App Service
      appCommandLine: 'gunicorn src.api:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 300'
      // App settings
      appSettings: [
        // Application Configuration
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'ENABLE_ORYX_BUILD'
          value: 'true'
        }
        // Azure OpenAI Configuration
        {
          name: 'AZURE_OPENAI_ENDPOINT'
          value: azureOpenAiEndpoint
        }
        {
          name: 'AZURE_OPENAI_DEPLOYMENT'
          value: azureOpenAiDeployment
        }
        {
          name: 'AZURE_OPENAI_API_VERSION'
          value: azureOpenAiApiVersion
        }
        // Authentication
        {
          name: 'API_KEY'
          value: apiKey
        }
        // Logging
        {
          name: 'LOG_LEVEL'
          value: logLevel
        }
        {
          name: 'LOG_FORMAT'
          value: 'json'
        }
        // Application Insights
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: applicationInsightsConnectionString
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: applicationInsightsInstrumentationKey
        }
        // Python-specific
        {
          name: 'PYTHONUNBUFFERED'
          value: '1'
        }
        {
          name: 'WEBSITE_HTTPLOGGING_RETENTION_DAYS'
          value: '7'
        }
        // GitHub Copilot SDK Configuration
        {
          name: 'COPILOT_CLI_URL'
          value: copilotCliUrl
        }
        {
          name: 'COPILOT_USE_AZURE_OPENAI'
          value: string(copilotUseAzureOpenAi)
        }
        {
          name: 'COPILOT_MODEL'
          value: copilotModel
        }
        {
          name: 'COPILOT_AZURE_OPENAI_ENDPOINT'
          value: copilotAzureOpenAiEndpoint
        }
        {
          name: 'COPILOT_AZURE_OPENAI_API_KEY'
          value: copilotAzureOpenAiApiKey
        }
        {
          name: 'COPILOT_AZURE_OPENAI_API_VERSION'
          value: '2024-10-21'
        }
      ]
    }
  }
}

// Logging configuration
resource webAppLogs 'Microsoft.Web/sites/config@2023-12-01' = {
  parent: webApp
  name: 'logs'
  properties: {
    httpLogs: {
      fileSystem: {
        enabled: true
        retentionInDays: 7
        retentionInMb: 35
      }
    }
    applicationLogs: {
      fileSystem: {
        level: 'Information'
      }
    }
    detailedErrorMessages: {
      enabled: true
    }
    failedRequestsTracing: {
      enabled: true
    }
  }
}

// =============================================================================
// Outputs
// =============================================================================

@description('Web App URL')
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'

@description('Web App name')
output webAppName string = webApp.name

@description('Web App resource ID')
output webAppResourceId string = webApp.id

@description('Web App principal ID (managed identity)')
output webAppPrincipalId string = webApp.identity.principalId

@description('App Service Plan name')
output appServicePlanName string = appServicePlan.name
