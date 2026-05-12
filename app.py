import streamlit as st
import whisper
from moviepy.editor import *
from moviepy.audio.fx import all as afx

st.set_page_config(page_title="Aashu AI Editor", page_icon="🎬")
st.title("🎬 Aashu AI Editor - Real Wala")

uploaded_file = st.file_uploader("Video Daal Bhai", type=["mp4", "mov", "mkv"])
bg_music = st.file_uploader("BG Music Daal (Optional)", type=["mp3", "wav"])

if uploaded_file:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input.mp4")
    st.success("Video upload ho gayi ✅")

    if st.button("🚀 FULL AUTO EDIT KARO"):
        with st.spinner('Bhai 3-4 min lagega... AI kaam kar raha hai...'):
            
            st.write("Step 1/4: Video sun raha hu...")
            model = whisper.load_model("base")
            result = model.transcribe("input.mp4", word_timestamps=True)
            
            st.write("Step 2/4: Video process kar raha hu...")
            video = VideoFileClip("input.mp4")
            
            st.write("Step 3/4: Subtitle bana raha hu...")
            subs = []
            for segment in result["segments"]:
                for word in segment["words"]:
                    txt_clip = TextClip(word["word"].upper(), fontsize=80, color='yellow', 
                                       stroke_color='black', stroke_width=4, font='Arial-Bold')
                    txt_clip = txt_clip.set_position(('center', 0.85), relative=True)
                    txt_clip = txt_clip.set_start(word["start"]).set_duration(word["end"]-word["start"])
                    subs.append(txt_clip)
            
            st.write("Step 4/4: Logo + Music laga raha hu...")
            logo = TextClip("Aashu Edits 🔥", fontsize=40, color='white', stroke_color='black', stroke_width=2)
            logo = logo.set_position(("right", "top")).set_duration(video.duration)
            
            clips_to_composite = [video, logo] + subs
            final_video = CompositeVideoClip(clips_to_composite)
            
            if bg_music:
                with open("bg.mp3", "wb") as f:
                    f.write(bg_music.read())
                bg_audio = AudioFileClip("bg.mp3").volumex(0.15)
                bg_audio = afx.audio_loop(bg_audio, duration=final_video.duration)
                final_audio = CompositeAudioClip([final_video.audio, bg_audio])
                final_video = final_video.set_audio(final_audio)
            
            final_video.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
        
        st.balloons()
        st.success("LE BHAI HO GAYI REAL EDITING ✅")
        st.video("output.mp4")
        
        with open("output.mp4", "rb") as file:
            st.download_button("📥 Download Edited Video", file, "aashu_edited.mp4", mime="video/mp4")
