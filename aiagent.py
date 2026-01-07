import ollama as oa
co=oa.Client('http://localhost:11434')
a=input()
b=input("请输入文件名，推荐扩展名为csv")
stream=co.chat(model='qwen3:8b',messages=[{'role':'user','content':a}],stream=True)
m,n,reslai,reslai1=[],[],[],[]
for c in stream:
    m.append(c['message']['content'])
for cc in m:
    if cc =='':
        pass
    else:
        n.append(cc)
res=''
for p in n:
    res=res+p
rres=res.split('\n')
#for z in range(len(rres)):
#    if rres[z]=='### 说明：':
#        resnum=z
for z in range(len(rres)):
    if rres[z]!='':
        if rres[z][-1]=='|':
            resnum=z
for z in range(resnum):
    reslai.append(rres[z])
for z in reslai:
    if z=='':
        pass
    else:
        reslai1.append(z)
fp=open(b,"w")
num=len(reslai1)
for z in range(num):
    t=reslai1[z]+'\n'
    fp.write(t)
fp.close()
