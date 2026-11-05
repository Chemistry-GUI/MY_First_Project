import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import qrcode
import os

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("550x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f7fb")

        self.qr_image = None
        self.preview_image = None

        # Header
        header = tk.Frame(root, bg="#1f4e78", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="QR CODE GENERATOR",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#1f4e78"
        ).pack(pady=(14, 0))

        tk.Label(
            header,
            text="Create and save QR codes easily",
            font=("Segoe UI", 10),
            fg="#dbeafe",
            bg="#1f4e78"
        ).pack()

        # Main card
        card = tk.Frame(root, bg="white", bd=1, relief="solid")
        card.pack(padx=35, pady=25, fill="both", expand=True)

        tk.Label(
            card,
            text="Enter Text or URL",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#222222"
        ).pack(anchor="w", padx=30, pady=(25, 8))

        self.input_box = tk.Text(
            card,
            height=4,
            font=("Segoe UI", 11),
            wrap="word",
            bd=1,
            relief="solid"
        )
        self.input_box.pack(fill="x", padx=10)
        self.input_box.insert("1.0", "https://example.com")

        # Options
        options = tk.Frame(card, bg="white")
        options.pack(fill="x", padx=30, pady=15)

        tk.Label(
            options,
            text="QR Color:",
            font=("Segoe UI", 10, "bold"),
            bg="white"
        ).grid(row=0, column=0, padx=(0, 8), pady=5)

        self.fg_color = ttk.Combobox(
            options,
            values=["black", "blue", "green", "red", "purple"],
            state="readonly",
            width=12
        )
        self.fg_color.set("black")
        self.fg_color.grid(row=0, column=1, padx=5)

        tk.Label(
            options,
            text="Background:",
            font=("Segoe UI", 10, "bold"),
            bg="white"
        ).grid(row=0, column=2, padx=(25, 8))

        self.bg_color = ttk.Combobox(
            options,
            values=["white", "lightyellow", "lightblue", "lightgreen"],
            state="readonly",
            width=12
        )
        self.bg_color.set("white")
        self.bg_color.grid(row=0, column=3, padx=5)

        # Buttons
        button_frame = tk.Frame(card, bg="white")
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Generate QR",
            command=self.generate_qr,
            font=("Segoe UI", 11, "bold"),
            bg="#1f4e78",
            fg="white",
            activebackground="#163a5c",
            activeforeground="white",
            padx=20,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).grid(row=0, column=0, padx=6)

        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear,
            font=("Segoe UI", 11),
            bg="#e5e7eb",
            fg="#222222",
            padx=20,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).grid(row=0, column=1, padx=6)

        # Preview
        tk.Label(
            card,
            text="QR Preview",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#222222"
        ).pack(pady=(15, 5))

        self.preview = tk.Label(
            card,
            text="Your QR code will appear here",
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg="#64748b",
            width=42,
            height=12,
            relief="solid",
            bd=1
        )
        self.preview.pack(padx=30, pady=5)

        # Save button
        self.save_button = tk.Button(
            card,
            text="Save QR Code",
            command=self.save_qr,
            font=("Segoe UI", 11, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            padx=25,
            pady=8,
            cursor="hand2",
            relief="flat",
            state="disabled"
        )
        self.save_button.pack(pady=15)

        tk.Label(
            card,
            text="Tip: You can enter a URL, text, Wi-Fi information, contact details, etc.",
            font=("Segoe UI", 9),
            fg="#64748b",
            bg="white"
        ).pack(pady=(0, 15))

    def generate_qr(self):
        data = self.input_box.get("1.0", "end").strip()

        if not data:
            messagebox.showwarning("Empty Input", "Please enter some text or a URL.")
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8,
                border=4
            )

            qr.add_data(data)
            qr.make(fit=True)

            self.qr_image = qr.make_image(
                fill_color=self.fg_color.get(),
                back_color=self.bg_color.get()
            ).convert("RGB")

            # Create preview
            preview = self.qr_image.copy()
            preview.thumbnail((150, 150))

            self.preview_image = ImageTk.PhotoImage(preview)
            self.preview.config(
                image=self.preview_image,
                text="",
                width=150,
                height=150
            )

            self.save_button.config(state="normal")

        except Exception as e:
            messagebox.showerror("Error", f"Could not generate QR code.\n\n{e}")

    def save_qr(self):
        if self.qr_image is None:
            messagebox.showwarning("No QR Code", "Generate a QR code first.")
            return

        filename = filedialog.asksaveasfilename(
            title="Save QR Code",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*")
            ]
        )

        if filename:
            try:
                self.qr_image.save(filename)
                messagebox.showinfo(
                    "Saved",
                    f"QR code saved successfully:\n{os.path.basename(filename)}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Could not save QR code.\n\n{e}")

    def clear(self):
        self.input_box.delete("1.0", "end")
        self.preview.config(
            image="",
            text="Your QR code will appear here",
            width=42,
            height=12
        )
        self.preview_image = None
        self.qr_image = None
        self.save_button.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()
