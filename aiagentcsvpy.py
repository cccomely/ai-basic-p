import ollama as oa
co=oa.Client('http://localhost:11434')
a=input()
b=input("请输入文件名，推荐扩展名为csv：\n")
stream=co.chat(model='qwen3:8b',messages=[{'role':'user','content':a}],stream=True)
m,n,reslai,reslai1=[],[],[],[]
#for b in stream:
#    print(b['message']['content'],end='',flush=True)
for c in stream:
    m.append(c['message']['content'])
for cc in m:
    n.append(cc) if cc != '' else None
res=''
for p in n:
    res=res+p
rres=res.split('\n')
for z in range(len(rres)):
    if rres[z]!='':
        if rres[z][-1]=='|':
            resnumwei=z
for z in range(len(rres)-resnumwei-1):
    print(rres[resnumwei+z+1])
for z in range(resnumwei):
    reslai.append(rres[z])
for z in reslai:
    reslai1.append(z) if z != '' else None
shouhang=reslai1[0]+'\n'
for z in range(len(reslai1)):
    if reslai1[z]!='':
        if reslai1[z][0]=='|':
            resnumtou=z
            break
print(f"resnumtou is {resnumtou}.")
for z in range(resnumtou):
    reslai1.pop(0)
while True:
    temp=0
    for z in range(len(reslai1)):
        p=reslai1[z].replace("|","")
        (hanghao:=z,temp:=1) if ('----------' in p ) else None
    if temp==0:
        break
    reslai1.remove(reslai1[hanghao])
fp=open(b,"w")
fp.write(shouhang)
num=len(reslai1)
for z in range(num):
    t=reslai1[z]+'\n'
    fp.write(t)
fp.close()
