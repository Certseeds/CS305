import dns.resolver
dns.resolver.query("www.baidu.com",'a')
a = dns.resolver.query("www.baidu.com",'a')
print(a)
for i in a.response.answer:
    for j in i.items:
        print(j)