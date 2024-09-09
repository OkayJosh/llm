"""
LLM Performance Module
"""
import logging

from decouple import config
from celery import shared_task

from core.models import LLMModel, LLMPerformance
from core.services import LLMMetricSimulator
from infrastructure.repositories import LLMRepository

LOG = logging.getLogger(__name__)

class LLMPerformanceService:
    """
    The LLMPerformanceService provides functionality
    for performing LLM performance creation and queries.
    """
    AI_MODELS = config('AI_MODELS').split(',')
    MAX_ONE_TIME_GENERATION = int(config('MAX_ONE_TIME_GENERATION', 1000))

    def __init__(self):
        self.llm_repository = LLMRepository()

    def log_performance(self, performance: LLMPerformance):
        """
        Log LLM performance in the data
        :param performance:
        :return:
        """
        llm = self.llm_repository.find_by_name(performance.llm)
        if not llm:
            llm = LLMModel(name=performance.llm.name, description=performance.llm.name)
            self.llm_repository.create(llm)

        self.llm_repository.save_performance(performance)

    @staticmethod
    @shared_task
    def generate_performance_metrics():
        """
        Generates x LLM performance metrics and logs them.
        """

        for _ in range(LLMPerformanceService.MAX_ONE_TIME_GENERATION):
            for model_name in LLMPerformanceService.AI_MODELS:
                metric_simulator = LLMMetricSimulator(model_name=model_name)
                performance = metric_simulator.generate_performance_metrics()
                LLMPerformanceService().log_performance(performance)


class LLMPerformanceRankingService:
    """
    Service to fetch and rank LLMs based on their performance metrics.
    """
    MEAN_TTFT = 'mean_ttft'
    MEAN_TPS = 'mean_tps'
    MEAN_E2E_LATENCY = 'mean_e2e_latency'
    MEAN_RPS = 'mean_rps'

    VALIDATED_METRICS = [MEAN_TTFT, MEAN_TPS, MEAN_E2E_LATENCY, MEAN_RPS]

    def __init__(self):
        self.llm_repository = LLMRepository()

    def fetch_and_rank_llms(self, rank_by='mean_ttft'):
        """
        Fetch simulation results and rank LLMs based on their mean performance metrics.

        :param rank_by: The metric to rank LLMs by. Options include 'mean_ttft', 'mean_tps', 'mean_e2e_latency', 'mean_rps'.
        :return: A list of LLMs ranked by the specified metric.
        """
        # Validate rank_by parameter
        if rank_by not in self.VALIDATED_METRICS:
            raise ValueError(f"Invalid rank_by value. Must be one of {self.VALIDATED_METRICS}.")

        # Fetch aggregated data from repository
        aggregated_data = self.llm_repository.get_aggregated_performance_data(rank_by=rank_by)

        return aggregated_data