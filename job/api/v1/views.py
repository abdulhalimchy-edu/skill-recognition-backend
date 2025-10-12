from rest_framework import generics

from job.api.v1.serializers import SkillSerializer
from job.models import Skill


class SkillListAPIView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = None
