# Created by Nicolas Ollervides 
# Version 1.00 (May 31st, 2022)

import imaplib
import email
from email.header import decode_header

# Initializing the word database and the blacklist
highpriority = open("highpriority.txt", "r")
lines = highpriority.readlines()
hpwords = []
for word in lines:
    word = word.strip()
    hpwords.append(word)
highpriority.close()

mediumpriority = open("mediumpriority.txt", "r")
lines = mediumpriority.readlines()
mpwords = []
for word in lines :
     word = word.strip()
     mpwords.append(word)
mediumpriority.close()

lowpriority = open("lowpriority.txt", "r")
lines = lowpriority.readlines()
lpwords = []
for word in lines :
     word = word.strip()
     lpwords.append(word)
lowpriority.close()

blacklist = open("blacklist.txt", "r")
lines = blacklist.readlines()
blacklistedpeople = []
for word in lines:
    word = word.strip()
    blacklistedpeople.append(word)
blacklist.close()

def spamOrNot(sub, fr, txt):
   # initialize the variables  
   spamwords = 0
   hpspamwords = 0
   mpspamwords = 0
   lpspamwords = 0
   subspamwords = 0
   blacklisted = False
   grade = 0
   
   print(sub + "\n")

   # checking if the sender of the mail isn't blacklisted
   for word in blacklistedpeople:
       if word in fr:
           blacklisted = True
           break

   if(blacklisted == True):
       sendToBox(sub, fr, txt, True)
       return

   # analyze the header of the mail and update the grade
   for word in hpwords:
       if word in sub:
           subspamwords += 1
   for word in mpwords:
        if word in sub:
            subspamwords += 1
   for word in mpwords:
       if word in sub:
           subspamwords += 1 

   if(subspamwords > 0):
       grade += 10

   # analyze the content of the mail and update the grade
   lowtxt = txt.lower()

   totalwords = len(lowtxt.split())
   print(f"{totalwords} words in total")

   for word in hpwords:
       if word in lowtxt:
           spamwords += 1
           hpspamwords += 1
   for word in mpwords:
       if word in lowtxt:
           spamwords += 1
           mpspamwords += 1
   for word in lpwords:
       if word in lowtxt:
           spamwords += 1
           lpspamwords += 1

   grade = grade + ((hpspamwords/totalwords)*200.0)
   grade = grade + ((mpspamwords/totalwords)*150.0)
   grade = grade + ((lpspamwords/totalwords)*100.0)

   # Sending the message to the inbox file or the spam box file depending on the grade
   if (grade > 20):
       print("Spam!")
       sendToBox(sub, fr, txt, True)
   else:
       print("not spam!")
       sendToBox(sub, fr, txt, False)

   print(f"{spamwords} spam words")
   print(f"{hpspamwords} high priority")
   print(f"{mpspamwords} medium priority")
   print(f"{lpspamwords} low priority")
   print(grade)

# Method that writes the email into the inbox file or the spam box file
def sendToBox(sub,fr,txt,spam):
    if(spam == True):
        spamfile = open("spam.txt", "a+")
        try:
            spamfile.write(sub + "\n" + fr + "\n" + txt + "\n")
            spamfile.write("=======================================================\n")
        except:
            print("Mail contains a forbidden character or is an image, cannot write it")
        spamfile.close()
    else:
        inboxfile = open("inbox.txt", "a+")
        try:
            inboxfile.write(sub + "\n" + fr + "\n" + txt + "\n")
            inboxfile.write("=======================================================\n")
        except:
            print("Mail contains a forbidden character or is an image, cannot write it")
        inboxfile.close()


run = True
# Main menu of the application
while(run == True):

    print("\nSpam Filter by Nicolas Ollervides")
    print("Version 1.00")
    print("==================================")
    print("Options: ")
    print("1: Write your own email and see if the algorithm detects it as spam")
    print("2: Analyze your own inbox using the filter (only works for gmail for the moment)")
    print("3: Exit the program\n")
    try: 
        number = input("What would you like to do? ")
        number = int(number)
    except:
        print("Unauthorized character!")
        continue

    # Option to write your own mail
    if(number == 1):
        subject = input("Enter the subject of the mail: ")
        subject = subject.strip()

        sender = input("Enter the sender of the mail (name or address): ")
        sender = sender.strip()

        text = input("Enter the content of the mail (if it contains new line characters, please copy and paste it): ")
        text = text.strip()

        spamOrNot(subject, sender, text)

    # Option to analyze your own inbox    
    if(number == 2):
        everythingAlright = True
        authentification = True

        # account credentials
        username = input("Enter your username: ")
        username = username.strip()

        password = input("Enter your password: ")
        password = password.strip()

        # create an IMAP4 class with SSL 
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        try:
            imap.login(username, password)
        except:
            print("Incorrect username or password, returning to menu")
            authentification = False
        
        if(authentification == True):

            status, messages = imap.select("INBOX")
            # number of top emails to fetch
            try:
                N = int(input("How many of your most recent emails would you like to analyze? "))
            except:
                print("Unauthorized character!")
                everythingAlright = False

            # total number of emails
            messages = int(messages[0])

            messagesArray = []
            if(everythingAlright == True):
                for i in range(messages, messages-N, -1):
                    # fetch the email message by ID
                    res, msg = imap.fetch(str(i), "(RFC822)")
                    for response in msg:
                        if isinstance(response, tuple):
                            # parse a bytes email into a message object
                            msg = email.message_from_bytes(response[1])
                            # decode the email subject
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                # if it's a bytes, decode to str
                                subject = subject.decode(encoding)
                            # decode email sender
                            From, encoding = decode_header(msg.get("From"))[0]
                            if isinstance(From, bytes):
                                try:
                                    From = From.decode(encoding)
                                except:
                                    print("An error has occurred, skipping this mail")
                                    continue               
                            # if the email message is multipart
                            if msg.is_multipart():
                                # iterate over email parts
                                for part in msg.walk():
                                    # extract content type of email
                                    content_type = part.get_content_type()
                                    content_disposition = str(part.get("Content-Disposition"))
                   
                                    if content_type == "text/plain" and "attachment" not in content_disposition:
                                        try:
                                            # get the email body
                                            body = part.get_payload(decode=True).decode()
                                            body = body.replace("\r\n", " ")
                                        except:
                                            pass                   
                            else:
                                # extract content type of email
                                content_type = msg.get_content_type()
                                # get the email body               
                                if content_type == "text/plain":
                                    body = msg.get_payload(decode=True).decode()
                                    body = body.replace("\r\n", " ")
                 
                            messagesArray.append((subject, From, body))      
       
            # close the connection and logout
            imap.close()
            imap.logout()            
  
            # Verifying the mails
            for (sub, fr, txt) in messagesArray:
                spamOrNot(sub, fr, txt)

    # Option to exit the application
    if(number == 3):
        run = False
