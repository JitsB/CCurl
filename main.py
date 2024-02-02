import sys
from turtle import exitonclick
import socket

sock = socket.socket()

class cCurl:
    def get_method(self, api_request):
        method = 'GET'
        if '-X' in api_request:
            method = api_request[api_request.index('-X')+1]
            api_request.pop(api_request.index('-X')+1)
            api_request.remove('-X')
            
        return method

    def deconstruct_api_request(self, api_request):
        is_verbose = False
        if '-v' in api_request:
            is_verbose = True
            api_request.remove('-v')
        else:
            is_verbose = False
        
        headers = ""
        data = {}
        
        if '-H' in api_request:
            headers = api_request[api_request.index('-H')+1]
            api_request.remove('-H')
            api_request.remove(headers)
            
        if '-d' in api_request:
            data = api_request[api_request.index('-d')+1]
            api_request.remove('-d')
            api_request.remove(data)
        
        protocol, rest_of_the_url = api_request[0].split('//')
        protocol_version = "1.1"
        
        if not ':' in rest_of_the_url:
            url_split = rest_of_the_url.split('/')
            rest_of_the_url = url_split[0]+':80/'+url_split[1]

        host_with_method = rest_of_the_url
        host = host_with_method.split('/')[0]
        host = host.split(':')[0]
        
        return protocol, protocol_version, host, host_with_method, is_verbose, headers, data

    def __init__(self, api_request):
        
        method = self.get_method(api_request)
        protocol, protocol_version, host, host_with_method, is_verbose, headers, data = self.deconstruct_api_request(api_request)
        

        self.protocol = protocol
        self.protocol_version = protocol_version
        self.is_verbose = is_verbose
        self.host = host
        self.host_with_method = host_with_method
        self.method = method
        self.data = data
        self.headers = headers
    
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
        data = self.method.upper() + " /"+self.method.lower()+ ' '+self.protocol[0:-1].upper()\
        +'/'+self.protocol_version+'\r\n'+'Host: www.'+self.host+':80\r\n\r\n'
        
        content_length = len(self.data)
        if self.method == 'POST' or self.method == 'PUT':
            data = data[::-1]
            data = data.replace('\r\n', '', 1)
            data = data[::-1]
            data += f"{self.headers}\r\nContent-Length: {content_length}\r\n\r\n{self.data}"
        
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
