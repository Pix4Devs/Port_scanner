#!/usr/bin/env python3
import optparse
from socket import *
from threading import *
screenLock = Semaphore(value=1)
def connScan(tgtHost,tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))
        connSkt.send(b'Hello\r\n')
        results = connSkt.recv(100)
        results = results.decode().removesuffix('\r\n')
        screenLock.acquire()
        print(f'[+] {tgtPort}/tcp open')
        print(f'[+] {str(results)}')
    except Exception as e:
        screenLock.acquire()
        print(f'[-] {tgtPort}/tcp closed')
    finally:
        screenLock.release()
        connSkt.close()

def portScan(tgtHost,tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print(f'[-] Cannot resolve {tgtHost}: Unknown host')
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print(f'[+] Scan Results for: {tgtName[0]}')
    except:
        print(f'[+] Scan Results for: {tgtIP}')
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()

def main():
    parser = optparse.OptionParser('usage portscanner: -H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost',type='string',help='specify target host')
    parser.add_option('-p', dest='tgtPort',type='string',help='specify target ports separated by a comma')
    (options,args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')
    if (tgtHost == None) | (tgtPorts[0] == None):
        print(parser.usage)
        exit(0)
    portScan(tgtHost,tgtPorts)

if __name__ == '__main__':
    main()
