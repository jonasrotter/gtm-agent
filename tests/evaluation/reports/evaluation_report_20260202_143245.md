# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T14:32:45.690443
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
| Tool Selection | 90.7% | 85% | ✅ |
| Keyword Coverage | 71.6% | 75% | ❌ |
| Performance | 95.9% | 80% | ✅ |

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
| architecture | 8 | 0.00s | 100.0% |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 5 (100%) | 0.89 | 109.3s |
| code | 10 | 10 (100%) | 0.84 | 75.5s |
| complex | 5 | 0 (0%) | 0.56 | 148.6s |
| research | 10 | 9 (90%) | 0.89 | 69.6s |

## Recommendations

1. Average keyword coverage is 71.6% (target: 75%). Responses may be missing key information. Check sub-agent prompts.
2. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ✅ PASSED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 25.68s |
| Overall Score | 0.97 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage is Azure’s object storage service for storing large amounts of unstructured data—data that doesn’t fit a traditional relational database—such as text and binary files.

Key points:
- Stores data as **blobs** inside **containers** within an Azure **storage account**.
- Designed for scenarios like **serving images/video**, **storing files for distributed access**, **streaming**, **backup/restore & disaster recovery**, and **data archiving**.
- Supports different blob types (comm...
```

</details>

---

### factual_002: ✅ PASSED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 18.59s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Blob Storage supports four **access tiers** (storage tiers):

- **Hot**: For data accessed frequently (lowest access costs, higher storage cost).
- **Cool**: For infrequently accessed data stored for at least ~30 days (lower storage cost, higher access cost than Hot).
- **Cold**: For rarely accessed data stored for at least ~90 days (lower storage cost than Cool, higher access cost).
- **Archive**: For rarely accessed data stored for at least ~180 days (lowest storage cost; data must be re...
```

</details>

---

### factual_003: ✅ PASSED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 34.44s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure Functions and Azure Logic Apps are both *serverless* ways to build integrations and automation in Azure, but they target different needs:

## Azure Functions (code-first compute)
- **What it is:** Event-driven code (C#, JavaScript/TypeScript, Python, Java, etc.) that runs when triggered (HTTP request, timer, queue/message, Event Grid, etc.).
- **Best for:** Custom logic, computation, transformations, APIs, event processing—anything where **writing code** is the main work.
- **How you build...
```

</details>

---

### factual_004: ✅ PASSED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 18.89s |
| Overall Score | 0.87 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure OpenAI is available in a subset of Azure regions, and the exact list varies by **model** and can change over time.

The up-to-date, official list is published in Microsoft Learn here (see the **“Model availability”** / region availability tables):

https://learn.microsoft.com/azure/ai-services/openai/concepts/models#model-availability Azure OpenAI is available in a subset of Azure regions, and the exact list varies by **model** and can change over time.

The up-to-date, official list is pu...
```

</details>

---

### factual_005: ✅ PASSED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 17.69s |
| Overall Score | 0.90 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Azure App Service has these **pricing tiers** (via the App Service plan you choose):

- **Free (F1)** – Shared infrastructure; for dev/test and trials.
- **Shared (D1)** – Shared infrastructure; low-cost dev/test.
- **Basic (B1–B3)** – Dedicated compute; entry-level production.
- **Standard (S1–S3)** – Dedicated compute; production features and scaling.
- **Premium (P0v3–P3v3)** – Dedicated compute; higher performance and advanced scaling/features.
- **Isolated (I1v2–I3v2)** – Dedicated compute ...
```

</details>

---

### howto_001: ✅ PASSED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 166.91s |
| Overall Score | 0.74 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

---

### howto_002: ❌ FAILED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 85.56s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"TypeError","error_details":"float() argument must be a string or a real number, not 'dict'","processing_

---

### howto_003: ✅ PASSED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 87.01s |
| Overall Score | 0.86 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To enable Application Insights for an Azure Function:

## Option A (Portal)
1. Open your **Function App** in the Azure portal.
2. Go to **Settings → Application Insights**.
3. Choose **Turn on Application Insights** (create new) or **Select existing resource**.
4. **Save**.

## Option B (App settings / Configuration)
1. Create or select an **Application Insights** resource.
2. In your Function App, set this application setting (preferred):
   - `APPLICATIONINSIGHTS_CONNECTIO...
```

</details>

---

### howto_004: ✅ PASSED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 172.97s |
| Overall Score | 0.92 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

To set up **managed identity for Azure App Service to access Key Vault**:

1) **Enable managed identity on the App Service**
- App Service → **Identity**
- Turn **System assigned** = **On** → **Save**  
Docs: https://learn.microsoft.com/azure/app-service/overview-managed-identity

2) **Grant that identity permissions on the Key Vault**
First check Key Vault → **Access configuration** (RBAC vs Access policies).

- **If using Azure RBAC (recommended):**  
  Key Vault → **Acces...
```

</details>

---

### howto_005: ✅ PASSED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 83.91s |
| Overall Score | 1.00 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | research, code |

<details>
<summary>Response Preview</summary>

```
## Step 1: research

Auto-scaling in AKS is typically configured at two layers:

1) **Cluster Autoscaler (node scaling)** – adds/removes **nodes** by resizing a node pool.  
2) **Horizontal Pod Autoscaler (HPA) (pod scaling)** – adds/removes **pods** based on metrics (CPU/memory/custom).

## 1) Enable **Cluster Autoscaler** on an AKS node pool

### Enable during cluster creation
```bash
az aks create \
  -g <rg> -n <aksName> \
  --node-count 1 \
  --enable-cluster-autoscaler \
  --min-count 1 \
...
```

</details>

---

### arch_001: ✅ PASSED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 164.51s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

---

### arch_002: ✅ PASSED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 77.76s |
| Overall Score | 0.96 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture, research |

<details>
<summary>Response Preview</summary>

```
## Step 1: architecture

## Step 1 output (Architecture): Highly available web application on Azure

- **Define targets first:** choose availability objective (e.g., 99.9/99.99), plus **RTO/RPO**, and decide **zone-redundant** vs **multi-region active/active** vs **active/passive**.
- **Global entry + failover:** use **Azure Front Door** (often preferred) for global routing, health probes, TLS offload, and WAF; alternatives include **Traffic Manager** (DNS failover) and **Application Gateway** (...
```

</details>

---

### arch_003: ✅ PASSED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 45.79s |
| Overall Score | 0.80 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

<details>
<summary>Response Preview</summary>

```
Key Azure Kubernetes Service (AKS) cost optimization strategies (with the biggest savings levers first):

## 1) Right-size and autoscale compute
- **Use the Cluster Autoscaler** to automatically add/remove nodes based on pending pods, so you don’t pay for idle nodes long-term.  
  Docs: https://learn.microsoft.com/azure/aks/cluster-autoscaler
- **Use Horizontal Pod Autoscaler (HPA)/KEDA** so your workloads scale with demand; combine with Cluster Autoscaler for end-to-end elasticity.
- **Right-si...
```

</details>

---

### arch_004: ✅ PASSED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 96.52s |
| Overall Score | 0.99 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

<details>
<summary>Response Preview</summary>

```
## Step 2: architecture

## Checklist (actionable)

### 1) Define reliability targets (now)
- [ ] Identify critical user journeys (e.g., login, checkout, API read/write).
- [ ] Set **SLOs** per journey (availability, latency, error rate) and error budgets.
- [ ] Define **SLIs** and exact measurement windows (p50/p95/p99 latency, success rate, saturation).
- [ ] Establish RTO/RPO targets per data store and dependency.

### 2) Choose deployment topology (region/zone) (now)
- [ ] Decide: **Zonal (s...
```

</details>

---

### arch_005: ✅ PASSED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 161.70s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | architecture |

---

### code_cli_001: ✅ PASSED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 80.68s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_002: ✅ PASSED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 72.22s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_cli_003: ✅ PASSED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 72.38s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_001: ✅ PASSED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 74.03s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_002: ✅ PASSED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 78.49s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_sdk_003: ✅ PASSED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 72.59s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_001: ✅ PASSED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 77.33s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_002: ✅ PASSED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 72.69s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_003: ✅ PASSED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 71.92s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### code_iac_004: ✅ PASSED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 82.54s |
| Overall Score | 0.84 |
| Routing Score | 1.00 |
| Tool Selection | 1.00 |
| Tools Used | code |

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 176.90s |
| Overall Score | 0.65 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | architecture |

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 89.07s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.75 |
| Tools Used | code |

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 180.55s |
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
| Duration | 179.93s |
| Overall Score | 0.49 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | research |

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
