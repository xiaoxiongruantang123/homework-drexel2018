__Copyright__ =  "Copyright Li_Zhongxing 2020"  
__Author__ = "Li_Zhongxing"
__Version__ = "1.0" 

from subprocess import Popen, PIPE, DEVNULL
from matplotlib import pyplot as plt

def get_txt(repo,ver):
    cmd_tag = 'git tag -l ' + '"'+ ver + '.*"'
    value = Popen(cmd_tag, cwd = repo, stdout=PIPE)
    vtime, res = value.communicate()
    t_txt = vtime.decode('latin').encode('utf8').decode('utf8').split("\n")
    return t_txt

def get_list(x):
    t_list = []
    for i in x:
        data_get = 'git log -1 --pretty=format:\"%ct\" ' + str(i)
        t = Popen(data_get, cwd = repo, stdout=PIPE, stderr=DEVNULL)
        t_time, res1 = t.communicate()
        doc = t_time.decode('latin').encode('utf8').decode('utf8')
        t_list.append(doc)
    return t_list

def output(x, y):    
    plt.scatter(x, y)
    plt.title('time and order')
    plt.xlabel('time')
    plt.ylabel('order')
    plt.savefig('plot%s.png' % ver)

if __name__ == "__main__":
    address = "C:\Users\dell\Documents\GitHub\linux-stable"#The address of the file linux-stable.
    output(get_list(get_txt(address, "v4.5")), get_txt(address, "v4.5"))


