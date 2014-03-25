import sys, subprocess, time
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
nullpipe = open("/dev/null", 'w')
for i in sys.argv:
    if i[:2] == "-f":
        filename = i[2:]
xmldoc = minidom.parse(filename)
sitelist = xmldoc.getElementsByTagName('site') 
sys.stdout.write("Found %i site(s)" % len(sitelist)+"\n")
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
                siteActions.append(i.firstChild.nodeValue)
                try:
                    ports.append(i.attributes["port"])
                except KeyError:
                    ports.append(None)
    sys.stdout.write(siteName + "\n" + "="*len(siteName)+"\n")
    for i in siteActions:
        sys.stdout.write("   - Launching: %s" % i)
        try:
            proc = subprocess.Popen(i.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(2)
            code = proc.poll()
            if proc.poll() != None:
                if i in "".join(ps): 
                    sys.stdout.write(bcolors.OKBLUE + " [RESTARTING]"+ bcolors.ENDC)                  
                    for p in ps:
                        if i in p:
                            subprocess.Popen(["/bin/kill",p.split()[1]])
                            time.sleep(5)
                            proc = subprocess.Popen(i.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            time.sleep(2)
                if proc.poll() != None:
                    out, err = proc.communicate()
                    raise Exception(err)
            maxlen = max(maxlen, len(i))
            processes[proc.pid] = (proc,i,siteName)
        except Exception, e:
            sys.stdout.write(bcolors.FAIL + " [FAIL]"+"\n")
            sys.stdout.write(str(e) + bcolors.ENDC+"\n")
        else:    
            sys.stdout.write(bcolors.OKGREEN + " [OK]" + bcolors.ENDC+"\n")

    sys.stdout.write("\n" +"\n")


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
   	elif cmd == "help":
   		sys.stdout.write("Commands: list, detach, quit")
    else:
        todel = []
        for p in processes:
            retcode = processes[p][0].poll()
            if retcode != None:
                sys.stdout.write(bcolors.FAIL + "Process %s of %s  has quit" % (processes[p][1],processes[p][2]) + bcolors.ENDC+"\n")
                todel.append(p)
        while todel:
            del(processes[todel.pop()])

