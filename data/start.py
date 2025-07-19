#path="/var/log/syslog"
#path="/var/log/auth.log"
#path="/var/log/dmesg"
#path="/var/log/kern.log"
path="/var/log/Xorg.0.log"

fn=os.path.basename(path)

with open(path,"r") as f:
    data=f.read()
    print(f.read())
    with open(f"{fn}.txt","w") as f1:
        f1.write(data)
    f1.close()
f.close()
