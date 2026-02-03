# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-03T08:43:21.766152
- **Evaluation File**: tests/evaluation/evaluation.xml
- **Mode**: api

### Results Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 30 |
| Passed | 0 |
| Failed | 30 |
| Pass Rate | 0.0% |

### Dimension Scores

| Dimension | Score | Target | Status |
|-----------|-------|--------|--------|
| Routing Accuracy | 0.0% | 90% | ❌ |
| Tool Selection | 0.0% | 85% | ❌ |
| Keyword Coverage | 0.0% | 75% | ❌ |
| Performance | 0.0% | 80% | ❌ |

### Token Usage

| Metric | Count |
|--------|-------|
| Input Tokens | 0 |
| Output Tokens | 0 |
| Total Tokens | 0 |

## Per-Category Results

| Category | Tasks | Passed | Avg Score | Avg Duration |
|----------|-------|--------|-----------|--------------|
| architecture | 5 | 0 (0%) | 0.00 | 0.0s |
| code | 10 | 0 (0%) | 0.00 | 0.0s |
| complex | 5 | 0 (0%) | 0.00 | 0.0s |
| research | 10 | 0 (0%) | 0.00 | 0.0s |

## Recommendations

1. Routing accuracy is 0.0% (target: 90%). Consider reviewing classifier patterns for misclassified queries.
2. Tool selection accuracy is 0.0% (target: 85%). Review planner prompts to improve tool selection logic.
3. Average keyword coverage is 0.0% (target: 75%). Responses may be missing key information. Check sub-agent prompts.
4. Performance score is 0.0% (target: 80%). Consider optimizing slow tools or reducing unnecessary iterations.
5. Category 'research' has 0.0% pass rate. Review failed tasks for common issues.
6. Category 'architecture' has 0.0% pass rate. Review failed tasks for common issues.
7. Category 'code' has 0.0% pass rate. Review failed tasks for common issues.
8. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ❌ FAILED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 18.44s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":17642}}

---

### factual_002: ❌ FAILED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 180.84s |
| Overall Score | 0.36 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### factual_003: ❌ FAILED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 19.31s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":19292}}

---

### factual_004: ❌ FAILED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 14.58s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":14538}}

---

### factual_005: ❌ FAILED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 12.46s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":12419}}

---

### howto_001: ❌ FAILED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 11.35s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":11315}}

---

### howto_002: ❌ FAILED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 7.73s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":7711}}

---

### howto_003: ❌ FAILED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 8.66s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":8642}}

---

### howto_004: ❌ FAILED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 8.31s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":8282}}

---

### howto_005: ❌ FAILED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 7.21s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":7174}}

---

### arch_001: ❌ FAILED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 7.64s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":7610}}

---

### arch_002: ❌ FAILED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 9.27s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":9239}}

---

### arch_003: ❌ FAILED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 180.59s |
| Overall Score | 0.52 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"HTTPException","error_details":"504: {'error_code': 'REQUEST_TIMEOUT', 'message': 'Query processing time

---

### arch_004: ❌ FAILED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 10.72s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":10670}}

---

### arch_005: ❌ FAILED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 8.30s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":8271}}

---

### code_cli_001: ❌ FAILED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 5.03s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":5005}}

---

### code_cli_002: ❌ FAILED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 3.88s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":3842}}

---

### code_cli_003: ❌ FAILED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 5.85s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":5804}}

---

### code_sdk_001: ❌ FAILED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 4.61s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":4590}}

---

### code_sdk_002: ❌ FAILED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 4.05s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":4024}}

---

### code_sdk_003: ❌ FAILED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 5.09s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":5059}}

---

### code_iac_001: ❌ FAILED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 5.98s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":5940}}

---

### code_iac_002: ❌ FAILED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 5.19s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":5151}}

---

### code_iac_003: ❌ FAILED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 4.09s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":4063}}

---

### code_iac_004: ❌ FAILED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 14.10s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":14075}}

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 10.68s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":10662}}

---

### complex_002: ❌ FAILED

**Prompt**: Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed to create the target Azure SQL Database.

| Metric | Value |
|--------|-------|
| Duration | 7.87s |
| Overall Score | 0.30 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":7841}}

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 13.63s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":13591}}

---

### complex_004: ❌ FAILED

**Prompt**: Design a data analytics solution on Azure for processing IoT sensor data. Include architecture recommendations using Event Hubs and Stream Analytics, plus sample code for an Azure Function to process the events.

| Metric | Value |
|--------|-------|
| Duration | 12.12s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":12088}}

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 19.71s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred","error_type":"NameError","error_details":"name 'Content' is not defined","processing_time_ms":19660}}

---
