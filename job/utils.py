import requests
from django.conf import settings

from job.models import SkillExtractionInfo


def run_skill_extraction(skill_extraction_info: SkillExtractionInfo):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.RUNPOD_API_ACCESS_KEY}'
    }

    data = {
        "input": {
            "task_id": skill_extraction_info.id,
            "sentence": skill_extraction_info.job_description,
            "notification_url": "http://167.71.47.244/job/v1/skills/extraction-runpod-notification/"
        }
    }

    response = requests.post(settings.RUNPOD_API_ENDPOINT, headers=headers, json=data)

    print(response.json())
