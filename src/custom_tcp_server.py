import socketserver

class AddressReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True