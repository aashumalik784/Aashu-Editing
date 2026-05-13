import streamlit as st
import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont
import os
import whisper
import tempfile
import numpy as np

st.set_page_config(page_title="Aashu Pro Editor", layout="wide")
st.markdown("<style>.main { background-color: #050505; color: white; }</style>", unsafe_allow_html=True)
st.title("🎬 Aashu Pro Editor - 100% Working")

with st.sidebar:
    st.header("Settings")
    logo_text = st.text_input("Logo Watermark", "AASHU CREATIONS")
    subtitle_lang = st.selectbox("Language", ["English", "Hindi"])

uploaded_file = st.file_uploader("Upload Video", type=['mp4'])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    if st.button("🚀 RENDER VIDEO"):
        with st.status("Editing...", expanded=True) as status:
            # 1. AI Transcribe
            model = whisper.load_model("base")
            lang = 'hi' if subtitle_lang == "Hindi" else 'en'
            result = model.transcribe(tfile.name, language=lang)
            captions = result['segments']
            
            # 2. Process
            clip = mp.VideoFileClip(tfile.name)
            
            def add_overlays(get_frame, t):
                frame = get_frame(t)
                img = Image.fromarray(frame)
                draw = ImageDraw.Draw(img)
                font = ImageFont.load_default()

                # Logo - Fixed with textbbox
                l, t_b, r, b = draw.textbbox((0, 0), logo_text, font=font)
                draw.text((img.width - (r-l) - 20, 20), logo_text, font=font, fill=(255, 255, 255, 128))

                # Subtitles - Fixed with textbbox
                current_text = ""
                for seg in captions:
                    if seg['start'] <= t <= seg['end']:
                        current_text = seg['text'].strip().upper()
                        break
                
                if current_text:
                    left, top, right, bottom = draw.textbbox((0, 0), current_text, font=font)
                    w, h = right - left, bottom - top
                    draw.text(((img.width - w) / 2, img.height - h - 50), current_text, font=font, fill="yellow")
                
                return np.array(img)

            final_video = clip.fl(add_overlays)
            output_name = "final_output.mp4"
            final_video.write_videofile(output_name, codec="libx264", audio_codec="aac")
            status.update(label="Done!", state="complete")
            
        st.video(output_name)
        with open(output_name, "rb") as f:
            st.download_button("Download", f, file_name="Aashu_Edit.mp4")
            
