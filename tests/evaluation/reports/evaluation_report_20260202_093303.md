# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T09:33:03.325026
- **Evaluation File**: tests/evaluation/evaluation.xml
- **Mode**: api

### Results Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 30 |
| Passed | 1 |
| Failed | 29 |
| Pass Rate | 3.3% |

### Dimension Scores

| Dimension | Score | Target | Status |
|-----------|-------|--------|--------|
| Routing Accuracy | 100.0% | 90% | ✅ |
| Tool Selection | 0.0% | 85% | ❌ |
| Keyword Coverage | 94.2% | 75% | ✅ |
| Performance | 82.5% | 80% | ✅ |

### Token Usage

| Metric | Count |
|--------|-------|
| Input Tokens | 0 |
| Output Tokens | 0 |
| Total Tokens | 0 |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 1 (20%) | 0.69 | 94.8s |
| code | 10 | 0 (0%) | 0.62 | 153.5s |
| complex | 5 | 0 (0%) | 0.59 | 180.3s |
| research | 10 | 0 (0%) | 0.63 | 101.8s |

## Recommendations

1. Tool selection accuracy is 0.0% (target: 85%). Review planner prompts to improve tool selection logic.
2. Category 'research' has 0.0% pass rate. Review failed tasks for common issues.
3. Category 'architecture' has 20.0% pass rate. Review failed tasks for common issues.
4. Category 'code' has 0.0% pass rate. Review failed tasks for common issues.
5. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ❌ FAILED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 15.81s |
| Overall Score | 0.56 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage is Microsoft Azure’s object storage service for storing large amounts of unstructured data—such as text, images, video, backups, logs, and data files—accessible over HTTP/HTTPS.

Key points:
- **“Blob” = Binary Large Object**: stored as objects in **containers** within a **storage account**.
- **Designed for scale and durability**: supports massive data volumes with high availability options.
- **Common uses**: data lakes/analytics staging, serving files to apps or websites, b...
```

</details>

---

### factual_002: ❌ FAILED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 16.79s |
| Overall Score | 0.60 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage supports these **access tiers**:

- **Hot** – Optimized for frequent access (higher storage cost, lower access cost).
- **Cool** – Optimized for infrequent access (lower storage cost, higher access cost; intended for data kept at least ~30 days).
- **Cold** – Lower storage cost than cool for rarely accessed data (higher access cost; intended for data kept at least ~90 days).
- **Archive** – Lowest storage cost for long-term retention (offline; must be rehydrated to hot/cool/co...
```

</details>

---

### factual_003: ❌ FAILED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 31.53s |
| Overall Score | 0.67 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Azure Functions and Azure Logic Apps are both “serverless” ways to run work in Azure, but they target different kinds of problems.

## Core difference
- **Azure Functions**: *Code-first compute.* You write code (C#, JavaScript/TypeScript, Python, etc.) that runs in response to events (HTTP requests, messages, timers, blobs, etc.).
- **Azure Logic Apps**: *Workflow/orchestration-first integration.* You build workflows (low-code/designer or code view) that connect services via connectors, route da...
```

</details>

---

### factual_004: ❌ FAILED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 15.54s |
| Overall Score | 0.57 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Azure OpenAI is available in a **subset of Azure regions**, and the list changes over time. Microsoft maintains the up-to-date list here:

- **Azure OpenAI regions (official docs):** https://learn.microsoft.com/azure/ai-services/openai/concepts/models#model-availability

That section shows **which regions support Azure OpenAI** and, importantly, **which models are available in each region**. Azure OpenAI is available in a **subset of Azure regions**, and the list changes over time. Microsoft mai...
```

</details>

---

### factual_005: ❌ FAILED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 21.67s |
| Overall Score | 0.67 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Azure App Service pricing is based on the **App Service plan** tier you choose (which determines compute size/features). The main tiers are:

- **Free (F1)**: Shared infrastructure, limited resources; good for dev/test.
- **Shared (D1)**: Shared infrastructure, low-cost dev/test (more than Free).
- **Basic (B1–B3)**: Dedicated VM instances; suitable for low-traffic production.
- **Standard (S1–S3)**: Dedicated instances + production features like autoscale and traffic manager support.
- **Premiu...
```

</details>

---

### howto_001: ❌ FAILED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 167.14s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

## Step 1 — Research output: Recommended GitHub Actions workflow for deploying Azure Functions

### Required Azure resources (pre-reqs)
To deploy with GitHub Actions, you need an existing **Function App** (the workflow deploys code; provisioning is typically separate). A Function App requires:
- **Storage account** (required by Azure Functions)
- Hosting: **Consumption** or **Premium** or **Dedicated (App Service plan)**
- Commonly **Application Insights** for monitoring

So...
```

</details>

---

### howto_002: ❌ FAILED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 160.38s |
| Overall Score | 0.66 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To configure **VNet Integration** for **Azure App Service** (so the app can make **outbound** calls into a VNet):

**Prereqs**
- App Service plan that supports VNet Integration (commonly **Basic+ / Standard+**).
- A **dedicated, empty subnet** in the target VNet, **delegated** to `Microsoft.Web/serverFarms` (Microsoft recommends **/27 or larger**).

**Azure Portal steps**
1. Azure portal → **App Services** → select your app  
2. **Networking** → under **Outbound Traffic** ch...
```

</details>

---

### howto_003: ❌ FAILED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 145.50s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To enable Application Insights for an Azure Function, you can do it either at creation time or after the Function App exists:

## Option 1 (recommended): Enable during Function App creation (Portal)
1. Create a new **Function App**.
2. Open the **Monitoring** tab.
3. Set **Enable Application Insights** = **Yes**.
4. Select an existing Application Insights resource or create a new one.
5. Create the Function App.

## Option 2: Enable for an existing Function App (Portal)
1. O...
```

</details>

---

### howto_004: ❌ FAILED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 284.45s |
| Overall Score | 0.63 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

## Step 1 (research output): Authoritative Azure docs + steps

### Primary Microsoft documentation
- App Service managed identity (system- and user-assigned): https://learn.microsoft.com/azure/app-service/overview-managed-identity  
- Azure CLI `az webapp identity` (enable/assign/show identity): https://learn.microsoft.com/cli/azure/webapp/identity  
- Key Vault authorization via Azure RBAC: https://learn.microsoft.com/azure/key-vault/general/rbac-guide  
- Key Vault access ...
```

</details>

---

### howto_005: ❌ FAILED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 159.60s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

## Step 1 (research): Official Azure guidance for AKS autoscaling

### Cluster Autoscaler (node pool autoscale)
- Primary doc: **Cluster Autoscaler in AKS** (how it works, portal + CLI enablement, min/max per node pool, considerations/limitations)  
  https://learn.microsoft.com/azure/aks/cluster-autoscaler
- Configuration options called out in the doc include enabling autoscaler on a node pool and setting bounds (min/max node counts), via:
  - **Azure portal** (node pool → ...
```

</details>

---

### arch_001: ❌ FAILED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 91.13s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

## Step output (Research): Best practices for Azure App Service security

- **Identity & access**
  - Use **Microsoft Entra ID (Azure AD)** / App Service Authentication for sign-in; enforce MFA/Conditional Access.
  - Use **managed identities** to access Azure resources (avoid stored credentials).
  - Apply **least-privilege RBAC** for App Service and deployment slots.
  - **Restrict SCM (Kudu)** access; treat it as an admin endpoint.

- **Secrets management**
  - Store secr...
```

</details>

---

### arch_002: ❌ FAILED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 103.30s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

A highly available (HA) web application on Azure is typically built to survive **instance**, **Availability Zone**, and often **regional** failures by adding redundancy at each layer (ingress, compute, data, operations).

**Key building blocks and references (Microsoft docs):**
- Reference architectures:
  - Basic web app (single region, scalable/HA within region): https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/app-service-web-app/basic-web-app ...
```

</details>

---

### arch_003: ✅ PASSED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 37.90s |
| Overall Score | 0.70 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Below are practical, high-impact **cost optimization strategies for Azure Kubernetes Service (AKS)**, organized by where you typically save the most.

## 1) Right-size and autoscale compute
- **Use the Cluster Autoscaler** to automatically add/remove nodes based on pending pods; avoid paying for idle nodes. Tune min/max per node pool and scale-down behavior.  
  Docs: https://learn.microsoft.com/azure/aks/cluster-autoscaler
- **Use Horizontal Pod Autoscaler (HPA)** so workloads scale based on CP...
```

</details>

---

### arch_004: ❌ FAILED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 300.01s |
| Overall Score | 0.48 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: Timeout after 300.0s

---

### arch_005: ❌ FAILED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 146.71s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: architecture

## Step 1 Output — Recommended reference architecture for multi-tenant SaaS on Azure

### 1) Tenancy models
- **Shared (pooled):** shared compute + shared DB with `TenantId` discriminator. Lowest cost, highest scale; needs strong tenant-boundary enforcement.
- **Siloed:** per-tenant compute and/or per-tenant DB/storage. Best isolation for regulated/large tenants; higher ops overhead.
- **Hybrid (recommended):** default tenants pooled; “premium/regulated” tenants can be u...
```

</details>

---

### code_cli_001: ❌ FAILED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 154.48s |
| Overall Score | 0.63 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: code

```bash
# Variables (edit as needed)
SUBSCRIPTION_ID="<subscription-id>"
LOCATION="eastus"
RG="rg-pe-storage"
VNET_NAME="vnet-pe"
SUBNET_NAME="snet-pe"
PE_SUBNET_NAME="snet-endpoints"
SA_NAME="<globally-unique-sa-name>"   # must be 3-24 chars, lowercase+numbers only
PE_NAME="pe-${SA_NAME}"
DNS_ZONE_BLOB="privatelink.blob.core.windows.net"
DNS_ZONE_FILE="privatelink.file.core.windows.net"
DNS_ZONE_QUEUE="privatelink.queue.core.windows.net"
DNS_ZONE_TABLE="privatelink.table.core.w...
```

</details>

---

### code_cli_002: ❌ FAILED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 144.34s |
| Overall Score | 0.52 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---

### code_cli_003: ❌ FAILED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 272.23s |
| Overall Score | 0.46 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---

### code_sdk_001: ❌ FAILED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 146.79s |
| Overall Score | 0.52 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---

### code_sdk_002: ❌ FAILED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 149.56s |
| Overall Score | 0.67 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: code

```python
# pip install azure-servicebus

from azure.servicebus import ServiceBusClient, ServiceBusMessage

# --- Minimal setup placeholders ---
CONNECTION_STR = "<SERVICE_BUS_CONNECTION_STRING>"  # e.g., from Azure Portal -> Service Bus -> Shared access policies
QUEUE_NAME = "<QUEUE_NAME>"

def main():
    # Create a client using the connection string (SAS auth)
    servicebus_client = ServiceBusClient.from_connection_string(
        conn_str=CONNECTION_STR,
        logging_ena...
```

</details>

---

### code_sdk_003: ❌ FAILED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 147.73s |
| Overall Score | 0.67 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: code

### Required NuGet packages

```bash
dotnet add package Azure.Identity
dotnet add package Azure.Security.KeyVault.Secrets
```

### Minimal C# example: read a secret with `DefaultAzureCredential`

```csharp
using System;
using System.Threading.Tasks;
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

class Program
{
    static async Task Main()
    {
        // e.g., "https://my-vault-name.vault.azure.net/"
        var keyVaultUrl = Environment.GetEnvironmentVariable("...
```

</details>

---

### code_iac_001: ❌ FAILED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 164.57s |
| Overall Score | 0.65 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: code

```bicep
@description('Azure region for all resources.')
param location string = resourceGroup().location

@description('Prefix used for resource names. Use lowercase alphanumerics and hyphens.')
param namePrefix string

@description('SKU name for the App Service plan.')
@allowed([
  'F1'
  'B1'
  'B2'
  'B3'
  'S1'
  'S2'
  'S3'
  'P1v3'
  'P2v3'
  'P3v3'
])
param appServicePlanSkuName string = 'S1'

@description('Number of workers/instances for the App Service plan.')
param ap...
```

</details>

---

### code_iac_002: ❌ FAILED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 158.75s |
| Overall Score | 0.50 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---

### code_iac_003: ❌ FAILED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 150.63s |
| Overall Score | 0.50 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---

### code_iac_004: ❌ FAILED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 151.32s |
| Overall Score | 0.50 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: code

It looks like the **code** tool didn’t return any output (“No response generated”). I can’t complete Step 1 as written without a tool result.

If you want, I can still provide the ARM template directly here (same content you requested), or you can ask to re-run the tool. It looks like the **code** tool didn’t return any output (“No response generated”). I can’t complete Step 1 as written without a tool result.

If you want, I can still provide the ARM template directly here (sam...
```

</details>

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 300.01s |
| Overall Score | 0.37 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: Timeout after 300.0s

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 180.29s |
| Overall Score | 0.59 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: code

## Consolidated migration plan: On‑premises SQL Server → Azure SQL Database

### 1) Assess & choose the right target
- **Confirm fit for Azure SQL Database (PaaS):** Review feature compatibility (SQL Agent jobs, cross-database queries, CLR, FILESTREAM, SSIS, etc.). If heavy instance-level dependencies exist, consider **Azure SQL Managed Instance** instead.
- **Run discovery/assessment:**
  - Use **Data Migration Assistant (DMA)** to identify breaking changes, deprecated features...
```

</details>

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 300.02s |
| Overall Score | 0.37 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: Timeout after 300.0s

---

### complex_004: ❌ FAILED

**Prompt**: Design a data analytics solution on Azure for processing IoT sensor data. Include architecture recommendations using Event Hubs and Stream Analytics, plus sample code for an Azure Function to process the events.

| Metric | Value |
|--------|-------|
| Duration | 27.49s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 236.88s |
| Overall Score | 0.39 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---
