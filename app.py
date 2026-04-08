import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
import PyPDF2
import tempfile
import speech_recognition as sr
import time


st.set_page_config(page_title="Vijay's Translator", layout="centered")


st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
    color: white;
}

/* Card Style */
.card {
    background: rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(45deg, #ff7e5f, #feb47b);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* Text area */
textarea {
    border-radius: 12px !important;
}

/* Titles */
h1, h2, h3 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<h1>🌍 Vijay's AI Translator</h1>", unsafe_allow_html=True)


languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar"
}


if "history" not in st.session_state:
    st.session_state.history = []


st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("✍️ Enter Text")

text = st.text_area("Type or speak your text...")

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("From", languages.keys(), index=0)

with col2:
    target_lang = st.selectbox("To", languages.keys(), index=1)

# Voice input
if st.button("🎤 Speak"):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = r.listen(source)

        text = r.recognize_google(audio)
        st.success(f"You said: {text}")
    except:
        st.error("Speech recognition failed")

# Word stats
if text:
    words = len(text.split())
    st.caption(f"📝 {words} words")

st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<div class="card">', unsafe_allow_html=True)

multi_targets = st.multiselect(
    "🌐 Translate to multiple languages",
    list(languages.keys())[1:]
)

if st.button("🚀 Translate"):

    if text.strip():

        with st.spinner("🤖 Thinking..."):
            time.sleep(1.2)

            detected = detect(text)
            translated = GoogleTranslator(
                source=languages[source_lang],
                target=languages[target_lang]
            ).translate(text)

        st.success(f"**Detected:** {detected}")
        st.subheader("✅ Translation")
        st.write(translated)

        # Multi language
        if multi_targets:
            st.subheader("🌍 Multiple Translations")
            for lang in multi_targets:
                t = GoogleTranslator(source="auto", target=languages[lang]).translate(text)
                st.write(f"**{lang}:** {t}")

        # TTS
        try:
            tts = gTTS(text=translated, lang=languages[target_lang])
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)
        except:
            st.warning("TTS not available")

        # Download
        st.download_button("📥 Download", translated)

        # Save history
        st.session_state.history.append((text, translated))

    else:
        st.warning("Enter some text")

st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📜 History")

for inp, out in reversed(st.session_state.history[-5:]):
    st.write(f"🔹 {inp} → {out}")

st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📄 Document Translation")

file = st.file_uploader("Upload TXT or PDF", type=["txt", "pdf"])

doc_lang = st.selectbox("Translate document to", list(languages.keys())[1:])

if file and st.button("📄 Translate Document"):

    text_data = ""

    if file.type == "text/plain":
        text_data = file.read().decode("utf-8")

    elif file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text_data += page.extract_text()

    if text_data.strip():

        with st.spinner("Translating document..."):
            result = GoogleTranslator(source="auto", target=languages[doc_lang]).translate(text_data)

        st.text_area("Result", result, height=250)

        st.download_button("📥 Download File", result)

    else:
        st.error("No text found")

st.markdown('</div>', unsafe_allow_html=True)
