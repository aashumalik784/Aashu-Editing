import streamlit as st
import moviepy.editor as mp
from moviepy.video.fx.all import colorx, vignette, resize, speedx
import whisper
import tempfile
import os
import random

# Professional Dark UI
st.set_page_config(page_title="Aashu Malik Pro Safe Editor", layout="wide")
st.markdown("""
    <style>
    .main { background: #050505; color: #E50914; }
    .stButton>button { background: #E50914; color: white; border-radius: 10px; font-weight: bold; height: 3em; width: 100%; border: none; }
    .stButton>button:hover { background: #B20710; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Aashu Pro AI - Copyright Protection Mode")

# Sidebar for Controls
with st.sidebar:
    st.header("⚙️ Safety Settings")
    copyright_shield = st.checkbox("Enable Anti-Copyright Shield", value=True)
    subtitle_lang = st.selectbox("Lyrics Language", ["English", "Hindi"])
    bgm_volume = st.slider("BGM Volume", 0.0, 0.5, 0.1)
    brand_logo = st.text_input("Brand Watermark", "AASHU CREATIONS")

uploaded_video = st.file_uploader("Upload Raw Video", type=['mp4'])

if uploaded_video:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())
    
    if st.button("🚀 RENDER PROFESSIONAL & SAFE VIDEO"):
        with st.status("Shielding Video from Copyright...", expanded=True) as status:
            # 1. AI Transcription (Hindi/English Support)
            st.write("🔍 Extracting Lyrics...")
            model = whisper.load_model("base")
            lang_code = 'hi' if subtitle_lang == "Hindi" else 'en'
            result = model.transcribe(tfile.name, language=lang_code)
            
            # 2. Loading Clip
            clip = mp.VideoFileClip(tfile.name)
            
            # 3. ANTI-COPYRIGHT ENGINE (The Secret Sauce)
            if copyright_shield:
                st.write("🛡️ Modifying Digital Fingerprint...")
                # Halki speed change (0.1% jo pata nahi chalti par ID badal deti hai)
                clip = speedx(clip, factor=1.01)
                # Halka sa zoom
                clip = resize(clip, width=clip.w * 1.05)
                # Color shift aur Vignette
                clip = colorx(clip, 1.05)
                clip = vignette(clip, radius=clip.w*0.6, intensity=0.1)

            # 4. Generating Subtitles Clips
            st.write("✨ Rendering Pro Lyrics...")
            subtitle_clips = []
            for segment in result['segments']:
                txt = mp.TextClip(
                    segment['text'].strip().upper(),
                    fontsize=60, color='yellow', font='Arial-Bold',
                    stroke_color='black', stroke_width=2,
                    method='caption', size=(clip.w*0.8, None)
                ).set_start(segment['start']).set_duration(segment['end']-segment['start']).set_position(('center', clip.h*0.8))
                subtitle_clips.append(txt)

            # 5. Branding Overlay
            logo = mp.TextClip(brand_logo, fontsize=25, color='white').set_opacity(0.4).set_duration(clip.duration).set_position(('right', 'top'))

            # 6. Final Export
            final_video = mp.CompositeVideoClip([clip, logo] + subtitle_clips)
            output_name = "copyright_safe_output.mp4"
            final_video.write_videofile(output_name, codec="libx264", audio_codec="aac", fps=24, threads=4)
            
            status.update(label="Ready for YouTube/Reels!", state="complete")
            
        st.video(output_name)
        with open(output_name, "rb") as f:
            st.download_button("📥 Download Safe Video", f, file_name="Aashu_Safe_Edit.mp4")
            
