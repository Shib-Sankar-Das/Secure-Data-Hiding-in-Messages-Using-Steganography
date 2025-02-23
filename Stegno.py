import streamlit as st  # For web interface
#import cv2  # OpenCV for image processing
import numpy as np  # Handling image data
from cryptography.fernet import Fernet  # For encryption/decryption
from PIL import Image  # Handling images in Streamlit
import os  # File operations
import io  # Handling file streams

# Generate or load encryption key
KEY_FILE = "secret.key"


def generate_key():
    """Generate and save an encryption key."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key


def load_key():
    """Load the existing encryption key."""
    if os.path.exists(KEY_FILE):
        return open(KEY_FILE, "rb").read()
    else:
        return generate_key()


key = load_key()
cipher = Fernet(key)


# Function to encrypt message
def encrypt_message(message, password):
    """Encrypt the message with a password."""
    encryption_cipher = Fernet(key)
    encrypted_msg = encryption_cipher.encrypt(message.encode())
    return key + encrypted_msg  # Store key in the message for decryption


# Function to hide message in an image
def hide_message(image, message):
    """Embed the encrypted message into an image using LSB."""
    binary_msg = ''.join(format(byte, '08b') for byte in message)
    binary_msg += "1111111111111110"  # Stop marker

    img = np.array(image)
    idx = 0

    try:
        for row in img:
            for pixel in row:
                for channel in range(3):  # R, G, B channels
                    if idx < len(binary_msg):
                        pixel[channel] = (pixel[channel] & ~1) | int(binary_msg[idx])
                        idx += 1
                    else:
                        break

        encoded_img = Image.fromarray(img)
        return encoded_img
    except Exception as e:
        st.error(f"Error embedding message: {e}")
        return None


# Function to extract message from an image
def extract_message(image):
    """Extract the hidden binary message from the image."""
    binary_msg = ""
    img = np.array(image)

    try:
        for row in img:
            for pixel in row:
                for channel in range(3):  # R, G, B channels
                    binary_msg += str(pixel[channel] & 1)

        # Locate stop marker
        end_marker = "1111111111111110"
        index = binary_msg.find(end_marker)
        if index == -1:
            return None

        binary_msg = binary_msg[:index]
        byte_data = [binary_msg[i:i + 8] for i in range(0, len(binary_msg), 8)]
        extracted_data = bytes([int(byte, 2) for byte in byte_data])
        return extracted_data
    except Exception as e:
        st.error(f"Error extracting message: {e}")
        return None


# Function to decrypt message
def decrypt_message(encrypted_data, password):
    """Decrypt the extracted message using AES encryption."""
    try:
        extracted_key = encrypted_data[:44]
        encrypted_msg = encrypted_data[44:]
        decryption_cipher = Fernet(extracted_key)
        decrypted_msg = decryption_cipher.decrypt(encrypted_msg).decode()
        return decrypted_msg
    except Exception:
        return None  # If decryption fails


# Streamlit Sidebar
st.set_page_config(page_title="LSB Steganography", page_icon="🔐", layout="centered")
st.sidebar.title("LSB-Based Steganography")
app_mode = st.sidebar.radio("Select Mode", ["HOME", "ENCODE MESSAGE", "DECODE MESSAGE"])

# Home Page
if app_mode == "HOME":
    st.markdown("<h1 style='text-align: center;'>🔐 LSB-Based Steganography System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Securely Hide & Extract Messages in Images</h3>",
                unsafe_allow_html=True)

    st.markdown("""
        ## 🔒 How to Use - Encryption:
        1. **Upload a Cover Image** - Choose a PNG, JPG, or JPEG image.
        2. **Enter a Secret Message or Upload a Text File** - Either type the message directly or upload a text file.
        3. **Set a Password for Encryption** - This password will be required for decryption.
        4. **Click "Encode & Download Image"** - The image will now contain the hidden message.
        5. **Download the Encoded Image** - Save the image for later decryption.
    """, unsafe_allow_html=True)

    st.markdown("""
        ## 🔓 How to Use - Decryption:
        1. **Upload the Encoded Image** - Choose the image that contains the hidden message.
        2. **Enter the Correct Password** - This must match the password used during encryption.
        3. **Click "Decode Message"** - The hidden message will be extracted and displayed.
        4. **Download the Decoded Message** - Save the extracted message as a text file if needed.
    """, unsafe_allow_html=True)

    #st.image("Diseases.png")  # Change this to a relevant image for your project

# Encoding Page
elif app_mode == "ENCODE MESSAGE":
    st.title("🛠 Encode Message into Image")

    uploaded_image = st.file_uploader("📂 Upload Cover Image", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        input_type = st.radio("Select Input Type", ["✏ Enter Text", "📄 Upload Text File"])

        if input_type == "✏ Enter Text":
            message = st.text_area("Enter the secret message")
        else:
            text_file = st.file_uploader("📄 Upload a Text File", type=["txt"])
            if text_file is not None:
                message = text_file.read().decode()
            else:
                message = ""

        password = st.text_input("🔑 Enter Password for Encryption", type="password")

        if st.button("🔒 Encode & Download Image"):
            if uploaded_image and message and password:
                image = Image.open(uploaded_image)
                encrypted_message = encrypt_message(message, password)
                encoded_img = hide_message(image, encrypted_message)

                if encoded_img:
                    st.success("✅ Encoding Successful! Download the Image Below")
                    img_buffer = io.BytesIO()
                    encoded_img.save(img_buffer, format="PNG")
                    img_buffer.seek(0)

                    st.download_button(
                        label="📥 Download Encoded Image",
                        data=img_buffer,
                        file_name="encoded_image.png",
                        mime="image/png"
                    )
            else:
                st.warning("⚠ Please provide all inputs!")

# Decoding Page
elif app_mode == "DECODE MESSAGE":
    st.title("🔓 Decode Message from Image")

    uploaded_encoded_image = st.file_uploader("📂 Upload the Encoded Image", type=["png", "jpg", "jpeg"])
    if uploaded_encoded_image:
        image = Image.open(uploaded_encoded_image)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    password = st.text_input("🔑 Enter Password for Decryption", type="password")

    if st.button("🔍 Decode Message"):
        if uploaded_encoded_image and password:
            image = Image.open(uploaded_encoded_image)
            extracted_data = extract_message(image)

            if extracted_data:
                decrypted_msg = decrypt_message(extracted_data, password)
                if decrypted_msg:
                    st.success("✅ Message Successfully Decoded!")
                    st.text_area("📜 Hidden Message", decrypted_msg, height=150)

                    # Downloadable text file
                    text_file = io.BytesIO()
                    text_file.write(decrypted_msg.encode())
                    text_file.seek(0)

                    st.download_button(
                        label="📥 Download Decoded Message",
                        data=text_file,
                        file_name="decoded_message.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("❌ Incorrect password or corrupted data!")
            else:
                st.error("❌ No hidden message found!")
        else:
            st.warning("⚠ Please upload an image and enter the password!")
