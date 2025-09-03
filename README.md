# TEZEKSEL 🐮

A FastAPI-based application that allows you to:

- Download videos from **YouTube** and **Instagram Reels**
- Upload them directly as **YouTube Shorts** or **YouTube Videos**

## Installation & Run

```bash
# Clone the repository
git clone https://github.com/Nivtras/fastapi-youtube-shorts-uploader.git
cd fastapi-youtube-shorts-uploader

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment

# Linux / macOS
source .venv/bin/activate

# Windows (cmd)
# .venv\Scripts\activate

# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app:app --reload --port 8081
```

Once running:

- Swagger UI → http://localhost:8081/docs
- ReDoc → http://localhost:8081/redoc

## Example Usage

### Upload a Short

```http
POST /upload/short
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ" or "https://www.instagram.com/watch?v=dQw4w9WgXcQ",
  "title": "Funny Short",
  "description": "My short description",
  "tags": ["fun", "shorts"],
  "category_id": "23"
}
```

Response:

```json
{ "status": "Short uploaded" }
```

## Google API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **YouTube Data API v3**
3. Download the `client.json` file and place it in the project root
4. On the first run, you will be prompted to log in with your Google account
5. After authorization, a `token.pickle` file will be generated automatically

## Disclaimer

This project is for **educational purposes only**.  
Downloading and re-uploading content without permission may violate platform policies.  
Use responsibly ✅

## License

MIT
