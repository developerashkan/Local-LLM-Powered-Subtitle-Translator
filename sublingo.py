import streamlit as st
import requests
from typing import List, Dict
import time

# App Configuration & Styling
OLLAMA_URL = "http://localhost:11434/api/generate"

st.set_page_config(
    page_title="SubLingo – SRT Translator",
    page_icon="🎬",
    layout="centered"
)

# Custom CSS to turn the primary button green
st.markdown("""
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #28a745;
        color: white;
        border: none;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #218838;
        color: white;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# HTTP Session (cached for performance)
@st.cache_resource
def get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session

# Logic Functions
def build_prompt(text: str, target_language: str) -> str:
    return f"""
You are a professional subtitle translator.
Translate the following subtitle text into {target_language}.
Rules:
- Output ONLY the translated text
- Preserve line breaks
- Keep it natural and subtitle-friendly
- Do NOT add explanations or extra text

Subtitle text:
{text}
""".strip()

def call_ollama(session: requests.Session, model: str, prompt: str, timeout: int) -> str:
    try:
        response = session.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=timeout
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return "[Error: Ollama not running]"
    except requests.exceptions.ReadTimeout:
        return "[Error: Timeout]"
    except Exception as e:
        return f"[Error: {str(e)}]"

def parse_srt(content: str) -> List[Dict[str, str]]:
    blocks = []
    raw_blocks = content.replace("\r\n", "\n").strip().split("\n\n")
    for block in raw_blocks:
        lines = block.splitlines()
        if len(lines) >= 3:
            blocks.append({
                "index": lines[0].strip(),
                "timestamp": lines[1].strip(),
                "text": "\n".join(lines[2:]).strip()
            })
    return blocks

def rebuild_srt(blocks: List[Dict[str, str]]) -> str:
    output = []
    for b in blocks:
        output.append(f"{b['index']}\n{b['timestamp']}\n{b['text']}")
    return "\n\n".join(output)

# UI Layout
st.title("🎬 SubLingo")
st.caption("Local LLM–powered, SRT-safe subtitle translator")

with st.sidebar:
    st.header("⚙️ Settings")
    st.info("Ensure Ollama is running on port 11434")
    
    model = st.selectbox("LLM Model", ["aya-expanse:8b", "gemma3:1b", "llama3"])
    target_language = st.selectbox(
        "Target Language",
        ["Persian (informal)", "French", "German", "Spanish", "Portuguese", "Chinese", "Russian"]
    )

    st.subheader("⏱ Timeout (hours)")
    timeout_hours = st.selectbox("Select max timeout per request", [1, 2, 3, 4, 5], index=0)
    timeout_seconds = timeout_hours * 3600

# Main Process
st.subheader("📁 Upload SRT File")
uploaded_file = st.file_uploader("Choose a .srt subtitle file", type=["srt"])

if uploaded_file:
    srt_text = uploaded_file.read().decode("utf-8", errors="ignore")
    blocks = parse_srt(srt_text)
    
    if not blocks:
        st.error("Could not parse subtitles. Check your file format.")
    else:
        st.info(f"Detected {len(blocks)} subtitle blocks")

        if st.button("Translate Subtitles", type="primary"):
            session = get_session()
            translated_blocks = []
            
            # Progress placeholders
            progress_bar = st.progress(0.0)
            status_text = st.empty()
            
            total = len(blocks)

            for i, block in enumerate(blocks):
                # Update UI before the call for better responsiveness
                status_text.markdown(f"**Processing:** block {i+1} of {total}")
                
                prompt = build_prompt(block["text"], target_language)
                translated_text = call_ollama(session, model, prompt, timeout_seconds)
                
                if "Ollama not running" in translated_text:
                    st.error("🚨 Connection to Ollama failed.")
                    break

                translated_blocks.append({
                    "index": block["index"],
                    "timestamp": block["timestamp"],
                    "text": translated_text
                })

                # Update progress bar safely (capped at 1.0)
                current_progress = min((i + 1) / total, 1.0)
                progress_bar.progress(current_progress)

            if len(translated_blocks) == total:
                status_text.success("✅ All subtitles translated!")
                final_srt = rebuild_srt(translated_blocks)
                
                st.download_button(
                    label="⬇️ Download Translated SRT",
                    data=final_srt,
                    file_name=f"translated_{uploaded_file.name}",
                    mime="text/plain"
                )
