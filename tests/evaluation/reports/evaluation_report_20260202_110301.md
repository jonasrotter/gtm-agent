# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T11:03:01.475614
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
| Keyword Coverage | 58.3% | 75% | ❌ |
| Performance | 96.6% | 80% | ✅ |

### Token Usage

| Metric | Count |
|--------|-------|
| Input Tokens | 0 |
| Output Tokens | 0 |
| Total Tokens | 0 |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 1 (20%) | 0.58 | 129.8s |
| code | 10 | 0 (0%) | 0.55 | 74.5s |
| complex | 5 | 0 (0%) | 0.37 | 152.3s |
| research | 10 | 0 (0%) | 0.56 | 56.4s |

## Recommendations

1. Tool selection accuracy is 0.0% (target: 85%). Review planner prompts to improve tool selection logic.
2. Average keyword coverage is 58.3% (target: 75%). Responses may be missing key information. Check sub-agent prompts.
3. Category 'research' has 0.0% pass rate. Review failed tasks for common issues.
4. Category 'architecture' has 20.0% pass rate. Review failed tasks for common issues.
5. Category 'code' has 0.0% pass rate. Review failed tasks for common issues.
6. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ❌ FAILED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 15.83s |
| Overall Score | 0.60 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage is Microsoft Azure’s object storage service for storing large amounts of unstructured data—such as files, images, videos, backups, logs, and data for analytics—over HTTP/HTTPS.

Key points:
- **“Blob” = Binary Large Object**: data is stored as objects, not in folders/disks like traditional file systems.
- **Scalable and durable**: designed for massive scale with built-in redundancy options.
- **Access methods**: via Azure portal, SDKs/REST API, Azure CLI, and tools like AzCopy...
```

</details>

---

### factual_002: ❌ FAILED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 20.72s |
| Overall Score | 0.60 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage supports these **access tiers**:

- **Hot** – Optimized for frequent access.
- **Cool** – Optimized for infrequent access (lower storage cost, higher access cost than Hot).
- **Cold** – Optimized for rarely accessed data (lower storage cost than Cool, higher access cost).
- **Archive** – Lowest storage cost for long-term retention; data is **offline** and must be **rehydrated** before it can be read. Azure Blob Storage supports these **access tiers**:

- **Hot** – Optimized fo...
```

</details>

---

### factual_003: ❌ FAILED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 40.68s |
| Overall Score | 0.69 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Azure Functions and Azure Logic Apps are both “serverless” offerings, but they’re optimized for different kinds of work:

## Azure Functions (serverless code)
- **What it is:** Event-driven **compute** for running your own code (C#, Java, JavaScript/TypeScript, Python, PowerShell, etc.).
- **Best for:** Custom logic, APIs, data processing, event handling, lightweight microservices—when you need full control over code and libraries.
- **How you build:** You write code; you wire triggers/bindings ...
```

</details>

---

### factual_004: ❌ FAILED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 28.41s |
| Overall Score | 0.57 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Azure OpenAI is available in a set of Azure regions, and **availability varies by model** (some models are only deployable in certain regions).

The authoritative, up-to-date list is maintained in Microsoft Learn’s **“Model summary table and region availability”**:

- https://learn.microsoft.com/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability

If you tell me **which model(s)** you care about (e.g., GPT-4.1, GPT-4o, text-embedding-3-large, etc.) and whether yo...
```

</details>

---

### factual_005: ❌ FAILED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 26.57s |
| Overall Score | 0.67 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Azure App Service runs in an **App Service plan**, and the plan’s **pricing tier** determines the compute (CPU/memory), scale features, and networking/isolation options you get.

Common **Azure App Service pricing tiers** include:

- **Free (F1)** – For dev/test and trials; limited resources, shared infrastructure.
- **Shared (D1)** – Low-cost shared infrastructure (historically available; not for production).
- **Basic (B1–B3)** – Dedicated VM instances, manual scale; good for simple production...
```

</details>

---

### howto_001: ❌ FAILED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 84.72s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### howto_002: ❌ FAILED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 88.90s |
| Overall Score | 0.67 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To configure **VNet Integration** for **Azure App Service** (primarily for **outbound** access to resources in a VNet), use **Regional VNet Integration**.

**Prerequisites**
- App Service plan in a supported tier (commonly **Basic+**).
- A VNet in the **same region** as the App Service.
- A **dedicated, empty subnet** for integration, delegated to **Microsoft.Web/serverFarms** (use at least **/27** recommended).

**Azure portal steps**
1. App Service → **Networking**
2. **VN...
```

</details>

---

### howto_003: ❌ FAILED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 85.18s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### howto_004: ❌ FAILED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 84.32s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### howto_005: ❌ FAILED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 88.36s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### arch_001: ❌ FAILED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 190.52s |
| Overall Score | 0.52 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---

### arch_002: ❌ FAILED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 114.00s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### arch_003: ✅ PASSED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 65.73s |
| Overall Score | 0.70 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

<details>
<summary>Response Preview</summary>

```
Key cost-optimization strategies for **Azure Kubernetes Service (AKS)** fall into a few buckets: *right-size/scale*, *use discounted compute*, *avoid paying for idle*, and *govern/observe*.

## 1) Scale only what you need
- **Cluster Autoscaler**: Automatically adds/removes nodes based on pending pods and scheduling needs. Use per node pool so expensive pools don’t scale unnecessarily.  
  Docs: https://learn.microsoft.com/azure/aks/cluster-autoscaler
- **Horizontal/Vertical Pod Autoscaling (HPA...
```

</details>

---

### arch_004: ❌ FAILED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 164.17s |
| Overall Score | 0.54 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### arch_005: ❌ FAILED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 175.28s |
| Overall Score | 0.54 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_cli_001: ❌ FAILED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 79.54s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_cli_002: ❌ FAILED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 74.51s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_cli_003: ❌ FAILED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 72.97s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_sdk_001: ❌ FAILED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 72.83s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_sdk_002: ❌ FAILED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 71.95s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_sdk_003: ❌ FAILED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 71.01s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_iac_001: ❌ FAILED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 79.72s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_iac_002: ❌ FAILED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 73.79s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_iac_003: ❌ FAILED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 72.73s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_iac_004: ❌ FAILED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 76.34s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 178.58s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 78.06s |
| Overall Score | 0.30 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 177.22s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### complex_004: ❌ FAILED

**Prompt**: Design a data analytics solution on Azure for processing IoT sensor data. Include architecture recommendations using Event Hubs and Stream Analytics, plus sample code for an Azure Function to process the events.

| Metric | Value |
|--------|-------|
| Duration | 175.48s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 180.01s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---
