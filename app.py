import streamlit as st
import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont
import os
import whisper
import tempfile
import numpy as np

# Professional UI Styling
st.set_page_config(page_title="Pro Video Editor", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        background-color: #e50914; 
        color: white; 
        border-radius: 8px; 
        height: 3em; 
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #ff0f1a; border: none; }
    .stFileUploader { border: 2px dashed #e50914; border-radius: 10px; padding: 10px; }
    h1 { color: #e50914; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Professional AI Video Editor")
st.write("Automatically add subtitles and logos to your videos.")

# Sidebar for customization
st.sidebar.header("Settings")
logo_text = st.sidebar.text_input("Logo Watermark", value="Aashu Editing")
font_size = st.sidebar.slider("Font Size", 20, 100, 40)
text_color = st.sidebar.color_picker("Subtitle Color", "#FFFFFF")

uploaded_file = st.file_uploader("Upload Video", type=['mp4', 'mov', 'avi'])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.video(video_path)

    if st.button("🚀 START REAL EDITING"):
        with st.status("Editing in progress...", expanded=True) as status:
            # Step 1: Transcription
            st.write("Step 1/3: AI is listening to video (Whisper)...")
            try:
                model = whisper.load_model("base")
                result = model.transcribe(video_path)
                captions = result['segments']
                st.write("Step 1 Complete: Audio transcribed.")
            except Exception as e:
                st.error(f"Whisper Error: {e}")
                st.stop()

            # Step 2: Processing Video with MoviePy
            st.write("Step 2/3: Loading Video Frames...")
            video = mp.VideoFileClip(video_path)
            
            # Step 3: Subtitles + Logo (Fixing Pillow textsize error)
            st.write("Step 3/3: Applying Subtitles & Logo...")
            
            def add_overlays(get_frame, t):
                frame = get_frame(t)
                img = Image.fromarray(frame)
                draw = ImageDraw.Draw(img)
                
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                    logo_font = ImageFont.truetype("arial.ttf", 30)
                except:
                    font = ImageFont.load_default()
                    logo_font = ImageFont.load_default()

                # Fix for 'textsize' error: use textbbox
                # 1. Drawing Logo
                left, top, right, bottom = draw.textbbox((0, 0), logo_text, font=logo_font)
                img_w, img_h = img.size
                draw.text((img_w - (right-left) - 20, 20), logo_text, font=logo_font, fill=(255, 255, 255, 128))

                # 2. Drawing Subtitles
                current_text = ""
                for seg in captions:
                    if seg['start'] <= t <= seg['end']:
                        current_text = seg['text']
                        break
                
                if current_text:
                    left, top, right, bottom = draw.textbbox((0, 0), current_text, font=font)
                    w, h = right - left, bottom - top
                    draw.text(((img_w - w) / 2, img_h - h - 50), current_text, font=font, fill=text_color)
                
                return np.array(img)

            processed_video = video.fl(add_overlays)
            output_path = "edited_video.mp4"
            processed_video.write_videofile(output_path, audio_codec='aac')
            
            status.update(label="Editing Finished!", state="complete", expanded=False)
        
        st.success("Video processed successfully!")
        with open(output_path, "rb") as file:
            st.download_button("📥 Download Edited Video", file, file_name="edited_video.mp4")
else:
    st.info("Please upload a video to start.")
    
