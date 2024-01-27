import sys
from turtle import exitonclick
import socket

sock = socket.socket()

class cCurl:
    def deconstruct_api_request(self, api_request):
        is_verbose = False
        if '-v' in api_request:
            is_verbose = True
            api_request.remove('-v')
        else:
            is_verbose = False

        protocol, rest_of_the_url = api_request[0].split('//')
        protocol_version = "1.1"
        
        host, method = rest_of_the_url.split('/')
        return protocol, protocol_version, host, method, is_verbose

    def __init__(self, api_request):

        protocol, protocol_version, host, method, is_verbose = self.deconstruct_api_request(api_request)

        self.protocol = protocol
        self.protocol_version = protocol_version
        self.is_verbose = is_verbose
        self.host = host
        self.method = method
    
    def deconstruct_server_response(self, response):
        headers, body = response.split('\r\n\r\n', 1)
        return headers, body
    
    def show_response(self, response):
        headers, body = self.deconstruct_server_response(response)
        if self.is_verbose:
            print("Headers: ")
            print(headers)
            print("Body: ")
            print(body)
        else:
            print("Body: ")
            print(body)
    
    def get_encoded_data(self):
        data = self.method.upper() + " / "+self.protocol[0:-1].upper()\
        +'/'+self.protocol_version+'\r\n'+'Host:www.'+self.host+'\r\n\r\n'
        
        data = data.encode('utf-8')
        return data
        
    def send_request(self):
        sock.connect((self.host, 80))
        data = self.get_encoded_data()

        sock.send(data)

        response = ''
        response = sock.recv(4096).decode()

        return response
        

if __name__ == '__main__':
    args = sys.argv[1:]
    c = cCurl(args)
    response = c.send_request()
    c.show_response(response)
