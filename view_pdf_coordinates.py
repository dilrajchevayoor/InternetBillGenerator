import fitz  # PyMuPDF
import sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def get_pdf_path():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        print("No file selected.")
        sys.exit()
    return file_path

def on_drag(event):
    print(f"Mouse dragged at ({event.x}, {event.y})")

def main():
    # Initialize Tkinter first
    root = tk.Tk()
    root.withdraw()  # Hide the root window for file dialog
    pdf_path = get_pdf_path()
    
    # Load the PDF after Tkinter is initialized
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)
    pix = page.get_pixmap()

    # Convert pixmap to PIL Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Show the main Tkinter window
    root.deiconify()
    root.title("PDF Coordinate Viewer")

    canvas = tk.Canvas(root, width=pix.width, height=pix.height)
    canvas.pack()

    # Convert PIL Image to ImageTk PhotoImage
    img_tk = ImageTk.PhotoImage(img)

    # Store reference in root to prevent garbage collection
    root.img_tk = img_tk  

    # Now create the image
    canvas.create_image(0, 0, anchor=tk.NW, image=root.img_tk)

    canvas.bind("<B1-Motion>", on_drag)

    root.mainloop()

if __name__ == "__main__":
    main()
