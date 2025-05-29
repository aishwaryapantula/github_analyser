import os
import requests
import json
import boto3
from datetime import datetime

def main():
    GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not all([GITHUB_USERNAME, BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY]):
        print("Error: Missing one or more required environment variables.")
        return

    FILE_NAME = f"github_profile_report_{GITHUB_USERNAME}.json"

    # Fetch GitHub repos
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch GitHub data: {response.status_code}")
        return

    repos = response.json()

    # Analyze data
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
    languages = {}
    for repo in repos:
        lang = repo.get('language')
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    summary = {
        "username": GITHUB_USERNAME,
        "total_repos": len(repos),
        "total_stars": total_stars,
        "top_languages": sorted(languages.items(), key=lambda x: x[1], reverse=True),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    # Save JSON report locally
    with open(FILE_NAME, 'w') as f:
        json.dump(summary, f, indent=4)

    print(f"Report created: {FILE_NAME}")

    # Upload to S3
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY)

    try:
        s3.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
        print(f"File uploaded to S3 bucket '{BUCKET_NAME}' as '{FILE_NAME}'")
    except Exception as e:
        print(f"Failed to upload to S3: {e}")

if __name__ == "__main__":
    main()
