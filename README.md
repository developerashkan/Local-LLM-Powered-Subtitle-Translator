# 🎬 SubLingo – SRT Translator

**SubLingo** is a robust, local LLM-powered tool designed to translate subtitle files (`.srt`) while maintaining strict formatting. By leveraging **Ollama**, it ensures your data stays private, secure, and runs entirely on your local machine.

---

## Key Features

* **Privacy-Centric:** All translations happen locally via Ollama. No data is sent to the cloud.
* **SRT-Safe Parsing:** Specifically engineered to handle SRT structures, ensuring timestamps and sequence numbers remain untouched.
* **Responsive UI:** Features a real-time progress bar and status updates, so you’re never left wondering if the app is frozen.
* **Customizable Settings:** * Choose between different local models (Aya, Gemma, Llama, etc.).
    * Multiple target languages including Persian, French, Russian, and more.
    * Adjustable timeout settings for older hardware.
* **Green-Light Workflow:** A clear, color-coded interface for easy navigation.

---

## Prerequisites

1.  **Ollama Installed:** [Download Ollama here](https://ollama.com/).
2.  **Models Downloaded:** Open your terminal and pull the models you want to use:
    ```bash
    ollama pull aya-expanse:8b
    ollama pull gemma3:1b
    ```
3.  **Python Environment:** Python 3.9 or higher is recommended.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/sublingo.git](https://github.com/yourusername/sublingo.git)
   cd sublingo
   ```
## How to Use:
Launch Ollama: Ensure the Ollama server is running in the background.

Upload File: Drag and drop your .srt file into the upload box.

Configure Sidebar:

Select your Model (use smaller models like gemma3:1b for faster results on CPUs).

Choose your Target Language.

Translate: Click the green Translate Subtitles button.

Download: Once the progress bar hits 100%, the ⬇️ Download Translated SRT button will appear.


## Technical Details
The Translation Prompt
SubLingo uses a specialized "Professional Translator" prompt to ensure the LLM doesn't hallucinate or add conversational filler:

"Output ONLY the translated text. Preserve line breaks. Keep it natural and subtitle-friendly."

Progress Handling
The app uses a min((i + 1) / total_blocks, 1.0) logic to ensure the Streamlit progress bar never exceeds 100%, even with floating-point math variances, providing a smooth user experience.

## Contributing
Feel free to fork this project, submit PRs, or report issues. Suggestions for batch-processing features or additional language support are always welcome!

License: MIT

Author: Ashkan Bahmani
