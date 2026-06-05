from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class AgentMathState(TypedDict):
    # Menyimpan riwayat percakapan/pesan antara user dan AI
    messages: List[BaseMessage]
    # Soal matematika mentah dari user
    problem: str
    # Kode Python (SymPy/Matplotlib) yang ditulis oleh AI
    generated_code: Optional[str]
    # Log error jika kode yang dijalankan di sandbox mengalami crash
    error_log: Optional[str]
    # Path lokasi file gambar grafik jika ada grafik yang dibuat
    graph_path: Optional[str]
    # Berapa kali agen mencoba memperbaiki kodenya sendiri (mencegah loop tak terbatas)
    retry_count: int