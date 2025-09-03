import os
import yt_dlp
import instaloader
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pathlib import Path
import shutil
# Download

def download_reel_with_insta(reel_url: str) -> str:
    if not reel_url or not isinstance(reel_url, str):
        print("Geçerli bir URL giriniz!")
        return

    loader = instaloader.Instaloader()

    # media klasörünü oluştur
    MEDIA_DIR = Path.cwd() / "media"
    os.makedirs(MEDIA_DIR, exist_ok=True)

    # videos klasörünü oluştur
    VIDEOS_DIR = Path.cwd() / "videos"
    os.makedirs(VIDEOS_DIR, exist_ok=True)

    try:    

        # Reel kodunu URL'den al
        reel_code = reel_url.strip('/').split('/')[-1]
        post = instaloader.Post.from_shortcode(loader.context, reel_code)


        loader.download_post(post, target=MEDIA_DIR)  # -> media/<shortcode>/

        print(f"{reel_url} başarıyla '{MEDIA_DIR/reel_code}' klasörüne indirildi!")

        # txt dosyasını oku
        txt_files = list(MEDIA_DIR.glob("*.txt"))
        txt_content = ""
        if txt_files:
            txt_path = txt_files[0]  # ilk txt dosyasını alıyoruz
            with open(txt_path, "r", encoding="utf-8") as f:
                txt_content = f.read()  # içerik txt_content değişkenine atandı

        # mp4 dosyasını bul
        mp4_files = list(MEDIA_DIR.glob("*.mp4"))
        if mp4_files and txt_content:
            old_mp4_path = mp4_files[0]
            # Geçerli işletim sistemi dosya adlarına uygun hale getir
            safe_name = "".join(c for c in txt_content if c.isalnum() or c in " _-")
            new_mp4_path = MEDIA_DIR / f"{safe_name}.mp4"
            old_mp4_path.rename(new_mp4_path)
            print(f"MP4 dosyası yeniden adlandırıldı: {new_mp4_path.name}")

        # mp4 dışındaki tüm dosyaları sil
        for file in MEDIA_DIR.iterdir():
            if file.suffix != ".mp4":
                file.unlink()

        # mp4 dosyasını media'dan videos'a taşı
        mp4_files = list(MEDIA_DIR.glob("*.mp4"))
        if mp4_files:
            mp4_path = mp4_files[0]
            dest_path = VIDEOS_DIR / mp4_path.name
            shutil.move(str(mp4_path), str(dest_path))
            return dest_path  # <- dosya yolunu döndür


    except Exception as e:
        print(f"{reel_url} indirilemedi. Hata: {e}")


def download_video_with_youtube(url: str) -> str:
    # Script hangi klasördeyse orada "videos/" klasörü oluştur
    DOWNLOAD_DIR = os.path.join(os.getcwd(), "videos")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    ydl_opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),  # Kaydetme formatı
        "format": "bestvideo+bestaudio/best",  # En iyi kalite (video+ses)
        "merge_output_format": "mp4"           # Ses + video birleşip mp4 olur
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        file_path = ydl.prepare_filename(info_dict)      # Tam dosya yolu
        print(f"ydl path: {file_path}")
        return file_path  # <- dosya yolunu döndür
        
# UPLOAD

# --- Ayarlar ---
VIDEO_DIR = "videos"                 # Normal videoların klasörü
CLIENT_SECRET_FILE = "client.json"  # Google API'den indirdiğin dosya
SCOPES = ["https://www.googleapis.com/auth/youtube"]

def get_authenticated_service():
    """Google hesabıyla yetkilendirme yapar ve YouTube servisini döndürür."""
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        # refresh_token alabilmek için offline erişim istiyoruz
        creds = flow.run_local_server(
            port=8080,
            access_type='offline',
        )
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def upload_short(
    youtube,
    file_path: str,
    title: str,
    description="#short #komedi #eğlence",
    tags=None,
    category_id="23",
    privacy="public"
):
    """Belirtilen tek Shorts videosunu YouTube'a yükler."""

    if file_path == "":
        print("Dosya yolu boş geldi")
        return

    if not os.path.exists(file_path):
        print(f"⚠ Dosya bulunamadı: {file_path}")
        return

    filename = os.path.basename(file_path)

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or ["shorts"],
            "categoryId": category_id,
            "defaultLanguage": "tr",
            "defaultAudioLanguage": "tr"
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
            "embeddable": True,
        }
    }

    print(f"▶ Yükleniyor (short): {filename}...")
    media_file = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )
    response = request.execute()
    print(f"✅ Yüklendi: {title} | Video ID: {response['id']}")

