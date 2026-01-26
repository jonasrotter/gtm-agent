// =============================================================================
// GTM Agent - Azure App Service Infrastructure
// =============================================================================
// Deploys:
// - App Service Plan (Linux)
// - Web App (Python 3.11)
// - Application Insights
// - Log Analytics Workspace
// =============================================================================

targetScope = 'resourceGroup'

// =============================================================================
// Parameters
// =============================================================================

@description('Base name for all resources')
param appName string = 'gtm-agent'

@description('Azure region for resources')
param location string = resourceGroup().location

@description('Environment (dev, staging, prod)')
@allowed(['dev', 'staging', 'prod'])
param environment string = 'dev'

@description('App Service Plan SKU')
@allowed(['B1', 'B2', 'B3', 'P1V3', 'P2V3', 'P3V3'])
param appServicePlanSku string = 'B1'

@description('Azure OpenAI endpoint URL')
@secure()
param azureOpenAiEndpoint string

@description('Azure OpenAI deployment name')
param azureOpenAiDeployment string = 'gpt-5.2'

@description('Azure OpenAI API version')
param azureOpenAiApiVersion string = '2024-02-15-preview'

@description('Optional API key for authentication')
@secure()
param apiKey string = ''

@description('Log level (DEBUG, INFO, WARNING, ERROR)')
@allowed(['DEBUG', 'INFO', 'WARNING', 'ERROR'])
param logLevel string = 'INFO'

// GitHub Copilot SDK Configuration (BYOK mode)
@description('Enable Copilot CLI for SDK code tool (requires Node.js on App Service)')
param copilotCliEnabled bool = false

@description('Copilot CLI server port (used internally)')
param copilotCliPort int = 4321

@description('Use Azure OpenAI as the LLM provider for Copilot SDK (BYOK mode)')
param copilotUseAzureOpenAi bool = true

@description('Azure OpenAI endpoint for Copilot SDK BYOK mode')
@secure()
param copilotAzureOpenAiEndpoint string = ''

@description('Azure OpenAI API key for Copilot SDK BYOK mode')
@secure()
param copilotAzureOpenAiApiKey string = ''

@description('Model name for Copilot SDK')
param copilotModel string = 'gpt-5.2'

// =============================================================================
// Variables
// =============================================================================

var resourcePrefix = '${appName}-${environment}'
var tags = {
  Application: appName
  Environment: environment
  ManagedBy: 'Bicep'
}

// =============================================================================
// Modules
// =============================================================================

// Application Insights and Log Analytics
module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring-deployment'
  params: {
    resourcePrefix: resourcePrefix
    location: location
    tags: tags
  }
}

// App Service Plan and Web App
module appService 'modules/appservice.bicep' = {
  name: 'appservice-deployment'
  params: {
    resourcePrefix: resourcePrefix
    location: location
    tags: tags
    appServicePlanSku: appServicePlanSku
    applicationInsightsConnectionString: monitoring.outputs.applicationInsightsConnectionString
    applicationInsightsInstrumentationKey: monitoring.outputs.applicationInsightsInstrumentationKey
    azureOpenAiEndpoint: azureOpenAiEndpoint
    azureOpenAiDeployment: azureOpenAiDeployment
    azureOpenAiApiVersion: azureOpenAiApiVersion
    apiKey: apiKey
    logLevel: logLevel
    // Copilot SDK configuration
    copilotCliEnabled: copilotCliEnabled
    copilotCliPort: copilotCliPort
    copilotUseAzureOpenAi: copilotUseAzureOpenAi
    copilotAzureOpenAiEndpoint: copilotAzureOpenAiEndpoint
    copilotAzureOpenAiApiKey: copilotAzureOpenAiApiKey
    copilotModel: copilotModel
  }
}

// =============================================================================
// Outputs
// =============================================================================

@description('Web App URL')
output webAppUrl string = appService.outputs.webAppUrl

@description('Web App name')
output webAppName string = appService.outputs.webAppName

@description('MCP Server endpoint')
output mcpServerEndpoint string = '${appService.outputs.webAppUrl}/mcp/mcp'

@description('Health check endpoint')
output healthEndpoint string = '${appService.outputs.webAppUrl}/health'

@description('Application Insights name')
output applicationInsightsName string = monitoring.outputs.applicationInsightsName

@description('Log Analytics Workspace ID')
output logAnalyticsWorkspaceId string = monitoring.outputs.logAnalyticsWorkspaceId
