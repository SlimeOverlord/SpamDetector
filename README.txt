Hello, and welcome to my Spam Filter!

This is a project I did during the summer of 2022 to practice my Python skills and I am pretty proud of it!

=======================================================================

How it works:

This program uses a system of word analysis to try to filter the emails it receives by analyzing the header, the sender and the content of the mail. Instead of just counting
the number of spam words found in the header, it uses a system of high priority words, as well as medium priority and low priority words as well as a blacklist of senders to
make the analysis more precise.

If the sender of the mail is in the blacklist, the mail is immediatly flagged as spam and sent to the spam box

If not, then the program uses a system of grades to check whether or not the mail is spam. If the header contains spam words, the grade gains 10 points immediatly. The rest of
the points are determined by the quantity of spam words in the content of the mail. The points are calculated as follows:

       (number of high priority words/total number of words)*200 + (number of medium priority words/total number of words)*150 + (number of low priority words/total number of words)*100

At the end, if the total grade is bigger than 20, the mail gets sent to the spam box, if it is lower, the mail gets sent to the inbox

The mails are then written into one of two .txt files, one called spam.txt and another called inbox.txt, where are respectively sent the spam mails and non-spam mails

=======================================================================

Words and blacklist:

High priority words: Words that are almost exclusive to spam emails and unwanted ads. They can be found in the highpriority.txt file
Medium priority words: Words that can be found in spam emails, but can also be found sometimes in regular emails. They can be found in the mediumpriority.txt file
Low priority words: Words that are sometimes found in spam emails, but are the most common in regular mails. They can be found in the lowpriority.txt file

Blacklist: A file where users can put the people they don't wnat to receive messages from. It can be a name or a mail address

=======================================================================

Specifications:

The "Analyze your own inbox" only works for gmail at the moment, and also only works for English messages in text form since it's the first version. It won't work if the text is in an 
image, but if anyone knows how to analyze text in an image, I am open to suggestions!

The blacklist is empty, do not forget to add some people in it if you wish to test how it works!

If you wish to add more words that can be considered as spam or wish to not consider some as spam, you can modify the highpriority.txt, mediumpriority.txt and lowpriority.txt files to 
create your own word databases! 

