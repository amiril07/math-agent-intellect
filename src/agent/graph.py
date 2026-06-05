from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from .state import AgentMathState
from .prompts import SYSTEM_MATH_PROMPT
from ..tools.solver import execute_math_tools

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

def planner_node(state: AgentMathState):
    print("🤖 Agen sedang menganalisis soal dan menyusun formula...")
    
    messages = [SystemMessage(content=SYSTEM_MATH_PROMPT)]
    
    if state.get('error_log'):
        context_msg = f"Your previous code failed with this error:\n{state['error_log']}\nPlease fix it and write a better code."
        messages.append(HumanMessage(content=context_msg))
    else:
        messages.append(HumanMessage(content=state['problem']))
        
    response = llm.invoke(messages)
    
    content = response.content
    code = None
    
    if "```python" in content:
        code = content.split("```python")[1].split("```")[0].strip()
        
    return {
        "messages": state.get('messages', []) + [response],
        "generated_code": code,
        "retry_count": state.get('retry_count', 0) + 1
    }

def router_conditional(state: AgentMathState):
    if not state.get('generated_code'):
        return "complete_response"
        
    if state.get('error_log') is None and state.get('retry_count', 0) == 1:
        return "execute_math_tools"
        
    if state.get('error_log') and state.get('retry_count', 0) < 4:
        print(f"⚠️ Terjadi error internal! Agen mendesain ulang kode (Remidi ke-{state['retry_count']-1})")
        return "write_code_again"
        
    return "complete_response"

workflow = StateGraph(AgentMathState)

workflow.add_node("planner", planner_node)
workflow.add_node("execute_math_tools", execute_math_tools)

workflow.set_entry_point("planner")

workflow.add_edge("execute_math_tools", "planner")

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