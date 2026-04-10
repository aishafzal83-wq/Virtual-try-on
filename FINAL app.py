import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="Virtual Try-On", layout="wide")

st.title("👗 AI Virtual Try-On System (Pakistani Dresses)")

# -----------------------
# Upload Image
# -----------------------
uploaded_file = st.file_uploader("Upload Full Body Image", type=["png","jpg","jpeg"])

user_img = None

if uploaded_file:
    user_img = Image.open(uploaded_file)
    st.image(user_img, caption="Your Image", use_column_width=True)

# -----------------------
# Category Selection
# -----------------------
st.sidebar.title("Filters")

category = st.sidebar.selectbox("Select Category", ["casual", "formal", "bridal"])

# -----------------------
# Load Dresses
# -----------------------
dress_folder = f"dresses/{category}"

dress_files = []
if os.path.exists(dress_folder):
    dress_files = os.listdir(dress_folder)

selected_dress_path = None

st.subheader(f"{category.capitalize()} Dresses")

cols = st.columns(3)

for i, dress_name in enumerate(dress_files):
    dress_path = os.path.join(dress_folder, dress_name)

    with cols[i % 3]:
        dress_img = Image.open(dress_path)
        st.image(dress_img, use_column_width=True)

        if st.button(f"Try {dress_name}", key=dress_name):
            selected_dress_path = dress_path

# -----------------------
# Overlay Function
# -----------------------
def overlay_dress(user_img, dress_path):
    user = np.array(user_img)
    dress = cv2.imread(dress_path, cv2.IMREAD_UNCHANGED)

    user_h, user_w = user.shape[:2]

    dress = cv2.resize(dress, (user_w, int(user_h * 0.6)))

    y_offset = int(user_h * 0.3)
    x_offset = 0

    if dress.shape[2] == 4:
        alpha = dress[:, :, 3] / 255.0
        for c in range(3):
            user[y_offset:y_offset+dress.shape[0], x_offset:x_offset+dress.shape[1], c] = \
                alpha * dress[:, :, c] + (1 - alpha) * user[y_offset:y_offset+dress.shape[0], x_offset:x_offset+dress.shape[1], c]
    else:
        user[y_offset:y_offset+dress.shape[0], x_offset:x_offset+dress.shape[1]] = dress

    return user

# -----------------------
# RESULT
# -----------------------
if user_img and selected_dress_path:
    st.subheader("Result")

    result = overlay_dress(user_img, selected_dress_path)

    st.image(result, use_column_width=True)

    # Save result
    if st.button("💾 Save Result"):
        if not os.path.exists("outputs"):
            os.mkdir("outputs")
        output_path = "outputs/result.png"
        cv2.imwrite(output_path, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
        st.success("Saved Successfully!")

    # Buy Now
    st.markdown("[🛍️ Buy Now](https://example.com)", unsafe_allow_html=True)

# -----------------------
# Extra Features Info
# -----------------------
st.markdown("---")
st.write("✔ Category Filters")
st.write("✔ Dress Selection Gallery")
st.write("✔ Virtual Try-On")
st.write("✔ Save Output")
st.write("✔ Buy Redirect System")
