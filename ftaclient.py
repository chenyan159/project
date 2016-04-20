#!/usr/bin/env python

import time, sys
from socket import *
from rtp import rtp
from threads import RecvThread, SendThread

# FxAClient
# deals with the client side command line arguments and supports:
# Connect - to establish connection
# Get File(File Name) - download the file from server
# Post File (File Name) - upload the file to server
# Window (size) - change window size, default window size = 2
# Disconnect - close the connection

def main():
    window = 2
    rtpProtocol = None

    # Handling the argument
    arg = sys.argv
    if len(arg) != 3:
        print 'Invalid command. Please try again.'
        sys.exit()

    arg1 = arg[1].split(":")

    # Server IP address
    serverIP = arg1[0];

    if not _validIP(serverIP):
        print 'IP address is not valid, please try again'
        sys.exit()

        # Dest. port number
    desPort = int(arg1[1])
    if not 0 < desPort < 65536:
        print 'Invalid port number. Please try again.'
        sys.exit()

    window = int(arg[2])


    log = "output-client.txt"

    clientProtocol = None
    sendThread = None

    connThread = None
    sThread = None
    hostAddress = '127.0.0.1'
    # connect
    rtpProtocol = rtp(hostAddress, 8889, serverIP, desPort, None, True)
    clientProtocol = RecvThread(rtpProtocol)
    clientProtocol.start()
    rtpProtocol.connect()
    rtpProtocol.setWindowSize(window)
    #execute user's commend
    while True:
        time.sleep(.500)
        Sinput = raw_input("get F - to download the file from server \n"
                    + "post G - to upload the file to server \n"
                    + "get-post F G - to download F and upload G at same time \n"
                    + "disconnect - to close the connection\n"
                    + 'quit - to quit the application\n')
        # get file form server
        if "get-post" in Sinput:
            if rtpProtocol != None:
                s = Sinput.split(' ')
                sendThread = SendThread(rtpProtocol, s[2])
                sendThread.start()
                rtpProtocol.getFile(s[1])
        elif "get" in Sinput:
            if rtpProtocol != None:
                s = Sinput.split()
                rtpProtocol.getFile(s[1])
        # post file form server
        elif "post" in Sinput:
            if rtpProtocol != None:
                s = Sinput.split()
                sendThread = SendThread(rtpProtocol, s[1])
                sendThread.start()
        #close connection
        elif Sinput.__eq__("disconnect"):
            if rtpProtocol != None:
                rtpProtocol.close()
                clientProtocol.stop()
                rtpProtocol.socket.close()
                rtpProtocol = None
        elif Sinput.__eq__("quit"):
            if rtpProtocol:
                print 'disconnect before quit'
            else:
                break


# check IP format validation
def _validIP(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for num in parts:
        try:
            part = int(num)
        except ValueError:
            print 'Invalid IP. Please try again.'
            sys.exit()
        if not 0 <= part <= 255:
            return False
    return True


if __name__ == "__main__":
    main()