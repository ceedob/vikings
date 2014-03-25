import sys, subprocess, time, os
from xml.dom import minidom
from subprocess import call
import pipes

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class mypipe:
    def __init__(self,prefix):
        self.prefix = prefix
    def write(self,s):
        sys.stdout.write(self.prefix + ": " + bcolors.WARNING + s + bcolors.ENDC+"\n")

maxlen = 0
filename = "/var/www/sites.xml"
#nullpipe = open("/dev/null", 'w')
start = True
if "stop" in sys.argv:
    sys.stdout.write(bcolors.FAIL + "STOPPING ALL SERVERS" + bcolors.ENDC+"\n")
    start=False
for i in sys.argv:
    if i[:7] == "--file=":
        filename = i[2:]
xmldoc = minidom.parse(filename)
sitelist = xmldoc.getElementsByTagName('site') 
if len(sitelist) > 1:
    sys.stdout.write("Found %i sites" % len(sitelist)+"\n")
elif len(sitelist) == 0:
    sys.stdout.write("Found 1 site \n")
else:
    sys.stdout.write("Found no sites \n")
    exit()
#sys.stdout.write(itemlist[0].attributes['name'].value+"\n")
processes = {}
ps = subprocess.Popen(["/bin/ps", "aux"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
ps = ps.communicate()[0].split("\n")
for s in sitelist :
    siteName = ""
    siteActions = []
    ports = []
    isstatic = False
    for i in s.childNodes:
        if i.nodeType == 1:
            #sys.stdout.write(dir(i)+"\n")
            if i.nodeName == "name":
                siteName = str(i.firstChild.nodeValue)
            if i.nodeName == "launch":
                if i.firstChild.nodeValue != None:
                    siteActions.append(i.firstChild.nodeValue)
#                elif i.firstChild.nodeName == "disabled":
#                    siteActions.append
                try:
                    ports.append(i.attributes["port"])
                except KeyError:
                    ports.append(None)
    sys.stdout.write(siteName + "\n" + "="*len(siteName)+"\n")
    for i in siteActions:
        if start:
            sys.stdout.write("   - Launching: %s" % i)
            sys.stdout.flush()
        try:
            proc = None
            if i in "".join(ps): 
                if start:
                    sys.stdout.write(bcolors.OKBLUE + " [RESTARTING]"+ bcolors.ENDC)  
                    sys.stdout.flush()                
                for p in ps:
                    if i in p:
                        subprocess.Popen(["/bin/kill",p.split()[1]])
                        if start:
                            time.sleep(5)
                            proc = subprocess.Popen(i.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=os.path.split(i.split()[1])[0])
        
            elif start:
                proc = subprocess.Popen(i.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=os.path.split(i.split()[1])[0])
                time.sleep(2)
            if proc.poll() != None:
                out, err = proc.communicate()
                raise Exception(err)
            maxlen = max(maxlen, len(i))
            processes[proc.pid] = (proc,i,siteName)
        except Exception, e:
            if start:
                sys.stdout.write(bcolors.FAIL + " [FAIL]"+"\n")
                sys.stdout.write(str(e) + bcolors.ENDC+"\n")
            else:
                sys.stdout.write(i + " is not running\n")
        else:    
            if start:
                sys.stdout.write(bcolors.OKGREEN + " [OK]" + bcolors.ENDC+"\n")

    sys.stdout.write("\n" +"\n")

if not start:
    for p in processes:
            processes[p][0].kill()
            sys.stdout.write(bcolors.FAIL + "killed %s of %s" % (processes[p][1],processes[p][2]) + bcolors.ENDC+"\n")
    exit()
while True:
    cmd = raw_input("viking > ")
    if cmd == "quit":
        for p in processes:
            processes[p][0].kill()
            sys.stdout.write(bcolors.FAIL + "killed %s of %s" % (processes[p][1],processes[p][2]) + bcolors.ENDC+"\n")
        sys.stdout.write("Goodbye"+"\n")
        exit()
    elif cmd == "list":
        for p in processes:
            sys.stdout.write(str(p) + " "*(10-len(str(p))) + processes[p][1]+" "*(maxlen+2-len(str(processes[p][1]))) + " of " + processes[p][2] + "\n")
    elif cmd == "detach":
        exit()
    elif cmd == "netstat":
        subprocess.Popen(["/bin/netstat","-lt"])

    elif cmd == "help":
        sys.stdout.write("Commands: list, detach, netstat, quit\n")
    else:
        todel = []
        for p in processes:
            retcode = processes[p][0].poll()
            if retcode != None:
                sys.stdout.write(bcolors.FAIL + "Process %s of %s  has quit" % (processes[p][1],processes[p][2]) + bcolors.ENDC+"\n")
                todel.append(p)
        while todel:
            del(processes[todel.pop()])