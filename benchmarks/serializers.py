"""
Benchmarks Serializers
"""
from rest_framework import serializers

class LLMPerformanceRankingSerializer(serializers.Serializer):
    RANK_BY = ['mean_ttft', 'mean_tps', 'mean_e2e_latency', 'mean_rps']
    rank_by = serializers.ChoiceField(
        choices=RANK_BY,
        default='mean_ttft'
    )

    def validate_rank_by(self, value):
        if value not in self.RANK_BY:
            raise serializers.ValidationError(f"Invalid rank_by value. Must be one of {self.RANK_BY}.")
        return value
