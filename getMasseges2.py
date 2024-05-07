import base64
import email
import imaplib
import quopri
from email.header import decode_header
import datetime
print(str(datetime.datetime.now())[:-7])


FROM_EMAIL = "slava.kush39@gmail.com"
FROM_PWD = "iqpk evew sdkm zxml"
SMTP_SERVER = "imap.gmail.com"

imap = imaplib.IMAP4_SSL(SMTP_SERVER)

imap.login(FROM_EMAIL, FROM_PWD)

print(imap.list()[1][5], sep='\n')
# imap.select("[Gmail]/&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-")
imap.select("INBOX")

typ, data = imap.search(None, 'ALL')

data = data[0].split()

lis = []
for i in data:
    dic = {'id':i,
            "From": '',
           "To": '',
           "Subject": '',
           "Text": ''}
    status, msg = imap.fetch(i, '(RFC822)')
    msg = email.message_from_bytes(msg[0][1])
    # print(msg)
    dic['To'] = msg['To']
    # if not msg['Received']:
    #     a = msg['To']
    #     if a.find('<') != -1:
    #         dic['To'] = a[a.find('<') + 1:a.find('>') ]
    #     else:
    #         dic['To'] = a
    # else:
    #     a = str(msg['Received']).split('\r\n')[2]
    #     if a.find('<') != -1:
    #         dic['To'] =a[a.find('<') + 1:a.find('>') ]
    #     else:
    #         dic['To'] = a

    subj = quopri.decodestring(decode_header(msg["Subject"])[0][0]).decode('UTF-8')
    dic["From"] = msg['From'].split()[-1].replace('<', '').replace('>', '')
    dic["Subject"] = quopri.decodestring(decode_header(msg["Subject"])[0][0]).decode('UTF-8')
    # dic['Date'] = str(decode_header(msg["Date"])[0][0][5:-12]).replace(' ', '-', 2)
    dic['Date'] = email.utils.parsedate_tz(msg["Date"])[:-4]

    for part in msg.walk():
        if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
            try:
                a = base64.b64decode(part.get_payload()).decode()
                if a.find('>') != -1:
                    a = a[:a.find('>')]
            except:
                a = 'qwerty'
            b = quopri.decodestring(part.get_payload()).decode('UTF-8')
            b = b[:b.find('.2024')][:-6] if b.find('2024') != -1 else b
            dic['Text'] = a.replace('\r', '') if a != 'qwerty' else b.replace('\r', '')
    print(dic)
    lis.append(dic)
imap.close()
