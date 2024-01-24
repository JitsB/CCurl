import sys
from turtle import exitonclick

for arg in sys.argv[1:]:
    print(arg)

url = sys.argv[1:][0]

protocol = url.split('//')[0]
rest_of_the_url = url.split('//')[1]

host = rest_of_the_url.split('/')[0]
method = rest_of_the_url.split('/')[1]

print("protocol: ", protocol)
print("host: ", host)
print("Method: ", method)
