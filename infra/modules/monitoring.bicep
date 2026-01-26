// =============================================================================
// Monitoring Module
// =============================================================================
// Creates:
// - Log Analytics Workspace
// - Application Insights
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

@description('Log Analytics retention in days')
@minValue(30)
@maxValue(730)
param logRetentionDays int = 30

// =============================================================================
// Resources
// =============================================================================

// Log Analytics Workspace
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${resourcePrefix}-logs'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: logRetentionDays
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    workspaceCapping: {
      dailyQuotaGb: 1
    }
  }
}

// Application Insights
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${resourcePrefix}-insights'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
    RetentionInDays: logRetentionDays
  }
}

// =============================================================================
// Outputs
// =============================================================================

@description('Application Insights connection string')
output applicationInsightsConnectionString string = applicationInsights.properties.ConnectionString

@description('Application Insights instrumentation key')
output applicationInsightsInstrumentationKey string = applicationInsights.properties.InstrumentationKey

@description('Application Insights name')
output applicationInsightsName string = applicationInsights.name

@description('Application Insights resource ID')
output applicationInsightsResourceId string = applicationInsights.id

@description('Log Analytics Workspace ID')
output logAnalyticsWorkspaceId string = logAnalyticsWorkspace.id

@description('Log Analytics Workspace name')
output logAnalyticsWorkspaceName string = logAnalyticsWorkspace.name
