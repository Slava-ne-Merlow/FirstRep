import base64
import email
import imaplib
import quopri
from email.header import decode_header


def answers_by_subject(theme:str, folder:str):
    FROM_EMAIL = "slava.kush39@gmail.com"
    FROM_PWD = "iqpk evew sdkm zxml"
    SMTP_SERVER = "imap.gmail.com"

    imap = imaplib.IMAP4_SSL(SMTP_SERVER)

    imap.login(FROM_EMAIL, FROM_PWD)
    if folder == 'INBOX':
        imap.select('INBOX')
    elif folder == 'OUTBOX':
        imap.select('[Gmail]/&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-')
    typ, data = imap.search(None, 'ALL')

    data = data[0].split()

    lis = []
    for i in data:
        dic = {'id': i,
               "From": '',
               "To": '',
               "Subject": '',
               "Text": ''}
        status, msg = imap.fetch(i, '(RFC822)')

        msg = email.message_from_bytes(msg[0][1])

        subj = quopri.decodestring(decode_header(msg["Subject"])[0][0]).decode('UTF-8')
        if subj[:3].upper() != 'RE:' or subj.split(maxsplit=1)[1] != theme:
            continue
        dic["From"] = msg['From'].split()[-1].replace('<', '').replace('>', '')
        dic["Subject"] = quopri.decodestring(decode_header(msg["Subject"])[0][0]).decode('UTF-8')
        dic['Date'] = msg["Date"]

        if folder == 'INBOX':
            dic['To'] = msg['To']
            dic['Folder'] = folder
        elif folder == 'OUTBOX':
            dic['Folder'] = '[Gmail]/&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-'
            if not msg['Received']:
                a = msg['To']
                if a.find('<') != -1:
                    dic['To'] = a[a.find('<') + 1:a.find('>') ]
                else:
                    dic['To'] = a
            else:
                a = str(msg['Received']).split('\r\n')[2]
                if a.find('<') != -1:
                    dic['To'] =a[a.find('<') + 1:a.find('>') ]
                else:
                    dic['To'] = a

        for part in msg.walk():
            if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                try:
                    a = base64.b64decode(part.get_payload()).decode()
                    if a.find('>') != -1:
                        a = a[:a.find('>')]
                    a = a[:a.find('2024')][:-10] if a.find('2024') != -1 else a
                except:
                    a = 'qwerty'
                b = quopri.decodestring(part.get_payload()).decode('UTF-8')
                b = b[:b.find('2024')][:-6] if b.find('2024') != -1 else b
                dic['Text'] = a.replace('\r', '') if a != 'qwerty' else b.replace('\r', '')
        lis.append(dic)
    imap.close()
    return lis
