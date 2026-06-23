import streamlit as st
import whisper
import os
from googletrans import Translator
from gtts import gTTS
from audiorecorder import audiorecorder

# టైటిల్ మార్చబడింది
st.title("Global AI Translator & Voice Assistant")

st.subheader("ఇన్‌పుట్ పద్ధతిని ఎంచుకోండి")
input_option = st.radio("ఎలా ఇన్‌పుట్ ఇస్తారు?", ("ఫైల్ అప్‌లోడ్", "లైవ్ ఆడియో రికార్డ్"))

file_path = None

if input_option == "లైవ్ ఆడియో రికార్డ్":
    audio = audiorecorder("రికార్డ్ బటన్", "స్టాప్ బటన్")
    if audio:
        audio.export("temp_audio.mp3", format="mp3")
        file_path = "temp_audio.mp3"
else:
    file = st.file_uploader("వీడియో లేదా ఆడియో ఫైల్ అప్‌లోడ్ చేయండి", type=['mp3', 'wav', 'mp4'])
    if file:
        with open("temp_file.mp3", "wb") as f:
            f.write(file.read())
        file_path = "temp_file.mp3"

def clone_voice(text, target_lang_code):
    # ఇక్కడ RVC మోడల్ కోసం కోడ్ రాసుకోవాలి
    st.info("వాయిస్ క్లోనింగ్ ప్రాసెస్ అవుతోంది...")
    return gTTS(text=text, lang=target_lang_code)

if file_path:
    if st.button("ప్రాసెస్ చెయ్యి"):
        with st.spinner("ప్రాసెసింగ్ జరుగుతోంది..."):
            # 1. టెక్స్ట్ కి మార్చడం
            model = whisper.load_model("base")
            result = model.transcribe(file_path)
            text = result["text"]
            st.write("Transcription:", text)
            
            # 2. అనువాదం
            translator = Translator()
            translated = translator.translate(text, dest='te').text 
            
            # 3. ఆడియోగా మార్చడం
            tts = clone_voice(translated, 'te')
            tts.save("output.mp3")
            st.audio("output.mp3")
            st.success("పని పూర్తయింది!")
