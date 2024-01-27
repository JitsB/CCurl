import sys
from turtle import exitonclick
import socket

url = sys.argv[1:]
print("Url: ", url)
verbose = False

if '-v' in url:
    verbose=True
    url = url[1]
else:
    url = url[0]

print("URL: ", url)
protocol = url.split('//')[0]
protocol_version = "1.1"
rest_of_the_url = url.split('//')[1]

host = rest_of_the_url.split('/')[0]
method = rest_of_the_url.split('/')[1]

# print("protocol: ", protocol)
# print("host: ", host)
# print("Method: ", method)

data_to_be_sent = method.upper() + " / "+protocol[0:-1].upper()+'/'+protocol_version+'\r\n'+'Host:www.'+host+'\r\n\r\n'

print("data to be sent: ")
print(data_to_be_sent.encode('utf-8'))

sock = socket.socket()
sock.connect((host, 80))

# print('request: ')
# print(data_to_be_sent.encode('utf-8'))
sock.send(data_to_be_sent.encode('utf-8'))

data = ''
data = sock.recv(4096).decode()

headers, body = data.split('\r\n\r\n', 1)

if verbose:
    print("Verbose: ")
    print(headers+body)
else:
    print("Non verbose: ")
    print(body)
