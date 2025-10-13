from rest_framework import serializers
from job.models import Skill, SkillExtractionInfo


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class SkillExtractionInfoSerializer(serializers.ModelSerializer):
    extracted_skills = SkillSerializer(many=True, read_only=True)
    processing_status = serializers.ReadOnlyField(source="get_processing_status_display")

    class Meta:
        model = SkillExtractionInfo
        fields = [
            "id",
            "job_description",
            "extracted_skills",
            "processing_status",
            "processing_done_at",
            "created_at",
            "updated_at",
        ]


class SkillExtractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillExtractionInfo
        fields = ['job_description']
        required_fields = ['job_description']


class SkillExtractionRunpodNotificationSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(required=True)
    extracted_skills = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    processing_status = serializers.CharField(required=True)
