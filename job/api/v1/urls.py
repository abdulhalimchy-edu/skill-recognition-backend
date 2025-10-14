from django.urls import path

from job.api.v1.views import (
    SkillListAPIView, SkillExtractAPIView, SkillExtractionInfoRetrieveAPIView, SkillExtractionRunpodNotificationAPIView,
    MatchJobAPIView
)

urlpatterns = [
    path("skills/", SkillListAPIView.as_view(), name="skill-list"),
    path("skills/extract/", SkillExtractAPIView.as_view(), name="skill-extract"),
    path("skills/extraction-infos/<int:pk>/", SkillExtractionInfoRetrieveAPIView.as_view(), name="skill-extract-infos"),
    path("skills/extraction-runpod-notification/", SkillExtractionRunpodNotificationAPIView.as_view(),
         name="runpod-notification"),
    path("skills/match-jobs/", MatchJobAPIView.as_view(), name="match-jobs")
]
