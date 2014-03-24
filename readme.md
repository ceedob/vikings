Vikings
=======

Vikings is a utility program to replace a collection of `screen ...` instances for linux servers running multiple python servers on different ports.

Vikings works with a `sites.xml` file, which is by default at `/var/www/sites.xml` or custom specified with the -f argument (do not include a space after the -f argument)

Sites.xml
---------
Sites.xml contains a root sitelist node, which itself consists of site nodes. Each site node contains a name node and zero or more launch nodes. A name node simply contains text and acts as a decriptive name when interacting with sites in the cli. Each launch node represents a process that is spawned to run a server. Attributes of launch nodes will be passed as environment variables (in a future version).

An example sites.xml is provided below:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitelist>
    <site>
        <name>411 Here</name>
        <launch>/usr/bin/python /var/www/411here/application.py</launch>
    </site>
    <site>
        <name>chrisdobson.ca</name>
    </site>
    <site>
        <name>fullservicewebsite.ca</name>
        <launch port="8891">/usr/bin/python /var/www/fullservicewebsite.ca/server.py</launch>
    </site>
    <site>
        <name>bitcoin.penguinleaf.com</name>
        <launch port="8081">/usr/bin/python /var/www/bitcoin.penguinleaf.com</launch>
    </site>
    <site>
        <name>DNSreport.ca</name>
        <launch port="8902">/usr/bin/python /var/www/dns.penguinleaf.com/webserver.py</launch>
        <launch port="9998">/usr/bin/python /var/www/dns.penguinleaf.com/checkserver.py</launch>
        <launch port="9998">/usr/bin/python /var/www/dns.penguinleaf.com/monitorserver.py</launch>
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
