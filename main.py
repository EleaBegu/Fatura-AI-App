
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# Krijimi i aplikacionit
app = FastAPI(
    title="FaturaAI",
    version="0.1.0",
    description="Sistem inteligjent per leximin e porosive dhe gjenerimin e faturave."
)


# Percaktimi i folderave
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Lidhja e CSS dhe skedareve statike
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# Faqja kryesore
@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


# Kontrolli i funksionimit te serverit
@app.get("/api/status")
def status():
    return {
        "sistemi": "FaturaAI",
        "statusi": "aktiv",
        "mesazhi": "Serveri funksionon me sukses."
    }


# Ngarkimi i fotografise se porosise
@app.post("/ngarko-porosine")
async def ngarko_porosine(foto: UploadFile = File(...)):

    # Kontrollo nese eshte zgjedhur nje fotografi
    if not foto.filename:
        raise HTTPException(
            status_code=400,
            detail="Ju lutem zgjidhni nje fotografi."
        )

    # Kontrollo formatin e fotografise
    formatet_lejuara = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp"
    }

    if foto.content_type not in formatet_lejuara:
        raise HTTPException(
            status_code=400,
            detail="Lejohen vetem fotografite JPG, PNG ose WEBP."
        )

    # Lexo fotografine
    permbajtja = await foto.read()

    if not permbajtja:
        raise HTTPException(
            status_code=400,
            detail="Fotografia eshte bosh."
        )

    # Kufiri maksimal: 10 MB
    madhesia_maksimale = 10 * 1024 * 1024

    if len(permbajtja) > madhesia_maksimale:
        raise HTTPException(
            status_code=413,
            detail="Fotografia nuk duhet te jete me e madhe se 10 MB."
        )

    # Krijo emer unik per fotografine
    prapashtesa = formatet_lejuara[foto.content_type]
    emri_skedarit = f"{uuid4().hex}{prapashtesa}"

    # Ruaje fotografine ne folderin uploads
    rruga = UPLOAD_DIR / emri_skedarit
    rruga.write_bytes(permbajtja)

    return {
        "mesazhi": "Fotografia e porosise u ngarkua me sukses!",
        "skedari": emri_skedarit
    }
