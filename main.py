import json
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from ai_service import analyze_syllabus
from pdf_service import extract_text_from_pdf
from youtube_service import search_youtube_playlist
from image_service import extract_text_from_image


app = FastAPI()

# -------------------------------
# CORS (OK for now)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for now, can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# STATIC FILES (FRONTEND)
# -------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------------------
# FRONTEND ENTRY POINT
# -------------------------------
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


# -------------------------------
# HELPER: ATTACH YT PLAYLISTS
# -------------------------------
def attach_playlists(data: dict):
    for unit in data.get("units", []):
        for level in ["very_important", "important"]:
            new_list = []

            for topic in unit.get(level, []):
                query = f"{topic} full course playlist"
                playlist = search_youtube_playlist(query)

                new_list.append({
                    "topic": topic,
                    "playlist": playlist
                })

            unit[level] = new_list

    return data


# -------------------------------
# ANALYZE TEXT
# -------------------------------
@app.post("/analyze-text")
async def analyze_text(
    text: str = Form(...),
    include_playlists: bool = Form(True)
):
    raw = analyze_syllabus(text)
    data = json.loads(raw)

    if include_playlists:
        data = attach_playlists(data)

    return data


# -------------------------------
# ANALYZE PDF
# -------------------------------
@app.post("/analyze-pdf")
async def analyze_pdf(
    pdf: UploadFile = File(...),
    include_playlists: bool = Form(True)
):
    text = extract_text_from_pdf(pdf.file)
    raw = analyze_syllabus(text)
    data = json.loads(raw)

    if include_playlists:
        data = attach_playlists(data)

    return data


# -------------------------------
# ANALYZE IMAGE
# -------------------------------
@app.post("/analyze-image")
async def analyze_image(
    image: UploadFile = File(...),
    include_playlists: bool = Form(True)
):
    text = extract_text_from_image(image.file)
    raw = analyze_syllabus(text)
    data = json.loads(raw)

    if include_playlists:
        data = attach_playlists(data)

    return data
