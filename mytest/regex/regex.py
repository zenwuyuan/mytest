import re

if 'a' in '[asd]':
    print(1)
else:
    print(2)

m = re.match('^[a-z]{2}','asasdas')
print(m.group())

m2 = re.search('[a-z][0-9]','aa2as')
print(m2.group())

m1 = re.match('[a-z][0-9]','a2as')
print(m1.group())

bt = 'bat|bct|bbt'
#m3 = re.match(bt,'asd bct dasd')
m3 = re.search(bt,'asd bct dasd')
print(m3.group())
