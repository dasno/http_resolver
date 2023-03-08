import socket
import re
import sys

def GETMethod(message):
    decoded = message.decode("utf-8")
    parsed = decoded.splitlines()
    msgtype = parsed[0][0:3]
    try:
        reqtype = re.search(r'\/(.*?)\?',parsed[0]).group(1)
        address = re.search(r'name=(.*?)\&',parsed[0]).group(1)
        addrType = re.search(r'type=(.*?)\ .',parsed[0]).group(1)
    except:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"
    
    if(msgtype != "GET"):
        return "HTTP/1.1405 Method Not Allowed\r\n\r\n"

    if((reqtype != "resolve" and reqtype != "dns-query")  or address == "" or (addrType != 'A' and addrType != "PTR")):
        return "HTTP/1.1 400 Bad Request\r\n\r\n"



    if(addrType == "A"):
        if(re.search('(?:^|\b(?<!\.))(?:1?\d?\d|2[0-4]\d|25[0-5])(?:\.(?:1?\d?\d|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])', address)):
            return "HTTP/1.1 400 Bad Request\r\n\r\n"
        try:
            adr = socket.gethostbyname(address)
        except:
            return "HTTP/1.1 404 Not Found\r\n\r\n"
    
    if(addrType == "PTR"):
        if(not re.search('(?:^|\b(?<!\.))(?:1?\d?\d|2[0-4]\d|25[0-5])(?:\.(?:1?\d?\d|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])',address)):
            return "HTTP/1.1 400 Bad Request\r\n\r\n"
        try:
            adr = socket.gethostbyaddr(address)[0]
        except:
            return "HTTP/1.1 404 Not Found\r\n\r\n"
        
    return ('HTTP/1.1 200 OK\r\n\r\n{0}:{1}={2}\n'.format(address, addrType, adr))

def POSTMethod(message):
    endOfHeader = False
    respList = []
    adr = ""
    decoded = message.decode("utf-8")
    sentOk = False
    parsed = decoded.splitlines()
    helpVar = 0
    lol = re.search(r'/(.*?) ',parsed[0])
    if(lol[1] != "dns-query"):
        c.send("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
        return
    for x in range (0, len(parsed)):
        if(parsed[x] == '' and endOfHeader == False):
            endOfHeader = True
            continue
        if(endOfHeader):
            try:
                address = re.search(r'(.*?)\:',parsed[x]).group(1)
                address = address.strip()
            except:
                continue
            addrType = parsed[x].split(":")
            addrType[1] = addrType[1].strip()
            if(addrType[1] == "A"):
                if(re.search('(?:^|\b(?<!\.))(?:1?\d?\d|2[0-4]\d|25[0-5])(?:\.(?:1?\d?\d|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])', address)):
                    continue
                try:
                    if(sentOk == False):
                        sentOk = True
                    adr = socket.gethostbyname(address)
                    respList.append(('{0}:{1}={2}\n'.format(address.strip(), addrType[1].strip(), adr)))
                except:
                    respList.append("NOT FOUND\n")
                    
                    pass
    
            elif(addrType[1].strip() == "PTR"):
                if(not re.search('(?:^|\b(?<!\.))(?:1?\d?\d|2[0-4]\d|25[0-5])(?:\.(?:1?\d?\d|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])', address)):
                    continue
                try:
                    if(sentOk == False):
                        sentOk = True
                    adr = socket.gethostbyaddr(address)[0]
                    respList.append(('{0}:{1}={2}\n'.format(address.strip(), addrType[1].strip(), adr)))
                except:
                    respList.append("NOT FOUND\n")
                    pass
                    
            else:
                if(sentOk == False):
                  continue
        
    if(len(respList)<=0):
        c.send("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
        return
    else:
        response = "HTTP/1.1 200 OK\r\n\r\n"
        for j in range(0,len(respList)):
            if(respList[j] == "NOT FOUND\n"):
                helpVar = helpVar + 1
                respList[j] = ""
            response = response + respList[j]
    if(helpVar == len(respList)):
        
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    c.send(response.encode())
            
sckt = socket.socket()

if(len(sys.argv) < 2):
    print("Please specify port")
    exit(1)
try:
    port = int(sys.argv[1])
except:
    print("Something wrong with specified port")
    exit(1)
print("Listening on port " + str(port))

try:
    sckt.bind(('', port))
except:
    print("Unavailable port")
    exit(1)
sckt.listen(5)


#Listening Loop
while True: 
  
    try:

        c, addr = sckt.accept()
    except:
        exit(0)     
    print ('Connection from', addr) 

    msg = c.recv(1024)

    decoded = msg.decode("utf-8")
    parsed = decoded.splitlines()
    
    if(parsed[0][0:3] == "GET"):
        response = GETMethod(msg)
        c.send(response.encode())
    elif(parsed[0][0:4] == "POST"):
        POSTMethod(msg)
    else:
        response = "HTTP/1.1 405 Method Not Allowed \r\n\r\n"
        c.send(response.encode())
    
    c.close()





    



