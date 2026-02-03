# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T19:54:48.985742
- **Evaluation File**: tests/evaluation/evaluation.xml
- **Mode**: api

### Results Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 30 |
| Passed | 19 |
| Failed | 11 |
| Pass Rate | 63.3% |

### Dimension Scores

| Dimension | Score | Target | Status |
|-----------|-------|--------|--------|
| Routing Accuracy | 100.0% | 90% | ✅ |
| Tool Selection | 96.9% | 85% | ✅ |
| Keyword Coverage | 70.2% | 75% | ❌ |
| Performance | 95.6% | 80% | ✅ |

### Token Usage

| Metric | Count |
|--------|-------|
| Input Tokens | 0 |
| Output Tokens | 0 |
| Total Tokens | 0 |

## Tool Call Analysis

| Tool | Calls | Avg Duration | Success Rate |
|------|-------|--------------|--------------|
| code | 17 | 0.00s | 100.0% |
| research | 11 | 0.00s | 100.0% |
| architecture | 4 | 0.00s | 100.0% |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 0 (0%) | 0.00 | 0.0s |
| code | 10 | 10 (100%) | 0.84 | 77.1s |
| complex | 5 | 0 (0%) | 0.64 | 244.9s |
| research | 10 | 9 (90%) | 0.90 | 60.8s |

## Recommendations

1. Average keyword coverage is 70.2% (target: 75%). Responses may be missing key information. Check sub-agent prompts.
2. Category 'architecture' has 0.0% pass rate. Review failed tasks for common issues.
3. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ✅ PASSED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 24.21s |
| Overall Score | 0.86 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage is Microsoft Azure’s object storage service for storing large amounts of unstructured data—such as text, images, video, audio, backups, logs, and data files.

Key points:
- **“Blob” = Binary Large Object**: stored as objects in containers within a storage account.
- **Highly scalable and durable**: designed to handle massive data volumes and high throughput.
- **Access methods**: via Azure Portal, REST APIs, SDKs, Azure CLI/PowerShell, and tools like AzCopy/Storage Explorer.
-...
```

</details>

---

### factual_002: ✅ PASSED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 22.09s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage supports these access tiers:

- **Hot**: Optimized for frequent access.
- **Cool**: Optimized for infrequent access (lower storage cost, higher access cost than Hot).
- **Cold**: Optimized for very infrequent access/longer retention (typically lower storage cost than Cool, higher access cost).
- **Archive**: Lowest storage cost for data that’s rarely accessed; data must be **rehydrated** before it can be read.

Notes:
- **Hot/Cool/Cold** are *online* tiers (immediate access).
...
```

</details>

---

### factual_003: ✅ PASSED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 36.14s |
| Overall Score | 0.99 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
## Core difference

- **Azure Functions**: *Serverless compute* for running **code** in response to events (HTTP requests, queues, timers, Event Grid, etc.). You build and deploy functions in languages like C#, JavaScript/TypeScript, Python, Java, PowerShell, etc.  
  Docs: https://learn.microsoft.com/azure/azure-functions/functions-overview

- **Azure Logic Apps**: *Serverless workflow/integration* service to **orchestrate** processes using a visual designer and **connectors** (Microsoft 365, D...
```

</details>

---

### factual_004: ✅ PASSED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 27.51s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure OpenAI is available in these **Azure regions** (regional availability can vary by model/feature and changes over time):

- **Australia East**
- **Canada East**
- **East US**
- **East US 2**
- **France Central**
- **Japan East**
- **North Central US**
- **Norway East**
- **South Central US**
- **Sweden Central**
- **Switzerland North**
- **UK South**
- **West Europe**
- **West US**
- **West US 3**

Source (and kept up to date here): https://learn.microsoft.com/en-us/azure/ai-services/openai...
```

</details>

---

### factual_005: ✅ PASSED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 23.93s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure App Service apps run in an **App Service plan**, and the plan determines the **pricing tier**. The main tiers are:

- **Free (F1)** – Shared infrastructure, limited resources; good for testing/dev.
- **Shared (D1)** – Shared infrastructure, more than Free but still constrained; dev/test.
- **Basic (B1–B3)** – Dedicated VMs; suitable for low-traffic production.
- **Standard (S1–S3)** – Dedicated VMs with more scaling/features; general production.
- **Premium v2 (P1v2–P3v2)** – Higher perfor...
```

</details>

---

### howto_001: ✅ PASSED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 87.76s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

You can deploy an Azure Function using GitHub Actions in two common ways:

## Option A (fastest): Generate the workflow from Azure Portal
1. Azure portal → open your **Function App**
2. **Deployment Center**
3. Choose **GitHub**, authenticate, select repo + branch
4. Finish wizard → Azure commits a workflow under `.github/workflows/...`

## Option B: Write your own workflow (example)
### 1) Create a GitHub secret with the publish profile
- Azure portal → Function App → **Ove...
```

</details>

---

### howto_002: ❌ FAILED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 180.70s |
| Overall Score | 0.42 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### howto_003: ✅ PASSED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 81.78s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

You can enable Application Insights for an Azure Function via the portal or by setting app settings.

## Option 1: Azure portal (recommended)
1. Open **Azure portal** → **Function App**
2. Go to **Settings** → **Application Insights**
3. Toggle **Application Insights** to **On**
4. Select an existing Application Insights resource or **create new**
5. **Save**

## Option 2: App settings (CI/CD / IaC-friendly)
In **Function App** → **Configuration** → **Application settings**,...
```

</details>

---

### howto_004: ✅ PASSED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 80.41s |
| Overall Score | 0.93 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To set up **managed identity for Azure App Service to access Key Vault**:

1) **Enable Managed Identity on the App Service**
- App Service → **Identity**
  - **System assigned**: Status = **On** → **Save**  
  (Or attach a **User-assigned** identity under the *User assigned* tab.)
Source: https://learn.microsoft.com/azure/app-service/overview-managed-identity

2) **Grant that identity permissions in Key Vault**
Key Vault permissions are granted via either **Azure RBAC** or *...
```

</details>

---

### howto_005: ✅ PASSED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 163.44s |
| Overall Score | 0.74 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

I ran the **research** tool with the query **“Execute step”**.

**Step output (tool response):**  
> I can, but I need the context.  
>  
> Please paste the instructions/workflow and tell me **which step number** you want me to execute (or upload a screenshot). Also tell me what environment this is for (e.g., Azure portal, PowerShell, CLI, Windows, etc.). I ran the **research** tool with the query **“Execute step”**.

**Step output (tool response):**  
> I can, but I need th...
```

</details>

---

### arch_001: ❌ FAILED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 1581.08s |
| Overall Score | 0.46 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"CredentialUnavailableError","error_details":"Failed to invoke the Azure CLI","processing_time_ms":157918

---

### arch_002: ❌ FAILED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 32.73s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"CredentialUnavailableError","error_details":"Failed to invoke the Azure CLI","processing_time_ms":31854}

---

### arch_003: ❌ FAILED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 26.55s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"CredentialUnavailableError","error_details":"Failed to invoke the Azure CLI","processing_time_ms":25993}

---

### arch_004: ❌ FAILED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 12.27s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"CredentialUnavailableError","error_details":"Failed to invoke the Azure CLI","processing_time_ms":12111}

---

### arch_005: ❌ FAILED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 180.11s |
| Overall Score | 0.52 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### code_cli_001: ✅ PASSED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 74.73s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_002: ✅ PASSED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 76.61s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_003: ✅ PASSED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 78.50s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_001: ✅ PASSED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 77.24s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_002: ✅ PASSED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 72.44s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_003: ✅ PASSED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 75.28s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_001: ✅ PASSED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 78.55s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_002: ✅ PASSED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 77.61s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_003: ✅ PASSED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 76.32s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_004: ✅ PASSED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 83.71s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 276.31s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture, code, research |

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 83.10s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | code |

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 289.03s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | architecture |

---

### complex_004: ❌ FAILED

**Prompt**: Design a data analytics solution on Azure for processing IoT sensor data. Include architecture recommendations using Event Hubs and Stream Analytics, plus sample code for an Azure Function to process the events.

| Metric | Value |
|--------|-------|
| Duration | 290.96s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture, code, research |

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 285.21s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | architecture |

---
