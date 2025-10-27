from rest_framework import serializers

from job.models import Skill, SkillExtractionInfo


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class SkillExtractionInfoSerializer(serializers.ModelSerializer):
    extracted_skills = serializers.SerializerMethodField()
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

    def get_extracted_skills(self, obj):
        # Return a list of skill names
        return [skill.name for skill in obj.extracted_skills.all()]


class SkillExtractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillExtractionInfo
        fields = ['job_description']
        required_fields = ['job_description']


class SkillExtractionRunpodNotificationSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(required=True)
    extracted_skills = serializers.ListField(
        child=serializers.CharField(allow_blank=True), required=False
    )
    processing_status = serializers.CharField(required=True)


class JobSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=100)
    location = serializers.CharField(required=False, max_length=100, default="San Francisco")
    max_rows = serializers.IntegerField(required=False, default=15, min_value=1, max_value=50)
    job_type = serializers.CharField(required=False, default="fulltime")
    radius = serializers.IntegerField(required=False, default=50)
    sort = serializers.CharField(required=False, default="relevance")
    from_days = serializers.IntegerField(required=False, default=7)