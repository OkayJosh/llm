"""
Benchmark views module
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from application.llm_service import LLMPerformanceRankingService
from benchmarks.serializers import LLMPerformanceRankingSerializer


class LLMPerformanceRankingView(APIView):
    """
    API view to fetch and rank LLMs based on a given performance metric.
    """
    @swagger_auto_schema(
        query_serializer=LLMPerformanceRankingSerializer,
        responses={
            200: 'Successful response with a list of ranked LLMs.',
            400: 'Bad request with validation errors.'
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Get Endpoint
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = LLMPerformanceRankingSerializer(data=request.query_params)
        if serializer.is_valid():
            rank_by = serializer.validated_data['rank_by']
            ranking_service = LLMPerformanceRankingService()

            try:
                ranked_llms = ranking_service.fetch_and_rank_llms(rank_by=rank_by)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(ranked_llms, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)