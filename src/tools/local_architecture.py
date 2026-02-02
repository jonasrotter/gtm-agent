"""
Local architecture tools using direct HTTP calls.

These tools provide a fallback when HostedMCPTool (Azure AI) is not available.
They use public APIs and Well-Architected Framework knowledge.
"""

from typing import Annotated

from agent_framework import ai_function

from src.lib.logging import get_logger


logger = get_logger(__name__)


# Well-Architected Framework reference data
WAF_PILLARS = {
    "reliability": {
        "name": "Reliability",
        "description": "Ensure workloads meet availability and resilience commitments",
        "key_principles": [
            "Design for failure - assume things will fail",
            "Use availability zones for redundancy",
            "Implement health probes and self-healing",
            "Define and test disaster recovery procedures",
            "Use managed services for built-in reliability",
        ],
        "docs_url": "https://learn.microsoft.com/en-us/azure/well-architected/reliability/",
    },
    "security": {
        "name": "Security",
        "description": "Protect applications and data from threats",
        "key_principles": [
            "Use Zero Trust security model",
            "Implement defense in depth",
            "Use managed identities, avoid secrets",
            "Encrypt data at rest and in transit",
            "Apply least privilege access",
        ],
        "docs_url": "https://learn.microsoft.com/en-us/azure/well-architected/security/",
    },
    "cost": {
        "name": "Cost Optimization",
        "description": "Manage costs while maximizing value",
        "key_principles": [
            "Right-size resources for workloads",
            "Use Azure Reservations for predictable workloads",
            "Implement auto-scaling for variable loads",
            "Use spot instances for fault-tolerant workloads",
            "Monitor and analyze spending patterns",
        ],
        "docs_url": "https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/",
    },
    "operations": {
        "name": "Operational Excellence",
        "description": "Keep systems running in production",
        "key_principles": [
            "Use Infrastructure as Code (IaC)",
            "Implement comprehensive monitoring",
            "Automate deployment and testing",
            "Document runbooks and procedures",
            "Practice incident management",
        ],
        "docs_url": "https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/",
    },
    "performance": {
        "name": "Performance Efficiency",
        "description": "Adapt to changes in demand efficiently",
        "key_principles": [
            "Design for horizontal scaling",
            "Use caching where appropriate",
            "Implement async processing for long tasks",
            "Choose appropriate data stores",
            "Monitor and optimize performance",
        ],
        "docs_url": "https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/",
    },
}


SERVICE_BEST_PRACTICES = {
    "cosmos-db": {
        "name": "Azure Cosmos DB",
        "practices": [
            "Choose appropriate consistency level for your use case",
            "Design partition keys for even data distribution",
            "Use provisioned throughput for predictable workloads",
            "Enable automatic failover for multi-region deployments",
            "Use Cosmos DB's built-in change feed for event-driven patterns",
            "Implement TTL for automatic data expiration",
        ],
        "multi_region": [
            "Configure multi-region writes for low-latency global writes",
            "Use automatic failover with defined priorities",
            "Consider strong consistency only when necessary (impacts latency)",
            "Use session consistency for user-specific data",
            "Replicate data to regions closest to your users",
        ],
        "docs_url": "https://learn.microsoft.com/en-us/azure/cosmos-db/",
    },
    "app-service": {
        "name": "Azure App Service",
        "practices": [
            "Use deployment slots for zero-downtime deployments",
            "Configure auto-scaling based on metrics",
            "Use managed identity for Azure service access",
            "Enable application logging and monitoring",
            "Use always-on for production workloads",
        ],
        "docs_url": "https://learn.microsoft.com/en-us/azure/app-service/",
    },
    "functions": {
        "name": "Azure Functions",
        "practices": [
            "Choose appropriate hosting plan for workload",
            "Use durable functions for stateful workflows",
            "Implement proper error handling and retries",
            "Use managed identity for secure access",
            "Configure appropriate timeout and scaling limits",
        ],
        "docs_url": "https://learn.microsoft.com/en-us/azure/azure-functions/",
    },
}


@ai_function(
    description="""Get Azure Well-Architected Framework guidance and best practices.
    Provides recommendations aligned with WAF pillars: Reliability, Security, 
    Cost Optimization, Operational Excellence, and Performance Efficiency.
    You can optionally specify a pillar and/or topic.""",
    max_invocation_exceptions=3,
)
async def get_waf_guidance(
    pillar: Annotated[str, "WAF pillar: reliability, security, cost, operations, or performance. Leave empty for all pillars."] = "",
    topic: Annotated[str, "Specific topic or Azure service to get guidance for. Example: 'cosmos-db'"] = "",
) -> str:
    """
    Get Well-Architected Framework guidance.
    
    Args:
        pillar: WAF pillar (reliability, security, cost, operations, performance).
        topic: Specific topic or service to get guidance for.
        
    Returns:
        WAF-aligned best practices and recommendations.
    """
    logger.debug("Getting WAF guidance", pillar=pillar, topic=topic)
    
    output_lines = ["## Well-Architected Framework Guidance\n"]
    
    # If a specific pillar is requested
    pillar_lower = pillar.lower()
    if pillar_lower in WAF_PILLARS:
        p = WAF_PILLARS[pillar_lower]
        output_lines.append(f"### {p['name']} Pillar\n")
        output_lines.append(f"*{p['description']}*\n")
        output_lines.append("**Key Principles:**\n")
        for principle in p["key_principles"]:
            output_lines.append(f"- {principle}")
        output_lines.append(f"\n**Learn More:** {p['docs_url']}")
    else:
        # Provide overview of all pillars
        output_lines.append("The Azure Well-Architected Framework consists of five pillars:\n")
        for key, p in WAF_PILLARS.items():
            output_lines.append(f"### {p['name']}")
            output_lines.append(f"*{p['description']}*")
            output_lines.append(f"- {p['key_principles'][0]}")
            output_lines.append(f"- {p['key_principles'][1]}")
            output_lines.append(f"- [Documentation]({p['docs_url']})\n")
    
    # Add topic-specific guidance if available
    topic_lower = topic.lower().replace(" ", "-")
    for service_key, service in SERVICE_BEST_PRACTICES.items():
        if service_key in topic_lower or topic_lower in service_key:
            output_lines.append(f"\n### {service['name']} Best Practices\n")
            for practice in service["practices"]:
                output_lines.append(f"- {practice}")
            if "multi_region" in service and "multi" in topic_lower:
                output_lines.append("\n**Multi-Region Deployment:**\n")
                for tip in service["multi_region"]:
                    output_lines.append(f"- {tip}")
            output_lines.append(f"\n**Documentation:** {service['docs_url']}")
            break
    
    return "\n".join(output_lines)


@ai_function(
    description="""Get Azure service best practices and architecture recommendations.
    Provides specific guidance for Azure services including Cosmos DB, App Service,
    Functions, and more. MUST provide a service name.""",
    max_invocation_exceptions=3,
)
async def get_service_best_practices(
    service: Annotated[str, "Azure service name - REQUIRED. Example: 'cosmos-db', 'app-service', 'functions'"],
    scenario: Annotated[str, "Specific scenario like 'multi-region' or 'high-availability'"] = "",
) -> str:
    """
    Get best practices for a specific Azure service.
    
    Args:
        service: Azure service name (e.g., cosmos-db, app-service, functions).
        scenario: Specific scenario (e.g., multi-region, high-availability).
        
    Returns:
        Service-specific best practices and recommendations.
    """
    logger.debug("Getting service best practices", service=service, scenario=scenario)
    
    service_lower = service.lower().replace(" ", "-").replace("azure-", "").replace("azure ", "")
    
    output_lines = []
    
    # Find matching service
    matched_service = None
    for key, s in SERVICE_BEST_PRACTICES.items():
        if key in service_lower or service_lower in key:
            matched_service = s
            break
    
    if matched_service:
        output_lines.append(f"## {matched_service['name']} Best Practices\n")
        
        for practice in matched_service["practices"]:
            output_lines.append(f"- {practice}")
        
        # Add scenario-specific guidance
        if "multi_region" in matched_service and scenario:
            scenario_lower = scenario.lower()
            if "multi" in scenario_lower or "region" in scenario_lower or "global" in scenario_lower:
                output_lines.append("\n### Multi-Region Deployment\n")
                for tip in matched_service["multi_region"]:
                    output_lines.append(f"- {tip}")
        
        output_lines.append(f"\n**Official Documentation:** {matched_service['docs_url']}")
        output_lines.append("\n### Related WAF Pillars\n")
        output_lines.append("- **Reliability**: High availability and disaster recovery")
        output_lines.append("- **Performance**: Scaling and latency optimization")
        output_lines.append("- **Security**: Data protection and access control")
    else:
        # Generic guidance
        output_lines.append(f"## Azure Best Practices for {service}\n")
        output_lines.append("General Azure architecture best practices:\n")
        output_lines.append("- Design for high availability with redundancy")
        output_lines.append("- Use managed identities for secure authentication")
        output_lines.append("- Implement monitoring and alerting")
        output_lines.append("- Use Infrastructure as Code for deployments")
        output_lines.append("- Follow the Well-Architected Framework pillars")
        output_lines.append("\n**Azure Architecture Center:** https://learn.microsoft.com/en-us/azure/architecture/")
    
    return "\n".join(output_lines)


def get_local_architecture_tools() -> list:
    """Get list of local architecture tools."""
    return [get_waf_guidance, get_service_best_practices]
