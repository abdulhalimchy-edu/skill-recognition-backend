from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Skill(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        default="",
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated At"),
        auto_now=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

    def __str__(self):
        return self.name

    @staticmethod
    def get_skill(name):
        skill = Skill.objects.filter(name__iexact=name).first()
        if skill:
            return skill
        return Skill.objects.create(name=name)


class SkillExtractionInfo(models.Model):
    class ProcessingStatus(models.IntegerChoices):
        PENDING = 0, _("Pending")
        IN_PROGRESS = 1, _("In Progress")
        COMPLETED = 2, _("Completed")
        FAILED = 3, _("Failed")

    job_description = models.TextField(
        verbose_name=_("Job Description")
    )
    extracted_skills = models.ManyToManyField(
        "job.Skill",
        verbose_name=_("Extracted Skills"),
        blank=True,
        related_name="extraction_infos"
    )
    processing_status = models.IntegerField(
        verbose_name=_("Processing Status"),
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.PENDING
    )
    processing_done_at = models.DateTimeField(
        verbose_name=_("Processing Done At"),
        default=timezone.now
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated At"),
        auto_now=True
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Skill Extraction Info")
        verbose_name_plural = _("Skill Extraction Infos")


"""

class Job(models.Model):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=300,
        blank=True
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    required_skills = models.ManyToManyField(
        verbose_name=_("Required Skills"),
        to="job.Skill",
        blank=True,
        related_name='jobs'
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated At"),
        auto_now=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")


    def __str__(self):
        return self.title

"""
