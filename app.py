import streamlit as st
import whisper
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

st.set_page_config(page_title="Aashu AI Editor", page_icon="🎬")
st.title("🎬 Aashu AI Editor - Working Wala")

uploaded_file = st.file_uploader("Video Daal Bhai", type=["mp4"])

def create_text_image(text, video_width):
    # PIL se text ka image banao - ye Streamlit pe chalega
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    img = Image.new('RGBA', (video_width, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Text ko center me laao
    w, h = draw.textsize(text, font=font)
    draw.text(((video_width-w)/2, 10), text, font=font, fill=(255,255,0,255), 
              stroke_width=3, stroke_fill=(0,0,0,255))
    return np.array(img)

if uploaded_file:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input.mp4")
    st.success("Video upload ho gayi ✅")

    if st.button("🚀 REAL EDIT KARO"):
        try:
            with st.spinner('Bhai 3-4 min ruk ja... Ye wala chalega pakka...'):
                
                st.write("Step 1/3: Video sun raha hu...")
                model = whisper.load_model("base")
                result = model.transcribe("input.mp4")
                
                st.write("Step 2/3: Video load kar raha hu...")
                video = VideoFileClip("input.mp4")
                
                st.write("Step 3/3: Subtitle + Logo laga raha hu...")
                
                # 1. SUBTITLE - PIL se banayenge
                subs = []
                for segment in result["segments"]:
                    txt_img = create_text_image(segment["text"], video.w)
                    txt_clip = ImageClip(txt_img).set_duration(segment["end"]-segment["start"])
                    txt_clip = txt_clip.set_start(segment["start"]).set_position(('center', 'bottom'))
                    subs.append(txt_clip)
                
                # 2. LOGO - PIL se banayenge
                logo_img = create_text_image("Aashu Edits 🔥", video.w)
                logo_clip = ImageClip(logo_img).set_duration(video.duration).set_position(("right", "top"))
                
                # 3. FINAL VIDEO
                final_video = CompositeVideoClip([video, logo_clip] + subs)
                final_video.write_videofile("output.mp4", codec="libx264", audio_codec="aac", logger=None)
            
            st.balloons()
            st.success("HO GAYA BHAI - AB REAL EDITING ✅")
            st.video("output.mp4")
            
            with open("output.mp4", "rb") as file:
                st.download_button("📥 Download Kar Le", file, "aashu_edited.mp4")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.error("packages.txt daala kya?")
