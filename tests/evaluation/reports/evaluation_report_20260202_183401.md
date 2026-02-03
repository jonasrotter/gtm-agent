# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T18:34:01.599532
- **Evaluation File**: tests/evaluation/evaluation.xml
- **Mode**: api

### Results Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 30 |
| Passed | 21 |
| Failed | 9 |
| Pass Rate | 70.0% |

### Dimension Scores

| Dimension | Score | Target | Status |
|-----------|-------|--------|--------|
| Routing Accuracy | 100.0% | 90% | ✅ |
| Tool Selection | 85.7% | 85% | ✅ |
| Keyword Coverage | 53.9% | 75% | ❌ |
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
| code | 15 | 0.00s | 100.0% |
| research | 12 | 0.00s | 100.0% |
| architecture | 7 | 0.00s | 100.0% |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 3 (60%) | 0.75 | 125.8s |
| code | 10 | 10 (100%) | 0.85 | 62.6s |
| complex | 5 | 0 (0%) | 0.63 | 198.2s |
| research | 10 | 8 (80%) | 0.86 | 79.5s |

## Recommendations

1. Average keyword coverage is 53.9% (target: 75%). Responses may be missing key information. Check sub-agent prompts.
2. Category 'architecture' has 60.0% pass rate. Review failed tasks for common issues.
3. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ✅ PASSED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 18.71s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage is Microsoft Azure’s object storage service for storing large amounts of unstructured data—data that doesn’t fit a traditional relational database model—such as text and binary files.

Key points:
- **What it stores:** files like images, videos, backups, logs, documents, and big data used for analytics.
- **How it’s organized:** data is stored as **blobs** inside **containers** within a **storage account**.
- **Common uses:** serving content to browsers, storing files for dist...
```

</details>

---

### factual_002: ❌ FAILED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 28.33s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"APITimeoutError","error_details":"Request timed out.","processing_time_ms":28242}}

---

### factual_003: ✅ PASSED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 44.98s |
| Overall Score | 0.99 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Functions and Azure Logic Apps are both “serverless,” but they solve different problems.

## Azure Functions
**What it is:** Event-driven *code* you write and run on demand (serverless compute).  
**Best for:** Custom logic, data processing, API endpoints, complex computations, and when you need full control of the runtime and libraries.  
**How you build:** Write functions in languages like C#, JavaScript/TypeScript, Python, Java, etc. Triggered by events (HTTP, timers, queues, Event Grid...
```

</details>

---

### factual_004: ✅ PASSED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 24.99s |
| Overall Score | 0.87 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure OpenAI region availability depends on **which model** you want to deploy (different models are available in different Azure regions). Microsoft maintains the up-to-date list in the **model summary table and region availability** section here:

https://learn.microsoft.com/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability

If you tell me the **model(s)** you care about (e.g., `gpt-4o`, `gpt-4.1`, `o3-mini`, `text-embedding-3-large`) and whether you need **g...
```

</details>

---

### factual_005: ✅ PASSED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 22.50s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure App Service offers these **pricing tiers (plan SKUs)**:

- **Free (F1)** – Shared infrastructure; for dev/test and small workloads.
- **Shared (D1)** – Shared infrastructure; low-cost dev/test.
- **Basic (B1–B3)** – Dedicated VMs; entry production tier.
- **Standard (S1–S3)** – Dedicated VMs; adds features like autoscale and staging slots.
- **Premium v2 (P1v2–P3v2)** – Higher performance dedicated VMs.
- **Premium v3 (P0v3–P3v3)** – Newer premium tier with better price/performance and mor...
```

</details>

---

### howto_001: ✅ PASSED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 70.07s |
| Overall Score | 0.93 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

You deploy an Azure Function using GitHub Actions by creating a workflow that builds your function app and then deploys it to the Azure Function App using either a **publish profile** or **Azure login (OIDC)**. Microsoft’s guidance and example workflow are here: https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-github-actions

### Option A: Deploy with a Publish Profile (simplest)
1) Azure Portal → **Function App → Overview → Get publish profile** (dow...
```

</details>

---

### howto_002: ✅ PASSED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 161.97s |
| Overall Score | 0.74 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

---

### howto_003: ❌ FAILED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 88.14s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"BadRequestError","error_details":"Error code: 400 - {'error': {'message': \"The response was filtered du

---

### howto_004: ✅ PASSED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 142.45s |
| Overall Score | 0.74 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research |

---

### howto_005: ✅ PASSED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 150.04s |
| Overall Score | 0.74 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

---

### arch_001: ❌ FAILED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 149.81s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

---

### arch_002: ❌ FAILED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 155.91s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

---

### arch_003: ✅ PASSED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 40.82s |
| Overall Score | 0.80 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Key cost-optimization strategies for **Azure Kubernetes Service (AKS)** (covering both Azure infrastructure costs and in-cluster efficiency):

## 1) Right-size and control node (VM) spend
- **Right-size VM SKUs**: pick the smallest SKU family that meets CPU/memory/disk/network needs; avoid overprovisioning “just in case.”
- **Separate node pools by workload** (system vs user, CPU vs memory-heavy, GPU, etc.) so each pool uses an appropriate VM size.
- **Use ephemeral OS disks** where suitable to ...
```

</details>

---

### arch_004: ✅ PASSED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 141.33s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

---

### arch_005: ✅ PASSED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 141.19s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

---

### code_cli_001: ✅ PASSED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 61.16s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_002: ✅ PASSED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 61.23s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_003: ✅ PASSED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 64.11s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_001: ✅ PASSED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 60.81s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_002: ✅ PASSED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 59.71s |
| Overall Score | 0.85 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_003: ✅ PASSED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 59.67s |
| Overall Score | 0.85 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_001: ✅ PASSED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 75.90s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_002: ✅ PASSED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 62.56s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_003: ✅ PASSED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 59.24s |
| Overall Score | 0.85 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_004: ✅ PASSED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 61.79s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 238.45s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | architecture |

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 62.38s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | code |

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 247.15s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | architecture |

---

### complex_004: ❌ FAILED

**Prompt**: Design a data analytics solution on Azure for processing IoT sensor data. Include architecture recommendations using Event Hubs and Stream Analytics, plus sample code for an Azure Function to process the events.

| Metric | Value |
|--------|-------|
| Duration | 213.54s |
| Overall Score | 0.65 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | architecture |

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 229.59s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture, code, research |

---
