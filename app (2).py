import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import io

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Desi Chic — Virtual Try-On",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Professional CSS ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Montserrat:wght@300;400;500;600&display=swap');

* { box-sizing: border-box; }

.stApp {
    background: #0e0b16;
    font-family: 'Montserrat', sans-serif;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Top navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 40px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    background: rgba(14,11,22,0.95);
    backdrop-filter: blur(20px);
    position: sticky;
    top: 0;
    z-index: 100;
}
.brand-name {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 26px;
    font-weight: 500;
    color: #e8d5b0;
    letter-spacing: 4px;
    text-transform: uppercase;
}
.brand-tagline {
    font-size: 9px;
    letter-spacing: 5px;
    color: rgba(232,213,176,0.45);
    text-transform: uppercase;
    margin-top: 2px;
}
.nav-links {
    display: flex;
    gap: 32px;
    align-items: center;
}
.nav-link {
    font-size: 11px;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
    cursor: pointer;
}
.nav-link.active { color: #e8d5b0; border-bottom: 1px solid #e8d5b0; }

/* Section headers */
.section-label {
    font-size: 9px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: rgba(232,213,176,0.5);
    margin-bottom: 6px;
}
.section-title {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 28px;
    font-weight: 400;
    color: #e8d5b0;
    letter-spacing: 1px;
    margin: 0 0 24px 0;
}

/* Upload zone */
.upload-zone {
    border: 1px solid rgba(232,213,176,0.15);
    border-radius: 4px;
    padding: 48px 24px;
    text-align: center;
    background: rgba(255,255,255,0.015);
    cursor: pointer;
    transition: all 0.3s;
}
.upload-zone:hover {
    border-color: rgba(232,213,176,0.35);
    background: rgba(232,213,176,0.03);
}
.upload-icon { font-size: 36px; margin-bottom: 14px; opacity: 0.6; }
.upload-text {
    font-size: 13px;
    color: rgba(255,255,255,0.45);
    letter-spacing: 1px;
    margin: 0;
}
.upload-sub {
    font-size: 10px;
    color: rgba(255,255,255,0.2);
    letter-spacing: 1px;
    margin-top: 6px;
}

/* Dress cards */
.dress-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}
.dress-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 4px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s;
}
.dress-card:hover {
    border-color: rgba(232,213,176,0.3);
    transform: translateY(-3px);
}
.dress-card.selected {
    border-color: #e8d5b0;
    box-shadow: 0 0 20px rgba(232,213,176,0.12);
}
.dress-name {
    padding: 10px 12px;
    font-size: 10px;
    letter-spacing: 1.5px;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
}

/* Category pills */
.cat-pill {
    display: inline-block;
    padding: 7px 18px;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 2px;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4);
    cursor: pointer;
    margin-right: 8px;
    transition: all 0.2s;
}
.cat-pill.active {
    background: #e8d5b0;
    color: #0e0b16;
    border-color: #e8d5b0;
    font-weight: 600;
}

/* Result area */
.result-container {
    position: relative;
    border: 1px solid rgba(232,213,176,0.12);
    border-radius: 4px;
    overflow: hidden;
    background: rgba(255,255,255,0.01);
}
.result-badge {
    position: absolute;
    top: 16px;
    left: 16px;
    background: rgba(14,11,22,0.85);
    border: 1px solid rgba(232,213,176,0.3);
    padding: 5px 12px;
    font-size: 9px;
    letter-spacing: 3px;
    color: #e8d5b0;
    text-transform: uppercase;
    border-radius: 2px;
    backdrop-filter: blur(8px);
}

/* Buttons */
.btn-primary {
    background: #e8d5b0;
    color: #0e0b16;
    border: none;
    padding: 12px 32px;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 600;
    cursor: pointer;
    border-radius: 2px;
    width: 100%;
    transition: all 0.2s;
}
.btn-primary:hover { background: #d4b896; }
.btn-outline {
    background: transparent;
    color: #e8d5b0;
    border: 1px solid rgba(232,213,176,0.3);
    padding: 12px 32px;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 500;
    cursor: pointer;
    border-radius: 2px;
    width: 100%;
    transition: all 0.2s;
}

/* Divider */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(232,213,176,0.3), transparent);
    margin: 32px 0;
}

/* Streamlit overrides */
.stButton > button {
    background: #e8d5b0 !important;
    color: #0e0b16 !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 12px 24px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #d4b896 !important;
    transform: none !important;
}
.stButton > button[data-selected="true"],
button[kind="secondary"] {
    background: transparent !important;
    color: #e8d5b0 !important;
    border: 1px solid rgba(232,213,176,0.3) !important;
}
.stDownloadButton > button {
    background: transparent !important;
    color: #e8d5b0 !important;
    border: 1px solid rgba(232,213,176,0.3) !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background: rgba(232,213,176,0.08) !important;
}
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.01) !important;
    border: 1px solid rgba(232,213,176,0.15) !important;
    border-radius: 4px !important;
    padding: 16px !important;
}
[data-testid="stFileUploader"] label {
    color: rgba(255,255,255,0.4) !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
}
.stSelectbox > div, .stRadio > div {
    background: transparent !important;
}
.stRadio label {
    color: rgba(255,255,255,0.55) !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
}
.stSlider label {
    color: rgba(232,213,176,0.6) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] {
    background: #0a0812 !important;
    border-right: 1px solid rgba(232,213,176,0.08) !important;
}
.stAlert {
    background: rgba(232,213,176,0.05) !important;
    border: 1px solid rgba(232,213,176,0.15) !important;
    border-radius: 4px !important;
    color: rgba(255,255,255,0.6) !important;
    font-size: 12px !important;
}
p, li { color: rgba(255,255,255,0.6) !important; font-size: 13px !important; }
h1, h2, h3 { color: #e8d5b0 !important; }
code {
    background: rgba(232,213,176,0.08) !important;
    color: #e8d5b0 !important;
    border-radius: 3px !important;
    padding: 2px 6px !important;
    font-size: 11px !important;
}
.stSpinner p { color: rgba(232,213,176,0.6) !important; }
hr { border-color: rgba(232,213,176,0.1) !important; }
</style>
""", unsafe_allow_html=True)


# ── Overlay Function ──────────────────────────────────────────
def smart_overlay(user_pil, dress_path, y_pos=0.22, size=0.68):
    """Smart dress overlay with proper body alignment"""
    user = np.array(user_pil.copy())
    uh, uw = user.shape[:2]

    dress_bgra = cv2.imread(dress_path, cv2.IMREAD_UNCHANGED)
    if dress_bgra is None:
        return user

    dh_orig, dw_orig = dress_bgra.shape[:2]

    # Width based on size slider
    target_w = int(uw * size)
    # Maintain aspect ratio
    aspect = dh_orig / dw_orig
    target_h = int(target_w * aspect)

    # Height cap
    max_h = int(uh * 0.80)
    if target_h > max_h:
        target_h = max_h
        target_w = int(target_h / aspect)

    dress_resized = cv2.resize(dress_bgra, (target_w, target_h))

    # Center horizontally
    x_start = max(0, int((uw - target_w) / 2))
    y_start = int(uh * y_pos)

    h, w = dress_resized.shape[:2]

    # Bounds
    if y_start + h > uh: h = uh - y_start
    if x_start + w > uw: w = uw - x_start
    dress_resized = dress_resized[:h, :w]

    # Blend
    if dress_resized.shape[2] == 4:
        alpha = dress_resized[:, :, 3:4].astype(float) / 255.0
        dress_rgb = cv2.cvtColor(dress_resized[:, :, :3], cv2.COLOR_BGR2RGB)
        roi = user[y_start:y_start+h, x_start:x_start+w].astype(float)
        blended = (alpha * dress_rgb.astype(float) + (1 - alpha) * roi).astype(np.uint8)
        user[y_start:y_start+h, x_start:x_start+w] = blended
    else:
        dress_rgb = cv2.cvtColor(dress_resized[:, :, :3], cv2.COLOR_BGR2RGB)
        user[y_start:y_start+h, x_start:x_start+w] = dress_rgb

    return user


# ── Session State ─────────────────────────────────────────────
defaults = {
    "selected_dress": None,
    "selected_name": "",
    "y_pos": 0.22,
    "size": 0.68,
    "category": "casual",
    "step": 1
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── NAVBAR ────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div>
        <div class="brand-name">✦ Desi Chic</div>
        <div class="brand-tagline">Virtual Try-On Studio</div>
    </div>
    <div class="nav-links">
        <span class="nav-link active">Try-On</span>
        <span class="nav-link">Collection</span>
        <span class="nav-link">About</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)


# ── STEP INDICATOR ────────────────────────────────────────────
step = st.session_state.step

st.markdown(f"""
<div style='display:flex; align-items:center; gap:0; margin-bottom:36px; padding:0 8px;'>

    <div style='display:flex; align-items:center; gap:10px;'>
        <div style='width:28px; height:28px; border-radius:50%;
            background:{"#e8d5b0" if step >= 1 else "rgba(255,255,255,0.08)"};
            display:flex; align-items:center; justify-content:center;
            font-size:12px; font-weight:700;
            color:{"#0e0b16" if step >= 1 else "rgba(255,255,255,0.3)"};'>1</div>
        <span style='font-size:10px; letter-spacing:2px; text-transform:uppercase;
            color:{"#e8d5b0" if step >= 1 else "rgba(255,255,255,0.2)"};'>Upload Photo</span>
    </div>

    <div style='flex:1; height:1px; background:rgba(255,255,255,0.08); margin:0 16px;'></div>

    <div style='display:flex; align-items:center; gap:10px;'>
        <div style='width:28px; height:28px; border-radius:50%;
            background:{"#e8d5b0" if step >= 2 else "rgba(255,255,255,0.08)"};
            display:flex; align-items:center; justify-content:center;
            font-size:12px; font-weight:700;
            color:{"#0e0b16" if step >= 2 else "rgba(255,255,255,0.3)"};'>2</div>
        <span style='font-size:10px; letter-spacing:2px; text-transform:uppercase;
            color:{"#e8d5b0" if step >= 2 else "rgba(255,255,255,0.2)"};'>Select Dress</span>
    </div>

    <div style='flex:1; height:1px; background:rgba(255,255,255,0.08); margin:0 16px;'></div>

    <div style='display:flex; align-items:center; gap:10px;'>
        <div style='width:28px; height:28px; border-radius:50%;
            background:{"#e8d5b0" if step >= 3 else "rgba(255,255,255,0.08)"};
            display:flex; align-items:center; justify-content:center;
            font-size:12px; font-weight:700;
            color:{"#0e0b16" if step >= 3 else "rgba(255,255,255,0.3)"};'>3</div>
        <span style='font-size:10px; letter-spacing:2px; text-transform:uppercase;
            color:{"#e8d5b0" if step >= 3 else "rgba(255,255,255,0.2)"};'>Try On</span>
    </div>

</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# STEP 1 — UPLOAD PHOTO
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-label'>Step 01</div>
<div class='section-title'>Upload Your Photo</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    uploaded = st.file_uploader(
        "Upload full body photo — JPG or PNG",
        type=["jpg", "jpeg", "png"],
        key="photo_upload"
    )

    user_img = None
    if uploaded:
        user_img = Image.open(uploaded).convert("RGB")
        if st.session_state.step < 2:
            st.session_state.step = 2
        st.image(user_img, use_container_width=True)
    else:
        st.markdown("""
        <div class='upload-zone'>
            <div class='upload-icon'>⬆</div>
            <p class='upload-text'>Drop your photo here</p>
            <p class='upload-sub'>Full body • Front facing • Good lighting</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='padding: 24px; border: 1px solid rgba(232,213,176,0.08);
    border-radius:4px; background: rgba(255,255,255,0.01);'>
        <p style='font-size:10px !important; letter-spacing:3px; text-transform:uppercase;
        color:rgba(232,213,176,0.5) !important; margin-bottom:20px;'>Tips for best result</p>

        <div style='margin-bottom:16px; display:flex; gap:12px; align-items:flex-start;'>
            <span style='color:#e8d5b0; font-size:16px; margin-top:2px;'>◆</span>
            <div>
                <p style='color:rgba(255,255,255,0.7) !important; font-size:12px !important;
                margin:0 0 3px; font-weight:500;'>Full body photo</p>
                <p style='color:rgba(255,255,255,0.3) !important; font-size:11px !important; margin:0;'>
                Head to toe visible honi chahiye</p>
            </div>
        </div>

        <div style='margin-bottom:16px; display:flex; gap:12px; align-items:flex-start;'>
            <span style='color:#e8d5b0; font-size:16px; margin-top:2px;'>◆</span>
            <div>
                <p style='color:rgba(255,255,255,0.7) !important; font-size:12px !important;
                margin:0 0 3px; font-weight:500;'>Front facing pose</p>
                <p style='color:rgba(255,255,255,0.3) !important; font-size:11px !important; margin:0;'>
                Seedha khara hona best result deta hai</p>
            </div>
        </div>

        <div style='margin-bottom:16px; display:flex; gap:12px; align-items:flex-start;'>
            <span style='color:#e8d5b0; font-size:16px; margin-top:2px;'>◆</span>
            <div>
                <p style='color:rgba(255,255,255,0.7) !important; font-size:12px !important;
                margin:0 0 3px; font-weight:500;'>Background removed dress</p>
                <p style='color:rgba(255,255,255,0.3) !important; font-size:11px !important; margin:0;'>
                PNG with transparent background use karein</p>
            </div>
        </div>

        <div style='display:flex; gap:12px; align-items:flex-start;'>
            <span style='color:#e8d5b0; font-size:16px; margin-top:2px;'>◆</span>
            <div>
                <p style='color:rgba(255,255,255,0.7) !important; font-size:12px !important;
                margin:0 0 3px; font-weight:500;'>Achhi lighting</p>
                <p style='color:rgba(255,255,255,0.3) !important; font-size:11px !important; margin:0;'>
                Natural light ya bright room mein photo lein</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# STEP 2 — SELECT DRESS
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-label'>Step 02</div>
<div class='section-title'>Select a Dress</div>
""", unsafe_allow_html=True)

# Category selector
cat_cols = st.columns([1, 1, 1, 4])
with cat_cols[0]:
    if st.button("Casual", key="cat_casual",
                 type="primary" if st.session_state.category == "casual" else "secondary"):
        st.session_state.category = "casual"
        st.rerun()
with cat_cols[1]:
    if st.button("Formal", key="cat_formal",
                 type="primary" if st.session_state.category == "formal" else "secondary"):
        st.session_state.category = "formal"
        st.rerun()
with cat_cols[2]:
    if st.button("Bridal", key="cat_bridal",
                 type="primary" if st.session_state.category == "bridal" else "secondary"):
        st.session_state.category = "bridal"
        st.rerun()

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

folder_path = f"dresses/{st.session_state.category}"
os.makedirs(folder_path, exist_ok=True)

allowed_ext = [".png", ".jpg", ".jpeg"]
files = sorted([
    f for f in os.listdir(folder_path)
    if os.path.splitext(f)[1].lower() in allowed_ext
])

if len(files) == 0:
    st.markdown(f"""
    <div style='border:1px solid rgba(255,255,255,0.06); border-radius:4px;
    padding:60px 24px; text-align:center;'>
        <p style='font-size:32px; margin:0 0 16px;'>📂</p>
        <p style='font-size:13px !important; color:rgba(255,255,255,0.35) !important; margin:0;'>
            No dresses in this collection yet</p>
        <p style='font-size:10px !important; color:rgba(255,255,255,0.2) !important;
        letter-spacing:1px; margin-top:8px;'>
            Add PNG images to <code>dresses/{st.session_state.category}/</code>
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    dress_cols = st.columns(4)
    for i, filename in enumerate(files):
        dress_path = os.path.join(folder_path, filename)
        dress_name = (
            os.path.splitext(filename)[0]
            .replace("_", " ").replace("-", " ").title()
        )
        is_selected = st.session_state.selected_dress == dress_path

        with dress_cols[i % 4]:
            border = "rgba(232,213,176,0.7)" if is_selected else "rgba(255,255,255,0.06)"
            bg = "rgba(232,213,176,0.04)" if is_selected else "rgba(255,255,255,0.01)"
            shadow = "0 0 24px rgba(232,213,176,0.1)" if is_selected else "none"

            st.markdown(
                f"<div style='border:1px solid {border}; background:{bg};"
                f"border-radius:4px; overflow:hidden; box-shadow:{shadow};"
                f"transition:all 0.3s; margin-bottom:4px;'>",
                unsafe_allow_html=True
            )
            st.image(dress_path, use_container_width=True)
            st.markdown(
                f"<div style='padding:8px 10px;'>"
                f"<p style='font-size:9px !important; letter-spacing:1.5px;"
                f"text-transform:uppercase; margin:0;"
                f"color:{'#e8d5b0' if is_selected else 'rgba(255,255,255,0.4)'} !important;'>"
                f"{dress_name}</p></div>",
                unsafe_allow_html=True
            )

            btn_text = "✓ Selected" if is_selected else "Select"
            if st.button(btn_text, key=f"sel_{st.session_state.category}_{i}"):
                st.session_state.selected_dress = dress_path
                st.session_state.selected_name = dress_name
                if st.session_state.step < 3:
                    st.session_state.step = 3
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# STEP 3 — TRY ON
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-label'>Step 03</div>
<div class='section-title'>Virtual Try-On</div>
""", unsafe_allow_html=True)

if user_img is None and not st.session_state.selected_dress:
    st.markdown("""
    <div style='border:1px solid rgba(255,255,255,0.05); border-radius:4px;
    padding:60px; text-align:center;'>
        <p style='font-size:11px !important; letter-spacing:3px; text-transform:uppercase;
        color:rgba(255,255,255,0.2) !important;'>
            Complete Step 1 & 2 to see try-on result
        </p>
    </div>
    """, unsafe_allow_html=True)

elif user_img is None:
    st.info("↑ Step 1 mein apni photo upload karein")

elif not st.session_state.selected_dress:
    st.info("↑ Step 2 mein koi dress select karein")

else:
    result_col, control_col = st.columns([2, 1], gap="large")

    with control_col:
        st.markdown("""
        <p style='font-size:9px !important; letter-spacing:3px; text-transform:uppercase;
        color:rgba(232,213,176,0.5) !important; margin-bottom:16px;'>Adjust Fit</p>
        """, unsafe_allow_html=True)

        y_pos = st.slider("⬆ Position (Upar/Neeche)",
                          0.05, 0.55, st.session_state.y_pos, 0.01)
        size = st.slider("↔ Size (Bari/Choti)",
                         0.35, 1.0, st.session_state.size, 0.01)

        if y_pos != st.session_state.y_pos or size != st.session_state.size:
            st.session_state.y_pos = y_pos
            st.session_state.size = size

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # Selected dress preview
        st.markdown("""
        <p style='font-size:9px !important; letter-spacing:3px; text-transform:uppercase;
        color:rgba(232,213,176,0.5) !important; margin-bottom:10px;'>Selected</p>
        """, unsafe_allow_html=True)

        st.image(st.session_state.selected_dress, use_container_width=True)
        st.markdown(
            f"<p style='font-size:10px !important; letter-spacing:1px; text-transform:uppercase;"
            f"color:rgba(232,213,176,0.7) !important; margin-top:6px; text-align:center;'>"
            f"{st.session_state.selected_name}</p>",
            unsafe_allow_html=True
        )

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        if st.button("Change Dress", key="change"):
            st.session_state.selected_dress = None
            st.session_state.selected_name = ""
            st.session_state.step = 2
            st.rerun()

    with result_col:
        with st.spinner("Processing..."):
            result = smart_overlay(
                user_img,
                st.session_state.selected_dress,
                y_pos=st.session_state.y_pos,
                size=st.session_state.size
            )

        st.markdown("<div class='result-container'>", unsafe_allow_html=True)
        st.image(result, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        dl_col, buy_col = st.columns(2)

        result_pil = Image.fromarray(result)
        buf = io.BytesIO()
        result_pil.save(buf, format="PNG")
        buf.seek(0)

        with dl_col:
            st.download_button(
                "↓  Save Result",
                data=buf,
                file_name="desi_chic_tryon.png",
                mime="image/png"
            )
        with buy_col:
            st.link_button("Buy This Dress →", "https://example.com")


# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class='gold-divider'></div>
<div style='text-align:center; padding:16px 0 32px;'>
    <p style='font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size:18px !important; color:rgba(232,213,176,0.25) !important;
    letter-spacing:6px; text-transform:uppercase; margin:0;'>
    ✦ Desi Chic ✦</p>
    <p style='font-size:9px !important; letter-spacing:3px;
    color:rgba(255,255,255,0.1) !important; margin-top:6px;'>
    VIRTUAL TRY-ON STUDIO</p>
</div>
""", unsafe_allow_html=True)
