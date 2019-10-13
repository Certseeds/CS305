import dns.resolver
openTCP = False
a = dns.resolver.query("www.baidu.com",'A',tcp=openTCP)
for i in a.response.answer:
    print(1)
    print(i)
    for j in i.items:
        print(j)



