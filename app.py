import streamlit as st
import moviepy.editor as mp
from moviepy.video.fx.all import colorx, vignette, resize, speedx
from PIL import Image, ImageDraw, ImageFont
import whisper
import tempfile
import os
import numpy as np

# Professional UI Styling
st.set_page_config(page_title="Aashu Pro Safe Editor", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stButton>button { background-color: #e50914; color: white; border-radius: 8px; width: 100%; border: none; font-weight: bold; }
    .stFileUploader { border: 2px dashed #e50914; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Aashu Malik Pro Editor (Copyright Safe)")

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Editor Controls")
    subtitle_lang = st.selectbox("Lyrics Language", ["English", "Hindi"])
    copyright_shield = st.checkbox("Anti-Copyright Mode", value=True)
    brand_logo = st.text_input("Brand Watermark", "AASHU CREATIONS")
    font_size = st.slider("Font Size", 20, 100, 50)

uploaded_file = st.file_uploader("Upload Raw Video", type=['mp4'])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    if st.button("🚀 RENDER PROFESSIONAL VIDEO"):
        with st.status("Shielding & Editing...", expanded=True) as status:
            # 1. AI Lyrics Generation
            st.write("🔍 Extracting Lyrics...")
            model = whisper.load_model("base")
            lang_code = 'hi' if subtitle_lang == "Hindi" else 'en'
            result = model.transcribe(tfile.name, language=lang_code)
            captions = result['segments']
            
            # 2. Loading Clip
            clip = mp.VideoFileClip(tfile.name)
            
            # 3. Anti-Copyright Shield
            if copyright_shield:
                st.write("🛡️ Changing Visual Signature...")
                clip = speedx(clip, factor=1.01) # Metadata changes
                clip = colorx(clip, 1.05)       # Visual change
                clip = vignette(clip, radius=clip.w*0.6, intensity=0.1)

            # 4. Overlay Logic (Fixing textsize Error)
            st.write("✨ Applying Subtitles & Logo...")
            
            def add_overlays(get_frame, t):
                frame = get_frame(t)
                img = Image.fromarray(frame)
                draw = ImageDraw.Draw(img)
                
                try:
                    # Font setup
                    font = ImageFont.load_default() # Professional setup: use path to .ttf
                except:
                    font = ImageFont.load_default()

                # LOGO: Drawing Brand Watermark
                # FIX: textbbox instead of textsize
                l, t_b, r, b = draw.textbbox((0, 0), brand_logo, font=font)
                draw.text((img.width - (r-l) - 20, 20), brand_logo, font=font, fill=(255, 255, 255, 128))

                # SUBTITLES: Match current time 't'
                current_text = ""
                for seg in captions:
                    if seg['start'] <= t <= seg['end']:
                        current_text = seg['text'].strip().upper()
                        break
                
                if current_text:
                    # FIX: textbbox instead of textsize
                    left, top, right, bottom = draw.textbbox((0, 0), current_text, font=font)
                    w, h = right - left, bottom - top
                    draw.text(((img.width - w) / 2, img.height - h - 50), current_text, font=font, fill="yellow")
                
                return np.array(img)

            # Applying changes
            final_video = clip.fl(add_overlays)
            output_name = "final_output.mp4"
            final_video.write_videofile(output_name, codec="libx264", audio_codec="aac", fps=24)
            
            status.update(label="Render Finished!", state="complete")
            
        st.video(output_name)
        with open(output_name, "rb") as f:
            st.download_button("📥 Download Safe Video", f, file_name="Aashu_Edited.mp4")
                                                             
