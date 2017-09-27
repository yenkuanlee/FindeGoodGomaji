import os

api_key = ""    # Google api key to get rate    <---------------------------
send_email = True   # Send new item to someone's email  <---------------------------
user = "USER"   # Initial
pwd = "PWD" # Initial
email_send_to = "NOBODY"    # Initial
if send_email:
    email_send_to = "" # Enter the email target <---------------------------
    import getpass
    user = raw_input("Enter your email address : ")
    pwd = getpass.getpass()



os.system("python GetInfo.py > info.txt")
os.system("python GetTaipeiInfo.py info.txt > info2.txt")
os.system("python crawler.py info2.txt "+api_key+" "+email_send_to+" "+user+" "+pwd)
