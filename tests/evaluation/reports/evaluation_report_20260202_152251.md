# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T15:22:51.306544
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
| Tool Selection | 91.0% | 85% | ✅ |
| Keyword Coverage | 77.3% | 75% | ✅ |
| Performance | 96.0% | 80% | ✅ |

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
| architecture | 5 | 0.00s | 100.0% |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 4 (80%) | 0.82 | 143.1s |
| code | 10 | 10 (100%) | 0.84 | 74.0s |
| complex | 5 | 0 (0%) | 0.55 | 77.7s |
| research | 10 | 9 (90%) | 0.93 | 52.0s |

## Recommendations

1. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ✅ PASSED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 24.48s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage is Microsoft Azure’s object storage service for storing large amounts of unstructured data—such as text, images, video, logs, backups, and files—accessible over HTTP/HTTPS.

Key points:
- **Scalable and durable** cloud storage for “blobs” (objects).
- Data is stored in a **storage account**, organized into **containers**, which hold **blobs**.
- Supports blob types like **block blobs** (most common for files), **append blobs** (logging), and **page blobs** (used for scenarios ...
```

</details>

---

### factual_002: ✅ PASSED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 19.05s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage supports four **access tiers**:

- **Hot**: Optimized for data that’s accessed frequently.
- **Cool**: For infrequently accessed data (typically stored at least ~30 days); lower storage cost, higher access cost than Hot.
- **Cold**: For rarely accessed data (typically stored at least ~90 days); even lower storage cost, higher access cost than Cool.
- **Archive**: Lowest storage cost for long-term retention; data is **offline** and must be **rehydrated** before it can be read (...
```

</details>

---

### factual_003: ✅ PASSED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 27.32s |
| Overall Score | 1.00 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Functions and Azure Logic Apps are both “serverless” ways to build cloud solutions, but they’re optimized for different kinds of work.

## Core difference
- **Azure Functions**: *Code-first* serverless compute. You write functions (C#, JavaScript/TypeScript, Python, etc.) that run on triggers (HTTP, timer, queue/event, etc.).
- **Azure Logic Apps**: *Workflow-first* integration and automation. You build orchestrations visually (or in workflow definition) using connectors (Microsoft 365, Dy...
```

</details>

---

### factual_004: ✅ PASSED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 20.70s |
| Overall Score | 0.87 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure OpenAI is available in a **subset of Azure regions**, and the exact list varies by **model** and can change over time.

The most reliable, always-up-to-date way to see the current availability is the official **Azure OpenAI “Models”** page, which links to region availability and shows it by model:

- **Azure OpenAI models (and regional availability links):** https://learn.microsoft.com/azure/ai-services/openai/concepts/models

If you tell me **which model(s)** you care about (e.g., GPT-4o,...
```

</details>

---

### factual_005: ✅ PASSED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 25.96s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure App Service offers these **App Service plan pricing tiers** (Windows/Linux):

- **Free (F1)** – Shared infrastructure, for dev/test.
- **Shared (D1)** – Shared infrastructure, low-cost dev/test.
- **Basic (B1–B3)** – Dedicated VM (per plan), for lower traffic/prod basics.
- **Standard (S1–S3)** – Dedicated VM with additional scale/features for production.
- **Premium v2 (P1v2–P3v2)** – Dedicated VMs with higher performance and scale.
- **Premium v3 (P0v3–P3v3)** – Newer generation dedicate...
```

</details>

---

### howto_001: ✅ PASSED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 90.40s |
| Overall Score | 0.96 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To deploy an Azure Function using GitHub Actions:

1. Create your Function App in Azure and push your function code to GitHub.
2. In Azure Portal, go to your Function App → **Get publish profile**. Add its contents to your GitHub repo as a secret (commonly `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`).
3. Create a workflow file at `.github/workflows/deploy.yml` using `Azure/functions-action`.

Example (Node.js):

```yaml
name: Deploy Azure Function

on:
  push:
    branches: [ "main"...
```

</details>

---

### howto_002: ✅ PASSED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 93.73s |
| Overall Score | 0.99 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To configure **VNet Integration** for **Azure App Service**:

## Prerequisites
- App Service plan tier that supports VNet Integration.
- A **VNet in the same region** as the app (for Regional VNet Integration).
- A **dedicated, empty subnet** for integration, delegated to `Microsoft.Web/serverFarms` (portal can delegate). Microsoft commonly recommends **/27 or larger**.  
Source: https://learn.microsoft.com/azure/app-service/overview-vnet-integration

## Enable VNet Integrat...
```

</details>

---

### howto_003: ✅ PASSED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 83.89s |
| Overall Score | 0.79 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To enable Application Insights for an Azure Function:

## Option 1 (Portal)
1. Azure portal → **Function App** → your function app  
2. **Settings** → **Application Insights**  
3. **Turn on / Enable Application Insights**  
4. Choose **Create new** or **Select existing** Application Insights resource  
5. **Save/Apply**

## Option 2 (App setting)
In **Function App** → **Configuration** → **Application settings**, set:
- `APPLICATIONINSIGHTS_CONNECTION_STRING` = your Applica...
```

</details>

---

### howto_004: ✅ PASSED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 82.22s |
| Overall Score | 0.96 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To set up **managed identity** for **Azure App Service** to access **Azure Key Vault**:

1) **Enable managed identity on the App Service**
- App Service → **Identity**
- Turn **System assigned** = **On** → **Save**  
Docs: https://learn.microsoft.com/azure/app-service/overview-managed-identity

2) **Grant that identity access to the Key Vault**
Choose one permission model:

- **RBAC (recommended if your vault uses “Azure role-based access control”)**
  - Key Vault → **Access...
```

</details>

---

### howto_005: ❌ FAILED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 181.57s |
| Overall Score | 0.42 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### arch_001: ✅ PASSED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 167.58s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

---

### arch_002: ✅ PASSED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 178.28s |
| Overall Score | 0.88 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, architecture |

<details>
<summary>Response Preview</summary>

```
## Step 2: research

A highly available (HA) web app on Azure is typically designed with redundancy and failover at each layer (global entry, region/zone, app, and data), plus health-based routing and automated recovery.

Key guidance and reference docs:
- Azure Well-Architected Framework (Reliability): https://learn.microsoft.com/en-us/azure/well-architected/reliability/
- Azure Front Door overview (global L7 entry + health probes/failover): https://learn.microsoft.com/en-us/azure/frontdoor/fro...
```

</details>

---

### arch_003: ✅ PASSED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 38.74s |
| Overall Score | 0.80 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Below are practical, high-impact **cost optimization strategies for Azure Kubernetes Service (AKS)**, aligned with Microsoft guidance and common real-world patterns.

## 1) Right-size and scale only when needed
- **Use Cluster Autoscaler** to automatically add/remove nodes based on pending pods and scheduling needs (avoid paying for idle nodes).  
  Docs: https://learn.microsoft.com/azure/aks/cluster-autoscaler
- Combine with **Horizontal Pod Autoscaler (HPA)** (and/or KEDA for event-driven scal...
```

</details>

---

### arch_004: ❌ FAILED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 158.97s |
| Overall Score | 0.64 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

---

### arch_005: ✅ PASSED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 171.75s |
| Overall Score | 0.95 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

<details>
<summary>Response Preview</summary>

```
## Step 2: architecture

A recommended Azure architecture for a multi-tenant SaaS app is typically a **hub-and-spoke landing zone** with **separation of control plane and data plane**, and a deliberate choice of **tenant isolation model** (pooled vs per-tenant DB vs silo).

**Key elements:**
- **Tenant isolation models**
  - **Pooled**: shared app + shared DB with tenant key (lowest cost; needs strong logical isolation).
  - **Pooled app + per-tenant database**: shared compute, separate DBs (goo...
```

</details>

---

### code_cli_001: ✅ PASSED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 75.58s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_002: ✅ PASSED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 74.01s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_003: ✅ PASSED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 74.15s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_001: ✅ PASSED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 73.12s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_002: ✅ PASSED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 76.41s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_003: ✅ PASSED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 71.97s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_001: ✅ PASSED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 75.65s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_002: ✅ PASSED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 71.66s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_003: ✅ PASSED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 73.25s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_004: ✅ PASSED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 74.29s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 180.06s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 77.74s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | code |

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 180.16s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### complex_004: ❌ FAILED

**Prompt**: Design a data analytics solution on Azure for processing IoT sensor data. Include architecture recommendations using Event Hubs and Stream Analytics, plus sample code for an Azure Function to process the events.

| Metric | Value |
|--------|-------|
| Duration | 180.05s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 180.07s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---
