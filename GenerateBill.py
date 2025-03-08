import re
from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import random
import string
import time
import os  # Add this import

########## Time Functions############
def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    start=start+" "+"10:00 AM"
    end=end+" "+"04:00 PM"
    return str_time_prop(start, end, '%d/%m/%Y %I:%M %p', prop)

################################
Xdir=70
Xindent=240
Ydir=500

#amount=input("Enter Amount: ")
amount="1100"
date=input("Enter Date: ")
name="NISHAD.K"
#number="0495-2922395"
number="04922-291550"
###############################
def randStr(chars = string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))

import time
from datetime import datetime  
time_stamp = time.time()
if date:
    date_time = random_date(date, date,  random.random())
    #date_time=date+" "+date_time
else:
    date_time = datetime.fromtimestamp(time_stamp).strftime("%y-%m-%d %H:%M:%S")

if amount:
    amount=amount+"/-"
else:
    amount="1150/-"

recno="88220"+randStr(chars="0123456789",N=10)
tranid="PYRO040922"+randStr(chars="0123456789",N=7)
invoiceno="SDCKL00"+randStr(chars="0123456789",N=8)
list = [
    {"Content": "Success! Your payment of Rs. "+amount+" is successful.", "X": Xdir, "Y": 700},
    {"Content": "Customer Name", "X": Xdir, "Y": Ydir},
    {"Content": name, "X": Xdir+Xindent, "Y": Ydir},
    {"Content": "Receipt No", "X": Xdir, "Y": 470},
    {"Content": recno, "X": Xdir+Xindent, "Y": 470},
    {"Content": "Transaction ID", "X": Xdir, "Y": 440},
    {"Content": tranid, "X": Xdir+Xindent, "Y": 440},
    {"Content": "Transaction Date", "X": Xdir, "Y": 410},
    {"Content": date_time, "X": Xdir+Xindent, "Y": 410},
    {"Content": "Amount", "X": Xdir, "Y": 380},
    {"Content": "Rs. "+amount, "X": Xdir+Xindent, "Y": 380},
    {"Content": "Phone No", "X": Xdir, "Y": 350},
    {"Content": number, "X": Xdir+Xindent, "Y": 350},
    {"Content": "Account No", "X": Xdir, "Y": 320},
    {"Content": "9041136580", "X": Xdir+Xindent, "Y": 320},
    {"Content": "Bank Reference No", "X": Xdir, "Y": 290},
    {"Content": "Invoice No", "X": Xdir, "Y": 260},
    {"Content": invoiceno, "X": Xdir+Xindent, "Y": 260}
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
existing_pdf = PdfReader(open(".\\Res\\Bill_Template.pdf", "rb"))
output = PdfWriter()
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
fname = output_dir + recno + "." + date.replace("/", "_")
outputStream = open(fname+".pdf", "wb")
output.write(outputStream)
outputStream.close()