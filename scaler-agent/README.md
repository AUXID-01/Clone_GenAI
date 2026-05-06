# Scaler Agent: Autonomous Web Cloner

An advanced, autonomous AI agent designed to create high-fidelity, pixel-perfect clones of modern websites, specifically optimized for Scaler.com.

## 🚀 Key Features
- **Sequential Building**: Enforces a strict top-to-bottom section build to maintain quality.
- **Asset Pipeline**: Automatically searches for, downloads, and integrates real media (logos, videos).
- **High-Fidelity Extraction**: Fetches live HTML from target sites to ensure accurate text and structure.
- **Interactive JS**: Mandates the creation of JavaScript for animations and UI logic.
- **Autonomous Recovery**: Self-corrects tool errors and JSON parsing hallucinations.

## 🛠️ Tech Stack
- **Reasoning**: Meta Llama 3.3 / OpenRouter / Groq
- **Validation**: Pydantic
- **Language**: Python 3.11+
- **Styling**: Vanilla CSS (Glassmorphism, Inter Fonts)

## 📦 Setup & Installation

1. **Clone & Virtual Env**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file with:
   ```env
   OPENROUTER_API_KEY=your_key_here
   ```

## 🎮 Usage
Run the main entry point:
```bash
python main.py
```
**Recommended Objective**: 
> "Execute the 5-Phase 50% Fidelity Plan. Start by extracting content from scaler.com and building the foundation."

## 📁 Architecture
- `/core`: Runtime logic, state management, and error recovery.
- `/prompts`: The "Master Prompt" and system instructions.
- `/tools`: Registry of capabilities (Search, Fetch, Download, Browser).
- `/output`: The final sandboxed clone (HTML/CSS/JS/Assets).
