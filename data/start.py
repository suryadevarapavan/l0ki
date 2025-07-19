path="/var/log/syslog"
with open(path,"r") as f:
    print(f.read())
f.close()
