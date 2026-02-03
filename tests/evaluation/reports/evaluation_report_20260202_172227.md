# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T17:22:27.776112
- **Evaluation File**: tests/evaluation/evaluation.xml
- **Mode**: api

### Results Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 30 |
| Passed | 23 |
| Failed | 7 |
| Pass Rate | 76.7% |

### Dimension Scores

| Dimension | Score | Target | Status |
|-----------|-------|--------|--------|
| Routing Accuracy | 100.0% | 90% | ✅ |
| Tool Selection | 87.9% | 85% | ✅ |
| Keyword Coverage | 58.0% | 75% | ❌ |
| Performance | 95.0% | 80% | ✅ |

### Token Usage

| Metric | Count |
|--------|-------|
| Input Tokens | 0 |
| Output Tokens | 0 |
| Total Tokens | 0 |

## Tool Call Analysis

| Tool | Calls | Avg Duration | Success Rate |
|------|-------|--------------|--------------|
| research | 17 | 0.00s | 100.0% |
| code | 16 | 0.00s | 100.0% |
| architecture | 7 | 0.00s | 100.0% |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 4 (80%) | 0.79 | 118.2s |
| code | 10 | 9 (90%) | 0.85 | 59.5s |
| complex | 5 | 0 (0%) | 0.61 | 208.5s |
| research | 10 | 10 (100%) | 0.91 | 74.8s |

## Recommendations

1. Average keyword coverage is 58.0% (target: 75%). Responses may be missing key information. Check sub-agent prompts.
2. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ✅ PASSED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 25.82s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage is Microsoft Azure’s object storage service for storing large amounts of unstructured data—data that doesn’t fit a traditional database model—such as text or binary files.

Key points:
- **What it stores:** files/blobs like images, videos, backups, logs, documents, and big data files.
- **How it’s organized:** blobs are stored in **storage accounts** and grouped into **containers** (similar to folders at a high level).
- **How it’s accessed:** via HTTP/HTTPS using Azure SDKs, ...
```

</details>

---

### factual_002: ✅ PASSED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 20.31s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage offers these **access tiers**:

- **Hot**: For data accessed frequently (highest storage cost, lowest access cost/latency).
- **Cool**: For infrequently accessed data stored at least ~30 days (lower storage cost than Hot, higher access cost).
- **Cold**: For rarely accessed data stored at least ~90 days (lower storage cost than Cool, higher access cost).
- **Archive**: For long-term retention and very rarely accessed data (lowest storage cost; must be **rehydrated** before acc...
```

</details>

---

### factual_003: ✅ PASSED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 23.50s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Functions and Azure Logic Apps are both ways to build serverless workflows, but they target different audiences and styles of work.

## Azure Functions
- **What it is:** “Code-first” serverless compute to run custom code (C#, JavaScript/TypeScript, Python, Java, etc.) on-demand.
- **Best for:** Custom business logic, complex computations, custom APIs, event processing, data transformations, extending systems where you need full control in code.
- **How you build:** Write and deploy code; y...
```

</details>

---

### factual_004: ✅ PASSED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 15.87s |
| Overall Score | 0.87 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure OpenAI is available in a **subset of Azure regions**, and **availability varies by model** (and can change over time). Microsoft maintains the current, authoritative list here:

- **Model + region availability (official table):** https://learn.microsoft.com/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability

If you tell me **which model(s)** you care about (e.g., GPT-4.1, GPT-4o, o3-mini, text-embedding-3-large), I can list the exact regions for those mode...
```

</details>

---

### factual_005: ✅ PASSED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 17.64s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure App Service apps run in an **App Service plan**, and the plan’s **pricing tier** determines the compute, features, and scaling you get. The main tiers are:

- **Free (F1)**  
- **Shared (D1)**  
- **Basic (B1, B2, B3)**  
- **Standard (S1, S2, S3)**  
- **Premium v2 (P1v2, P2v2, P3v2)**  
- **Premium v3 (P0v3, P1v3, P2v3, P3v3)**  
- **Isolated v2 (I1v2, I2v2, I3v2)** (runs in an App Service Environment)

Reference: App Service plan overview and tier list (Microsoft Learn): https://learn.m...
```

</details>

---

### howto_001: ✅ PASSED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 147.78s |
| Overall Score | 0.98 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

You deploy an Azure Function from GitHub Actions using the official **Azure Functions GitHub Action** (`Azure/functions-action`). Typical steps:

1. Create the **Function App** in Azure.
2. Download the app’s **Publish Profile** (or use Azure AD/OIDC).
3. Add the publish profile XML to GitHub as a secret, e.g. `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`.
4. Add a workflow file at `.github/workflows/deploy.yml`.
5. Push to your target branch to trigger deployment.

Example workflow (...
```

</details>

---

### howto_002: ✅ PASSED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 141.72s |
| Overall Score | 0.74 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

---

### howto_003: ✅ PASSED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 66.73s |
| Overall Score | 0.93 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

You can enable Application Insights for an Azure Function in the portal or by setting app settings.

## Option A — Azure Portal
1. Open your **Function App** in the Azure portal.
2. Go to **Application Insights** (under *Settings*).
3. Switch it **On**.
4. Choose **Create new** or **Select existing** Application Insights resource.
5. **Apply/Save**.

## Option B — App settings (any deployment method)
In **Function App → Configuration → Application settings**, set:

- **Recom...
```

</details>

---

### howto_004: ✅ PASSED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 137.53s |
| Overall Score | 0.74 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

---

### howto_005: ✅ PASSED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 151.09s |
| Overall Score | 0.99 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

Auto-scaling in **Azure Kubernetes Service (AKS)** is typically configured at two layers:

1) **Cluster autoscaler** (adds/removes **nodes** in a node pool)  
2) **Pod autoscaling** (adds/removes **pods** in a workload—HPA, or event-driven via KEDA)

---

## 1) Enable node autoscaling (Cluster Autoscaler)

### Enable on an existing node pool (Azure CLI)
```bash
az aks nodepool update \
  --resource-group <rg> \
  --cluster-name <aks-name> \
  --name <nodepool-name> \
  --ena...
```

</details>

---

### arch_001: ✅ PASSED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 145.03s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

---

### arch_002: ✅ PASSED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 144.70s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, architecture |

---

### arch_003: ✅ PASSED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 38.87s |
| Overall Score | 0.76 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Below are the most effective, **practical cost-optimization strategies for Azure Kubernetes Service (AKS)**, grouped by where they impact spend.

## 1) Right-size and autoscale compute (biggest lever)
- **Use Cluster Autoscaler** to match node count to pending pods (scale out) and remove underutilized nodes (scale in). Combine with Pod requests/limits so scheduling reflects real needs.  
  Docs: https://learn.microsoft.com/azure/aks/cluster-autoscaler
- **Use Horizontal Pod Autoscaler (HPA)** to...
```

</details>

---

### arch_004: ❌ FAILED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 126.95s |
| Overall Score | 0.65 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

---

### arch_005: ✅ PASSED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 135.51s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

---

### code_cli_001: ✅ PASSED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 61.10s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_002: ✅ PASSED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 54.03s |
| Overall Score | 0.85 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_003: ✅ PASSED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 54.25s |
| Overall Score | 0.85 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_001: ✅ PASSED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 56.11s |
| Overall Score | 0.85 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_002: ✅ PASSED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 60.95s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_003: ✅ PASSED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 62.86s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_001: ✅ PASSED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 61.46s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_002: ✅ PASSED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 62.41s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_003: ❌ FAILED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 879.11s |
| Overall Score | 0.46 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### code_iac_004: ✅ PASSED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 62.05s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 239.42s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, architecture, code |

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 66.47s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | code |

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 238.33s |
| Overall Score | 0.49 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

---

### complex_004: ❌ FAILED

**Prompt**: Design a data analytics solution on Azure for processing IoT sensor data. Include architecture recommendations using Event Hubs and Stream Analytics, plus sample code for an Azure Function to process the events.

| Metric | Value |
|--------|-------|
| Duration | 252.01s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, architecture, code |

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 246.40s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | architecture |

---
