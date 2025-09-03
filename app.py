from fastapi import FastAPI
from api import (
    download_reel_with_insta,
    download_video_with_youtube,
    upload_short,
    get_authenticated_service
)

from model import (
    Request,
)

app = FastAPI()
youtube_service = get_authenticated_service()

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.post("/upload/short")
def upload_short_api(request: Request):
    
    domain = request.url.split("/")[2].split(".")[1]
    file_path=""

    if domain == "youtube":
        file_path = download_video_with_youtube(request.url)
    elif domain == "instagram":
        file_path = download_reel_with_insta(request.url)

    print(file_path)
    upload_short(youtube_service, file_path, request.title, request.description, request.tags, request.category_id, privacy="public")
    return {"status": "Short yüklendi"}