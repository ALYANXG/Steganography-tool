"""
Steganography Tool - Hide Secret Messages in Images
-----------------------------------------------------
Hides text messages inside PNG/BMP images using the
Least Significant Bit (LSB) technique, with optional
password-based encryption for extra security.

Author: Alyan Ahmad
"""

import argparse
import base64
import hashlib
import sys

from PIL import Image
from cryptography.fernet import Fernet, InvalidToken

# Marker to know where the hidden message ends
DELIMITER = "1111111111111110"


# ---------------------------------------------------------
# Password-based encryption helpers
# ---------------------------------------------------------
def _derive_key(password: str) -> bytes:
    """Turn any password into a valid Fernet key (32 url-safe base64 bytes)."""
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)


def encrypt_message(message: str, password: str) -> str:
    key = _derive_key(password)
    f = Fernet(key)
    token = f.encrypt(message.encode())
    return token.decode()


def decrypt_message(token: str, password: str) -> str:
    key = _derive_key(password)
    f = Fernet(key)
    try:
        return f.decrypt(token.encode()).decode()
    except InvalidToken:
        raise ValueError("Wrong password or corrupted/no hidden message!")


# ---------------------------------------------------------
# Core LSB steganography
# ---------------------------------------------------------
def _text_to_binary(text: str) -> str:
    return ''.join(format(ord(c), '08b') for c in text)


def _binary_to_text(binary: str) -> str:
    chars = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)


def encode_image(img_path: str, message: str, output_path: str, password: str = None):
    img = Image.open(img_path)
    img = img.convert("RGB")  # ensure consistent 3-channel pixels

    # If password given, encrypt the message first
    if password:
        message = encrypt_message(message, password)

    binary_msg = _text_to_binary(message) + DELIMITER

    pixels = list(img.getdata())
    capacity = len(pixels)  # 1 bit per pixel (using only Red channel)

    if len(binary_msg) > capacity:
        raise ValueError(
            f"Message too long for this image! "
            f"Max capacity: {capacity // 8} characters, "
            f"message needs: {len(binary_msg) // 8} characters."
        )

    new_pixels = []
    msg_index = 0
    msg_len = len(binary_msg)

    for pixel in pixels:
        r, g, b = pixel[:3]
        if msg_index < msg_len:
            r = (r & ~1) | int(binary_msg[msg_index])
            msg_index += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_path)
    print(f"✅ Message hidden successfully in '{output_path}'")


def decode_image(img_path: str, password: str = None) -> str:
    img = Image.open(img_path)
    img = img.convert("RGB")
    pixels = list(img.getdata())

    binary_msg = ""
    for pixel in pixels:
        r = pixel[0]
        binary_msg += str(r & 1)
        if binary_msg.endswith(DELIMITER):
            break
    else:
        raise ValueError("No hidden message found in this image!")

    binary_msg = binary_msg[:-len(DELIMITER)]  # remove delimiter
    message = _binary_to_text(binary_msg)

    if password:
        message = decrypt_message(message, password)

    return message


# ---------------------------------------------------------
# Command-Line Interface
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Steganography Tool - Hide/Extract secret messages in images"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encode command
    encode_parser = subparsers.add_parser("encode", help="Hide a message inside an image")
    encode_parser.add_argument("-i", "--input", required=True, help="Path to input image (PNG/BMP)")
    encode_parser.add_argument("-m", "--message", required=True, help="Secret message to hide")
    encode_parser.add_argument("-o", "--output", required=True, help="Path to save the stego image")
    encode_parser.add_argument("-p", "--password", help="Optional password to encrypt the message")

    # Decode command
    decode_parser = subparsers.add_parser("decode", help="Extract a hidden message from an image")
    decode_parser.add_argument("-i", "--input", required=True, help="Path to stego image")
    decode_parser.add_argument("-p", "--password", help="Password (if message was encrypted)")

    args = parser.parse_args()

    try:
        if args.command == "encode":
            encode_image(args.input, args.message, args.output, args.password)
        elif args.command == "decode":
            message = decode_image(args.input, args.password)
            print(f"🔓 Decoded message: {message}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
