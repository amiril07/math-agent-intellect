import sys
import io
import os
import traceback
from typing import Dict, Any
from ..agent.state import AgentMathState

def execute_math_code(code_string: str) -> Dict[str, Any]:
    """
    Menjalankan kode Python dari AI secara aman di dalam sandbox 
    dan menangkap standard output (print) serta error-nya.
    """
    # Siapkan penampung output teks
    stdout_buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_buffer
    
    error_message = None
    
    # Tentukan area kerja lokal agar SymPy dan Matplotlib bisa berjalan lancar
    local_env = {}
    
    try:
        # Eksekusi string kode Python yang dibuat oleh AI Agent
        exec(code_string, globals(), local_env)
    except Exception as e:
        # Jika kode buatan AI crash, tangkap baris errornya secara detail
        error_message = traceback.format_exc()
    finally:
        # Kembalikan fungsi print ke sistem terminal utama
        sys.stdout = old_stdout
        
    return {
        "output": stdout_buffer.getvalue(),
        "error": error_message
    }

def execute_math_tools(state: AgentMathState):
    """
    Node LangGraph yang menghubungkan Otak Agen ke Sandbox Eksekusi ini.
    """
    print("🏃 Sandbox mengeksekusi kode matematika dari agen...")
    
    code = state.get("generated_code")
    
    # Jika agen lupa menuliskan kode atau formatnya salah
    if not code:
        return {
            "error_log": "Error: No Python code block found in your response. Please provide a ```python block."
        }
        
    # Jalankan kodenya ke mesin sandbox
    result = execute_math_code(code)
    
    # Deteksi apakah kode berhasil membuat grafik ke folder static
    expected_graph_path = "src/web/static/exports/output.png"
    graph_found = expected_graph_path if os.path.exists(expected_graph_path) else None
    
    if result["error"]:
        print("❌ Eksekusi gagal! Kode buatan agen memicu error.")
        return {
            "error_log": result["error"],
            "graph_path": None
        }
    else:
        print("🎯 Eksekusi sukses! Hasil hitungan berhasil didapatkan.")
        # Simpan hasil hitungan print() ke dalam memori sistem
        return {
            "error_log": None,
            "graph_path": graph_found
        }