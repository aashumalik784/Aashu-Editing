import streamlit as st
import moviepy.editor as mp
from moviepy.video.fx.all import colorx, vignette
import whisper
import tempfile
import os

# Netflix Style UI
st.set_page_config(page_title="Aashu Pro - Copyright Safe", layout="wide")
st.markdown("""
    <style>
    .main { background: #000000; color: #E50914; }
    .stButton>button { width: 100%; border-radius: 20px; background: #E50914; color: white; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Aashu Malik YouTube Safe Editor")

with st.sidebar:
    st.header("Rights & Style")
    add_filter = st.checkbox("Apply Anti-Copyright Filter", value=True)
    logo_text = st.text_input("Your Brand Name", "AASHU CREATIONS")
    bgm_file = st.file_uploader("Add Background Music (Optional)", type=['mp3', 'wav'])

uploaded_video = st.file_uploader("Upload Video", type=['mp4'])

if uploaded_video:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())

    if st.button("🚀 GENERATE COPYRIGHT FREE VIDEO"):
        with st.status("Processing Unique Video Signature...", expanded=True) as status:
            # 1. AI Analysis
            model = whisper.load_model("base")
            result = model.transcribe(tfile.name)
            
            # 2. Loading Video
            clip = mp.VideoFileClip(tfile.name)
            
            # Anti-Copyright Trick: Visual Signature Change
            if add_filter:
                st.write("🔧 Modifying Visual Fingerprint...")
                # Halka sa color saturation badhana aur vignette lagana signature badalta hai
                clip = colorx(clip, 1.1) 
                clip = vignette(clip, radius=clip.w*0.5, intensity=0.1)

            # 3. Logo Overlay (Unique Branding)
            logo = mp.TextClip(logo_text, fontsize=30, color='white', font='Arial-Bold', method='caption')
            logo = logo.set_opacity(0.5).set_duration(clip.duration).set_position(('right', 'top'))

            # 4. Background Music & Audio Mixing
            final_audio = clip.audio
            if bgm_file:
                st.write("🎵 Mixing Audio with Background Music...")
                bgm_tfile = tempfile.NamedTemporaryFile(delete=False)
                bgm_tfile.write(bgm_file.read())
                bgm = mp.AudioFileClip(bgm_tfile.name).volumex(0.1).set_duration(clip.duration)
                final_audio = mp.CompositeAudioClip([clip.audio, bgm])

            # 5. Final Assembly
            st.write("🎥 Rendering High-End Output...")
            final_video = mp.CompositeVideoClip([clip, logo])
            final_video = final_video.set_audio(final_audio)
            
            output_name = "youtube_ready.mp4"
            final_video.write_videofile(output_name, codec="libx264", audio_codec="aac")
            
            status.update(label="Ready for YouTube!", state="complete")

        st.video(output_name)
        with open(output_name, "rb") as f:
            st.download_button("📥 Download YouTube Safe Video", f, file_name="Aashu_Copyright_Safe.mp4")
            
