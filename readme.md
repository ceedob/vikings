Vikings
=======

Vikings is a utility program to replace a collection of `screen ...` instances for linux servers running multiple python servers on different ports. 
*Note*: this was only tested on python servers, but it should work with any other programming language.

Vikings works with a `sites.xml` file, which is at `/var/www/sites.xml` or custom specified with the --file= argument (do not include a space after the --file argument)

Starting and stoping
--------------------
With a properly configured sites.xml file, vikings can be launched as `python vikings.py`. Entering the command quit will terminate all of the spawed processes. Alternatively, vikings can detach and leave the spawed processes intact; these processes can subsiquently stopped with `python vikings.py stop`, which will instantly terminate them. 

As vikings was designed for servers in particular, launching the servers and restarting vikings without the `stop` argument will restart all servers.

Sites.xml
---------
Sites.xml contains a root sitelist node, which itself consists of site nodes. Each site node contains a name node and zero or more launch nodes. A name node simply contains text and acts as a decriptive name when interacting with sites in the cli. Each launch node represents a process that is spawned to run a server. Attributes of launch nodes will be passed as environment variables (in a future version). The cwd of each process is the folder of the script itself. Note that comments are properly supported.

An example sites.xml is provided below:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitelist>
    <site><!-- An example -->
        <name>411 Here</name>
        <launch>/usr/bin/python /var/www/411here/application.py</launch>
    </site>
    <site><!-- This is a static site -->
        <name>chrisdobson.ca</name>
    </site>
    <site>
        <name>fullservicewebsite.ca</name>
        <launch port="8891">/usr/bin/python /var/www/fullservicewebsite.ca/server.py</launch>
    </site>
    <site><!-- This site contains multiple launch nodes -->
        <name>DNSreport.ca</name>
        <launch port="8902">/usr/bin/python /var/www/dns.penguinleaf.com/webserver.py</launch>
        <launch port="9998">/usr/bin/python /var/www/dns.penguinleaf.com/checkserver.py</launch>
        <!-- Individual launch nodes can be commented out to disable -->
        <!--<launch port="9998">/usr/bin/python /var/www/dns.penguinleaf.com/monitorserver.py</launch>-->
        <launch>/usr/bin/python /var/www/dns.penguinleaf.com/monitorloop.py</launch>
    </site>
    <site>
        <name>penguinleaf.com</name>
        <launch port="8888">/usr/bin/python /var/www/dns.penguinleaf.com/webserver.py</launch>
    </site>
    <site>
        <name>write.penguinleaf.com</name>
        <launch port="8889">/usr/bin/python /var/www/dns.penguinleaf.com/webserver.py</launch>
    </site>
</sitelist>
```

TODO
----

- make launch attribute(s) get passed as environment variable(s)
- convert console interface in to argv parameters
- add functionality to target indivitual servers or sites
