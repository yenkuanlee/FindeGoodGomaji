import os
os.system("python GetInfo.py > info.txt")
os.system("python GetTaipeiInfo.py info.txt > info2.txt")
os.system("python cssiot_crawler.py info2.txt > output.txt")
