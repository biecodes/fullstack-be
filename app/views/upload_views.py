import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    try:
        uploaded_files = []

        for file in files:
            ext = os.path.splitext(file.filename)[1]
            filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}{ext}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            # Simpan file
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            uploaded_files.append(f"/{UPLOAD_DIR}/{filename}")

        return JSONResponse(content={"images": uploaded_files})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/upload-images/single")
async def upload_image(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[1]
        filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Simpan file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Return hasil upload
        return JSONResponse(content={"image": f"/{UPLOAD_DIR}/{filename}"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
