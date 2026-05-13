import streamlit as st
import whisper
from moviepy.editor import *
import os

st.set_page_config(page_title="Aashu AI Editor", page_icon="🎬")
st.title("🎬 Aashu AI Editor - Real Wala")

uploaded_file = st.file_uploader("Video Daal Bhai", type=["mp4", "mov"])

if uploaded_file:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input.mp4")
    st.success("Video upload ho gayi ✅")

    if st.button("🚀 FULL AUTO EDIT KARO"):
        try:
            with st.spinner('Bhai 3-4 min lagega... AI kaam kar raha hai...'):
                
                st.write("Step 1/3: Video sun raha hu...")
                model = whisper.load_model("base")
                result = model.transcribe("input.mp4")
                
                st.write("Step 2/3: Video process kar raha hu...")
                video = VideoFileClip("input.mp4")
                
                st.write("Step 3/3: Subtitle + Logo laga raha hu...")
                
                # Simple subtitle - poora sentence ek saath
                subs = []
                for segment in result["segments"]:
                    txt_clip = TextClip(segment["text"], fontsize=50, color='white', 
                                       bg_color='black', size=(video.w, None), method='caption')
                    txt_clip = txt_clip.set_position(('center', 'bottom')).set_start(segment["start"]).set_duration(segment["end"]-segment["start"])
                    subs.append(txt_clip)
                
                # Logo
                logo = TextClip("Aashu Edits 🔥", fontsize=40, color='yellow', bg_color='black')
                logo = logo.set_position(("right", "top")).set_duration(video.duration)
                
                final_video = CompositeVideoClip([video, logo] + subs)
                final_video.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
            
            st.balloons()
            st.success("LE BHAI HO GAYI REAL EDITING ✅")
            st.video("output.mp4")
            
            with open("output.mp4", "rb") as file:
                st.download_button("📥 Download Edited Video", file, "aashu_edited.mp4")
                
        except Exception as e:
            st.error(f"Bhai error aa gaya: {str(e)}")
            st.error("packages.txt me 'imagemagick' daala ya nahi?")
