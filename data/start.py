path="/var/log/syslog"
with open(path,"r") as f:
    data=f.read()
    print(f.read())
    with open("syslog.txt","w") as f1:
        f1.write(data)
    f1.close()
f.close()
