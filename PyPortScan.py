import sys
import socket
import time
import threading
from datetime import datetime
from queue import Queue
import array

printLock = threading.Lock()
firstPort = 1
lastPort = 1000
timeoutV = 1
threads = 100

def openP():
    openP.counter += 1
openP.counter = 0

def closedP():
    closedP.counter += 1
closedP.counter = 0

def time_convert(sec):
    min = sec // 60
    sec = sec % 60
    hour = min // 60
    min = min % 60
    print("Time elapsed: {0}:{1}:{2}".format(int(hour),int(min),int(sec)))

def helppage():
    print("\n\nPyPortScan v.1.1 created by Hayden Aspiranti. 2021.")
    print("-" * 50)
    print("HELP MENU\n\n")
    print("Ports are scanned by default with 100 threads set at a 1 second timeout.\n")
    print("-p       --indiv-port | Scan individual ports. Use syntax '-p [port] [port] ... '")
    print("-ap       --all-ports | Scan all 65535 ports.")
    print("-f             --fast | Set total threads to 500. There is a chance some open ports may be missed.")
    print("-s             --slow | Set timeout to 2 seconds. This is beneficial for a more thorough approach.")
    exit()

if len(sys.argv) >= 2:
    if sys.argv[1] == "--help":
        helppage()
    # Translate the hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Unknown argument. Refer to --help for more information.")

print("-" * 50)
print("Scanning Target: " + target)
print("Scanning started at: " + str(datetime.now().replace(microsecond=0)))
start_time = time.time()
print("-" * 50)

specificPorts = False
portsList = array.array("i",[])

# arg catch
for arg in sys.argv:
    if arg == "-ap" or arg == "--all-ports":
        lastPort = 65536
    elif arg == "-s" or arg == "--slow":
        timeoutV = 2
    elif arg == "-f" or arg == "--fast":
        threads = 500
    elif arg == "--help":
        helppage()
    elif arg == "-p" or arg == "--indiv-port":
        specificPorts = True
    elif specificPorts == True:
        try:
            portsList.append(int(arg))
        except:
            print("Unknown argument. Refer to --help for more information.")
            exit()
    # else:
    #     print("Unknown argument. Refer to --help for more information")
    #     exit()

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeoutV)
    try:
        con = s.connect((target,port))
        with printLock:
            print(port,'is open')
            openP()
        con.close()
    except:
        closedP()
        pass

def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

q = Queue()

for x in range(threads):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

portsToScan = range(firstPort,lastPort)

if specificPorts:
    portsToScan = portsList

for worker in portsToScan:
    q.put(worker)

q.join()

print("-" * 50)
print("Scanned",len(portsToScan), "ports")
print("{} port(s) open".format(openP.counter))
print("-" * 50)
end_time = time.time()
time_lapsed = end_time - start_time
time_convert(time_lapsed)
print("Scanning finished at: " + str(datetime.now().replace(microsecond=0)))
print("-" * 50)