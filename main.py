import uvicorn

if __name__ == "__main__":
    print("🚀 Menyalakan Server Math Agent Intellect...")
    print("🌍 Akses aplikasi di browser Anda melalui alamat: http://127.0.0.1:8000")
    
    uvicorn.run(
        "src.web.app:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )