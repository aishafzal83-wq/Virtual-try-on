import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import io

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Virtual Desi Chic",
    page_icon="👗",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0518 0%, #12082a 50%, #0d1b38 100%);
        color: white;
    }
    h1, h2, h3 { color: #FFD700 !important; }
    .stButton > button {
        background: linear-gradient(135deg, #B8860B, #FFD700);
        color: #1a0a2e;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFD700, #FFA000);
    }
    [data-testid="stSidebar"] {
        background: rgba(10,5,30,0.98) !important;
        border-right: 1px solid rgba(255,215,0,0.15);
    }
</style>
""", unsafe_allow_html=True)


# ── Overlay Function ──────────────────────────────────────────
def overlay_dress(user_pil, dress_path):
    user = np.array(user_pil)
    uh, uw = user.shape[:2]

    dress_bgra = cv2.imread(dress_path, cv2.IMREAD_UNCHANGED)
    if dress_bgra is None:
        st.error(f"Dress load nahi hui: {dress_path}")
        return user

    target_h = int(uh * 0.65)
    target_w = int(uw * 0.75)
    dress_resized = cv2.resize(dress_bgra, (target_w, target_h))

    y_start = int(uh * 0.22)
    x_start = int((uw - target_w) / 2)
    h, w = dress_resized.shape[:2]

    if y_start + h > uh:
        h = uh - y_start
        dress_resized = dress_resized[:h, :]
    if x_start + w > uw:
        w = uw - x_start
        dress_resized = dress_resized[:, :w]

    if dress_resized.ndim == 3 and dress_resized.shape[2] == 4:
        alpha = dress_resized[:, :, 3:4] / 255.0
        dress_rgb = cv2.cvtColor(dress_resized[:, :, :3], cv2.COLOR_BGR2RGB)
        roi = user[y_start:y_start+h, x_start:x_start+w]
        blended = (alpha * dress_rgb + (1 - alpha) * roi).astype(np.uint8)
        user[y_start:y_start+h, x_start:x_start+w] = blended
    else:
        dress_rgb = cv2.cvtColor(dress_resized[:, :, :3], cv2.COLOR_BGR2RGB)
        user[y_start:y_start+h, x_start:x_start+w] = dress_rgb

    return user


# ── Session State ─────────────────────────────────────────────
if "selected_dress" not in st.session_state:
    st.session_state.selected_dress = None
if "selected_name" not in st.session_state:
    st.session_state.selected_name = ""


# ── Header ────────────────────────────────────────────────────
st.title("✦ Virtual Desi Chic")
st.markdown(
    "<p style='text-align:center; color:rgba(255,215,0,0.5);"
    "letter-spacing:3px; font-size:12px;'>"
    "PAKISTANI FASHION · VIRTUAL TRY-ON</p>",
    unsafe_allow_html=True
)
st.divider()


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛍 Categories")
    category = st.radio(
        "Category chunein:",
        options=["casual", "formal", "bridal"],
        format_func=lambda x: {
            "casual": "👘 Casual / Kurta",
            "formal": "✨ Formal / Party",
            "bridal": "👑 Bridal / Lehenga"
        }[x]
    )
    st.divider()

    if st.session_state.selected_dress:
        st.markdown("### ✅ Selected:")
        st.markdown(
            f"<p style='color:#FFD700; font-size:13px;'>"
            f"👗 {st.session_state.selected_name}</p>",
            unsafe_allow_html=True
        )
        if st.button("❌ Clear Selection"):
            st.session_state.selected_dress = None
            st.session_state.selected_name = ""
            st.rerun()
    else:
        st.markdown(
            "<p style='color:rgba(255,255,255,0.4); font-size:12px;'>"
            "Koi dress select nahi</p>",
            unsafe_allow_html=True
        )

    st.divider()
    st.markdown(
        "<p style='color:rgba(255,255,255,0.25); font-size:11px;'>"
        "💡 Apni dresses baad mein<br>"
        "<code>dresses/casual/</code><br>"
        "folder mein add kar sakti hain</p>",
        unsafe_allow_html=True
    )


# ── Main Layout ───────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")


# ── LEFT — Upload + Result ────────────────────────────────────
with col_left:
    st.markdown("### 📸 Apni Photo Upload Karein")

    uploaded = st.file_uploader(
        "Photo upload karein",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    user_img = None

    if uploaded:
        user_img = Image.open(uploaded).convert("RGB")
        st.image(user_img, caption="✅ Aapki Photo", use_container_width=True)
    else:
        st.markdown("""
        <div style='
            background: rgba(255,255,255,0.03);
            border: 2px dashed rgba(255,215,0,0.2);
            border-radius: 16px;
            padding: 60px 20px;
            text-align: center;
            color: rgba(255,255,255,0.3);
        '>
            <div style='font-size:48px'>📷</div>
            <p>Yahan photo upload karein</p>
            <p style='font-size:11px'>JPG ya PNG</p>
        </div>
        """, unsafe_allow_html=True)

    # Result
    if user_img is not None and st.session_state.selected_dress:
        st.markdown("---")
        st.markdown("### 🎉 Try-On Result")
        with st.spinner("✨ Processing..."):
            result = overlay_dress(user_img, st.session_state.selected_dress)
        st.image(result, caption="Virtual Try-On Preview", use_container_width=True)

        result_pil = Image.fromarray(result)
        buf = io.BytesIO()
        result_pil.save(buf, format="PNG")
        buf.seek(0)

        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "💾 Download",
                data=buf,
                file_name="tryon_result.png",
                mime="image/png"
            )
        with c2:
            st.link_button("🛒 Buy Now", "https://example.com")

    elif user_img is not None and not st.session_state.selected_dress:
        st.info("👉 Right side se koi dress select karein")
    elif user_img is None and st.session_state.selected_dress:
        st.info("👆 Apni photo upload karein")


# ── RIGHT — Dress Catalog ─────────────────────────────────────
with col_right:
    st.markdown(f"### 👗 {category.title()} Collection")

    folder_path = f"dresses/{category}"
    os.makedirs(folder_path, exist_ok=True)

    allowed_ext = [".png", ".jpg", ".jpeg"]
    files = sorted([
        f for f in os.listdir(folder_path)
        if os.path.splitext(f)[1].lower() in allowed_ext
    ])

    if len(files) == 0:
        st.markdown(f"""
        <div style='
            background: rgba(255,100,100,0.05);
            border: 2px dashed rgba(255,100,100,0.2);
            border-radius: 16px;
            padding: 40px 20px;
            text-align: center;
            color: rgba(255,255,255,0.35);
        '>
            <div style='font-size:40px'>📂</div>
            <p><strong>Folder empty hai!</strong></p>
            <p style='font-size:12px'>
                <code>dresses/{category}/</code><br>mein PNG images daalein
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        dress_cols = st.columns(3)
        for i, filename in enumerate(files):
            dress_path = os.path.join(folder_path, filename)
            dress_name = (
                os.path.splitext(filename)[0]
                .replace("_", " ").replace("-", " ").title()
            )
            is_selected = st.session_state.selected_dress == dress_path

            with dress_cols[i % 3]:
                border = "#FFD700" if is_selected else "rgba(255,255,255,0.08)"
                bg = "rgba(255,215,0,0.08)" if is_selected else "rgba(255,255,255,0.02)"

                st.markdown(
                    f"<div style='border:2px solid {border};"
                    f"background:{bg}; border-radius:12px; padding:8px;'>",
                    unsafe_allow_html=True
                )
                st.image(dress_path, use_container_width=True)
                st.markdown(
                    f"<p style='color:rgba(255,255,255,0.7); font-size:11px;"
                    f"text-align:center; margin:4px 0;'>{dress_name}</p>",
                    unsafe_allow_html=True
                )
                btn_label = "✅ Selected" if is_selected else "👗 Try This"
                if st.button(btn_label, key=f"dress_{category}_{i}"):
                    st.session_state.selected_dress = dress_path
                    st.session_state.selected_name = dress_name
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:rgba(255,255,255,0.15);"
    "font-size:11px; letter-spacing:2px;'>"
    "✦ VIRTUAL DESI CHIC · Made with Streamlit ✦</p>",
    unsafe_allow_html=True
)
