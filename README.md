# 🔐 LSB-Based Steganography System  
**Securely Hide & Extract Messages in Images**  

## 📌 Project Overview  
This **LSB-Based Steganography System** is a **Streamlit-based** web application that allows users to **hide secret messages inside images** using **Least Significant Bit (LSB) Steganography** combined with **password-protected encryption**. The system ensures secure message transmission and retrieval while maintaining the image's appearance.  

## ✨ Features  
✔ **LSB Steganography** – Hides encrypted text within an image.  
✔ **Password-Protected Encryption** – Uses **Fernet Encryption** to ensure secure message encoding.  
✔ **Dual Input Options** – Supports **manual text input** and **text file upload** for encoding.  
✔ **Secure Message Retrieval** – Extracts and decrypts messages only with the correct password.  
✔ **Downloadable Encoded Images** – Allows users to save the **steganographic** image.  
✔ **Downloadable Decoded Messages** – Extracted messages can be downloaded as text files.  
✔ **User-Friendly Interface** – Built with **Streamlit** for an easy-to-use web experience.  

---

## 🛠 Technologies Used  
- **Python** 🐍 – Core programming language.  
- **Streamlit** 🎨 – Web interface development.  
- **OpenCV (cv2)** 📷 – Image processing.  
- **NumPy** 🔢 – Handling pixel data.  
- **Fernet Encryption (cryptography library)** 🔐 – Secure message encryption & decryption.  
- **PIL (Pillow)** 🖼️ – Image handling in Python.  

---

## 🚀 Installation & Setup  

### 🔹 Prerequisites  
Ensure you have **Python 3.7+** installed. You can check your Python version with:  
```bash
python --version
```

### 🔹 Install Required Libraries  
Use the following command to install dependencies:  
```bash
pip install -r requirements.txt
```

### 🔹 Run the Application  
To start the Streamlit app, navigate to the project folder and run:  
```bash
streamlit run Stegno.py
```

---

## 📜 How to Use the Tool  

### **🛠 Encoding (Hiding a Secret Message)**
1️⃣ **Upload a Cover Image** (PNG, JPG, JPEG).  
2️⃣ Choose how you want to input the message:  
   - **✏ Enter text manually**.  
   - **📄 Upload a text file** (.txt).  
3️⃣ **Enter a Password** to encrypt the message.  
4️⃣ Click **"🔒 Encode & Download Image"** – The encoded image will be available for download.  

### **🔍 Decoding (Extracting a Secret Message)**
1️⃣ **Upload the Encoded Image** (the image with hidden data).  
2️⃣ **Enter the correct Password** used during encoding.  
3️⃣ Click **"🔍 Decode Message"** – If the password is correct, the message will be displayed.  
4️⃣ **Download the extracted message** as a text file if needed.  

---

## ⚠️ Important Notes  
- Only images encoded using **this system** can be decoded correctly.  
- Using an **incorrect password** during decryption will result in an error.  
- The system uses **Fernet encryption**, which requires a **32-byte base64 key**, ensuring high security.  

---

## 🖥️ Demo Screenshot  
![screencapture-localhost-8501-2025-02-22-10_17_00](https://github.com/user-attachments/assets/b35fd4ea-54fa-4438-b50f-9b76b5b0b07e)
**🔹 For demo purposes, we have provided an encoded image (encoded_image.png) in the repository. You can try decoding it using the password:** `123456789` 🔓🖼️  



---

## 📌 Future Enhancements  
🚀 **Support for More Image Formats (BMP, GIF, etc.)**  
🔐 **AES-256 Encryption for Enhanced Security**  
📱 **Mobile-Friendly UI Improvements**  
📡 **Cloud Integration for Remote Access**  
