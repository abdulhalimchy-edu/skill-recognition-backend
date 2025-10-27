from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from job.api.v1.serializers import SkillSerializer, SkillExtractSerializer, SkillExtractionInfoSerializer, \
    SkillExtractionRunpodNotificationSerializer, JobSearchSerializer
from job.models import Skill, SkillExtractionInfo
from job.utils import run_skill_extraction, scrape_indeed_jobs


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


class MatchJobAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = JobSearchSerializer

    def post(self, request):
        serializer = JobSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data
        validated_data = serializer.validated_data
        query = validated_data['query']
        location = validated_data.get('location', 'Europe')
        max_rows = validated_data.get('max_rows', 10)
        job_type = validated_data.get('job_type', 'fulltime')
        radius = validated_data.get('radius', 50)
        sort = validated_data.get('sort', 'relevance')
        from_days = validated_data.get('from_days', 7)

        try:
            # Call the utility function to get jobs
            job_lists = scrape_indeed_jobs(
                query=query,
                location=location,
                max_rows=max_rows,
                job_type=job_type,
                radius=radius,
                sort=sort,
                from_days=from_days
            )

            return Response(data=job_lists, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'error': 'Failed to fetch job listings',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
