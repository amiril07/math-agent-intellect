# Math Agent Intellect

**Math Agent Intellect** is an autonomous AI agent platform designed to solve advanced mathematical problems through step-by-step reasoning. By combining visual processing (OCR), symbolic computation, and agentic logic, this system provides solutions that are not only accurate but also academically rigorous.

---

## 📌 Introduction
Solving complex mathematical problems automatically requires more than just a *Large Language Model* (LLM); it requires the ability to compute with precision and verify logical steps. This project provides an end-to-end implementation that bridges linguistic intelligence with symbolic computation engines to ensure mathematical validity in every generated response.

---

## 🧠 Model Architecture & Mechanism

This project does not rely purely on LLM "guessing." Instead, it implements an **Agentic Workflow** where the language model acts as an *orchestrator* that calls specialized tools for specific tasks.

The data processing flow follows this structured architecture:

### 1. Vision & Preprocessing
* **Input**: Mathematical problem images uploaded by the user.
* **OCR Engine**: Uses **EasyOCR** for optical character recognition, converting pixels into machine-readable mathematical text:
  $$\text{Image} \to \text{Text} \to \text{LaTeX Parse}$$

### 2. Intelligent Reasoning Engine
* **Logic Planner**: **LangGraph** manages conversation state and determines if a problem requires symbolic resolution or logical reasoning.
* **Symbolic Solver**: When calculation is required, the agent executes Python code safely in a sandbox using **SymPy**:
  $$\int f(x) dx \xrightarrow{\text{SymPy}} \text{Symbolic Result}$$
* **Constraint Solver**: For complex logic or systems of equations, the agent utilizes **Z3-solver** to find solutions that satisfy specific constraints.

### 3. Output Formatting
* **Structured Response**: The agent compiles a coherent, step-by-step explanation.
* **LaTeX Rendering**: All symbols and equations are formatted to be rendered beautifully in the browser using **MathJax**:
  $$f(x) = \sum_{n=1}^{\infty} \frac{x^n}{n^2} \implies \text{Professional Math Formatting}$$

---

## 🛠️ Tech Stack & Dependencies
* **Core AI Framework:** LangGraph, LangChain, Groq API (LLM)
* **Web Framework:** FastAPI (Python backend)
* **Math Engines:** SymPy (Symbolic), Z3-solver (Logic), NumPy/SciPy (Numerical)
* **Computer Vision:** EasyOCR, PyTorch
* **Frontend:** HTML5, MathJax (for equation rendering)

---
