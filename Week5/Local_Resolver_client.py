












from rdt import *

serverName = "127.0.0.1"
serverPort = 54831

dns_address = "223.5.5.5"
dns_port = 53

clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentences:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
