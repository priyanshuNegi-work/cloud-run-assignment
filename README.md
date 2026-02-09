# Cloud Run Assignment
**Author:** Priyanshu Negi
**Date:** February 2026

## Project Overview
This repository contains the solution for **Assignment 2: Cloud Deployment**.
It demonstrates how to containerize a Python Flask application and deploy it to **Google Cloud Run** using a serverless architecture.

## Project Structure
* **`deploy_app/`**: The main application folder.
    * `main.py`: A simple Flask web server.
    * `Dockerfile`: Configuration for packaging the app into a container.
    * `requirements.txt`: List of Python dependencies (Flask, Gunicorn).
* **`sys_check.sh`**: A Bash script for automating system health checks (Disk usage, Login history).

## How It Works
1.  **Containerization:** The app is packaged using Docker.
2.  **Registry:** The container image is stored in Google Artifact Registry.
3.  **Deployment:** The service is deployed to Cloud Run (fully managed).

## Live Demo
You can view the running application here:
[Paste your https://hello-priyanshu... link here]

## Deployment Command
For reference, the app was deployed using:
```bash
gcloud run deploy hello-priyanshu \
    --image us-central1-docker.pkg.dev/[PROJECT_ID]/assignment-repo/hello-cloud-run \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated

