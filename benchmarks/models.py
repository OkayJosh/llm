"""
The LLM models:
This is Specific to django
"""
from django.db import models
from django_extensions.db.models import TimeStampedModel


class LLMModel(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class LLMPerformance(TimeStampedModel):
    llm = models.ForeignKey(LLMModel, on_delete=models.CASCADE)
    time_to_first_token = models.FloatField()
    tokens_per_second = models.FloatField()
    e2e_latency = models.FloatField()
    requests_per_second = models.FloatField()
    tokens_generated = models.IntegerField()

    def __str__(self):
        return f"Performance for {self.llm.name}"
