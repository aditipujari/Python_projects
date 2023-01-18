import os
import schedule
from sys import *
import hashlib
import time
import smtplib, ssl
from email import encoders
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def EmailSend(dir,email,duplicate_count,file_scanned,start_time):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "xyz@gmail.com"  # Enter your address
    receiver_email = email  # Enter receiver address
    password = "------------" # 16-digit app password from your gmail settings

    msg = MIMEMultipart()
    subject = "An email with attachment from Python"
    body = f"This is an email with attachment sent from Python\nNumber of Duplicate files : {duplicate_count}\nNumber of files Scanned : {file_scanned}\nStart time of scanning : {start_time}"
    msg['Subject'] = "Complete Automation Script for Duplicates Removal and Email Scheduling"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Add body to email
    msg.attach(MIMEText(body, "plain"))

    filename = os.path.join(os.getcwd(),dir)

    files = os.listdir(filename)
    # Open file in binary mode
    for file in files:
        file_path = os.path.join(filename,file)
        with open(file_path, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file}",
    )

    # Add attachment to message and convert message to string
    msg.attach(part)
    text = msg.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

        print("Email Sent Successfully")

def hashfile(path, blocksize = 1024):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)

    afile.close()
    return hasher.hexdigest()

def PrintDuplicate(dict1,email,start_time):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    dir = "DuplicateInfo"
    if not os.path.exists(dir):
        try:
            os.mkdir(dir)
        except:
            pass

    if len(results) > 0:
        print("Duplicates found")
        timestr = time.strftime("%Y%m%d-%H%M%S")
        file_name = timestr+".txt"
        log_path = os.path.join(dir, file_name)
        fd = open(log_path, "w")

        icnt = 0
        counter = 0

        for result in results:
            for subresult in result:
                icnt += 1
                if icnt >= 2:
                    counter = counter + 1
                    fd.write(subresult)
                    fd.write("\n")
                    os.remove(subresult)
            icnt = 0
        fd.close()
        duplicate_count = counter
        file_scanned = len(result)
        EmailSend(dir,email,duplicate_count,file_scanned,start_time)

    else:
        print("No Duplicates Found")

def FindDuplicate(path,email):
    now = datetime.now()
    start_time = now.strftime("%H:%M:%S")

    flag = os.path.isabs(path)

    if flag == False:
        path = os.path.abspath(path)

    exists = os.path.isdir(path)

    dups = {}
    if exists:
        for dirname, subdirs, filelist in os.walk(path):
            for filen in filelist:
                path = os.path.join(dirname, filen)
                file_hash = hashfile(path)
                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]

        PrintDuplicate(dups, email, start_time)

    else:
        print("Invalid path")

def main():
    print("Complete Automation Script for Duplicates Removal and Email Scheduling")

    if(len(argv) != 4):
        print("Insufficient Arguments")
        exit()

    if((argv[1] == "-h") or (argv[1] == "-H")):
        print("This script will traverse the specific directory,remove the duplicate files, add duplicate file in email as attachment and send email to a specified email id by user.")
        exit()

    if((argv[1] == "-u") or (argv[1] == "-U")):
        print("Usage : Application_name AbsolutePath_Of_Directory")
        exit()

    try:

        schedule.every(int(argv[2])).minutes.do(FindDuplicate,path = argv[1],email=argv[3])
        while True:
            schedule.run_pending()
            time.sleep(1)

        #PrintDuplicate(arr,argv[2])

    except ValueError:
        print("Error : Invalid datatype of Input.")

    except Exception as E:
        print("Error : Invalid Input : ",E)

if __name__ == "__main__":
    start_time = time.process_time()
    main()
    end_time = time.process_time()
    print("Execution time is : ", end_time - start_time)