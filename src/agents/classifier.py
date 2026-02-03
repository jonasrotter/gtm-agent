"""
Query Classifier for intelligent query routing.

Classifies user queries into categories to determine optimal processing path:
- factual: Simple lookup → direct agent call (skip PEV)
- howto: Procedural → lite PEV (1 iteration)
- architecture: Design/best practices → standard PEV (2 iterations)
- code: Code generation → lite PEV (1 iteration)
- complex: Multi-part → full PEV (4 iterations)
"""

import re
from enum import Enum
from typing import Any

try:
    from src.utils.logging import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback for testing without full dependencies
    import logging
    logger = logging.getLogger(__name__)


class QueryCategory(str, Enum):
    """
    Query categories for routing decisions.
    
    Each category has associated configuration for:
    - max_iterations: Maximum PEV loop iterations
    - skip_pev: Whether to bypass PEV entirely
    - threshold: Acceptance threshold for verification
    - default_tool: Primary tool to use if skipping PEV
    """
    FACTUAL = "factual"
    HOWTO = "howto"
    ARCHITECTURE = "architecture"
    CODE = "code"
    COMPLEX = "complex"
    
    def get_config(self) -> dict[str, Any]:
        """
        Get processing configuration for this category.
        
        Returns:
            dict with max_iterations, skip_pev, threshold, and default_tool.
        """
        configs = {
            QueryCategory.FACTUAL: {
                "max_iterations": 1,
                "skip_pev": True,
                "threshold": None,  # No verification
                "early_accept_threshold": None,
                "default_tool": "research",
            },
            QueryCategory.HOWTO: {
                "max_iterations": 1,  # Single iteration to prevent timeouts
                "skip_pev": False,
                "threshold": 0.70,  # Standard threshold
                "early_accept_threshold": 0.85,  # Accept immediately if high quality
                "default_tool": "research",
            },
            QueryCategory.ARCHITECTURE: {
                "max_iterations": 2,
                "skip_pev": False,
                "threshold": 0.75,  # Standard threshold for architecture
                "early_accept_threshold": 0.90,
                "default_tool": "architecture",
            },
            QueryCategory.CODE: {
                "max_iterations": 1,
                "skip_pev": False,
                "threshold": 0.70,  # Standard threshold for code tasks
                "early_accept_threshold": 0.85,
                "default_tool": "code",
            },
            QueryCategory.COMPLEX: {
                "max_iterations": 2,  # Reduced from 3 to avoid extreme timeouts
                "skip_pev": False,
                "threshold": 0.70,  # Accept good quality to complete within time budget
                "early_accept_threshold": 0.80,  # Accept immediately if high quality
                "default_tool": None,  # Let planner decide
            },
        }
        return configs[self]


class QueryClassifier:
    """
    Classifies user queries into categories using pattern matching.
    
    Fast, lightweight classification without LLM calls.
    Uses regex patterns to identify query intent.
    """
    
    # Pattern groups for each category
    # Order matters: check complex first (compound detection), then specific categories
    
    # Complex patterns - compound queries with multiple intents
    COMPLEX_PATTERNS = [
        r"\band\s+(also\s+)?(write|generate|create|show|implement|design)",  # "explain X and write Y"
        r"\bthen\s+(write|generate|create|show|implement|design|research)",  # "do X then Y"
        r"\balso\s+(write|generate|create|show|explain|design)",  # "X and also Y"
        r"\?\s*[A-Z]",  # Multiple sentences with question + statement
        r"\?\s*\w+.*\?",  # Multiple question marks
        r"(design|architect).*\b(implement|code|template|bicep|terraform)",  # Design + implement
        r"(explain|research|what).*\b(and|then)\s*(generate|write|create|show)",  # Explain then code
    ]
    
    # Factual patterns - simple lookup/explanation queries
    FACTUAL_PATTERNS = [
        r"^what\s+(is|are)\s+",  # "What is X?"
        r"^explain\s+",  # "Explain X"
        r"^define\s+",  # "Define X"
        r"^describe\s+",  # "Describe X"
        r"^tell\s+me\s+about\s+",  # "Tell me about X"
        r"^what\s+does\s+",  # "What does X do?"
        r"^what\s+do\s+",  # "What do X mean?"
        r"^can\s+you\s+explain\s+",  # "Can you explain X?"
        r"^what('s|\s+is)\s+the\s+(definition|meaning)\s+of",  # "What's the definition of"
        r"^overview\s+of\s+",  # "Overview of X"
        r"^introduction\s+to\s+",  # "Introduction to X"
    ]
    
    # HowTo patterns - procedural/step-by-step queries
    HOWTO_PATTERNS = [
        r"^how\s+(do|can|should)\s+i\s+",  # "How do I X?"
        r"^how\s+to\s+",  # "How to X"
        r"^steps\s+to\s+",  # "Steps to X"
        r"^guide\s+(to|for|on)\s+",  # "Guide to X"
        r"^tutorial\s+(on|for)\s+",  # "Tutorial on X"
        r"^help\s+me\s+(with|to)\s+",  # "Help me with X"
        r"^walk\s+me\s+through\s+",  # "Walk me through X"
        r"^show\s+me\s+how\s+to\s+",  # "Show me how to X"
        r"^i\s+want\s+to\s+",  # "I want to X"
        r"^i\s+need\s+to\s+",  # "I need to X"
        r"^what\s+are\s+the\s+steps\s+",  # "What are the steps to"
    ]
    
    # Architecture patterns - design/best practices queries
    ARCHITECTURE_PATTERNS = [
        r"best\s+practices?\s+(for|of|in|when)",  # "Best practices for X"
        r"^design\s+(a|an|the)?\s*",  # "Design a X"
        r"^architect\s+",  # "Architect X"
        r"(how\s+)?should\s+i\s+design",  # "How should I design X?"
        r"^recommend\s+(a|an)?\s*",  # "Recommend a X"
        r"architecture\s+(for|of|pattern)",  # "Architecture for X"
        r"(security|reliability|performance|cost)\s+(considerations|recommendations|best)",  # WAF pillars
        r"waf\s+(pillar|framework|recommendation)",  # WAF explicit
        r"well.?architected",  # Well-architected
        r"^what\s+is\s+the\s+(best|recommended)\s+(way|approach|pattern)",  # "What is the best way"
    ]
    
    # Code patterns - code generation requests
    CODE_PATTERNS = [
        r"^generate\s+",  # "Generate X"
        r"^write\s+(a|an|the|me)?\s*",  # "Write a X"
        r"^create\s+(a|an|the)?\s*(script|code|template|command)",  # "Create a script"
        r"^show\s+me\s+(the\s+)?(code|script|template|command|cli)",  # "Show me the code"
        r"^give\s+me\s+(the\s+)?(code|script|template|command|cli)",  # "Give me the CLI"
        r"(bicep|terraform|arm)\s+(template|configuration|config|code)",  # IaC templates/config
        r"^(bicep|terraform|arm)\s+",  # "Terraform X" at start
        r"(cli|powershell|bash)\s+(command|script)",  # CLI/scripts
        r"^code\s+(for|to)\s+",  # "Code for X"
        r"azure\s+cli\s+(to|for|command)",  # "Azure CLI to X"
        r"^implement\s+",  # "Implement X"
        r"\bpython\s+(code|script|function)",  # Python code
        r"\bc#\s+(code|class|method)",  # C# code
        r"\bjavascript\s+(code|function)",  # JavaScript code
    ]
    
    def __init__(self):
        """Initialize QueryClassifier with compiled patterns."""
        # Compile patterns for performance
        self._complex_re = [re.compile(p, re.IGNORECASE) for p in self.COMPLEX_PATTERNS]
        self._factual_re = [re.compile(p, re.IGNORECASE) for p in self.FACTUAL_PATTERNS]
        self._howto_re = [re.compile(p, re.IGNORECASE) for p in self.HOWTO_PATTERNS]
        self._architecture_re = [re.compile(p, re.IGNORECASE) for p in self.ARCHITECTURE_PATTERNS]
        self._code_re = [re.compile(p, re.IGNORECASE) for p in self.CODE_PATTERNS]
        
        logger.info("QueryClassifier initialized")
    
    def classify(self, query: str) -> QueryCategory:
        """
        Classify a query into a category.
        
        Uses pattern matching with priority order:
        1. Complex (compound queries)
        2. Code (explicit code requests)
        3. Architecture (design/best practices)
        4. HowTo (procedural)
        5. Factual (informational - default)
        
        Args:
            query: The user's query string.
            
        Returns:
            QueryCategory indicating the query type.
        """
        if not query or not query.strip():
            logger.debug("Empty query, defaulting to FACTUAL")
            return QueryCategory.FACTUAL
        
        query = query.strip()
        
        # Check for complex queries first (compound requests)
        if self._matches_any(query, self._complex_re):
            logger.debug("Query classified as COMPLEX", query=query[:50])
            return QueryCategory.COMPLEX
        
        # Check for code generation requests
        if self._matches_any(query, self._code_re):
            logger.debug("Query classified as CODE", query=query[:50])
            return QueryCategory.CODE
        
        # Check for architecture/best practices
        if self._matches_any(query, self._architecture_re):
            logger.debug("Query classified as ARCHITECTURE", query=query[:50])
            return QueryCategory.ARCHITECTURE
        
        # Check for howto/procedural
        if self._matches_any(query, self._howto_re):
            logger.debug("Query classified as HOWTO", query=query[:50])
            return QueryCategory.HOWTO
        
        # Check for factual/informational
        if self._matches_any(query, self._factual_re):
            logger.debug("Query classified as FACTUAL", query=query[:50])
            return QueryCategory.FACTUAL
        
        # Default to FACTUAL for ambiguous queries (safest/fastest path)
        logger.debug("Query ambiguous, defaulting to FACTUAL", query=query[:50])
        return QueryCategory.FACTUAL
    
    def _matches_any(self, text: str, patterns: list[re.Pattern]) -> bool:
        """Check if text matches any pattern in the list."""
        return any(p.search(text) for p in patterns)
    
    def get_category_info(self, category: QueryCategory) -> dict[str, Any]:
        """
        Get detailed information about a category.
        
        Args:
            category: The query category.
            
        Returns:
            dict with config and description.
        """
        descriptions = {
            QueryCategory.FACTUAL: "Simple factual lookup - direct agent call, no verification",
            QueryCategory.HOWTO: "Procedural question - lite PEV with single verification pass",
            QueryCategory.ARCHITECTURE: "Design/best practices - standard PEV with 2 iterations max",
            QueryCategory.CODE: "Code generation - lite PEV with single verification pass",
            QueryCategory.COMPLEX: "Multi-part request - full PEV loop with up to 4 iterations",
        }
        
        return {
            "category": category.value,
            "description": descriptions[category],
            "config": category.get_config(),
        }
