
urlS = "http://www.chance.org.tw/%E7%B1%A4%E8%A9%A9%E9%9B%86/%E5%85%AD%E5%8D%81%E7%94%B2%E5%AD%90%E7%B1%A4/%E7%B1%A4%E8%A9%A9%E7%B6%B2%E2%80%A7%E5%85%AD%E5%8D%81%E7%94%B2%E5%AD%90%E7%B1%A4__%E7%AC%AC"
urlE =  "%E7%B1%A4.htm"
import subprocess


for i in range(60):
    t = i+1
    theNo = "%02d" % (t)
    wgetUrl = urlS + theNo +urlE
    cmd = "wget "+wgetUrl+ " -O "+theNo+".htm"
    subprocess.call(cmd.split(" "))
   

for i in range(60):
    tt = i +1
    theNo = "%02d" % (tt)
    cmd = "iconv -f big5 -t utf-8 " + theNo+".htm -o " + theNo+"utf.htm"
    subprocess.call(cmd.split(" "))
   
