# 🕵️ Steganography Tool – Hide Secret Messages in Images

A Python-based command-line tool that hides secret text messages inside image files using the **Least Significant Bit (LSB)** technique — without visibly changing the image. Includes optional **password-based encryption** for extra security.

---

## 📌 Why This Project?

Cryptography hides the *content* of a message, but not the *existence* of it. **Steganography** goes a step further — it hides the message inside something completely ordinary, like a photo, so no one even suspects a secret is there.

> Example: A secret message hidden inside a normal-looking family photo.

### Real-World Connection
- Cyber criminals have used steganography to hide malware commands inside images.
- It's a well-known technique in CTF (Capture The Flag) cybersecurity competitions.
- Journalists and whistleblowers have used it to pass information secretly.

This project demonstrates how such hidden communication works, for educational and cybersecurity-awareness purposes.

---

## ✨ Features

- ✅ Hide text messages inside image pixels (LSB method)
- ✅ Extract hidden messages back out
- ✅ Supports PNG and BMP formats (lossless, so hidden data isn't destroyed)
- ✅ Doesn't visibly change the image
- ✅ Optional password protection (message is encrypted with Fernet/AES before hiding)
- ✅ Simple command-line interface

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Libraries:**
  - [`Pillow`](https://python-pillow.org/) — image processing
  - [`cryptography`](https://cryptography.io/) — password-based encryption

---

## ⚙️ How It Works (Logic)

1. Load the input image.
2. (Optional) Encrypt the secret message with the given password.
3. Convert the message into binary (0s and 1s), and append an end marker.
4. Modify the **Least Significant Bit** of each pixel's Red value to embed the message bits.
5. Save the new "stego" image — visually identical to the original.
6. To extract: read the LSBs of each pixel, reconstruct the bits, convert back to text, and decrypt if a password was used.

---

## 📥 Installation

```bash
git clone https://github.com/ALYANXG/Steganography-tool.git
cd steganography-tool
pip install -r requirements.txt
```

---

## 🚀 Usage

### Hide a message (encode)

```bash
python stego.py encode -i input.png -m "Hello, this is a secret!" -o stego.png
```

With password protection:

```bash
python stego.py encode -i input.png -m "Top secret data" -o stego.png -p "mypassword123"
```

### Extract a message (decode)

```bash
python stego.py decode -i stego.png
```

With password:

```bash
python stego.py decode -i stego.png -p "mypassword123"
```

---

## 💻 Demo

```
$ python stego.py encode -i input.png -m "Hello Ali, Secret msg!" -o stego.png
✅ Message hidden successfully in 'stego.png'

$ python stego.py decode -i stego.png
Decoded message: Hello Ali, Secret msg!
```

---

## 🎯 Use Cases

- **Cybersecurity Education:** Understand how attackers can hide data inside images.
- **CTF Challenges:** Steganography is a common category in security competitions.
- **Journalists/Whistleblowers:** Sending sensitive info discreetly.
- **Cyber Awareness:** Demonstrating why images shouldn't always be trusted at face value.

---


## 👤 Author

Made by Alyan Ahmad as part of a cybersecurity learning project series.
