import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import io

st.set_page_config(
    page_title="DESI CHIC — Try On",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CSS — Sapphire / Khaadi brand level
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Jost', sans-serif !important;
    background-color: #FAFAF8 !important;
    color: #1a1a1a !important;
}

.stApp { background: #FAFAF8 !important; }

#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton, div[data-testid="stToolbar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #1a1a1a !important;
    font-weight: 400 !important;
}

p { color: #555 !important; font-size: 13px !important; }

/* ── TOP NAV ── */
.topnav {
    background: #fff;
    border-bottom: 1px solid #e8e4de;
    padding: 0 60px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
}
.logo {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 22px;
    font-weight: 500;
    letter-spacing: 6px;
    color: #1a1a1a;
    text-transform: uppercase;
}
.nav-items {
    display: flex;
    gap: 36px;
}
.nav-item {
    font-size: 11px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #888;
    cursor: pointer;
}
.nav-item.active { color: #1a1a1a; border-bottom: 1px solid #1a1a1a; padding-bottom: 2px; }

/* ── HERO STRIP ── */
.hero-strip {
    background: #1a1a1a;
    color: #e8d5b0;
    text-align: center;
    padding: 10px;
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
}

/* ── SECTION ── */
.section-wrap {
    padding: 48px 60px;
}
.section-tag {
    font-size: 9px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #b5a48a;
    margin-bottom: 8px;
}
.section-heading {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 28px;
    font-weight: 400;
    color: #1a1a1a;
    margin: 0 0 32px;
    letter-spacing: 1px;
}

/* ── UPLOAD BOX ── */
.upload-box {
    border: 1px solid #e0dbd4;
    background: #fff;
    border-radius: 2px;
    padding: 48px 24px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s;
}
.upload-box:hover { border-color: #b5a48a; }

/* ── DRESS CARD ── */
.dress-card {
    background: #fff;
    border: 1px solid #ede9e3;
    border-radius: 2px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.25s ease;
    position: relative;
}
.dress-card:hover {
    border-color: #b5a48a;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    transform: translateY(-2px);
}
.dress-card.selected {
    border-color: #1a1a1a;
    box-shadow: 0 4px 24px rgba(0,0,0,0.1);
}
.dress-card-name {
    padding: 12px 14px;
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #888;
}
.selected-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #1a1a1a;
    color: #e8d5b0;
    font-size: 8px;
    letter-spacing: 2px;
    padding: 4px 8px;
    text-transform: uppercase;
}

/* ── CAT PILLS ── */
.cat-row {
    display: flex;
    gap: 8px;
    margin-bottom: 28px;
}
.cat-pill {
    border: 1px solid #e0dbd4;
    padding: 7px 20px;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #888;
    cursor: pointer;
    border-radius: 1px;
    background: #fff;
    transition: all 0.2s;
}
.cat-pill:hover { border-color: #1a1a1a; color: #1a1a1a; }
.cat-pill.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }

/* ── RESULT PANEL ── */
.result-panel {
    background: #fff;
    border: 1px solid #ede9e3;
    border-radius: 2px;
    overflow: hidden;
}
.result-label {
    background: #1a1a1a;
    color: #e8d5b0;
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 8px 16px;
    text-align: center;
}

/* ── DIVIDER ── */
.brand-divider {
    border: none;
    border-top: 1px solid #e8e4de;
    margin: 0;
}

/* ── STREAMLIT WIDGET OVERRIDES ── */
.stButton > button {
    background: #1a1a1a !important;
    color: #fff !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 1px !important;
    padding: 13px 28px !important;
    width: 100% !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background: #333 !important;
}

div[data-testid="stFileUploader"] {
    background: #fff !important;
    border: 1px solid #e0dbd4 !important;
    border-radius: 2px !important;
    padding: 20px 24px !important;
}
div[data-testid="stFileUploader"] label p {
    font-family: 'Jost', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: #999 !important;
}
div[data-testid="stFileUploader"] section {
    border: 1px dashed #d5cfc8 !important;
    border-radius: 2px !important;
    background: #faf9f7 !important;
    padding: 24px !important;
}

.stDownloadButton > button {
    background: transparent !important;
    color: #1a1a1a !important;
    border: 1px solid #1a1a1a !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    border-radius: 1px !important;
    padding: 13px 28px !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background: #1a1a1a !important;
    color: #fff !important;
}

.stSlider label p {
    font-family: 'Jost', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #888 !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #1a1a1a !important;
    border-color: #1a1a1a !important;
}

.stInfo {
    background: #faf8f5 !important;
    border: 1px solid #e8e4de !important;
    border-radius: 2px !important;
    color: #888 !important;
    font-size: 12px !important;
}
.stInfo p { color: #888 !important; font-size: 12px !important; }

.stSpinner p {
    font-family: 'Jost', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    color: #888 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SMART FIT FUNCTION
# ─────────────────────────────────────────────
def fit_dress_on_person(user_pil, dress_path, y_pos, size):
    """
    Dress image ko user photo pe smartly fit karta hai.
    Transparent PNG use karo best result ke liye.
    """
    user_arr = np.array(user_pil.copy())
    uh, uw = user_arr.shape[:2]

    dress = cv2.imread(dress_path, cv2.IMREAD_UNCHANGED)
    if dress is None:
        st.error("Dress image load nahi hui.")
        return user_arr

    dh, dw = dress.shape[:2]
    tw = int(uw * size)
    th = int(tw * (dh / dw))

    if th > int(uh * 0.80):
        th = int(uh * 0.80)
        tw = int(th * (dw / dh))

    dress = cv2.resize(dress, (tw, th), interpolation=cv2.INTER_LANCZOS4)

    xs = max(0, (uw - tw) // 2)
    ys = int(uh * y_pos)

    h, w = dress.shape[:2]
    if ys + h > uh: h = uh - ys
    if xs + w > uw: w = uw - xs
    dress = dress[:h, :w]

    channels = dress.shape[2] if dress.ndim == 3 else 1

    if channels == 4:
        alpha = dress[:, :, 3:4].astype(np.float32) / 255.0
        d_rgb = cv2.cvtColor(dress[:, :, :3], cv2.COLOR_BGR2RGB).astype(np.float32)
        roi = user_arr[ys:ys+h, xs:xs+w].astype(np.float32)
        blended = (alpha * d_rgb + (1.0 - alpha) * roi).astype(np.uint8)
        user_arr[ys:ys+h, xs:xs+w] = blended
    else:
        d_rgb = cv2.cvtColor(dress[:, :, :3], cv2.COLOR_BGR2RGB)
        user_arr[ys:ys+h, xs:xs+w] = d_rgb

    return user_arr


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for k, v in {
    "dress": None,
    "dname": "",
    "cat": "casual",
    "yp": 0.18,
    "sz": 0.62,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="topnav">
    <div class="logo">Desi Chic</div>
    <div class="nav-items">
        <span class="nav-item active">Try On</span>
        <span class="nav-item">New Arrivals</span>
        <span class="nav-item">Collections</span>
        <span class="nav-item">About</span>
    </div>
</div>
<div class="hero-strip">
    Free Shipping on Orders Over PKR 3,000 &nbsp;·&nbsp; New Collection Now Live
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 1 — UPLOAD
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-wrap" style="padding-bottom:0;">
    <p class="section-tag">Step 01 of 03</p>
    <p class="section-heading">Upload Your Photo</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='padding:0 60px;'>", unsafe_allow_html=True)
    col_up, col_tips = st.columns([1, 1], gap="large")

    with col_up:
        uploaded = st.file_uploader(
            "UPLOAD FULL BODY PHOTO",
            type=["jpg", "jpeg", "png"],
            key="uploader"
        )
        user_img = None
        if uploaded:
            user_img = Image.open(uploaded).convert("RGB")
            st.image(user_img, use_container_width=True)

    with col_tips:
        st.markdown("""
        <div style="background:#fff; border:1px solid #ede9e3;
        border-radius:2px; padding:32px;">
            <p style="font-size:9px !important; letter-spacing:4px;
            text-transform:uppercase; color:#b5a48a !important;
            margin-bottom:24px;">Photo Guide</p>

            <div style="display:flex; gap:16px; margin-bottom:20px; align-items:flex-start;">
                <div style="width:32px; height:32px; background:#faf8f5;
                border:1px solid #e8e4de; display:flex; align-items:center;
                justify-content:center; flex-shrink:0; font-size:14px;">①</div>
                <div>
                    <p style="color:#1a1a1a !important; font-size:12px !important;
                    font-weight:500; margin:0 0 4px;">Full body visible</p>
                    <p style="color:#999 !important; font-size:11px !important; margin:0;">
                    Head to toe photo best result deti hai</p>
                </div>
            </div>

            <div style="display:flex; gap:16px; margin-bottom:20px; align-items:flex-start;">
                <div style="width:32px; height:32px; background:#faf8f5;
                border:1px solid #e8e4de; display:flex; align-items:center;
                justify-content:center; flex-shrink:0; font-size:14px;">②</div>
                <div>
                    <p style="color:#1a1a1a !important; font-size:12px !important;
                    font-weight:500; margin:0 0 4px;">Front facing pose</p>
                    <p style="color:#999 !important; font-size:11px !important; margin:0;">
                    Seedha camera ki taraf dekhen</p>
                </div>
            </div>

            <div style="display:flex; gap:16px; margin-bottom:20px; align-items:flex-start;">
                <div style="width:32px; height:32px; background:#faf8f5;
                border:1px solid #e8e4de; display:flex; align-items:center;
                justify-content:center; flex-shrink:0; font-size:14px;">③</div>
                <div>
                    <p style="color:#1a1a1a !important; font-size:12px !important;
                    font-weight:500; margin:0 0 4px;">Good lighting</p>
                    <p style="color:#999 !important; font-size:11px !important; margin:0;">
                    Natural ya bright indoor light use karein</p>
                </div>
            </div>

            <div style="display:flex; gap:16px; align-items:flex-start;">
                <div style="width:32px; height:32px; background:#faf8f5;
                border:1px solid #e8e4de; display:flex; align-items:center;
                justify-content:center; flex-shrink:0; font-size:14px;">④</div>
                <div>
                    <p style="color:#1a1a1a !important; font-size:12px !important;
                    font-weight:500; margin:0 0 4px;">Transparent dress PNG</p>
                    <p style="color:#999 !important; font-size:11px !important; margin:0;">
                    remove.bg se background hatayein</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr class='brand-divider' style='margin:48px 0 0;'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 2 — SELECT DRESS
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-wrap" style="padding-bottom:0;">
    <p class="section-tag">Step 02 of 03</p>
    <p class="section-heading">Choose Your Dress</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='padding:0 60px;'>", unsafe_allow_html=True)

    cat_c1, cat_c2, cat_c3, cat_rest = st.columns([0.7, 0.7, 0.7, 5])
    with cat_c1:
        if st.button("Casual"):
            st.session_state.cat = "casual"
            st.rerun()
    with cat_c2:
        if st.button("Formal"):
            st.session_state.cat = "formal"
            st.rerun()
    with cat_c3:
        if st.button("Bridal"):
            st.session_state.cat = "bridal"
            st.rerun()

    st.markdown(
        f"<p style='font-size:9px !important; letter-spacing:3px; "
        f"text-transform:uppercase; color:#b5a48a !important; margin:12px 0 20px;'>"
        f"Collection: {st.session_state.cat.upper()}</p>",
        unsafe_allow_html=True
    )

    folder = f"dresses/{st.session_state.cat}"
    os.makedirs(folder, exist_ok=True)
    exts = [".png", ".jpg", ".jpeg"]
    files = sorted([f for f in os.listdir(folder)
                    if os.path.splitext(f)[1].lower() in exts])

    if not files:
        st.markdown(f"""
        <div style="border:1px solid #e8e4de; border-radius:2px;
        padding:60px; text-align:center; background:#fff;">
            <p style="font-size:11px !important; letter-spacing:3px;
            text-transform:uppercase; color:#ccc !important;">
            No dresses in dresses/{st.session_state.cat}/ folder</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        dcols = st.columns(4, gap="medium")
        for i, fname in enumerate(files):
            fpath = os.path.join(folder, fname)
            dname = os.path.splitext(fname)[0].replace("_"," ").replace("-"," ").title()
            is_sel = st.session_state.dress == fpath

            with dcols[i % 4]:
                border = "#1a1a1a" if is_sel else "#ede9e3"
                shadow = "0 4px 20px rgba(0,0,0,0.1)" if is_sel else "none"
                st.markdown(
                    f"<div style='border:1px solid {border}; border-radius:2px; "
                    f"overflow:hidden; background:#fff; box-shadow:{shadow}; "
                    f"margin-bottom:4px; position:relative;'>",
                    unsafe_allow_html=True
                )
                if is_sel:
                    st.markdown(
                        "<div style='position:absolute; top:8px; right:8px; "
                        "background:#1a1a1a; color:#e8d5b0; font-size:8px; "
                        "letter-spacing:1.5px; padding:4px 8px; "
                        "text-transform:uppercase; z-index:10;'>Selected</div>",
                        unsafe_allow_html=True
                    )
                st.image(fpath, use_container_width=True)
                st.markdown(
                    f"<p style='padding:10px 12px; font-size:9px !important; "
                    f"letter-spacing:1.5px; text-transform:uppercase; "
                    f"color:{'#1a1a1a' if is_sel else '#999'} !important; margin:0;'>"
                    f"{dname}</p>",
                    unsafe_allow_html=True
                )
                if st.button("Select" if not is_sel else "✓ Selected",
                             key=f"btn_{st.session_state.cat}_{i}"):
                    st.session_state.dress = fpath
                    st.session_state.dname = dname
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr class='brand-divider' style='margin:48px 0 0;'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 3 — TRY ON RESULT
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-wrap" style="padding-bottom:0;">
    <p class="section-tag">Step 03 of 03</p>
    <p class="section-heading">Your Look</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='padding:0 60px 60px;'>", unsafe_allow_html=True)

    if not user_img and not st.session_state.dress:
        st.markdown("""
        <div style="border:1px solid #e8e4de; padding:60px; text-align:center;
        background:#fff; border-radius:2px;">
            <p style="font-size:11px !important; letter-spacing:3px;
            text-transform:uppercase; color:#ccc !important;">
            Complete Step 1 and Step 2 above</p>
        </div>
        """, unsafe_allow_html=True)
    elif not user_img:
        st.info("Please upload your photo in Step 1")
    elif not st.session_state.dress:
        st.info("Please select a dress in Step 2")
    else:
        left, right = st.columns([2, 1], gap="large")

        with right:
            st.markdown(
                "<p style='font-size:9px !important; letter-spacing:3px; "
                "text-transform:uppercase; color:#b5a48a !important; "
                "margin-bottom:16px;'>Adjust Fitting</p>",
                unsafe_allow_html=True
            )
            yp = st.slider("Vertical Position", 0.05, 0.50,
                           st.session_state.yp, 0.01, key="yslider")
            sz = st.slider("Dress Size", 0.30, 0.95,
                           st.session_state.sz, 0.01, key="sslider")
            st.session_state.yp = yp
            st.session_state.sz = sz

            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

            st.markdown(
                "<p style='font-size:9px !important; letter-spacing:3px; "
                "text-transform:uppercase; color:#b5a48a !important; "
                "margin-bottom:12px;'>Selected</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div style='border:1px solid #ede9e3; border-radius:2px; "
                "overflow:hidden; background:#fff;'>",
                unsafe_allow_html=True
            )
            st.image(st.session_state.dress, use_container_width=True)
            st.markdown(
                f"<p style='padding:10px; font-size:9px !important; "
                f"letter-spacing:1.5px; text-transform:uppercase; "
                f"text-align:center; color:#1a1a1a !important;'>"
                f"{st.session_state.dname}</p></div>",
                unsafe_allow_html=True
            )

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            if st.button("Change Dress", key="change_btn"):
                st.session_state.dress = None
                st.session_state.dname = ""
                st.rerun()

        with left:
            with st.spinner("Creating your look..."):
                result = fit_dress_on_person(
                    user_img,
                    st.session_state.dress,
                    st.session_state.yp,
                    st.session_state.sz
                )

            st.markdown(
                "<div style='border:1px solid #ede9e3; background:#fff; "
                "border-radius:2px; overflow:hidden;'>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div style='background:#1a1a1a; text-align:center; "
                "padding:8px; font-size:9px; letter-spacing:3px; "
                "color:#e8d5b0; text-transform:uppercase;'>"
                "Your Virtual Try-On</div>",
                unsafe_allow_html=True
            )
            st.image(result, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            result_pil = Image.fromarray(result)
            buf = io.BytesIO()
            result_pil.save(buf, format="PNG")
            buf.seek(0)

            bc1, bc2 = st.columns(2, gap="small")
            with bc1:
                st.download_button(
                    "Download Look",
                    data=buf,
                    file_name="desi_chic_look.png",
                    mime="image/png"
                )
            with bc2:
                st.link_button("Buy This Dress", "https://example.com")

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="background:#1a1a1a; padding:40px 60px; margin-top:0;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <p style="font-family:'Playfair Display',serif !important;
            font-size:18px !important; color:#e8d5b0 !important;
            letter-spacing:5px; text-transform:uppercase; margin:0;">Desi Chic</p>
            <p style="font-size:10px !important; color:rgba(255,255,255,0.3) !important;
            letter-spacing:2px; margin-top:4px;">Virtual Try-On Studio</p>
        </div>
        <p style="font-size:10px !important; color:rgba(255,255,255,0.25) !important;
        letter-spacing:2px;">© 2025 Desi Chic. All rights reserved.</p>
    </div>
</div>
""", unsafe_allow_html=True)
