import oss2
import crcmod._crcfunext
from itertools import islice


auth = oss2.Auth('LTAIrtNQMqJA9Tku','8aIKMgN8qujhRjYEI90Gt9N6nwF62V')
bucket = oss2.Bucket(auth,'oss-cn-hongkong-internal.aliyuncs.com','jf87')

#upload
bucket.put_object_from_file('222.txt','/root/PycharmProjects/mytest/mytest/oss/222.txt')

#download
bucket.get_object_to_file('222.txt','/root/PycharmProjects/mytest/mytest/oss/222/222.txt')

#delete
#bucket.delete_object('222.txt')

#
try:
    bucket.get_object('222/222.txt')
    print('cun zai')
except Exception as err:
    print('bu cun zai')

# list
for b in islice(oss2.ObjectIterator(bucket), 10):
    print(b.key)
