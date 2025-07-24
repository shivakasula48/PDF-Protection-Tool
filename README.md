# 🔐 Advanced PDF Protection Tool Using Python

A comprehensive command-line tool to **encrypt PDF files** with a **strong password**, featuring:

✅ Password validation & strength check  
✅ Compression option  
✅ Encrypted input file handling  
✅ Metadata preservation  
✅ User-friendly prompts and error handling

---

## 📁 Project Information
 
- **Language**: Python 3  
- **Library Used**: [`PyPDF2`](https://pypi.org/project/PyPDF2/)  
- **Purpose**: Secure PDF documents with password encryption using Python  

---

## 📦 Features

- 📌 Validate input/output file paths  
- 🔒 Confirm password with strength analysis (`Weak`, `Medium`, `Strong`)  
- 🔁 Encrypts even previously encrypted PDFs (if user provides correct password)  
- 📄 Preserves PDF metadata (title, author, etc.)  
- 📉 Optional compression to reduce PDF size  
- 📊 File size comparison after encryption  
- 🧼 Clean command-line interface and graceful error handling  

---

## 🧰 Prerequisites

Install PyPDF2:

```bash
pip install PyPDF2
```

## 🚀 Usage

```bash
python3 protect_pdf.py
```

### 🧭 Interactive Prompts

1. **Enter input PDF file path**  
2. **Review file details**, including:
   - Total pages  
   - File size  
   - Encryption status  
   - Metadata (if any)  
3. **Enter output PDF path**  
   - ⚠️ Warns if the file already exists (with overwrite option)  
4. **Set and confirm a secure password**  
5. **Choose whether to enable compression**  
6. ✅ The tool encrypts and saves the output PDF securely, with real-time feedback


---

## 🔑 Password Guidelines

- Minimum **4 characters** required
- Displays password strength: **Weak**, **Medium**, **Strong**
- ⚠️ Warns users when a password is **Weak**
  - Offers an option to **retry** and enter a stronger password

---

## 📌 Example Walkthrough

```
🔒 PDF Encryption Tool
==================================================
Enter input PDF file path: /home/user/documents/file.pdf

📄 File Information:
   Pages: 5
   Size: 423.3 KB
   Already encrypted: No
   Title: My Report
   Author: John Doe

Enter output PDF file path: /home/user/output/encrypted.pdf

🔑 Password Setup:
Enter password for PDF encryption: *********
Confirm password: *********
Password strength: Strong

⚙️  Additional Options:
Enable compression to reduce file size? (y/n): y

🔄 Encrypting PDF...

✅ Success! Password-protected PDF created.
📁 Output file: /home/user/output/encrypted.pdf
📊 Original size: 423.3 KB
📊 New size: 310.8 KB
📉 Size reduction: 26.6%

🛡️  Your PDF is now protected with a password!
```
---

## 🧬 Cloning the Repository

```bash
git clone https://github.com/shivakasula48/pdf-protection-tool.git
cd pdf-protection-tool
```


---
## 🧠 Key Functions Explained

### `validate_file_path(path, check_exists)`
- Validates the given file path
- Ensures it's a `.pdf` file
- If `check_exists` is `True`, verifies that the file exists

---

### `get_password()`
- Prompts the user to enter and confirm a password
- Displays password strength: **Weak**, **Medium**, or **Strong**
- Option to retry if the password is weak

---

### `check_password_strength(password)`
- Evaluates the strength of a password based on:
  - Length ≥ 8
  - Use of **uppercase**, **lowercase**, **digits**, and **special characters**

---

### `get_file_info(path)`
- Extracts and displays key PDF details:
  - Total pages  
  - Encryption status  
  - Metadata (title, author, etc.)

---

### `create_password_protected_pdf(...)`
- Reads the input PDF
- Optionally decrypts and compresses it
- Encrypts the output with the chosen password
- Writes the new PDF while **preserving original metadata**


---

## 📂 Folder Structure

```
project/
│
├── protect_pdf.py        # 🔐 Main Python script
├── README.md             # 📘 Project documentation (this file)
└── test.pdf            # 📄 Test PDF file (optional)
```

---
## 🙌 Author

**Kasula Shiva**  
🎓 B.Tech CSE (Cybersecurity)  
🔗 GitHub: [shivakasula48](https://github.com/shivakasula48)  
📧 Email: [shivakasula10@gmail.com](mailto:shivakasula10@gmail.com)

---

## 🧠 Future Enhancements

- GUI version using **Tkinter** or **PyQt**
- **Password manager** integration
- **Drag & drop** file support for easier input
