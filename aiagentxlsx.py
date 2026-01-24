import ollama as oa
import openpyxl
from openpyxl import Workbook
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
            resnumwei=z
for z in range(len(rres)-resnumwei-1):
    print(rres[resnumwei+z+1])
for z in range(resnumwei):
    reslai.append(rres[z])
for z in reslai:
    if z=='':
        pass
    else:
        reslai1.append(z)
shouhang=reslai1[0]+'\n'
for z in range(len(reslai1)):
    if reslai1[z]!='':
        if reslai1[z][0]=='|':
            resnumtou=z
            break
print(f"resnumtou is {resnumtou}.")
for z in range(resnumtou):
    reslai1.pop(0)
wb = Workbook()
ws = wb.active
t=[]
ceshi=[]
for i in range(lenr):
    t=[]
    ceshi=reslai1[i].split('|')
    for p in range(len(ceshi)):
        if ceshi[p]=='':
            pass
        else:
            t.append(ceshi[p])
    for q in range(len(t)):
        ws.cell(row=i+1,column=q+1).value=t[q]
wb.save(b)
wb.close()
