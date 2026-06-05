# src/web/app.py
import os
import cv2
import easyocr
import numpy as np
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import config untuk memastikan API Key terbaca, dan math_agent sebagai otaknya
from .. import config
from ..agent.graph import math_agent

app = FastAPI(title="Math Agent Intellect")

# Inisialisasi EasyOCR Reader untuk bahasa Indonesia ('id') dan Inggris ('en')
# Ini diletakkan di luar endpoint agar model OCR hanya di-load sekali saat server dinyalakan
print("📸 Menginisialisasi modul EasyOCR...")
ocr_reader = easyocr.Reader(['id', 'en'])

# Pastikan folder tempat ekspor grafik sudah dibuat agar tidak error saat menyimpan file
os.makedirs("src/web/static/exports", exist_ok=True)

# Daftarkan folder static untuk file gambar dan templates untuk file HTML
app.mount("/static", StaticFiles(directory="src/web/static"), name="static")
templates = Jinja2Templates(directory="src/web/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Menampilkan halaman utama aplikasi web"""
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {"request": request}
    )

@app.post("/solve")
async def solve_math(
    problem: str = Form(None),              # Mengubah parameter menjadi opsional jika user memakai gambar
    image: UploadFile = File(None)          # Menangkap payload berkas gambar dari frontend
):
    """Endpoint yang menerima soal matematika (teks dan/atau gambar) lalu mengeksekusinya via LangGraph"""
    
    final_problem = problem if problem else ""
    
    # 1. Hapus grafik lama di folder ekspor jika ada, supaya tidak tertukar dengan soal baru
    old_graph = "src/web/static/exports/output.png"
    if os.path.exists(old_graph):
        os.remove(old_graph)
        
    try:
        # 2. Pemrosesan OCR jika user mengunggah file gambar
        if image is not None:
            print(f"📸 Menerima file gambar baru: {image.filename}")
            
            # Baca data biner file biner langsung dari memory stream
            contents = await image.read()
            nparr = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is not None:
                # Ekstrak string teks matematika dari matriks gambar
                ocr_results = ocr_reader.readtext(img, detail=0)
                extracted_text = " ".join(ocr_results).strip()
                
                print(f"🔍 Hasil OCR Gambar: '{extracted_text}'")
                
                # Gabungkan hasil ekstraksi OCR ke variabel penampung soal utama
                if extracted_text:
                    final_problem = f"{final_problem} {extracted_text}".strip()
            else:
                print("❌ Gagal membaca atau mendecode file gambar yang diunggah.")

        # 3. Validasi Akhir: Pastikan ada teks soal yang siap dikirim ke LLM
        if not final_problem.strip():
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Input kosong! Ketik soal Anda atau masukkan gambar soal yang jelas."}
            )
            
        print(f"📥 Mengeksekusi soal ke LangGraph: {final_problem}")
        
        # 4. Jalankan agen LangGraph dengan input soal akhir
        inputs = {"problem": final_problem}
        config_run = {"recursion_limit": 20}
        
        result = await math_agent.ainvoke(inputs, config=config_run)
        
        # Ambil pesan terakhir dari hasil pengerjaan agen
        final_message = result["messages"][-1].content
        
        # Periksa apakah ada file grafik baru yang dihasilkan oleh tools plotter
        has_graph = os.path.exists(old_graph)
        
        return JSONResponse(content={
            "status": "success",
            "response": final_message,
            "has_graph": has_graph
        })
        
    except Exception as e:
        print(f"❌ Error saat mengeksekusi agen: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )