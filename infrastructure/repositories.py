"""
The LLM Repository Module:

Abstracting the persistence of generated performance metrics

"""
from django.db.models import Avg, Func, DecimalField

from benchmarks.models import LLMModel as LLMModelORM, LLMPerformance as LLMPerformanceORM
from core.models import LLMModel, LLMPerformance

# Utils
# Move this to it own directory when they are getting many

class Round(Func):
    """
    Custom round function to round numbers to a specified number of decimal places.
    """
    function = 'ROUND'
    template = '%(function)s(CAST(%(expressions)s AS NUMERIC), 2)'
    output_field = DecimalField()

# Service classes

class LLMRepository:
    """
    The LLM Repository Class
    """
    def __init__(self):
        self.orm = LLMModelORM.objects
        self.performance_orm = LLMPerformanceORM.objects

    def find_by_name(self, name):
        """
        Find LLM by name
        :param name:
        :return:
        """
        try:
            llm = self.orm.get(name=name)
            return LLMModel(name=llm.name, description=llm.description)
        except LLMModelORM.DoesNotExist:
            return None

    def create(self, llm: LLMModel):
        """
        Create LLM
        :param llm:
        :return:
        """
        self.orm.get_or_create(name=llm.name, description=llm.description)

    def save_performance(self, performance: LLMPerformance):
        """
        Save the performance metrics of the LLM to the database.
        :param performance:
        :return:
        """
        llm_orm, _ = self.orm.get_or_create(name=performance.llm.name)
        LLMPerformanceORM.objects.create(
            llm=llm_orm,
            time_to_first_token=performance.time_to_first_token,
            tokens_per_second=performance.tokens_per_second,
            e2e_latency=performance.e2e_latency,
            requests_per_second=performance.requests_per_second,
            tokens_generated=performance.tokens_generated
        )

    def get_aggregated_performance_data(self, rank_by):
        """
        Fetch aggregated performance data with mean values for each LLM.
        :return: QuerySet with aggregated performance metrics.
        """
        aggregated_data = (
            self.performance_orm
            .values('llm__name')
            .annotate(
                mean_ttft=Round(Avg('time_to_first_token')),
                mean_tps=Round(Avg('tokens_per_second')),
                mean_e2e_latency=Round(Avg('e2e_latency')),
                mean_rps=Round(Avg('requests_per_second'))
            )
            .order_by(rank_by)
        )
        # from django.db import connection
        print(aggregated_data.query)
        return aggregated_data

