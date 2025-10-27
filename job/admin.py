from django.contrib import admin

from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")


from django.contrib import admin
from .models import SkillExtractionInfo


@admin.register(SkillExtractionInfo)
class SkillExtractionInfoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "processing_status",
        "processing_time_seconds",
        "created_at",
        "updated_at",
    )
    list_filter = ("processing_status",)
    filter_horizontal = ("extracted_skills",)

    @admin.display(description="Processing Time")
    def processing_time_seconds(self, obj):
        if obj.processing_status == SkillExtractionInfo.ProcessingStatus.COMPLETED:
            delta = obj.processing_done_at - obj.created_at
            return f"{int(delta.total_seconds())}s"
        return "-"
