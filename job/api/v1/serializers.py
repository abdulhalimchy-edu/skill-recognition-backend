from rest_framework import serializers
from job.models import Skill, SkillExtractionInfo


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class SkillExtractionInfoSerializer(serializers.ModelSerializer):
    extracted_skills = SkillSerializer(many=True, read_only=True)

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
