# src/agent/graph.py
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq  # Integrasi Groq Gratis & Kilat
from langchain_core.messages import SystemMessage, HumanMessage
from .state import AgentMathState
from .prompts import SYSTEM_MATH_PROMPT
from ..tools.solver import execute_math_tools  # Sinkron dengan fungsi di solver.py

# 1. Inisialisasi Otak Llama 3.1 8B via Groq
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# 2. Node 1: Tempat Agen Merancang Solusi & Menulis Kode Python
def planner_node(state: AgentMathState):
    print("🤖 Agen sedang menganalisis soal dan menyusun formula...")
    
    # Ambil instruksi utama dari file prompts.py
    messages = [SystemMessage(content=SYSTEM_MATH_PROMPT)]
    
    # Jalur Koreksi: Jika eksekusi sebelumnya error, masukkan log error ke konteks berpikir AI
    if state.get('error_log'):
        context_msg = f"Your previous code failed with this error:\n{state['error_log']}\nPlease fix it and write a better code."
        messages.append(HumanMessage(content=context_msg))
    else:
        # Jalur Normal: Masukkan soal matematika dari user
        messages.append(HumanMessage(content=state['problem']))
        
    response = llm.invoke(messages)
    
    # Ekstrak blok kode python dari jawaban markdown teks LLM
    content = response.content
    code = None
    
    # KUNCI PERBAIKAN: Ditulis dalam satu baris horizontal lurus tanpa enter terputus
    if "```python" in content:
        code = content.split("```python")[1].split("```")[0].strip()
        
    return {
        "messages": state.get('messages', []) + [response],
        "generated_code": code,
        "retry_count": state.get('retry_count', 0) + 1
    }

# 3. Node 2: Router Kondisional (Logika Pengatur Alur Kerja Agen)
def router_conditional(state: AgentMathState):
    # Jika LLM tidak memberikan instruksi berupa kode Python sama sekali
    if not state.get('generated_code'):
        return "complete_response"
        
    # Putaran Pertama: Jika kode baru dibuat dan belum pernah diuji coba ke sandbox
    if state.get('error_log') is None and state.get('retry_count', 0) == 1:
        return "execute_math_tools"
        
    # Putaran Remidi: Jika kode error dan jumlah percobaan belum melewati batas (maksimal 3 kali)
    if state.get('error_log') and state.get('retry_count', 0) < 4:
        print(f"⚠️ Terjadi error internal! Agen mendesain ulang kode (Remidi ke-{state['retry_count']-1})")
        return "write_code_again"
        
    # Jalur Selesai: Jika kode sukses tanpa error, atau kesempatan remidi sudah habis
    return "complete_response"

# 4. Membangun Struktur Alur (Graph)
workflow = StateGraph(AgentMathState)

# Daftarkan node-node kerja
workflow.add_node("planner", planner_node)
workflow.add_node("execute_math_tools", execute_math_tools)

# Tentukan gerbang masuk awal agen
workflow.set_entry_point("planner")

# Hubungkan node alat kembali ke planner setelah selesai dieksekusi
workflow.add_edge("execute_math_tools", "planner")

# Daftarkan logika percabangan kondisional
workflow.add_conditional_edges(
    "planner",
    router_conditional,
    {
        "execute_math_tools": "execute_math_tools", 
        "write_code_again": "planner",              
        "complete_response": END                    
    }
)

math_agent = workflow.compile()
print("✅ Otak Alur Berpikir & Alat Sandbox Berhasil Terhubung Sempurna!")