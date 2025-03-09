from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
import random
import string
import time
import os
from datetime import datetime
from tkinter import Tk, Label, Entry, Button, StringVar
from tkcalendar import DateEntry
from reportlab.lib import colors

# Define font paths
FONT_REGULAR_PATH = "NotoSans-Regular.ttf"
FONT_BOLD_PATH = "NotoSans-Bold.ttf"

# Check if the font files exist
if not os.path.exists(FONT_REGULAR_PATH):
    print("Error: Regular font file not found!")
    exit(1)

if not os.path.exists(FONT_BOLD_PATH):
    print("Error: Bold font file not found!")
    exit(1)

# Register fonts
pdfmetrics.registerFont(TTFont("UnicodeFont", FONT_REGULAR_PATH))
pdfmetrics.registerFont(TTFont("UnicodeFont-Bold", FONT_BOLD_PATH))

# Time Functions
def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))

def random_date(start, end, prop):
    start = start + " 10:00 AM"
    end = end + " 04:00 PM"
    return str_time_prop(start, end, '%d/%m/%Y %I:%M %p', prop)

# Positioning Constants
Xdir = 70
Xindent = 150
Ydir = 650
Ystep = 30
FONT_NAME = "UnicodeFont"
FONT_SIZE = 8

def get_user_inputs():
    def submit():
        global amount, date, name, number
        amount = amount_var.get()
        date = date_var.get()
        name = name_var.get()
        number = number_var.get()
        root.destroy()

    root = Tk()
    root.title("User Inputs")

    amount_var = StringVar(value="1100")
    date_var = StringVar(value="29/05/2023")
    name_var = StringVar(value="DILRAJ M")
    number_var = StringVar(value="0495-2922395")

    Label(root, text="Amount:").grid(row=0, column=0)
    Entry(root, textvariable=amount_var).grid(row=0, column=1)

    Label(root, text="Date (DD/MM/YYYY):").grid(row=1, column=0)
    DateEntry(root, textvariable=date_var, date_pattern='dd/MM/yyyy').grid(row=1, column=1)

    Label(root, text="Name:").grid(row=2, column=0)
    Entry(root, textvariable=name_var).grid(row=2, column=1)

    Label(root, text="Phone Number:").grid(row=3, column=0)
    Entry(root, textvariable=number_var).grid(row=3, column=1)

    Button(root, text="Submit", command=submit).grid(row=4, columnspan=2)

    root.mainloop()

amount = ""
date = ""
name = ""
number = ""

get_user_inputs()

# Random Strings
def randStr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))

time_stamp = time.time()
if date:
    date_time = random_date(date, date, random.random())
else:
    date_time = datetime.fromtimestamp(time_stamp).strftime("%y-%m-%d %H:%M:%S")

amount = amount + "/-" if amount else "1150/-"
recno = "88220" + randStr(chars="0123456789", N=10)
tranid = randStr(chars="0123456789", N=8)
invoiceno = "SDCKL00" + randStr(chars="0123456789", N=8)
refno = "SKLR" + randStr(chars="0123456789", N=11)

# Ensure Output Directory Exists
output_dir = "./Out/"
os.makedirs(output_dir, exist_ok=True)

# Receipt Data
# PDF Content Data
receipt_data = [
    {"content": f"Receipt Details", "x": 31.96, "y": 717.73, "size": FONT_SIZE},
    {"content": f"Your payment of ₹{amount} is successful.", "x": 44.94, "y": 682.00, "size": FONT_SIZE},
    {"content": "Receipt for payment of Bills/Demand Notes: This receipt has been generated from the BSNL portal", "x": Xdir, "y": 629.76, "size": FONT_SIZE},
    {"content": "Customer Name", "x": Xdir, "y": Ydir - 2*Ystep, "size": FONT_SIZE},
    {"content": name, "x": Xdir + Xindent, "y": Ydir - 2*Ystep, "size": FONT_SIZE},
    {"content": "Receipt No", "x": Xdir, "y": Ydir - 3*Ystep, "size": FONT_SIZE},
    {"content": recno, "x": Xdir + Xindent, "y": Ydir - 3*Ystep, "size": FONT_SIZE},
    {"content": "Transaction ID", "x": Xdir, "y": Ydir - 4*Ystep, "size": FONT_SIZE},
    {"content": tranid, "x": Xdir + Xindent, "y": Ydir - 4*Ystep, "size": FONT_SIZE},
    {"content": "Transaction Date", "x": Xdir, "y": Ydir - 5*Ystep, "size": FONT_SIZE},
    {"content": date_time, "x": Xdir + Xindent, "y": Ydir - 5*Ystep, "size": FONT_SIZE},
    {"content": "Amount", "x": Xdir, "y": Ydir - 6*Ystep, "size": FONT_SIZE},
    {"content": f"₹{amount}", "x": Xdir + Xindent, "y": Ydir - 6*Ystep, "size": FONT_SIZE},
    {"content": "Phone No", "x": Xdir, "y": Ydir - 7*Ystep, "size": FONT_SIZE},
    {"content": number, "x": Xdir + Xindent, "y": Ydir - 7*Ystep, "size": FONT_SIZE},
    {"content": "Account No", "x": Xdir, "y": Ydir - 8*Ystep, "size": FONT_SIZE},
    {"content": "9041136580", "x": Xdir + Xindent, "y": Ydir - 8*Ystep, "size": FONT_SIZE},
    {"content": "Bank Reference No", "x": Xdir, "y": Ydir - 9*Ystep, "size": FONT_SIZE},
    {"content": refno, "x": Xdir + Xindent, "y": Ydir - 9*Ystep, "size": FONT_SIZE},
    {"content": "Invoice No", "x": Xdir, "y": Ydir - 10*Ystep, "size": FONT_SIZE},
    {"content": invoiceno, "x": Xdir + Xindent, "y": Ydir - 10*Ystep, "size": FONT_SIZE},
]

# Tax Calculations
amount_value = float(amount.replace("/-", ""))
tax_amount = 2 * (0.09 * amount_value)
recurring_charges = amount_value - tax_amount

# Summary Box Positioning
#"x": 329.56, "y": 612.77
summary_x = 329.56
summary_y = 612.77
box_width = 200
box_height = 142

# Summary Data
summary_data = [
    {"content": "Summary of Charges", "x": summary_x, "y": summary_y + 100, "size": FONT_SIZE + 1, "font": "UnicodeFont-Bold"},
    {"content": f"Recurring Charges: ₹ {recurring_charges:.2f}", "x": summary_x + 10, "y": summary_y + 85, "size": FONT_SIZE, "font": "UnicodeFont"},
    {"content": "One Time Charges: ₹ 0.00", "x": summary_x + 10, "y": summary_y + 70, "size": FONT_SIZE, "font": "UnicodeFont"},
    {"content": "Usage Charges: ₹ 0.00", "x": summary_x + 10, "y": summary_y + 55, "size": FONT_SIZE, "font": "UnicodeFont"},
    {"content": "Miscellaneous Charges: ₹ 0.00", "x": summary_x + 10, "y": summary_y + 40, "size": FONT_SIZE, "font": "UnicodeFont"},
    {"content": "Discounts: ₹ 0.00", "x": summary_x + 10, "y": summary_y + 25, "size": FONT_SIZE, "font": "UnicodeFont"},
    {"content": "Late Fee: ₹ 0.00", "x": summary_x + 10, "y": summary_y + 10, "size": FONT_SIZE, "font": "UnicodeFont"},
    {"content": f"Total Taxable (Rs.): ₹ {recurring_charges:.2f}", "x": summary_x + 10, "y": summary_y - 5, "size": FONT_SIZE, "font": "UnicodeFont-Bold"},
    {"content": f"Tax: ₹ {tax_amount:.2f}", "x": summary_x + 10, "y": summary_y - 20, "size": FONT_SIZE, "font": "UnicodeFont-Bold"},
    {"content": f"Total Current Charges: ₹ {amount}", "x": summary_x + 10, "y": summary_y - 35, "size": FONT_SIZE, "font": "UnicodeFont-Bold"},
]

# Adjust Y positions for summary data to avoid overlap
for item in summary_data:
    item["y"] -= 100  # Shift summary data down by 40 units

receipt_data.extend(summary_data)

# Create PDF
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
for item in receipt_data:
    can.setFont(item.get("font", "UnicodeFont"), item["size"])  # Default to UnicodeFont if not specified
    can.drawString(item["x"], item["y"], item["content"])
can.setStrokeColorRGB(0, 0, 0)
can.rect(summary_x, summary_y - 145, box_width, box_height, stroke=1, fill=0)

# Tax Table Positioning
#"x": 329.56, "y": 447.83
tax_table_x = 329.56
tax_table_y = 447.83 # Position below summary
col_widths = [80, 60, 60]  # Column widths for Description, Tax Rate, Amount
row_height = 25  # Row height
table_width = sum(col_widths)
table_height = row_height * 4  # 1 header row + 3 data rows

# Draw "Tax Details" Heading
can.setFont("UnicodeFont-Bold", FONT_SIZE + 2)
#"x": 329.56, "y": 451.83
can.drawString(329.56, 451.83, "Tax Details")

# Tax Table Data
tax_table_data = [
    ["Description", "Tax Rate", "Amount"],  # Table Header
    ["CGST", "9.00%", f"₹ {0.09 * amount_value:.2f}"],
    ["SGST/UTGST", "9.00%", f"₹ {0.09 * amount_value:.2f}"],
    ["VAT-Flood Cess", "1.00%", f"₹ {0.00 * amount_value:.2f}"],
]

# Draw Table Borders (Outer)
can.setStrokeColorRGB(0, 0, 0)
can.rect(tax_table_x, tax_table_y - table_height, table_width, table_height, stroke=1, fill=0)

# Fill Table Cells
y_offset = tax_table_y
for i, row in enumerate(tax_table_data):
    x_offset = tax_table_x

    # Set Header Background Color & Border
    if i == 0:
        can.setFillColor(colors.lightgrey)  # Header background color
        can.rect(tax_table_x, y_offset - row_height, table_width, row_height, fill=1, stroke=1)
        can.setFillColor(colors.black)  # Reset text color to black

    # Draw Row Text (Centered)
    for j, col in enumerate(row):
        font = "UnicodeFont-Bold" if i == 0 else "UnicodeFont"  # Bold for headers
        can.setFont(font, FONT_SIZE)
        
        # Center Text in Cell
        text_width = can.stringWidth(col, font, FONT_SIZE)
        x_text = x_offset + (col_widths[j] - text_width) / 2  # Center alignment
        y_text = y_offset - row_height + 8  # Adjust vertical position
        
        can.drawString(x_text, y_text, col)
        x_offset += col_widths[j]

    y_offset -= row_height  # Move to next row

# Draw Column Lines (Including Header Separator)
x_line = tax_table_x
for width in col_widths:  # Ensure all columns (including last one) have a border
    x_line += width
    can.line(x_line, tax_table_y, x_line, tax_table_y - table_height)

# Draw Row Lines (Including Header Separator)
for i in range(1, len(tax_table_data)):  # Skip first row (already covered)
    y_line = tax_table_y - (i * row_height)
    can.line(tax_table_x, y_line, tax_table_x + table_width, y_line)

can.save()
packet.seek(0)

# Merge with Template
template_path = "./Res/Bill_Template_1.2.pdf"
if not os.path.exists(template_path):
    print("Error: Template file not found!")
    exit(1)
new_pdf = PdfReader(packet)
existing_pdf = PdfReader(open(template_path, "rb"))
output = PdfWriter()
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)

# Save Final PDF
fname = os.path.join(output_dir, f"{recno}_{date.replace('/', '_')}.pdf")
with open(fname, "wb") as outputStream:
    output.write(outputStream)
print(f"Receipt successfully generated: {fname}")
