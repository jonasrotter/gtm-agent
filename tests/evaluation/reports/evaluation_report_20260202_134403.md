# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T13:44:03.226024
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
| Tool Selection | 88.4% | 85% | ✅ |
| Keyword Coverage | 63.4% | 75% | ❌ |
| Performance | 95.7% | 80% | ✅ |

### Token Usage

| Metric | Count |
|--------|-------|
| Input Tokens | 0 |
| Output Tokens | 0 |
| Total Tokens | 0 |

## Tool Call Analysis

| Tool | Calls | Avg Duration | Success Rate |
|------|-------|--------------|--------------|
| research | 18 | 0.00s | 100.0% |
| code | 17 | 0.00s | 100.0% |
| architecture | 8 | 0.00s | 100.0% |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 3 (60%) | 0.78 | 121.5s |
| code | 10 | 10 (100%) | 0.84 | 75.0s |
| complex | 5 | 1 (20%) | 0.66 | 131.8s |
| research | 10 | 9 (90%) | 0.89 | 76.8s |

## Recommendations

1. Average keyword coverage is 63.4% (target: 75%). Responses may be missing key information. Check sub-agent prompts.
2. Category 'architecture' has 60.0% pass rate. Review failed tasks for common issues.
3. Category 'complex' has 20.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ✅ PASSED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 27.33s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage is Microsoft Azure’s object storage service for storing massive amounts of unstructured data—data that doesn’t fit a traditional relational database—such as text or binary files.

Key points:
- **Stores “blobs” (objects)** in **containers** within an Azure **storage account**.
- Optimized for **high durability, availability, and scalability**.
- Common uses include **serving images/videos**, **storing documents and backups**, **data lakes/analytics**, **logging**, and **disast...
```

</details>

---

### factual_002: ✅ PASSED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 13.02s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage supports these **access tiers**:

- **Hot** – Optimized for frequent access.
- **Cool** – Optimized for infrequent access (lower storage cost, higher access cost than Hot).
- **Cold** – Optimized for rarely accessed data (lower storage cost than Cool, higher access cost).
- **Archive** – Lowest storage cost for long-term retention; data must be **rehydrated** before it can be read.

Source: https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview Azure Blob ...
```

</details>

---

### factual_003: ✅ PASSED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 27.48s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Functions and Azure Logic Apps both let you build “serverless” solutions, but they’re optimized for different kinds of work:

## Azure Functions
- **What it is:** A **serverless compute** service for running your **code** (C#, JavaScript/TypeScript, Python, Java, etc.) in response to events (HTTP calls, queue messages, timers, Event Grid, etc.).
- **Best for:** Custom logic, algorithms, transformations, API endpoints, event processing, or anything that’s easiest to express in code.
- **How...
```

</details>

---

### factual_004: ✅ PASSED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 17.18s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure OpenAI is available in these Azure regions (listed in Microsoft Learn under **“Available regions”**):

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

Source: https://learn.microsoft.com/en-us/azure/ai-services/openai/overview#available-regions Azure OpenAI is a...
```

</details>

---

### factual_005: ✅ PASSED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 27.05s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure App Service (via an **App Service plan**) offers these main **pricing tiers (SKUs)**:

- **Free (F1)** – For dev/test and trying App Service (shared infrastructure).
- **Shared (D1)** – Low-cost shared compute (legacy/limited scenarios).
- **Basic (B1–B3)** – Dedicated VM instances; suitable for small production workloads.
- **Standard (S1–S3)** – Production tier with autoscale and more features than Basic.
- **Premium v2 (P1v2–P3v2)** – Higher performance/dedicated compute with more scale...
```

</details>

---

### howto_001: ✅ PASSED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 166.49s |
| Overall Score | 0.74 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

---

### howto_002: ✅ PASSED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 165.98s |
| Overall Score | 0.74 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

---

### howto_003: ❌ FAILED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 180.38s |
| Overall Score | 0.42 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### howto_004: ✅ PASSED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 86.45s |
| Overall Score | 1.00 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

## Step 1 — Microsoft guidance + common steps (App Service managed identity → Key Vault)

### Enable managed identity on Azure App Service

**System-assigned (Portal)**
1. Web App → **Identity**
2. **System assigned** → **Status: On** → **Save**
3. Note the **Object (principal) ID**  
Docs: https://learn.microsoft.com/azure/app-service/overview-managed-identity

**User-assigned (Portal)**
1. Create/select a **User Assigned Managed Identity**
2. Web App → **Identity** → **Use...
```

</details>

---

### howto_005: ✅ PASSED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 160.61s |
| Overall Score | 0.74 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

---

### arch_001: ❌ FAILED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 163.23s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

---

### arch_002: ❌ FAILED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 171.10s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

---

### arch_003: ✅ PASSED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 27.57s |
| Overall Score | 0.76 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Key cost-optimization strategies for **Azure Kubernetes Service (AKS)**:

## 1) Right-size and control node compute
- **Use cluster autoscaler** to scale node pools up/down with demand.
- **Use multiple node pools** (separate “system” and “user” pools; size them independently).
- **Pick the right VM families/sizes** (avoid oversized nodes; consider memory/CPU-optimized SKUs where appropriate).
- **Scale to zero where possible** (for appropriate workloads via KEDA + event-driven scaling; for dev/...
```

</details>

---

### arch_004: ✅ PASSED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 165.77s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, architecture |

<details>
<summary>Response Preview</summary>

```
## Step 2: architecture

I called the **architecture** tool with the query **"Execute step"**.

**Step output:**
I can’t execute a “step” yet because I don’t have the plan/steps you’re referring to.

Paste the step text (or the `.azure/plan.copilotmd` contents) and tell me which step number to run, and whether you want it executed via Azure CLI (`az`) or Azure Developer CLI (`azd`). I called the **architecture** tool with the query **"Execute step"**.

**Step output:**
I can’t execute a “step” y...
```

</details>

---

### arch_005: ✅ PASSED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 79.64s |
| Overall Score | 1.00 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, architecture |

<details>
<summary>Response Preview</summary>

```
## Step 2: architecture

A recommended Azure architecture for a multi-tenant SaaS application typically follows **CAF SaaS tenancy guidance** and the **Azure Well-Architected Framework**, using these building blocks:

## 1) Tenant identity, onboarding, isolation
- **Microsoft Entra ID** (workforce) and/or **Microsoft Entra External ID (CIAM/B2C)** (customer identities).
- A **tenant catalog** storing tenant metadata (tenant ID, plan, region, isolation mode, shard/stamp, keys, etc.).
- Isolation ...
```

</details>

---

### code_cli_001: ✅ PASSED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 88.92s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_002: ✅ PASSED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 79.98s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_003: ✅ PASSED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 71.39s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_001: ✅ PASSED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 72.08s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_002: ✅ PASSED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 73.70s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_003: ✅ PASSED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 70.80s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_001: ✅ PASSED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 76.17s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_002: ✅ PASSED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 72.10s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_003: ✅ PASSED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 70.67s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_004: ✅ PASSED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 74.36s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 174.83s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research, architecture |

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 76.01s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | research |

---

### complex_003: ✅ PASSED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 108.70s |
| Overall Score | 0.70 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research, architecture |

---

### complex_004: ❌ FAILED

**Prompt**: Design a data analytics solution on Azure for processing IoT sensor data. Include architecture recommendations using Event Hubs and Stream Analytics, plus sample code for an Azure Function to process the events.

| Metric | Value |
|--------|-------|
| Duration | 167.61s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code, research, architecture |

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 180.94s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---
