#
# References: 对字符串切割 https://www.cnblogs.com/adampei-bobo/p/6378390.html
# git命令不在仓库中运行 https://www.cnblogs.com/linyihai/p/5696934.html
from subprocess import Popen, PIPE, DEVNULL


# 获得commits:author
# 有的commits有两个作者，此处使用:规避了这种情况  '2f633d5820e4': 'Tan', ' Tee Min'
git_cmd = 'git -C C:/Users/admin/Desktop/linux-stable log --no-merges --pretty=format:"%h:%an" --since ==2019-12-10'
git_cnt = Popen(git_cmd, stdout=PIPE, stderr=DEVNULL, shell=True)
com_an,non = git_cnt.communicate()
# 构建{commit:author}
# txt = data.decode('latin').encode('utf8').decode('utf8').split('\n')
com_ans = dict([s.split(':') for s in com_an.decode('latin').encode('utf8').decode('utf8').split('\n')])
# 统计每个人的提交次数，构建{author:numbers}
an_count=dict()
ans = list(com_ans.values())
for an in ans:
    an_count[an] = an_count.get(an, 0) + 1
    # 如果an在字典中，那么更新字典的值；反正则记为1
# 生成{commit:(author,numbers}
print(an_count)
