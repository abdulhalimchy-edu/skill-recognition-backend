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
            "notification_url": "https://skill-recog.mooo.com/job/v1/skills/extraction-runpod-notification/"
        }
    }

    response = requests.post(settings.RUNPOD_API_ENDPOINT, headers=headers, json=data)

    print(response.json())


def scrape_indeed_jobs(query, location="Europe", max_rows=10, job_type="fulltime", radius=50, sort="relevance",
                       from_days=7):
    url = "https://indeed-scraper-api.p.rapidapi.com/api/job"

    headers = {
        "X-RapidAPI-Key": settings.RAPID_API_KEY,
        "X-RapidAPI-Host": "indeed-scraper-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    payload = {
        "scraper": {
            "maxRows": max_rows,
            "query": query,
            "location": location,
            "jobType": job_type,
            "radius": str(radius),
            "sort": sort,
            "fromDays": str(from_days),
            # "country": country  # Provide Country code Alpha 2
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        job_data = response_data['returnvalue']['data']
        return job_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
