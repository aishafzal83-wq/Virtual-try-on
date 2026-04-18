import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import io

# ─────────────────────────────
# PAGE CONFIG
# ─────────────────────────────
st.set_page_config(
    page_title="Desi Chic Try-On",
    page_icon="👗",
    layout="wide"
)

# ─────────────────────────────
# CLEAN UI FIX (no code leakage)
# ─────────────────────────────
st.markdown("""
<style>
.block-container {padding-top: 1rem;}
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# SMART TRY-ON FUNCTION (BEST POSSIBLE IN STREAMLIT)
# ─────────────────────────────
def fit_dress(user_img, dress_path, y_pos, size):
    user = np.array(user_img)
    h, w = user.shape[:2]

    dress = cv2.imread(dress_path, cv2.IMREAD_UNCHANGED)
    if dress is None:
        return user

    # resize dress
    target_w = int(w * size)
    scale = target_w / dress.shape[1]
    target_h = int(dress.shape[0] * scale)

    dress = cv2.resize(dress, (target_w, target_h))

    x = w // 2 - target_w // 2
    y = int(h * y_pos)

    dh, dw = dress.shape[:2]

    if y + dh > h:
        dh = h - y
    if x + dw > w:
        dw = w - x

    dress = dress[:dh, :dw]

    # blending
    if dress.shape[2] == 4:
        alpha = dress[:, :, 3] / 255.0

        for c in range(3):
            user[y:y+dh, x:x+dw, c] = (
                alpha * dress[:, :, c] +
                (1 - alpha) * user[y:y+dh, x:x+dw, c]
            )

    return user.astype(np.uint8)

# ─────────────────────────────
# TITLE
# ─────────────────────────────
st.markdown("<h1 style='text-align:center;'>DESI CHIC 👗</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Virtual Try-On System</p>", unsafe_allow_html=True)

# ─────────────────────────────
# UPLOAD IMAGE
# ─────────────────────────────
uploaded = st.file_uploader("Upload Your Photo", type=["jpg","png","jpeg"])

user_img = None
if uploaded:
    user_img = Image.open(uploaded).convert("RGB")
    st.image(user_img, caption="Your Image", width=250)

# ─────────────────────────────
# SELECT DRESS
# ─────────────────────────────
category = st.selectbox("Select Category", ["casual", "formal", "bridal"])

folder = f"dresses/{category}"
os.makedirs(folder, exist_ok=True)

files = os.listdir(folder)

selected_dress = None

st.subheader("Select Dress")

cols = st.columns(4)

for i, file in enumerate(files):
    path = os.path.join(folder, file)

    with cols[i % 4]:
        st.image(path, width=120)

        if st.button(f"Select {i}"):
            selected_dress = path
            st.session_state["dress"] = path

# ─────────────────────────────
# SLIDERS
# ─────────────────────────────
y_pos = st.slider("Vertical Position", 0.05, 0.5, 0.22)
size = st.slider("Dress Size", 0.3, 0.9, 0.55)

# ─────────────────────────────
# TRY ON RESULT
# ─────────────────────────────
if user_img and "dress" in st.session_state:

    st.subheader("Your Result 👇")

    result = fit_dress(
        user_img,
        st.session_state["dress"],
        y_pos,
        size
    )

    st.image(result, use_container_width=True)

    # download
    result_img = Image.fromarray(result)
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")

    st.download_button(
        "Download Result",
        data=buf.getvalue(),
        file_name="desi_chic_result.png",
        mime="image/png"
    )
