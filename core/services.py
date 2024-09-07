"""
The LLMMetric Simulator Module
"""
import random
from scipy.stats import norm
from decouple import config

from core.models import LLMModel, LLMPerformance


class LLMMetricSimulator:
    """
    The class definition for the LLMMetric Simulator
    """
    # Retrieve AI models and their configurations from environment variables
    AI_MODELS = config('AI_MODELS').split(',')

    # Configurations for model parameters
    MEAN_TTF = {}
    STD_DEV_TTF = {}
    MEAN_E2E = {}
    STD_DEV_E2E = {}

    for model in AI_MODELS:
        MEAN_TTF[model] = config(f'MEAN_TTF_{model.upper()}', 1.0)
        STD_DEV_TTF[model] = config(f'STD_DEV_TTF_{model.upper()}', 0.2)
        MEAN_E2E[model] = config(f'MEAN_E2E_{model.upper()}', 3.0)
        STD_DEV_E2E[model] = config(f'STD_DEV_E2E_{model.upper()}', 0.5)

    # Default values for unknown models
    DEFAULT_TTF = (
    config('DEFAULT_MEAN_TTF', 3.7), config('DEFAULT_STD_DEV_TTF', 0.7)
    )
    DEFAULT_E2E = (
    config('DEFAULT_MEAN_E2E', 3.7), config('DEFAULT_STD_DEV_E2E', 0.7)
    )

    # Random generation range
    MIN_TOKENS_GENERATED = int(config('MIN_TOKENS_GENERATED', 50))
    MAX_TOKENS_GENERATED = int(config('MAX_TOKENS_GENERATED', 200))

    def __init__(self, model_name):
        """
        The initialization for the LLMMetric Simulator class
        :param model_name: Name of the LLM model
        """
        self.model_name = model_name

    def simulate_ttft(self):
        """
        Simulate Time to First Token (TTFT) using normal distribution.
        """
        mean, std_dev = self._get_ttft_params()
        return max(0.0, norm.rvs(loc=mean, scale=std_dev))

    def simulate_e2e_latency(self):
        """
        Simulate End-to-End Latency using normal distribution.
        """
        mean, std_dev = self._get_e2e_params()
        return max(0.1, norm.rvs(loc=mean, scale=std_dev))

    def generate_performance_metrics(self):
        """
        Generate a full set of performance metrics for a model.
        """
        ttft = self.simulate_ttft()
        e2e_latency = self.simulate_e2e_latency()
        tokens_generated = random.randint(self.MIN_TOKENS_GENERATED, self.MAX_TOKENS_GENERATED)
        tps = tokens_generated / e2e_latency
        rps = 1 / e2e_latency if e2e_latency > 0 else 0

        return LLMPerformance(
            llm=LLMModel(name=self.model_name, description=self.model_name),
            time_to_first_token=round(ttft, 2),
            tokens_per_second=round(tps, 2),
            e2e_latency=round(e2e_latency, 2),
            requests_per_second=round(rps, 2),
            tokens_generated=tokens_generated
        )

    def _get_ttft_params(self):
        """
        Retrieve TTFT parameters based on the model name.
        """
        return self.MEAN_TTF.get(self.model_name, self.DEFAULT_TTF[0]), \
            self.STD_DEV_TTF.get(self.model_name, self.DEFAULT_TTF[1])

    def _get_e2e_params(self):
        """
        Retrieve e2e Latency parameters based on the model name.
        """
        return self.MEAN_E2E.get(self.model_name, self.DEFAULT_E2E[0]), \
            self.STD_DEV_E2E.get(self.model_name, self.DEFAULT_E2E[1])
