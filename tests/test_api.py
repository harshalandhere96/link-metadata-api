
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.extractor import MetadataError

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_extract_metadata():
    html = """
    <html>
      <head>
        <title>Example Page</title>
        <meta name="description" content="A test page">
        <meta property="og:image" content="https://example.com/image.png">
        <meta property="og:site_name" content="Example">
      </head>
      <body></body>
    </html>
    """

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = html
    mock_response.headers = {"Content-Type": "text/html"}

    with patch(
        "app.extractor.validate_public_url",
        return_value="https://example.com/",
    ), patch(
        "app.extractor.requests.get",
        return_value=mock_response,
    ):
        response = client.post(
            "/extract",
            json={"url": "https://example.com/"},
        )

    assert response.status_code == 200
    assert response.json()["title"] == "Example Page"
    assert response.json()["description"] == "A test page"
    assert response.json()["site_name"] == "Example"


def test_invalid_url_scheme():
    response = client.post(
        "/extract",
        json={"url": "ftp://example.com/file"},
    )
    assert response.status_code == 400


def test_missing_url():
    response = client.post("/extract", json={})
    assert response.status_code == 422


def test_redirect_rejected():
    with patch(
        "app.extractor.validate_public_url",
        return_value="https://example.com/",
    ), patch(
        "app.extractor.requests.get",
    ) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 301
        mock_response.headers = {"Location": "https://other.example/"}
        mock_get.return_value = mock_response

        response = client.post(
            "/extract",
            json={"url": "https://example.com/"},
        )

    assert response.status_code == 400
    assert "redirect" in response.json()["detail"].lower()
