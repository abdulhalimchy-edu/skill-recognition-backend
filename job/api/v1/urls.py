from django.urls import path

from job.api.v1.views import SkillListAPIView

urlpatterns = [
    path("skills/", SkillListAPIView.as_view(), name="skill-list"),
]
