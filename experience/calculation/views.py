from rest_framework.generics import ListCreateAPIView
from calculation.models import Candidate
from calculation.serializers import CandidateSerializer
from rest_framework.response import Response


class CandidateList(ListCreateAPIView):
    queryset = Candidate.objects.all().order_by('-total_experience')
    serializer_class = CandidateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        result = {'candidates': serializer.data}
        return Response(result)
