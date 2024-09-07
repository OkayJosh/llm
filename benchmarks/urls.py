"""
Expose teh endpoints
"""
from django.urls import path
from .views import LLMPerformanceRankingView

urlpatterns = [
    path('v1/ranking/', LLMPerformanceRankingView.as_view(), name='llm-ranking'),
]
