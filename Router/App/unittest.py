import os
print(os.path.dirname(__file__))
path = '{}/../../webapp/'.format(os.path.dirname(__file__))
path1 = '../../webapp/'
print(os.path.isdir(path1))
# print(path)