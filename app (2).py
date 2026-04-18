import streamlit as st
import os
import io
import numpy as np
from PIL import Image

# ─────────────────────────────
# PAGE CONFIG
# ─────────────────────────────
st.set_page_config(page_title="Desi Chic Try-On", layout="wide")

# ─────────────────────────────
# CLEAN UI (NO HTML SHOW)
# ─────────────────────────────
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container {padding-top:1rem;}
.stButton>button {width:100%; border-radius:8px; background:black; color:white;}
img {border-radius:10px;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# TRY-ON FUNCTION (IMPROVED)
# ─────────────────────────────
def apply_dress(user_img, dress_img, scale, y_shift):
    user = user_img.convert("RGBA")
    dress = dress_img.convert("RGBA")

    uw, uh = user.size

    # resize dress
    new_w = int(uw * scale)
    aspect = dress.height / dress.width
    new_h = int(new_w * aspect)

    dress = dress.resize((new_w, new_h))

    # position (center + adjustable)
    x = (uw - new_w) // 2
    y = int(uh * y_shift)

    result = Image.new("RGBA", user.size)
    result.paste(user, (0, 0))

    result.alpha_composite(dress, (x, y))

    return result

# ─────────────────────────────
# SESSION
# ─────────────────────────────
if "dress" not in st.session_state:
    st.session_state.dress = None

# ─────────────────────────────
# TITLE
# ─────────────────────────────
st.title("👗 Desi Chic Virtual Try-On")
st.write("Upload → Select → Adjust → Try On")

# ─────────────────────────────
# STEP 1 - UPLOAD
# ─────────────────────────────
st.header("1. Upload Image")
uploaded = st.file_uploader("Upload full body image", type=["png","jpg","jpeg"])

user_img = None
if uploaded:
    user_img = Image.open(uploaded)
    st.image(user_img, width=250)

# ─────────────────────────────
# STEP 2 - CATEGORY
# ─────────────────────────────
st.header("2. Choose Dress")

category = st.selectbox("Category", ["casual", "formal", "bridal"])

folder = os.path.join("dresses", category)

if os.path.exists(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith(("png","jpg","jpeg"))]

    if files:
        cols = st.columns(3)

        for i, file in enumerate(files):
            path = os.path.join(folder, file)

            try:
                img = Image.open(path)

                with cols[i % 3]:
                    st.image(img, width=150)

                    if st.button("Select", key=path):
                        st.session_state.dress = path

            except:
                st.error(f"Error loading {file}")
    else:
        st.warning("No dresses found")
else:
    st.warning("Folder missing")

# ─────────────────────────────
# STEP 3 - ADJUSTMENT
# ─────────────────────────────
st.header("3. Adjust Fitting")

scale = st.slider("Dress Size", 0.4, 0.9, 0.6)
y_shift = st.slider("Vertical Position", 0.1, 0.4, 0.2)

# ─────────────────────────────
# STEP 4 - RESULT
# ─────────────────────────────
st.header("4. Result")

if user_img and st.session_state.dress:

    dress_img = Image.open(st.session_state.dress)

    with st.spinner("Applying dress..."):
        result = apply_dress(user_img, dress_img, scale, y_shift)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Before")
        st.image(user_img, use_container_width=True)

    with col2:
        st.subheader("After")
        st.image(result, use_container_width=True)

    # download
    buf = io.BytesIO()
    result.save(buf, format="PNG")

    st.download_button(
        "Download Result",
        data=buf.getvalue(),
        file_name="tryon.png",
        mime="image/png"
    )

elif not user_img:
    st.info("Upload image first")
else:
    st.info("Select a dress first")
