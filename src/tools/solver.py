import sys
import io
import os
import traceback
from typing import Dict, Any
from ..agent.state import AgentMathState

def execute_math_code(code_string: str) -> Dict[str, Any]:
    stdout_buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_buffer
    
    error_message = None
    local_env = {}
    
    try:
        exec(code_string, globals(), local_env)
    except Exception as e:
        error_message = traceback.format_exc()
    finally:
        sys.stdout = old_stdout
        
    return {
        "output": stdout_buffer.getvalue(),
        "error": error_message
    }

def execute_math_tools(state: AgentMathState):
    print("🏃 Sandbox mengeksekusi kode matematika dari agen...")
    
    code = state.get("generated_code")
    
    if not code:
        return {
            "error_log": "Error: No Python code block found in your response. Please provide a ```python block."
        }
        
    result = execute_math_code(code)
    
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
        return {
            "error_log": None,
            "graph_path": graph_found
        }