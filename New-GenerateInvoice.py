import re
from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random
import string
import time
import os
from datetime import datetime

########## Time Functions############
def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))

def random_date(start, end, prop):
    start = start + " 10:00 AM"
    end = end + " 04:00 PM"
    return str_time_prop(start, end, '%d/%m/%Y %I:%M %p', prop)

################################
Xdir = 70
Xindent = 240
Ydir = 500

amount = "1100"
date = input("Enter Date: ")
name = "NISHAD.K"
number = "04922-291550"

def randStr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))

time_stamp = time.time()
if date:
    date_time = random_date(date, date, random.random())
else:
    date_time = datetime.fromtimestamp(time_stamp).strftime("%y-%m-%d %H:%M:%S")

amount = amount + "/-" if amount else "1150/-"

recno = "88220" + randStr(chars="0123456789", N=10)
tranid = "PYRO040922" + randStr(chars="0123456789", N=7)
invoiceno = "SDCKL00" + randStr(chars="0123456789", N=8)

list = [
    {"Content": "Success! Your payment of Rs. " + amount + " is successful.", "X": 70, "Y": 750},
    {"Content": "Customer Name", "X": 70, "Y": 700},
    {"Content": name, "X": 310, "Y": 700},
    {"Content": "Receipt No", "X": 70, "Y": 670},
    {"Content": recno, "X": 310, "Y": 670},
    {"Content": "Transaction ID", "X": 70, "Y": 640},
    {"Content": tranid, "X": 310, "Y": 640},
    {"Content": "Transaction Date", "X": 70, "Y": 610},
    {"Content": date_time, "X": 310, "Y": 610},
    {"Content": "Amount", "X": 70, "Y": 580},
    {"Content": "Rs. " + amount, "X": 310, "Y": 580},
    {"Content": "Phone No", "X": 70, "Y": 550},
    {"Content": number, "X": 310, "Y": 550},
    {"Content": "Account No", "X": 70, "Y": 520},
    {"Content": "9041136580", "X": 310, "Y": 520},
    {"Content": "Bank Reference No", "X": 70, "Y": 490},
    {"Content": "Invoice No", "X": 70, "Y": 460},
    {"Content": invoiceno, "X": 310, "Y": 460}
]

# Ensure the output directory exists
output_dir = ".\\Out\\"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
for i in list:
    can.drawString(i["X"], i["Y"], i["Content"])
can.setFont('Times-Roman', 30)
can.save()
packet.seek(0)

new_pdf = PdfReader(packet)
existing_pdf = PdfReader(open(".\\Res\\Bill_Template_1.1.pdf", "rb"))
output = PdfWriter()
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)

fname = output_dir + recno + "." + date.replace("/", "_")
with open(fname + ".pdf", "wb") as outputStream:
    output.write(outputStream)
