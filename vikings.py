import sys, subprocess
from xml.dom import minidom
from subprocess import call
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
        print self.prefix + ": " + bcolors.WARNING + s + bcolors.ENDC

filename = "/var/www/sites.xml"
nullpipe = open("/dev/null", 'w')
for i in sys.argv:
    if i[:2] == "-f":
        filename = i[2:]
xmldoc = minidom.parse(filename)
sitelist = xmldoc.getElementsByTagName('site') 
print "Found %i site(s)" % len(sitelist)
#print itemlist[0].attributes['name'].value
processes = {}
for s in sitelist :
    siteName = ""
    siteActions = []
    ports = []
    isstatic = False
    for i in s.childNodes:
        if i.nodeType == 1:
            #print dir(i)
            if i.nodeName == "name":
                siteName = str(i.firstChild.nodeValue)
            if i.nodeName == "launch":
                siteActions.append(i.firstChild.nodeValue)
                try:
                    ports.append(i.attributes["port"])
                except KeyError:
                    ports.append(None)
    print siteName + "\n" + "="*len(siteName)
    for i in siteActions:
        print "   - Launching: %s" % i,
        try:
            proc = subprocess.Popen(i.split(),stdout=nullpipe, stderr=nullpipe)
            processes[proc.pid] = (proc,i,siteName)
        except Exception, e:
            print bcolors.FAIL + "[FAIL]"
            print str(e) + bcolors.ENDC
        else:    
            print bcolors.OKBLUE + "[OK]" + bcolors.ENDC

    print "\n" 


while True:
    cmd = raw_input("viking > ")
    if cmd == "quit":
        for p in processes:
            processes[p][0].kill()
            print bcolors.FAIL + "killed %s of %s" % (processes[p][1],processes[p][2]) + bcolors.ENDC
        print "Goodbye"
        exit()
    else:
        todel = []
        for p in processes:
            retcode = processes[p][0].poll()
            if retcode != None:
                print bcolors.FAIL + "Process %s of %s  has quit" % (processes[p][1],processes[p][2]) + bcolors.ENDC
                todel.append(p)
        while todel:
            del(processes[todel.pop()])

