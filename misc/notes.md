```

sudo tcpdump -i any dst port 389 and tcp -nn -s 0 -v

sudo tcpdump -i any dst port 389 -nn -s 0 -w ldap_outbound.pcap


ss -pnt sport = :389

##
ss -pnt dport = :389

lsof -iTCP -sTCP:ESTABLISHED -nP | grep ':389'


netstat -pant | grep ':389'


ps -fp 1234


find /etc -type f -name "*.conf" -exec grep -Hn "ldap" {} +

```
