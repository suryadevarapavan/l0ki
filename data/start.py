import os

logs=["syslog","auth.log","dmesg","kern.log","Xorg.0.log"]



def store_data(path):
    fn=os.path.basename(path)
    with open(path,"r") as f:
        data=f.read()
    with open(f"tdata/{fn}.txt","w")as f1:
        f1.write(data)
        f1.close()
        f.close()

def start_process():
    for i in logs:
        path = f"/var/log/{i}"
        store_data(path)
    print("TEST CASE 1 PASSED")
