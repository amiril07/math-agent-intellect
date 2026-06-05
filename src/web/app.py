import os
import cv2
import easyocr
import numpy as np
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .. import config
from ..agent.graph import math_agent

app = FastAPI(title="Math Agent Intellect")

print("📸 Menginisialisasi modul EasyOCR...")
ocr_reader = easyocr.Reader(['id', 'en'])

os.makedirs("src/web/static/exports", exist_ok=True)

app.mount("/static", StaticFiles(directory="src/web/static"), name="static")
templates = Jinja2Templates(directory="src/web/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {"request": request}
    )

@app.post("/solve")
async def solve_math(
    problem: str = Form(None),
    image: UploadFile = File(None)
):
    
    final_problem = problem if problem else ""
    
    old_graph = "src/web/static/exports/output.png"
    if os.path.exists(old_graph):
        os.remove(old_graph)
        
    try:
        if image is not None:
            print(f"📸 Menerima file gambar baru: {image.filename}")
            
            contents = await image.read()
            nparr = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is not None:
                ocr_results = ocr_reader.readtext(img, detail=0)
                extracted_text = " ".join(ocr_results).strip()
                
                print(f"🔍 Hasil OCR Gambar: '{extracted_text}'")
                
                if extracted_text:
                    final_problem = f"{final_problem} {extracted_text}".strip()
            else:
                print("❌ Gagal membaca atau mendecode file gambar yang diunggah.")

        if not final_problem.strip():
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Input kosong! Ketik soal Anda atau masukkan gambar soal yang jelas."}
            )
            
        print(f"📥 Mengeksekusi soal ke LangGraph: {final_problem}")
        
        inputs = {"problem": final_problem}
        config_run = {"recursion_limit": 20}
        
        result = await math_agent.ainvoke(inputs, config=config_run)
        
        final_message = result["messages"][-1].content
        
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