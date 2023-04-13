import os
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from PIL import Image


# function to encrypt an image file using AES encryption
def encrypt_image(input_file_path, output_file_path, key):
    with open(input_file_path, 'rb') as f:
        plaintext = f.read()

    # initialize the cipher object with the key and mode
    cipher = AES.new(key, AES.MODE_CBC)

    # encrypt the plaintext using the cipher object
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    # create a new image with the encrypted data
    img = Image.frombytes("RGB", (len(ciphertext), 1), ciphertext)

    # save the encrypted image to the output file path
    img.save(output_file_path)


# function to decrypt an image file using AES encryption
def decrypt_image(input_file_path, output_file_path, key):
    # open the encrypted image file
    with Image.open(input_file_path) as img:
        # get the encrypted data from the image
        ciphertext = img.tobytes()

    # initialize the cipher object with the key and mode
    cipher = AES.new(key, AES.MODE_CBC)

    # decrypt the ciphertext using the cipher object
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # save the decrypted image to the output file path
    with open(output_file_path, 'wb') as f:
        f.write(plaintext)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visual Cryptography")
        self.geometry("400x200")
        self.file_path = ""
        self.encrypted_file_path = ""
        self.decrypted_file_path = ""

        self.file_path_label = tk.Label(self, text="No file selected")
        self.file_path_label.pack()

        select_file_button = tk.Button(self, text="Select file", command=self.select_file)
        select_file_button.pack(pady=10)

        self.password_label = tk.Label(self, text="Enter password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        encrypt_button = tk.Button(self, text="Encrypt", command=self.encrypt_file)
        encrypt_button.pack(pady=10)

        decrypt_button = tk.Button(self, text="Decrypt", command=self.decrypt_file)
        decrypt_button.pack(pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        self.file_path_label.configure(text=self.file_path)

    def encrypt_file(self):
        if not self.file_path:
            tk.messagebox.showwarning("No file selected", "Please select a file to encrypt.")
            return

        password = self.password_entry.get()
        if not password:
            tk.messagebox.showwarning("No password entered", "Please enter a password to encrypt the file.")
            return

        # Generate encryption key from password
        key = hashlib.sha256(password.encode()).digest()

        # Open the input file and read its contents
        with open(self.file_path, 'rb') as file:
            input_data = file.read()

        # Encrypt the input data using AES-256
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(input_data)

        # Save the encrypted file to disk
        self.encrypted_file_path = self.file_path + ".encrypted"
        with open(self.encrypted_file_path, 'wb') as file:
            file.write(nonce)
            file.write(tag)
            file.write(ciphertext)

        tk.messagebox.showinfo("Encryption successful", f"The file has been encrypted and saved to {self.encrypted_file_path}.")

    def decrypt_file(self):
        if not self.encrypted_file_path:
            tk.messagebox.showwarning("No encrypted file selected", "Please encrypt a file first.")
            return

        password = self.password_entry.get()
        if not password:
            tk.messagebox.showwarning("No password entered", "Please enter the password to decrypt the file.")
            return

        # Generate decryption key from password
        key = hashlib.sha256(password.encode()).digest()

        # Open the encrypted file and read its contents
        with open(self.encrypted_file_path, 'rb') as file:
            nonce = file.read(16)
            tag = file.read(16)
            ciphertext = file.read()

        # Decrypt the input data using AES-256
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        input_data = cipher.decrypt_and_verify(ciphertext, tag)

        # Save the decrypted file to disk
        self.decrypted_file_path = self.encrypted_file_path + ".decrypted"
        with open(self.decrypted_file_path, 'wb') as file:
            file.write(input_data)

        tk.messagebox.showinfo("Success", "File has been encrypted successfully!")


if __name__ == '__main__':
    App().mainloop()
