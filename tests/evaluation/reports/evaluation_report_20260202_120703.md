# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T12:07:03.644071
- **Evaluation File**: tests/evaluation/evaluation.xml
- **Mode**: api

### Results Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 30 |
| Passed | 24 |
| Failed | 6 |
| Pass Rate | 80.0% |

### Dimension Scores

| Dimension | Score | Target | Status |
|-----------|-------|--------|--------|
| Routing Accuracy | 100.0% | 90% | ✅ |
| Tool Selection | 92.0% | 85% | ✅ |
| Keyword Coverage | 75.3% | 75% | ✅ |
| Performance | 96.8% | 80% | ✅ |

### Token Usage

| Metric | Count |
|--------|-------|
| Input Tokens | 0 |
| Output Tokens | 0 |
| Total Tokens | 0 |

## Tool Call Analysis

| Tool | Calls | Avg Duration | Success Rate |
|------|-------|--------------|--------------|
| code | 18 | 0.00s | 100.0% |
| research | 17 | 0.00s | 100.0% |
| architecture | 7 | 0.00s | 100.0% |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 4 (80%) | 0.84 | 113.5s |
| code | 10 | 10 (100%) | 0.84 | 73.5s |
| complex | 5 | 0 (0%) | 0.65 | 142.3s |
| research | 10 | 10 (100%) | 0.95 | 49.3s |

## Recommendations

1. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ✅ PASSED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 13.36s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage is Azure’s object storage service for storing large amounts of unstructured data—data that doesn’t fit neatly into tables—such as images, videos, backups, logs, documents, and datasets for analytics.

Key points:
- **Scalable and durable**: Designed to store massive volumes of data with high durability and availability.
- **Access methods**: Data is accessed over HTTP/HTTPS via REST APIs, Azure SDKs, Azure CLI/PowerShell, and tools like Azure Storage Explorer.
- **Organization...
```

</details>

---

### factual_002: ✅ PASSED

**Prompt**: What are the storage tiers for Azure Blob Storage?

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
Azure Blob Storage supports these access (storage) tiers:

- **Hot**: Optimized for frequent access.
- **Cool**: Optimized for infrequent access (lower storage cost, higher access cost).
- **Cold**: Optimized for rarely accessed data with lower storage cost than cool (available in supported regions).
- **Archive**: Offline tier for long-term retention; must be rehydrated before access.

Source: https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview Azure Blob Storage supports thes...
```

</details>

---

### factual_003: ✅ PASSED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 20.43s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Functions and Azure Logic Apps are both ways to build automated workflows in Azure, but they target different styles of work.

## Azure Functions (code-first compute)
- **What it is:** Serverless functions that run **your code** (C#, JavaScript, Python, etc.) in response to triggers (HTTP, timers, queues, events).
- **Best for:** Custom business logic, data processing, APIs, event-driven compute, lightweight microservices.
- **Authoring model:** Code + tooling (VS Code/Visual Studio), CI/C...
```

</details>

---

### factual_004: ✅ PASSED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 23.63s |
| Overall Score | 0.89 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure OpenAI doesn’t have one fixed “regions list” that’s always accurate, because **availability depends on (1) your model and (2) the specific feature (e.g., chat/completions vs. Assistants vs. image generation, etc.)** and it changes over time.

**Official way to see the current regions:**
- **Azure OpenAI Service – Availability** (Microsoft Learn): https://learn.microsoft.com/en-us/azure/ai-services/openai/overview#availability  
  This section links you to the up-to-date regional availabili...
```

</details>

---

### factual_005: ✅ PASSED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 17.31s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure App Service runs on an **App Service plan**, and the plan determines the **pricing tier**. The main tiers are:

- **Free (F1)** – Limited features/resources; shared infrastructure.
- **Shared (D1)** – Low-cost shared infrastructure (legacy/limited scenarios).
- **Basic (B1–B3)** – Dedicated VM instances; dev/test or low-traffic production.
- **Standard (S1–S3)** – Production tier; supports autoscale and more advanced features.
- **Premium v2 (P1v2–P3v2)** – Higher performance, more scale, ...
```

</details>

---

### howto_001: ✅ PASSED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 78.63s |
| Overall Score | 0.96 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

## Step 1 — Research output: Recommended GitHub Actions approach for deploying Azure Functions

### Official GitHub Actions to use
- **Authenticate to Azure:** `azure/login` (recommended with **OIDC federated credentials**, i.e., no client secret)  
  Source: https://learn.microsoft.com/azure/developer/github/connect-from-azure-openid-connect
- **Deploy the Function App:** `Azure/functions-action` (deploys a package/zip to a Function App)  
  Source (Functions + GitHub Actio...
```

</details>

---

### howto_002: ✅ PASSED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 80.48s |
| Overall Score | 1.00 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

## Step 1 — Research output (Azure App Service regional VNet integration)

**Primary Microsoft Learn documentation**
- Overview (concepts, requirements, limits): https://learn.microsoft.com/azure/app-service/overview-vnet-integration  
- Enable via Portal: https://learn.microsoft.com/azure/app-service/configure-vnet-integration-enable  
- Enable via Azure CLI: https://learn.microsoft.com/azure/app-service/configure-vnet-integration-cli  
- Enable via ARM template: https://le...
```

</details>

---

### howto_003: ✅ PASSED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 80.46s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To enable Application Insights for your Azure Function:

**Option 1 (Azure portal)**
1. Open your **Function App** in the Azure portal.
2. Go to **Application Insights** (sometimes under **Settings > Application Insights**).
3. Select **Turn on Application Insights**.
4. Choose an existing Application Insights resource or **Create new**, then **Apply/Save**.

**Option 2 (App settings)**
In **Function App > Configuration > Application settings**, set either:
- `APPLICATIONINS...
```

</details>

---

### howto_004: ✅ PASSED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 78.26s |
| Overall Score | 0.82 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To let an **Azure App Service** access **Azure Key Vault** using **Managed Identity**:

## 1) Enable Managed Identity on the App Service
- Azure portal → **App Service** → **Identity**
  - **System assigned** → set **Status = On** → **Save**
  - Copy the **Object/Principal ID** (used for permissions)

(Optional) **User-assigned**: Create a user-assigned managed identity, then App Service → **Identity** → **User assigned** → **Add**.

## 2) Grant the identity access to Key Va...
```

</details>

---

### howto_005: ✅ PASSED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 83.04s |
| Overall Score | 1.00 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

## Step 1 output — AKS autoscaling options (authoritative guidance + steps)

### Cluster Autoscaler (node scaling)
- Purpose: scales **AKS node pools** up/down based on scheduling needs (pending/unschedulable pods) and removes underutilized nodes when possible.
- Configure **per node pool** with **min/max** node counts (works across system/user node pools).
- CLI (enable on node pool):
  ```bash
  az aks nodepool update -g <rg> --cluster-name <cluster> -n <nodepool> \
    --...
```

</details>

---

### arch_001: ❌ FAILED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 165.01s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

---

### arch_002: ✅ PASSED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 162.68s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture, research |

---

### arch_003: ✅ PASSED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 21.80s |
| Overall Score | 0.80 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Key cost-optimization strategies for **Azure Kubernetes Service (AKS)** (based on Microsoft guidance) include:

## 1) Right-size and control node (compute) costs
- **Right-size VM SKUs** for node pools (avoid oversized nodes; align CPU/memory to real workload needs).
- **Use multiple node pools** (separate system vs. user pools; isolate high-memory/GPU/special workloads to dedicated pools so you don’t overpay everywhere).
- **Use autoscaling**:
  - **Cluster Autoscaler** to scale node count up/d...
```

</details>

---

### arch_004: ✅ PASSED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 60.26s |
| Overall Score | 0.96 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To implement the **Reliability** pillar of the **Azure Well-Architected Framework (WAF)**, design and operate your solution so it **keeps working as intended**, **recovers from failures**, and **meets your uptime/availability targets**. Use this as an implementation checklist.

## 1) Define reliability targets and boundaries
- Document **SLOs/SLAs** per user journey (availability, latency, error rate) and per component.
- Establish **RTO/RPO** for each workload/data store.
-...
```

</details>

---

### arch_005: ✅ PASSED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 157.86s |
| Overall Score | 0.95 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

Step output (research):

Azure’s recommended approach for a multi-tenant SaaS architecture is to **start with tenant isolation requirements**, then choose a **tenancy model** (pooled/shared, siloed/single-tenant, or hybrid) and often implement a **“stamp/scale-unit” architecture** to scale out while limiting blast radius and noisy-neighbor impact. Key areas include **tenant resolution/identity**, **data partitioning strategy** (e.g., discriminator column vs DB-per-tenant vs ...
```

</details>

---

### code_cli_001: ✅ PASSED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 75.21s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_002: ✅ PASSED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 70.88s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_003: ✅ PASSED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 71.96s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_001: ✅ PASSED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 75.08s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_002: ✅ PASSED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 74.78s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_003: ✅ PASSED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 73.26s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_001: ✅ PASSED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 73.63s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_002: ✅ PASSED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 70.57s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_003: ✅ PASSED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 75.52s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_004: ✅ PASSED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 73.97s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 181.45s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 73.17s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | code |

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 180.01s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---

### complex_004: ❌ FAILED

**Prompt**: Design a data analytics solution on Azure for processing IoT sensor data. Include architecture recommendations using Event Hubs and Stream Analytics, plus sample code for an Azure Function to process the events.

| Metric | Value |
|--------|-------|
| Duration | 174.88s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture, research, code |

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 178.93s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture, research, code |

---
