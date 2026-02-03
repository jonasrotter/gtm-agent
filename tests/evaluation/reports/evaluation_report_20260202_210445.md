# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T21:04:45.332062
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
| Tool Selection | 88.0% | 85% | ✅ |
| Keyword Coverage | 73.6% | 75% | ❌ |
| Performance | 94.8% | 80% | ✅ |

### Token Usage

| Metric | Count |
|--------|-------|
| Input Tokens | 0 |
| Output Tokens | 0 |
| Total Tokens | 0 |

## Tool Call Analysis

| Tool | Calls | Avg Duration | Success Rate |
|------|-------|--------------|--------------|
| code | 16 | 0.00s | 100.0% |
| research | 14 | 0.00s | 100.0% |
| architecture | 6 | 0.00s | 100.0% |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 3 (60%) | 0.78 | 138.6s |
| code | 10 | 10 (100%) | 0.84 | 78.6s |
| complex | 5 | 0 (0%) | 0.61 | 268.1s |
| research | 10 | 10 (100%) | 0.93 | 66.8s |

## Recommendations

1. Average keyword coverage is 73.6% (target: 75%). Responses may be missing key information. Check sub-agent prompts.
2. Category 'architecture' has 60.0% pass rate. Review failed tasks for common issues.
3. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ✅ PASSED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 32.52s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage is Microsoft Azure’s massively scalable **object storage** service for storing **unstructured data** in the cloud.

- **What it stores:** text and binary data such as images, videos, audio, documents, backups, logs, archives, and big-data datasets.  
- **How it’s organized:** data is stored as **blobs** inside **containers** within an Azure **storage account**.  
- **How you access it:** over HTTP/HTTPS via REST APIs, SDKs, Azure CLI/PowerShell, and tools like Azure Storage Ex...
```

</details>

---

### factual_002: ✅ PASSED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 20.64s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage supports these **access tiers**:

- **Hot** – optimized for frequent access.
- **Cool** – optimized for infrequent access (typically stored at least 30 days).
- **Cold** – optimized for rarely accessed data (typically stored at least 90 days).
- **Archive** – lowest-cost for long-term retention; data is offline and must be **rehydrated** before it can be read.

Source: https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview Azure Blob Storage supports these...
```

</details>

---

### factual_003: ✅ PASSED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 39.80s |
| Overall Score | 0.99 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Functions and Azure Logic Apps both let you build event-driven solutions in Azure, but they target different needs.

## Core difference
- **Azure Functions**: *Code-first* serverless compute. You write code (C#, JavaScript/TypeScript, Python, Java, etc.) that runs when triggered (HTTP, timers, queues, events, etc.).
- **Azure Logic Apps**: *Workflow-first* integration/orchestration. You design workflows (visually or as workflow definitions) using built-in **connectors** to SaaS and Azure s...
```

</details>

---

### factual_004: ✅ PASSED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 24.31s |
| Overall Score | 0.87 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure OpenAI is available only in specific Azure regions, and the list varies by **model** (and changes over time). Microsoft maintains the up-to-date matrix here:

- **Azure OpenAI model/region availability (official list):** https://learn.microsoft.com/azure/ai-services/openai/concepts/models

Open that page and use the **“Model availability”** section to see exactly which regions support the model(s) you want (for example, GPT-4.1, GPT-4o, o-series, embeddings, image models, etc.). Azure Open...
```

</details>

---

### factual_005: ✅ PASSED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 24.12s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure App Service pricing tiers are defined by the **App Service plan** (the compute your apps run on). The main tiers are:

- **Free (F1)** – Shared infrastructure, dev/test only.
- **Shared (D1)** – Shared infrastructure, dev/test and low traffic.
- **Basic (B1–B3)** – Dedicated VM instances, entry-level production.
- **Standard (S1–S3)** – Dedicated instances with more scaling/features than Basic.
- **Premium v2 (P1v2–P3v2)** – Higher performance dedicated instances and advanced scale.
- **Pr...
```

</details>

---

### howto_001: ✅ PASSED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 100.35s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To deploy an Azure Function with GitHub Actions, use the official **Azure/functions-action**. Two common authentication options:

## Option A (simplest): Publish profile
1. Azure Portal → Function App → **Get publish profile** (download XML)
2. GitHub repo → **Settings → Secrets and variables → Actions** → create secret:
   - `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` = paste the XML contents
3. Add workflow `.github/workflows/deploy.yml`:

```yaml
name: Deploy Azure Function

on:
...
```

</details>

---

### howto_002: ✅ PASSED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 84.11s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To configure **VNet Integration** for **Azure App Service** (for outbound access to resources in a VNet):

1) **Meet prerequisites**
- App Service plan must support VNet Integration (not Free/Shared).
- Use **Regional VNet Integration**: VNet must be in the **same region** as the app.
- Have a **dedicated, empty subnet** for integration (plan enough IPs for scale-out).

2) **Prepare VNet + subnet**
- Create/select a VNet in the same region.
- Create a new subnet dedicated to...
```

</details>

---

### howto_003: ✅ PASSED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 90.58s |
| Overall Score | 0.86 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

You can enable Application Insights for an Azure Function in a few common ways, depending on how/where it’s hosted.

## Option 1 (recommended): Enable from the Azure Portal (existing Function App)
1. Azure portal → open your **Function App**
2. Left menu → **Application Insights**
3. Select **Turn on Application Insights** / **Enable**
4. Choose **Create new** or **Select existing**
5. Save/apply

## Option 2: Enable at creation time
When creating the Function App in the por...
```

</details>

---

### howto_004: ✅ PASSED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 80.93s |
| Overall Score | 0.86 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To set up **managed identity** for **Azure App Service** to access **Azure Key Vault**:

## 1) Enable Managed Identity on the App Service
**System-assigned (common):**
- Azure portal → **App Service** → **Identity** → **System assigned** → **On** → **Save**
- Note the **Object/Principal ID**

**User-assigned (optional):**
- Create/use a **User Assigned Managed Identity**
- App Service → **Identity** → **User assigned** → **Add**

## 2) Grant that identity access to Key Vault...
```

</details>

---

### howto_005: ✅ PASSED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 170.69s |
| Overall Score | 0.99 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

## AKS Cluster Autoscaler (node autoscaling)

Official guidance: https://learn.microsoft.com/azure/aks/cluster-autoscaler

### Enable (per node pool) — current Azure CLI syntax

**Create a new node pool with autoscaler enabled**
```bash
az aks nodepool add \
  --resource-group <rg> \
  --cluster-name <aksName> \
  --name <poolName> \
  --enable-cluster-autoscaler \
  --min-count <minNodes> \
  --max-count <maxNodes>
```

**Enable/update on an existing node pool**
```bash
az ...
```

</details>

---

### arch_001: ✅ PASSED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 171.38s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

---

### arch_002: ❌ FAILED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 210.89s |
| Overall Score | 0.52 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"CredentialUnavailableError","error_details":"Failed to invoke the Azure CLI","processing_time_ms":208908

---

### arch_003: ✅ PASSED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 32.07s |
| Overall Score | 0.80 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Key Azure Kubernetes Service (AKS) cost-optimization strategies fall into a few buckets: **right-sizing**, **scaling**, **cheaper compute options**, **storage/network tuning**, and **governance/visibility**.

## 1) Right-size clusters and node pools
- **Use multiple node pools** (system + user pools; separate pools by workload needs) so you don’t over-provision expensive VM sizes for everything.
- **Right-size VM SKUs** (CPU/memory) and avoid “one large node pool fits all.” Revisit regularly as ...
```

</details>

---

### arch_004: ✅ PASSED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 179.11s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

---

### arch_005: ❌ FAILED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 171.93s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

---

### code_cli_001: ✅ PASSED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 83.63s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_002: ✅ PASSED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 73.08s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_003: ✅ PASSED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 78.96s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_001: ✅ PASSED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 77.33s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_002: ✅ PASSED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 79.71s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_003: ✅ PASSED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 81.50s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_001: ✅ PASSED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 78.15s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_002: ✅ PASSED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 76.23s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_003: ✅ PASSED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 76.55s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_004: ✅ PASSED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 80.59s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 770.93s |
| Overall Score | 0.31 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 14.07s |
| Overall Score | 0.30 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"CredentialUnavailableError","error_details":"Failed to invoke the Azure CLI","processing_time_ms":13540}

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 273.72s |
| Overall Score | 0.49 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

---

### complex_004: ❌ FAILED

**Prompt**: Design a data analytics solution on Azure for processing IoT sensor data. Include architecture recommendations using Event Hubs and Stream Analytics, plus sample code for an Azure Function to process the events.

| Metric | Value |
|--------|-------|
| Duration | 261.13s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | architecture |

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 269.41s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research, architecture |

---
