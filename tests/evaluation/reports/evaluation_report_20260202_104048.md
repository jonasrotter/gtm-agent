# GTM-Agent Tool Evaluation Report

## Summary

- **Date**: 2026-02-02T10:40:48.500984
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
| Routing Accuracy | 100.0% | 90% | ✅ |
| Tool Selection | 0.0% | 85% | ❌ |
| Keyword Coverage | 80.0% | 75% | ✅ |
| Performance | 94.0% | 80% | ✅ |

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
| code | 10 | 0 (0%) | 0.54 | 87.5s |
| complex | 5 | 0 (0%) | 0.35 | 128.3s |
| research | 10 | 0 (0%) | 0.00 | 0.0s |

## Recommendations

1. Tool selection accuracy is 0.0% (target: 85%). Review planner prompts to improve tool selection logic.
2. Category 'research' has 0.0% pass rate. Review failed tasks for common issues.
3. Category 'architecture' has 0.0% pass rate. Review failed tasks for common issues.
4. Category 'code' has 0.0% pass rate. Review failed tasks for common issues.
5. Category 'complex' has 0.0% pass rate. Review failed tasks for common issues.

## Detailed Task Results

### factual_001: ❌ FAILED

**Prompt**: What is Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 2.35s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### factual_002: ❌ FAILED

**Prompt**: What are the storage tiers for Azure Blob Storage?

| Metric | Value |
|--------|-------|
| Duration | 2.31s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### factual_003: ❌ FAILED

**Prompt**: What is the difference between Azure Functions and Logic Apps?

| Metric | Value |
|--------|-------|
| Duration | 2.31s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### factual_004: ❌ FAILED

**Prompt**: What regions is Azure OpenAI available in?

| Metric | Value |
|--------|-------|
| Duration | 2.30s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### factual_005: ❌ FAILED

**Prompt**: What are the pricing tiers for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 2.30s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### howto_001: ❌ FAILED

**Prompt**: How do I deploy an Azure Function using GitHub Actions?

| Metric | Value |
|--------|-------|
| Duration | 2.31s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### howto_002: ❌ FAILED

**Prompt**: How do I configure VNet integration for Azure App Service?

| Metric | Value |
|--------|-------|
| Duration | 2.30s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### howto_003: ❌ FAILED

**Prompt**: How do I enable Application Insights for my Azure Function?

| Metric | Value |
|--------|-------|
| Duration | 2.30s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### howto_004: ❌ FAILED

**Prompt**: How do I set up managed identity for Azure App Service to access Key Vault?

| Metric | Value |
|--------|-------|
| Duration | 2.30s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### howto_005: ❌ FAILED

**Prompt**: How do I configure auto-scaling for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 2.31s |
| Overall Score | 0.45 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### arch_001: ❌ FAILED

**Prompt**: What are the best practices for Azure App Service security?

| Metric | Value |
|--------|-------|
| Duration | 2.30s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### arch_002: ❌ FAILED

**Prompt**: How do I design a highly available web application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 2.30s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### arch_003: ❌ FAILED

**Prompt**: What are the cost optimization strategies for Azure Kubernetes Service?

| Metric | Value |
|--------|-------|
| Duration | 2.29s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### arch_004: ❌ FAILED

**Prompt**: How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?

| Metric | Value |
|--------|-------|
| Duration | 2.32s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### arch_005: ❌ FAILED

**Prompt**: What is the recommended architecture for a multi-tenant SaaS application on Azure?

| Metric | Value |
|--------|-------|
| Duration | 2.30s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### code_cli_001: ❌ FAILED

**Prompt**: Give me the Azure CLI commands to create a storage account with private endpoint

| Metric | Value |
|--------|-------|
| Duration | 2.30s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### code_cli_002: ❌ FAILED

**Prompt**: Write the Azure CLI commands to create a resource group and deploy an App Service Plan

| Metric | Value |
|--------|-------|
| Duration | 2.31s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: ConnectError: All connection attempts failed

---

### code_cli_003: ❌ FAILED

**Prompt**: Generate Azure CLI commands to create an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 94.61s |
| Overall Score | 0.54 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_sdk_001: ❌ FAILED

**Prompt**: Write Python code to upload a file to Azure Blob Storage using the SDK

| Metric | Value |
|--------|-------|
| Duration | 88.30s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_sdk_002: ❌ FAILED

**Prompt**: Write Python code to send a message to Azure Service Bus queue

| Metric | Value |
|--------|-------|
| Duration | 83.16s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_sdk_003: ❌ FAILED

**Prompt**: Generate C# code to read secrets from Azure Key Vault

| Metric | Value |
|--------|-------|
| Duration | 76.34s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_iac_001: ❌ FAILED

**Prompt**: Generate Bicep code to deploy an Azure App Service with a SQL Database

| Metric | Value |
|--------|-------|
| Duration | 92.51s |
| Overall Score | 0.54 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_iac_002: ❌ FAILED

**Prompt**: Create Terraform code to deploy an AKS cluster with managed identity

| Metric | Value |
|--------|-------|
| Duration | 100.78s |
| Overall Score | 0.54 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_iac_003: ❌ FAILED

**Prompt**: Write Bicep code to create a Virtual Network with three subnets

| Metric | Value |
|--------|-------|
| Duration | 81.14s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### code_iac_004: ❌ FAILED

**Prompt**: Generate ARM template for an Azure Function App with Application Insights

| Metric | Value |
|--------|-------|
| Duration | 83.05s |
| Overall Score | 0.55 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### complex_001: ❌ FAILED

**Prompt**: Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample Bicep code for the API Gateway configuration.

| Metric | Value |
|--------|-------|
| Duration | 180.14s |
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
| Duration | 78.29s |
| Overall Score | 0.30 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### complex_003: ❌ FAILED

**Prompt**: I need to implement zero-trust security for my Azure environment. Provide the architecture recommendations, best practices, and Bicep templates for configuring Azure Firewall and Private Endpoints.

| Metric | Value |
|--------|-------|
| Duration | 181.30s |
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
| Duration | 178.37s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

---

### complex_005: ❌ FAILED

**Prompt**: Create a disaster recovery plan for an Azure web application. Include the architecture for multi-region deployment, best practices for data replication, and Terraform code for setting up Traffic Manager.

| Metric | Value |
|--------|-------|
| Duration | 180.05s |
| Overall Score | 0.40 |
| Routing Score | 1.00 |
| Tool Selection | 0.00 |
| Tools Used | None |

**Error**: HTTP 500: {"detail":{"error_code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}

---
