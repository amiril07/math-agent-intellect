# src/config.py
import os
from dotenv import load_dotenv

# Otomatis mencari dan membaca file .env di root folder
load_dotenv()

# Pastikan API Key Groq sudah terpasang di sistem environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("⚠️ Peringatan: GROQ_API_KEY tidak ditemukan di file .env Anda!")