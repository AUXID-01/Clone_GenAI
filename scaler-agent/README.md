# Scaler Agent — CLI Tool (NVIDIA NIM Edition)

A conversational CLI AI agent that builds a high-quality clone of the Scaler Academy website using natural language instructions, powered by NVIDIA NIM and Llama 3.3.

## 🚀 Features
- **Loop-based Reasoning**: Follows a START → THINK → TOOL → OBSERVE → OUTPUT workflow.
- **Powered by NVIDIA NIM**: Extremely fast inference using Llama 3.3 70B via NVIDIA's API.
- **Dynamic File Generation**: Generates responsive HTML/CSS/JS files inside an `output/` folder.
- **In-Browser Preview**: Automatically opens the generated website in your default browser.
- **Color-coded Logs**: Clearly prints agent steps for transparency during the reasoning process.

## 🛠️ Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   Create a `.env` file in the root directory and add your NVIDIA API key:
   ```env
   NVIDIA_API_KEY=your_nvidia_api_key_here
   ```

3. **Run the Agent**:
   ```bash
   python main.py
   ```

## 💬 Example Prompts
- "Clone the Scaler website and open it in my browser."
- "Create a Scaler landing page clone with a dark theme and orange call-to-action buttons."
- "Build the Scaler hero section and footer, and save it to output/scaler.html."

## 📁 Folder Structure
- `main.py`: Conversational loop entry point.
- `agent.py`: Core reasoning brain using NVIDIA NIM (OpenAI-compatible) SDK.
- `tools/`: Python functions for file creation and browser control.
- `prompts/`: System instructions for the LLM.
- `output/`: Directory where all generated files are stored.

## 📝 Note
This agent uses the NVIDIA NIM API (OpenAI-compatible) and requires an active internet connection and a valid API key.
