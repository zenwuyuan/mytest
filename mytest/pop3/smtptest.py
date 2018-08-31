from smtplib import SMTP
from time import sleep
from poplib import  POP3

smtpserver = 'smtp.163.com'

who = 'zenwuyuan@163.com'
body = '''\
From: %(who)s
To: %(who)s
Subject: test mesg
Hello
''' % {'who' : who}

sendserver = SMTP(smtpserver)
errs = sendserver.sendmail(who,[who],body)
sendserver.quit()

assert len(errs) == 0,errs
sleep(10)

recvserver = POP3('pop.163.com')
recvserver.user('zenwuyuan@163.com')
recvserver.pass_('wjf#18650@')
rsp,msg,siz = recvserver.retr(recvserver.stat()[0])
sep = msg.index('')
recvbody = msg[sep+1:]
# assert origBody == recvbody
assert body == recvbody

