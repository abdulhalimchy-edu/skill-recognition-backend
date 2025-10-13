from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from job.api.v1.serializers import SkillSerializer, SkillExtractSerializer, SkillExtractionInfoSerializer, \
    SkillExtractionRunpodNotificationSerializer
from job.models import Skill, SkillExtractionInfo
from job.utils import run_skill_extraction


class SkillListAPIView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = None


class SkillExtractAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = SkillExtractSerializer

    def post(self, request):
        serializer = SkillExtractSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        skill_extraction_info = SkillExtractionInfo.objects.create(
            job_description=serializer.validated_data.get('job_description'),
            processing_status=SkillExtractionInfo.ProcessingStatus.IN_PROGRESS
        )

        # TODO: Extract asynchronously
        run_skill_extraction(skill_extraction_info)

        return Response(SkillExtractionInfoSerializer(skill_extraction_info).data, status=status.HTTP_201_CREATED)


class SkillExtractionInfoRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = SkillExtractionInfoSerializer
    queryset = SkillExtractionInfo.objects.all()


class SkillExtractionRunpodNotificationAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = SkillExtractionRunpodNotificationSerializer

    def post(self, request):
        serializer = SkillExtractionRunpodNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if validated_data["processing_status"] == "COMPLETED":
            skill_extraction_info = SkillExtractionInfo.objects.get(pk=validated_data['task_id'])
            skill_extraction_info.processing_status = SkillExtractionInfo.ProcessingStatus.COMPLETED
            skill_extraction_info.processing_done_at = timezone.now()
            skills_objects_list = [Skill.get_skill(e_skill) for e_skill in validated_data["extracted_skills"]]

            # ✅ Add all related skills to the ManyToMany field
            skill_extraction_info.extracted_skills.add(*skills_objects_list)
            skill_extraction_info.save()

        else:  # FAILED
            skill_extraction_info = SkillExtractionInfo.objects.get(pk=validated_data['task_id'])
            skill_extraction_info.processing_status = SkillExtractionInfo.ProcessingStatus.FAILED
            skill_extraction_info.save()

        return Response("Okay", status=status.HTTP_200_OK)
