"""
The Core dataclass Definition module
"""
from dataclasses import dataclass

@dataclass
class LLMModel:
    """
    The dataclass for LLMModel definition
    """
    name: str
    description: str

@dataclass
class LLMPerformance:
    """
    The dataclass for LLMPerformance definition
    """
    llm: LLMModel
    time_to_first_token: float
    tokens_per_second: float
    e2e_latency: float
    requests_per_second: float
    tokens_generated: int
