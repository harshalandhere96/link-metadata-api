# Link Metadata Extraction API

A Python-based REST API that extracts metadata from publicly accessible webpages, including the page title, description, preview image, and website name.

This project demonstrates DevOps practices through automated testing, Docker containerization, GitHub Actions CI/CD, and cloud deployment.

## Objectives

- Develop a REST API using FastAPI.
- Extract webpage metadata using Beautiful Soup.
- Implement automated tests using Pytest.
- Containerize the application using Docker.
- Automate testing and Docker image builds with GitHub Actions.
- Deploy the application to a cloud hosting platform.

## Technology Stack

- **Language:** Python
- **API Framework:** FastAPI
- **HTTP Requests:** Requests
- **HTML Parsing:** Beautiful Soup
- **Testing:** Pytest
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Cloud Deployment:** Render

## Project Structure

```text
link-metadata-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── extractor.py
├── tests/
│   └── test_api.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns the API welcome message |
| GET | `/health` | Checks API health |
| POST | `/extract` | Extracts metadata from a webpage |

## Example Request

Send a POST request to `/extract` with the following JSON body:

```json
{
  "url": "https://example.com/"
}
```

The API returns a JSON response containing the URL, title, description, image, and website name. Metadata availability depends on the target webpage.

## Local Setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Start the API

```powershell
python -m uvicorn app.main:app --reload
```

### 4. Open the API documentation

http://127.0.0.1:8000/docs

## Automated Testing

Run the test suite:

```powershell
python -m pytest -v
```

The tests cover API endpoints, metadata extraction, invalid URL schemes, missing inputs, and redirect handling.

## Docker

### Build the image

```powershell
docker build -t link-metadata-api:1.0 .
```

### Run the container

Port 8000 is used by another service on the development machine, so the example below exposes the API on host port 8001:

```powershell
docker run -d --name link-metadata-api -p 8001:8000 link-metadata-api:1.0
```

Open the containerized API:

http://localhost:8001/docs

### Useful Docker commands

```powershell
docker ps
docker logs link-metadata-api
docker stop link-metadata-api
docker rm link-metadata-api
```

## CI/CD Pipeline

GitHub Actions automates the following stages:

1. Checks out the source code.
2. Sets up Python and installs dependencies.
3. Runs automated tests.
4. Builds the Docker image after successful tests.
5. Triggers cloud deployment after successful checks, when the deployment job and required secret are configured.

The build and deployment jobs depend on successful tests, preventing those stages from running when the tests fail.

## Cloud Deployment

The application can be deployed to Render using the repository's Dockerfile.

After deployment, the API documentation is available at:

`https://your-service-name.onrender.com/docs`

Replace the example hostname with the actual URL assigned by Render.

## Security Considerations

- The API accepts HTTP and HTTPS URLs only.
- Local and non-public IP addresses are rejected during URL validation.
- Requests use a timeout and redirects are rejected.
- GitHub tokens, deployment hooks, and other secrets must not be committed to the repository.

The URL validation implemented in this project is a demonstration-level safeguard and is not a complete production-grade SSRF defense.

## Conclusion

This project demonstrates how application development can be combined with automated testing, containerization, continuous integration, and deployment to improve the consistency and reliability of software delivery.