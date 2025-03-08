import fitz  # PyMuPDF
import sys
import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
import pyperclip  # For clipboard support

def get_pdf_path():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        print("No file selected.")
        sys.exit()
    return file_path

def on_click(event):
    """Show popup with accurate PDF X, Y coordinates when clicking on the viewer."""
    global popup, canvas, img_width, img_height, pdf_width, pdf_height  # Access global variables

    x, y = event.x, event.y
    
    # Convert canvas coordinates to PDF coordinates
    pdf_x = (x / img_width) * pdf_width  
    pdf_y = pdf_height - ((y / img_height) * pdf_height)  # Flip Y-axis

    # Close the old popup if it exists
    if popup and popup.winfo_exists():
        popup.destroy()

    # Create new popup window
    popup = Toplevel(root)
    popup.title("Coordinates")
    popup.geometry("220x100")
    
    coord_label = tk.Label(popup, text=f"X: {pdf_x:.2f}, Y: {pdf_y:.2f}", font=("Arial", 12))
    coord_label.pack(pady=10)

    copy_button = tk.Button(popup, text="Copy", font=("Arial", 10), command=lambda: copy_to_clipboard(pdf_x, pdf_y))
    copy_button.pack()

def copy_to_clipboard(x, y):
    """Copy accurate PDF X, Y coordinates to clipboard."""
    coords = f'"X": {x:.2f}, "Y": {y:.2f}'
    pyperclip.copy(coords)

def main():
    global root, popup, canvas, img_width, img_height, pdf_width, pdf_height  # Define global variables
    popup = None  # Initialize popup variable

    # Initialize Tkinter
    root = tk.Tk()
    root.withdraw()  # Hide root window for file dialog
    pdf_path = get_pdf_path()

    # Load the PDF
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)
    pdf_width, pdf_height = page.rect.width, page.rect.height  # Get actual PDF dimensions
    pix = page.get_pixmap()

    # Convert pixmap to PIL Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Store image dimensions
    img_width, img_height = pix.width, pix.height  

    # Show main Tkinter window
    root.deiconify()
    root.title("PDF Coordinate Viewer")

    canvas = tk.Canvas(root, width=img_width, height=img_height)  # Store globally
    canvas.pack()

    # Convert PIL Image to ImageTk PhotoImage
    img_tk = ImageTk.PhotoImage(img)
    root.img_tk = img_tk  # Keep reference to prevent garbage collection

    # Display image on canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=root.img_tk)

    # Bind mouse click event
    canvas.bind("<Button-1>", on_click)

    root.mainloop()

if __name__ == "__main__":
    main()
