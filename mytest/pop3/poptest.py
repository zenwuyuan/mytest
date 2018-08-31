from poplib import POP3

p = POP3('pop.163.com')
p.user('zenwuyuan@163.com')
p.pass_('wjf#18650@')

# rsp,msg,siz = p.retr(890)

rsp,msg,siz = p.list()
for m in msg:
    print(m.decode('gbk'))

p.dele(1674)
p.quit()