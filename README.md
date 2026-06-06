# Math Agent Intellect

Math Agent Intellect is an autonomous AI agent platform designed to solve advanced mathematical problems through step-by-step reasoning. By combining visual processing (OCR), symbolic computing, and agent logic, the system provides solutions that are not only accurate but also academically understandable.

---

## 📌 Introduction
Solving complex mathematical problems automatically requires more than just a Large Language Model (LLM); it requires the ability to compute precisely and verify logical steps. This project provides an end-to-end implementation that combines linguistic intelligence with a symbolic computation engine to ensure the mathematical correctness of every answer.
---

## 🧠 Model Architecture & Mechanism

Proyek ini tidak mengandalkan tebakan LLM murni, melainkan menerapkan alur kerja Agentic Workflow di mana model bahasa bertindak sebagai pengatur (orchestrator) yang memanggil alat bantu (tools) khusus untuk tugas tertentu.Alur pemrosesan data mengikuti struktur sebagai berikut:1. Vision & PreprocessingInput: Gambar soal matematika yang diunggah pengguna.OCR Engine: Menggunakan EasyOCR untuk melakukan pengenalan karakter optik, mengubah piksel menjadi teks matematis yang dapat diproses:$$\text{Image} \to \text{Text} \to \text{LaTeX Parse}$$2. Intelligent Reasoning EngineLogic Planner: LangGraph mengelola state percakapan dan menentukan apakah soal memerlukan penyelesaian simbolik atau cukup dengan penalaran logis.Symbolic Solver: Saat perhitungan diperlukan, agen mengeksekusi kode Python secara aman di sandbox menggunakan SymPy:$$\int f(x) dx \xrightarrow{\text{SymPy}} \text{Symbolic Result}$$Constraint Solver: Untuk masalah logika atau sistem persamaan yang kompleks, agen menggunakan Z3-solver untuk mencari solusi yang memenuhi kendala yang diberikan.3. Output FormattingStructured Response: Agen menyusun langkah penyelesaian yang koheren.LaTeX Rendering: Semua simbol dan persamaan diformat agar dirender dengan cantik di browser menggunakan MathJax:$$f(x) = \sum_{n=1}^{\infty} \frac{x^n}{n^2} \implies \text{Professional Math Formatting}$$
---

## 🛠️ Tech Stack & Dependencies
* **Core AI Framework:** LangGraph, LangChain, Groq API (LLM)
* **Web Framework:** FastAPI (Python backend)
* **Math Engines:** SymPy (Simbolik), Z3-solver (Logika), NumPy/SciPy (Numerik)
* **Computer Vision:** EasyOCR, PyTorch
* **Frontend:** HTML5, Tailwind CSS, MathJax

---
