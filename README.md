# 📊 GitHub Profile Analyzer

This project fetches public repository data from a specified GitHub user, analyzes key metrics (like stars and languages), generates a professional PDF report, and uploads the report to an AWS S3 bucket.

## 🚀 Features

- Fetches public repository data using the GitHub API
- Calculates total repositories, total stars, and top programming languages
- Generates a clean and concise PDF report
- Uploads the report to a specified AWS S3 bucket

---

## 🧰 Tech Stack

- Python
- GitHub API
- AWS S3 (via `boto3`)
- PDF generation using `fpdf`
