#!/usr/bin/env python
# coding: utf-8

# In[ ]:

biaozhi=False
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttc'))
import ollama as oa
co=oa.Client('http://localhost:11434')
a=input()
b=input("请输入文件名，推荐扩展名为txt：\n")
doc = SimpleDocTemplate(b, pagesize=A4)
stream=co.chat(model='qwen3:8b',messages=[{'role':'user','content':a}],stream=True)
m,n,reslai,reslai1,story=[],[],[],[],[]
styles = getSampleStyleSheet()
text_style = ParagraphStyle(
     'BodyStyle',
     parent=styles['Normal'],
     fontName='SimSun',
     fontSize=11,
     leading=14,
     alignment=TA_LEFT
 )
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
for z in range(len(rres)):
    if rres[z]!='':
        if rres[z][-1]=='|':
            resnumwei=z
#for z in range(len(rres)-resnumwei-1):
#    print(rres[resnumwei+z+1])
for z in range(resnumwei+1):
    reslai.append(rres[z])
for z in reslai:
    if z=='':
        pass
    else:
        reslai1.append(z)
shouhang=reslai1[0]+'\n'
reslai1.pop(0)
story.append(Paragraph(shouhang, text_style))
story.append(Spacer(1, 0.5*cm))
'''
for z in range(len(reslai1)):
    if reslai1[z]!='':
        if reslai1[z][0]=='|':
            resnumtou=z
            break
print(f"resnumtou is {resnumtou}.")
for z in range(resnumtou):
    reslai1.pop(0)'''
numoftable,hangbiao,biaotoures=0,[],[]
for item in reslai1:
     if item[0]!='|':
         numoftable+=1
         hangbiao.append(reslai1.index(item))
if len(hangbiao)>6:
     print("AI生成了不相干的多余废话，请AI再来一次")
     biaozhi=True
page=len(hangbiao)//3
col_widths = [4.5*cm, 3.5*cm, 3*cm, 3*cm]
if (page>0) and biaozhi:
    biao0,biao1,biao2=[],[],[]
    story.append(Paragraph(reslai1[0], text_style))
    story.append(Spacer(1, 0.25*cm))
    story.append(Paragraph(reslai1[1], text_style))
    story.append(Spacer(1, 0.25*cm))
    for i in range(page,hangbiao[3]-1):
         biaohang0=reslai1[i].replace("|","")
         biaohang=biaohang0.split(" ")
         biaohanglis=[]
         for item in biaohang:
             if item=="":
                 pass
             else:
                 biaohanglis.append(item)
         biao0.append(biaohanglis)
    table = Table(biao0, colWidths=col_widths)
    table.setStyle(TableStyle([
         # 表头样式
         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
         ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),
         ('FONTSIZE', (0, 0), (-1, 0), 11),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

         # 数据区域样式
         ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
         ('FONTSIZE', (0, 1), (-1, -1), 10),

         # 网格线
         ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
         ('BOX', (0, 0), (-1, -1), 1, colors.black),

         # 数字列右对齐
         ('ALIGN', (1, 1), (3, -1), 'RIGHT'),
     ]))
    story.append(table)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(reslai1[hangbiao[3]-1], text_style))
    story.append(Spacer(1, 0.25*cm))
    story.append(Paragraph(reslai1[hangbiao[3]], text_style))
    story.append(Spacer(1, 0.25*cm))
    for i in range(page+hangbiao[3]-1,hangbiao[5]-1):
         biaohang0=reslai1[i].replace("|","")
         biaohang=biaohang0.split(" ")
         biaohanglis=[]
         for item in biaohang:
             if item=="":
                 pass
             else:
                 biaohanglis.append(item)
         biao1.append(biaohanglis)
    table1 = Table(biao1, colWidths=col_widths)
    table1.setStyle(TableStyle([
         # 表头样式
         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
         ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),
         ('FONTSIZE', (0, 0), (-1, 0), 11),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

         # 数据区域样式
         ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
         ('FONTSIZE', (0, 1), (-1, -1), 10),

         # 网格线
         ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
         ('BOX', (0, 0), (-1, -1), 1, colors.black),

         # 数字列右对齐
         ('ALIGN', (1, 1), (3, -1), 'RIGHT'),
     ]))
    story.append(table1)
    story.append(Spacer(1, 0.5*cm))
    for i in range(page+hangbiao[5]-1,len(reslai1)):
         biaohang0=reslai1[i].replace("|","")
         biaohang=biaohang0.split(" ")
         biaohanglis=[]
         for item in biaohang:
             if item=="":
                 pass
             else:
                 biaohanglis.append(item)
         biao2.append(biaohanglis)
    table2 = Table(biao1, colWidths=col_widths)
    table2.setStyle(TableStyle([
         # 表头样式
         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
         ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),
         ('FONTSIZE', (0, 0), (-1, 0), 11),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

         # 数据区域样式
         ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
         ('FONTSIZE', (0, 1), (-1, -1), 10),

         # 网格线
         ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
         ('BOX', (0, 0), (-1, -1), 1, colors.black),

         # 数字列右对齐
         ('ALIGN', (1, 1), (3, -1), 'RIGHT'),
     ]))
    story.append(table2)
    story.append(Spacer(1, 0.5*cm))
    doc.build(story)
elif (page==0) and biaozhi:
    biao0=[]
    story.append(Paragraph(reslai1[0], text_style))
    story.append(Spacer(1, 0.25*cm))
    story.append(Paragraph(reslai1[1], text_style))
    story.append(Spacer(1, 0.25*cm))
    for i in range(page,len(reslai1)):
         biaohang0=reslai1[i].replace("|","")
         biaohang=biaohang0.split(" ")
         biaohanglis=[]
         for item in biaohang:
             if item=="":
                 pass
             else:
                 biaohanglis.append(item)
         biao0.append(biaohanglis)
    table = Table(biao0, colWidths=col_widths)
    table.setStyle(TableStyle([
         # 表头样式
         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
         ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),
         ('FONTSIZE', (0, 0), (-1, 0), 11),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

         # 数据区域样式
         ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
         ('FONTSIZE', (0, 1), (-1, -1), 10),

         # 网格线
         ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
         ('BOX', (0, 0), (-1, -1), 1, colors.black),

         # 数字列右对齐
         ('ALIGN', (1, 1), (3, -1), 'RIGHT'),
     ]))
    story.append(table)
    story.append(Spacer(1, 0.5*cm))
    doc.build(story)

