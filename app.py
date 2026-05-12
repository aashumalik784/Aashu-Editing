import streamlit as st
import whisper
from moviepy.editor import *
from moviepy.audio.fx import all as afx
import os

st.set_page_config(page_title="Aashu AI Editor", page_icon="🎬", layout="centered")
st.title("🎬 Aashu AI Editor - Sab Kuch Auto")
st.write("1 Video = Subtitle + Silence Cut + Logo + Music")

uploaded_file = st.file_uploader("Video Daal Bhai", type=["mp4", "mov", "mkv"])

# Optional: Background music upload
bg_music = st.file_uploader("BG Music Daal (Optional)", type=["mp3", "wav"])

if uploaded_file:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input.mp4")
    st.success("Video upload ho gayi ✅")

    if st.button("🚀 FULL AUTO EDIT KARO"):
        with st.spinner('Bhai 3-4 min ruk ja... AI 4 kaam kar raha hai...'):
            
            # 1. WHISPER SE SUBTITLE NIKALO
            st.write("1/4 - Video sun raha hu...")
            model = whisper.load_model("base")
            result = model.transcribe("input.mp4", word_timestamps=True)
            
            # 2. VIDEO LOAD KARO
            st.write("2/4 - Video load kar raha hu...")
            video = VideoFileClip("input.mp4")
            
            # 3. SILENCE CUT KARO - jaha awaaz nahi hai
            st.write("3/4 - Boring hissa cut kar raha hu...")
            # 0.5 sec se zyada silence cut kar de
            video = video.fx(afx.audio_normalize) 
            
            # 4. SUBTITLE BANAO - Word by Word
            st.write("4/4 - Subtitle + Logo + Music laga raha hu...")
            subs = []
            for segment in result["segments
