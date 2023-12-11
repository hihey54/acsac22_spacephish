import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import os
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity='all'
from urllib.parse import urlparse
from tld import get_tld,get_fld,parse_tld,is_tld
# from tqdm import tqdm
from bs4 import BeautifulSoup
# import requests
# import shutil #delete folder
import json
import pandas as pd
# from scipy.stats import pearsonr
import numpy as np
# from sklearn.feature_selection import SelectKBest,chi2,f_classif,RFE,SequentialFeatureSelector
# from sklearn.model_selection import train_test_split,GridSearchCV,cross_val_score,KFold,cross_val_predict,cross_validate
# import matplotlib.pyplot as plt
import re
import pickle
# from collections import Counter
pd.set_option('display.max_colwidth', None)
import csv
import base64
import cssutils
import openpyxl as xl
import random
import typo
from cssutils import parseStyle
import homoglyphs as hg
import randomcolor
import io
 

def addInLnk(ht,out_file):
    ind=ht.find('</body>')
    content=''
    for i in range(0,50):#50
        #add hidden internal items <a> or <img> "<img src=''/>" <a href='#' style='display:none'> can not see</a>\n
        con="<a href='#' style='display:none'>can not see </a>"+"\n"  #
        content=content+con
    final_string=ht[:ind]+content+ht[ind:]
    with open(out_file, 'w') as out:
        out.write(final_string)

'''
# change all <a  href="#" to <a href="javascript:void(0)" to do
#replace_ahref
def replace_ahref(ht,out_file):
    soup=BeautifulSoup(ht)

    for link in soup.find_all('a', href=True):
        print('lower is',link['href'].lower())
        if "#" in link['href'] or 'javascript' in link['href'].lower():
            #using jacascript:void(0) instead of "#"
            #link['href']="javascript:void(0)"
            #using "" instead of "#",javascript:void(0)
            link['href']=''
            #print('link is',link)
    #print('soup is',soup)
    with open(out_file, 'w') as out:
        out.write(str(soup))
'''
#del_title
def delTtl(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    try:
        title=soup.find('title')
        title.decompose()
    except:
        print('no title') 
    with open(out_file, 'w') as out:
        out.write(str(soup))
    print('success:',out_file)
#change_title
def modTtl(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    try:
        title=soup.find('title')
        title.string="Clarence Darrow was the most influential defense lawyer in the history of America. His closing arguments in one trial lasted for three days and reduced the trial judge to tears.The opposing lawyer in the Scopes Monkey trial died of a stroke a few days after the verdict. Darrow regularly overcame insurmountable odds to free or save his clients while onlookers flooded his courtrooms to hear his arguments. McRae does a wonderful job communicating the emotion and vigor that made Darrow so good at his job"
    except:
        print('no title') 
    with open(out_file, 'w') as out:
        out.write(str(soup))
#del html tag
#del_html
def brTg(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    ht=ht.replace("<html>","")
    ht=ht.replace("</html>","") 
    with open(out_file, 'w') as out:
        out.write(ht)
    print('success',out_file)
        
def del_attr(links):
    sus_item=["#",' ','javascript:void(0)','javascript::void(0)']
    del_item=[]
    for link in links:
        try:
            ori=link['src']
        except:
            ori=link['href']
        inter=[i for i in sus_item if i in ori.lower()]
        #print('inter is',inter)
        if len(inter)>0 or len(ori)<1:
            #print('delete link',link)
            del_item.append(link)
    #print('should delete items:',del_item)

    return del_item

#13 delete suspicious, target nulllinksinweb
# del_sus,delete suspicious links
def delSusLnk(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    anchors=soup.findAll('a',href=True)
    images=soup.findAll("img",src=True)
    links=soup.findAll('link',href=True)
    sounds=soup.findAll('source',src=True) #video and audio
    #print('anchors is',anchors)
    # delete anchors from html
    del_array=del_attr(anchors)+del_attr(images)+del_attr(links)+del_attr(sounds)
    #print('del_array is',del_array)
    for i in del_array: 
        i.decompose()  
    with open(out_file, 'w') as out:
        out.write(str(soup))
        
# 14 delete external links and null links target checkobject, metascript
def del_ex_attr(links):
    sus_item=["http://",'www.','https://','ftp:/','httpd:/',"#",'javascript:void(0)','javascript::void(0)']
    del_item=[]
    for link in links:
        try:
            ori=link['src']
        except:
            try:
                ori=link['href']
            except:
                ori=link['content']
        inter=[i for i in sus_item if i in ori.lower()]
        #print('inter is',inter)
        if len(inter)>0 or len(ori)<1:
            print('delete link',link)
            del_item.append(link)
    #print('should delete items:',del_item)

    return del_item

def del_external(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    anchors=soup.findAll('a',href=True)
    images=soup.findAll("img",src=True)
    links=soup.findAll('link',href=True)
    sounds=soup.findAll('source',src=True) #video and audio
    script=soup.findAll('script',src=True)
    meta=soup.findAll('meta',content=True)
    del_array=del_ex_attr(anchors)+del_ex_attr(images)+del_ex_attr(links)+del_ex_attr(sounds)+del_ex_attr(script)+del_ex_attr(meta)
    print('del_array is',del_array)
    for i in del_array: 
        i.decompose() 
    with open(out_file, 'w') as out:
        out.write(str(soup)) 
# delete footer tag, or any tags that include footer
def get_objects(ht):
    soup=BeautifulSoup(ht,features="html.parser")
    anchors=soup.findAll('a',href=True)
    images=soup.findAll("img",src=True)
    links=soup.findAll('link',href=True)
    sounds=soup.findAll('source',src=True) #video and audio
    script=soup.findAll('script',src=True)
    meta=soup.findAll('meta',content=True)
    objects=anchors+images+links+sounds+script+meta
    return objects
def check_class_foot(items):
    del_item=[]
    for item in items:
        if 'footer' in str(item['class']).lower():
            #print('item class includes footer',item)
            del_item.append(item)
    return del_item 
#delete all footer item
#del_footer
def delFtr(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    try:
        foots=soup.footer
        foots.decompose()
    except:
        print('no footer')
    #print('foots is, delte',foots) 
    #foots=soup.findAll('footer',href=True)
    anchors=soup.findAll('a',{"class":True})
    divs=soup.findAll('div',{"class":True})
    #print('div class is',divs)
    # delete
    del_array=check_class_foot(divs)+check_class_foot(anchors)

    for i in del_array:
        i.decompose()
    with open(out_file, 'w') as out:
        out.write(str(soup))
    print('success:',out_file)
    #print('del array is',del_array)

# change all sus links in footer to internal links
# change_footer
def replSusFtrLnk(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    sus_item=["#",'javascript:void(0)','javascript::void(0)']
    foots=soup.footer
    try:
        anchors=foots.findAll('a',href=True)
    #print('anchors are',anchors)
        for link in anchors:
            #print('link is',link)
            #ori=link['href']
            #print('ori href is',ori)
            inter=[i for i in sus_item if i in link['href'].lower()]
            #print('length of inter',len(inter))
            #print('len of link href %d, href is %s'%(len(link['href']),link['href']))
            if len(inter)>0 or len(link['href'])<1:
                #print('link is',link['href'])
                link['href']='test'
    except:
        print('no footer') 
    with open(out_file, 'w') as out:
        out.write(str(soup))
        
#delete all links of footer
def del_links_foot(ht,out_file):

    soup=BeautifulSoup(ht,features="html.parser")
    foot=soup.footer
    #print('foot is',foot)
    anchors=foot.findAll('a',href=True)
    images = foot.findAll("img")
    objects=anchors+images
    for link in objects:
        #print('del links',link)
        link.decompose()
    with open(out_file, 'w') as out:
        out.write(str(soup))
#delete copyright
def delCpy(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    #delete symbol
    symbol=u'\N{COPYRIGHT SIGN}'.encode('utf-8')
    symbol=symbol.decode('utf-8')
    print('symbol',symbol)
    pattern=r''+symbol
    for tag in soup.findAll(text=re.compile(pattern)):
        copyrighttext=tag.parent.text
        print('copyright is',copyrighttext)
        tag_name=tag.parent
        tag_name.decompose()
    with open(out_file, 'w') as out:
        out.write(str(soup))
        #print('tag is',tag.parent)

#change copyright   more mal
# change_copyright
def modCpy(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    #delete symbol
    symbol=u'\N{COPYRIGHT SIGN}'.encode('utf-8')
    symbol=symbol.decode('utf-8')
    title=soup.find('title')
    #print('title is',title.text)
    pattern=r''+symbol
    for tag in soup.findAll(text=re.compile(pattern)): 
        tag_name=tag.parent
        #random text 
        tag.parent.string="Clarence Darrow was the most influential defense lawyer in the history of America. His closing arguments in one trial lasted for three days and reduced the trial judge to tears.The opposing lawyer in the Scopes Monkey trial died of a stroke a few days after the verdict. Darrow"
         
    with open(out_file, 'w') as out:
        out.write(str(soup))
        #print('tag is',tag.parent)
#del_span

def delSpn(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    spans=soup.findAll('span')
#     print('all span is',spans)
    for i in spans:
        i.decompose()
        #print('delete span',i)
    with open(out_file, 'w') as out:
        out.write(str(soup))
    print('success:',out_file)
    
#delete sus forms ""
def delSusFrm(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    forms=soup.findAll('form',action=True)
    sus_item=["http://",'www.','https://','ftp:/','httpd:/',"#",'javascript:void(0)','javascript::void(0)','javascript']

    for form in forms:
        try:
            ori=form['action']
        except:
            print('no form, no change')
        inter=[i for i in sus_item if i in ori.lower()]
        #print('inter is',inter)
        if len(inter)>0 or len(ori)<1:
            print('delete form',form)
            form.decompose()
    with open(out_file, 'w') as out:
        out.write(str(soup))

# delete all login form
def delFrm(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    forms=soup.findAll('form',action=True)

    for form in forms:
        form.decompose()
#     print('soup is',str(soup))
    with open(out_file, 'w') as out:
        
        out.write(str(soup))
    print('success',out_file)

#delete hidden form and hidden items in form
def del_form_par(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    forms=soup.findAll('form',action=True)
    forms1=soup.form
    #print('len of children',forms1.children)
    try:
        for child in forms1.children:
            #print('child is',child) 
            if child.name == 'input' and 'hidden' in child['type']:
                #print('delete this child input',child)
                child.decompose()
    except:
        print('form no child')
    sus_item=["http://",'www.','https://','ftp:/','httpd:/',"#",'javascript:void(0)','javascript::void(0)','javascript']
    #type=hidden
    for form in forms:
        try:
            ori=form['action']
        except:
            print('no form, no change')
        inter=[i for i in sus_item if i in ori.lower()]
        #print('inter is',inter)
        if len(inter)>0 or len(ori)<1:
            print('delete form',form)
            form.decompose() 
    with open(out_file, 'w') as out:
        out.write(str(soup))
#add internal forms for the sfh,-1
def add_interform(ht,out_file):
    soup=BeautifulSoup(ht,features="html.parser")
    ind=ht.find("</body>") 
    content=""
    for j in range(1,num):
        for i in range (0,20*j):

            string="<form action="/">"
            content=content+string
            final_string=ht[:ind+6]+content+ht[ind+6:]

        '''
        if favicon1 is None and favicon2 is None:
            string="<link rel='icon' href='test_icon.ico'>"
            final_string=ht[:ind+6]+string+ht[ind+6:]
        else:
            final_string=ht
        '''
        out_file=out_file1+"_"+str(j)+".html"
        with open(out_file, 'w') as out:
            out.write(final_string)
        print('j success',j)  
    with open(out_file, 'w') as out:
        out.write(str(soup))  
#typos for both tag and text
def hmg(ht,out_file1):
    old_ind=[]
    # percent
    rounds=[0.1]#,0.7,0.8,0.9,1
    for j in range(0,len(rounds)):
        value=rounds[j]
        #print('value is',value)
        roun=int(value*len(ht))
        #print('rounds is',roun)
        for i in range(0,roun):

            ind=random.randint(0, len(ht))
            if ind not in old_ind:
                old_ind.append(ind)
            else:
                ind=random.randint(0, len(ht))
                continue
            cha=ht[ind-1]
            if cha.isspace()==False:
                #print('cha is',cha)
                all_ob=hg.Homoglyphs().get_combinations(cha)
                length_ob=len(all_ob)-1
                ob_ind=random.randint(0, length_ob)
                ob_cha=all_ob[ob_ind]
                ht = ht[:ind] + ob_cha + ht[ind+1:]
            else:
                #print('char is space',cha)
                continue 
#         out_file=out_file1+str(j)+".html"
        #print('out_file is',out_file)
        with open(out_file1,'w') as f:
            f.write(ht)
#         print('j success',j)
    print('success',out_file1)


#add_icon
def addIcn(ht,out_file1,num):
    soup = BeautifulSoup(ht,"html.parser")
    #print('soup is',soup)
    #print('icon is',soup.find(rel="shortcut icon"))
    #print('short icon is ',soup.find(rel="icon"))
    favicon1 = soup.find(rel="shortcut icon")
    favicon2=soup.find(rel="icon")
    #print('len of favicon',favicon1 is None)
    ind=ht.find("<head>")
    #
    content=""
    for j in range(1,num):
        for i in range (0,20*j):

            string="<link rel='icon' href='test_icon.ico'>"
            content=content+string
            final_string=ht[:ind+6]+content+ht[ind+6:]

        '''
        if favicon1 is None and favicon2 is None:
            string="<link rel='icon' href='test_icon.ico'>"
            final_string=ht[:ind+6]+string+ht[ind+6:]
        else:
            final_string=ht
        '''
        out_file=out_file1+"_"+str(j)+".html"
        with open(out_file, 'w') as out:
            out.write(final_string)
        print('j success',j)



# add favicon
def add_image_invi(ht,out_file1,num):
    soup = BeautifulSoup(ht,"html.parser")
    ind=ht.find("</body>")
    content=""
    for j in range(1,num):
        for i in range (0,20*j):
            string="<img src='/'>"
            content=content+string
            final_string=ht[:ind]+content+ht[ind:]

        out_file=out_file1+"_"+str(j)+".html"
        with open(out_file, 'w') as out:
            out.write(final_string)
        print('j success',j)

def add_image_vi(ht,out_file1,num):
    soup = BeautifulSoup(ht,"html.parser")
    ind=ht.find("</body>")
    content=""
    for j in range(1,num):
        for i in range (0,20*j):
            string="<img src='test_icon.png'>"
            content=content+string
            final_string=ht[:ind]+content+ht[ind:]

        out_file=out_file1+"_"+str(j)+".html"
        with open(out_file, 'w') as out:
            out.write(final_string)
        print('j success',j)
# 
def addSusLnk(ht,out_file1,num):
    soup = BeautifulSoup(ht,"html.parser")
    ind=ht.find("</body>")
    content=""
    for j in range(4,num):
        for i in range (0,20*j):
            string="<a href='#'> </a>"+"\n"+"<a href='/'> </a>"+"<a href='#skip'> </a>"+"<a href='javascript:void(0)'> </a>"
            content=content+string
            final_string=ht[:ind]+content+ht[ind:]

        out_file=out_file1+"_"+str(j)+".html"
        with open(out_file, 'w') as out:
            out.write(final_string)
        print('j success',j)
# adding small images to the bottom of the wepage, footer,

def addImgBot(ht,out_file1,num):
    #add all images
    folder="./images/"
    soup = BeautifulSoup(ht,"html.parser")
    ind=ht.find("</footer>")
    content=""
    if ind==-1:
        #print('no footer, need add')
        ind=ht.find("</body>")
        content="<footer style='position: absolute;bottom:0;'>"
    for i in range(0,num): 
        image='img'+str(i+1)+'.png'
        string="<img src='./images/"+image+"'>"
        content=content+string
    if ht.find("</footer>")==-1:
        content=content+"</footer>"
    #print('content is',content)

    final_string=ht[:ind]+content+ht[ind:]
    with open(out_file1, 'w') as out:
        out.write(final_string)
    print('success',out_file1)
#add background
#add_large_image
def modBgimg(ht,out_file):
    soup = BeautifulSoup(ht,"html.parser")
    ind=ht.find("</head>")
    content="<style>body {background-image:url('./background.jpg');}</style>"
    final_string=ht[:ind]+content+ht[ind:]
    with open(out_file, 'w') as out:
        out.write(final_string)
    print('success',out_file)

def cp_html(ht,out_file):
    soup = BeautifulSoup(ht,"html.parser")
    with open(out_file, 'w') as out:
        out.write(ht)
    print('success',out_file)


# change the color of background, div
# change_colorback
def modBgClr(html,out_file):

    c1=random.randint(0, 254)
    c2=random.randint(0, 254)
    c3=random.randint(0, 254)

    ind=html.find("</head>")
    content="<style>body {background-color:rgb("+str(c1)+","+str(c2)+","+str(c3)+");}</style>"
    #print('content is',content)
    final_string=html[:ind]+content+html[ind:]
    soup = BeautifulSoup(final_string,"html.parser")
    divs=soup.findAll('div',style=True)
    #print('divs is',divs)
    for div in divs:

        d_style=parseStyle(div['style'])
        d_style['background-color'] = 'red'
        div['style'] = d_style.cssText
        #print('div is',div)
    #print('final string is',final_string)
    with open(out_file, 'w') as out:
        out.write(str(soup))
    print('success',out_file)


#change the color of font

def modFntClr(ht,out_file):
    soup = BeautifulSoup(ht,"html.parser")
    ind=ht.find("</head>")
    rand_color=randomcolor.RandomColor()
    color=rand_color.generate()
    content="<style>body {color:"+color[0]+"}</style>"
#     print('content is',content)
    final_string=ht[:ind]+content+ht[ind:]
    with open(out_file, 'w') as out:
        out.write(final_string)
    print('success',out_file)
#change the font of the text
#change_fontsize
def modFntSiz(ht,out_file):
    soup = BeautifulSoup(ht,"html.parser")
    ind=ht.find("</head>")
    content="<style>body {font-size:0;}</style>"
    final_string=ht[:ind]+content+ht[ind:]
    with open(out_file, 'w') as out:
        out.write(final_string)
    print('success',out_file)
#change the font type
#change_fonttype
def modFntTyp(ht,out_file):
    soup = BeautifulSoup(ht,"html.parser")
    ind=ht.find("</head>")
    content="<style>body{font-style:italic;}</style>"
    final_string=ht[:ind]+content+ht[ind:]
    with open(out_file, 'w') as out:
        out.write(final_string)
    print('success',out_file)

#break the body and html
#delete the body
def delBdy(ht, out_file):
    soup = BeautifulSoup(ht,"html.parser")
    try:
        body=soup.body
        body.decompose()
    except:
        print('no body')
    with open(out_file, 'w') as out:
        out.write(str(soup))
# break_body
def brTgs(ht,out_file):
    soup = BeautifulSoup(ht,"html.parser")
    ht=ht.replace("</body>","")
    ht=ht.replace("</head>","")
    ht=ht.replace("<div ","")

    with open(out_file, 'w') as out:
        out.write(ht)
    print('success:',out_file)
#delete the html
#del_html_all
def delHt(ht, out_file):
    soup = BeautifulSoup(ht,"html.parser")
    try:
        body=soup.html
        body.decompose()
    except:
        print('no body')
    with open(out_file, 'w') as out:
        out.write(str(soup))
#add more text to the html
#add_text
def addLngTxt(ht,out_file):
    soup = BeautifulSoup(ht,"html.parser")
    ind=ht.find("</body>")
    string="Donald McRae tells the story of the one man who, in the span of just two years, pioneered the use of expert witnesses in American courts, upheld the teaching of evolution in public schools,  and saved a family of 11 from an unjust murder conviction. Clarence Darrow was the most influential defense lawyer in the history of America. His closing arguments in one trial lasted for three days and reduced the trial judge to tears.The opposing lawyer in the Scopes Monkey trial died of a stroke a few days after the verdict. Darrow regularly overcame insurmountable odds to free or save his clients while onlookers flooded his courtrooms to hear his arguments. McRae does a wonderful job communicating the emotion and vigor that made Darrow so good at his job.\
Well worth the read.cRae tells the story of the one man who, in the span of just two years, pioneered the use of expert witnesses in American courts, upheld the teaching of evolution in public schools, and saved a family of 11 from an unjust murder conviction. Clarence Darrow was the most influential defense lawyer in the history of America. His closing arguments in one trial lasted for three days and reduced the trial judge to tears.The opposing lawyer in the Scopes Monkey trial died of a stroke a few days after the verdict. Darrow regularly overcame insurmountable odds to free or save his clients while onlookers flooded his courtrooms to hear his arguments. McRae does a wonderful job communicating the emotion and vigor that made Darrow so good at his job.\
Well worth the readcRae tells the story of the one man who, in the span of just two years, pioneered the use of expert witnesses in American courts, upheld the teaching of evolution in public schools, and saved a family of 11 from an unjust murder conviction. Clarence Darrow was the most influential defense lawyer in the history of America. His closing arguments in one trial lasted for three days and reduced the trial judge to tears.The opposing lawyer in the Scopes Monkey trial died of a stroke a few days after the verdict.Darrow regularly overcame insurmountable odds to free or save his clients while onlookers flooded his courtrooms to hear his arguments. McRae does a wonderful job communicating the emotion and vigor that made Darrow so good at his job.\
Well worth the readcRae tells the story of the one man who, in the span of just two years, pioneered the use of expert witnesses in American courts, upheld the teaching of evolution in public schools, and saved a family of 11 from an unjust murder conviction. Clarence Darrow was the most influential defense lawyer in the history of America. His closing arguments in one trial lasted for three days and reduced the trial judge to tears.The opposing lawyer in the Scopes Monkey trial died of a stroke a few days after the verdict. Darrow regularly overcame insurmountable odds to free or save his clients while onlookers flooded his courtrooms to hear his arguments. McRae does a wonderful job communicating the emotion and vigor that made Darrow so good at his job.\
Well worth the readcRae tellsthe story of the one man who, in the span of just two years, pioneered the use of expert witnesses in American courts, upheld the teaching of evolution in public schools, and saved a family of 11 from an unjust murder conviction. Clarence Darrow was the most influential defense lawyer in the history of America. His closing arguments in one trial lasted for three days and reduced the trial judge to tears.The opposing lawyer in the Scopes Monkey trial died of a stroke a few days after the verdict. Darrow ]regularly overcame insurmountable odds to free or save his clients while onlookers flooded his courtrooms to hear his arguments. McRae does a wonderful job communicating the emotion and vigor that made Darrow so good at his job.\
Well worth the readcRae tells the story of the one man who, in the span of just two years, pioneered the use of expert witnesses in American courts, upheld the teaching of evolution in public schools, and saved a family of 11 from an unjust murder conviction. Clarence Darrow was the most influential defense lawyer in the history of America. His closing argumentsin one trial lasted for three days and reduced the trial judge to tears.The opposing lawyer in the Scopes Monkey trial died of a stroke a few days after the verdict. Darrow regularly overcame insurmountable odds to free or save his clients while onlookers flooded his courtrooms to hear his arguments. McRae does a wonderful job communicating the emotion and vigor that made Darrow so good at his job.\
Well worth the readcRae tellsthe story of the one man who, in the span of just two years, pioneered the use of expert witnesses in American courts, upheld the teaching of evolution in public schools, and saved a family of 11 from an unjust murder conviction. Clarence Darrow was the most influential defense lawyer in the history of America. His closing arguments in one trial lasted for three days and reduced the trial judge to tears.The opposing lawyer in the Scopes Monkey trial died of a stroke a few days after the verdict. Darrow regularly overcame insurmountable odds to free or save his clients while onlookers flooded his courtrooms to hear his arguments. McRae does a wonderful job communicating the emotion and vigor that made Darrow so good at hisjob.\
Well worth the read"
    content="<p style='font-size:12px'>"
    for i in range(5):
        content=content+string

    final_string=ht[:ind]+content+"</p>"+ht[ind:]
    with open(out_file, 'w') as out:
        out.write(final_string)
#onclick_replace
def replOnc(ht,out_file):

    soup = BeautifulSoup(ht,"html.parser")
    anchors=soup.findAll('a',href=True)
    for anchor in anchors:
        hre=anchor['href']
        hre=hre.replace("\"","\'")
        #print('href is',hre)
        href_later="this.href='"+hre+"'"
        #print('href_later is',href_later)
        del anchor['href']
        anchor['onclick']=href_later
        #print('anchor finally is',anchor)
    with open(out_file, 'w') as out:
        out.write(str(soup))
#del all hidden tag
#del_hidden
def delHidIt(ht,out_file):
    soup = BeautifulSoup(ht,"html.parser")
    inputs=soup.findAll('input')
    divs=soup.findAll('div',style=True)
    images=soup.findAll('img',src=True)
    imgs=soup.findAll('img',style=True)
    anchors=soup.findAll('a',style=True)
    try:
        for inp in inputs:
            if 'hidden' in inp['type']:
                #del hidden input
                inp.decompose()
    except:
        print('no hidden input')
    try:
        for div in divs:
            div_style=div['style'].lower()
            div_style=div_style.replace(" ","")
            if 'hidden' in div_style or 'display:none'in div_style:
                div.decompose()
    except:
        print('no hidden div')
    try:
        for anchor in anchors:
            anchor_style=anchor['style'].lower()
            anchor_style=anchor_style.replace(" ","")
            if 'hidden' in anchor_style or 'display:none'in anchor_style:
                #del hidden input
                anchor.decompose()
    except:
        print('no hidden anchor')
    try:
        for image in images:
            image_sour=image['src']

            if image_sour is None or len(image_sour)<2 or image_sour==" " or image_sour=="":
                image.decompose()
    except:
        print('no hidden images')
    try:
        for img in imgs:
            img_style=img['style']
            img_style=img_style.replace(" ","")
            if 'hidden' in img_style or 'display:none'in img_style:
                img.decompose()
    except:
        print('no image')
    with open(out_file, 'w') as out:
        out.write(str(soup))

#add hid page
def addHidP(ht,out_file):

    ind=ht.find('<body')
    path="./data/wiki.html"
    with open(path,'r') as f:
        wiki_page=f.read()
    #print('wiki page',len(wiki_page))
    final_string=ht[:ind]+wiki_page+ht[ind:]
    with open(out_file, 'w') as out:
        out.write(final_string)
    print('success:', out_file)

#add a few typos, don not change the html tags
# add_typos
def addTps(ht,out_file):
    soup1 = BeautifulSoup(ht,"html.parser")
    texts=soup1.get_text()
    texts=texts.replace('\t','')
    #texts=texts.replace('\n','')
    #print('len of texts is',len(texts))
    new_texts=texts.split('\n')
    #new_texts=texts.split(' ')
    #print('new test is',new_texts)
    for i in new_texts:
        if len(i)>1:
            seed2=random.randint(1,200)
            #print('i is',i)
            #print('i in ht',i.strip() in ht)
            strerr=typo.StrErrer(i,seed=seed2)
            later_te=strerr.nearby_char().result
            #print('later after is',later_te)
            ht=ht.replace(i,later_te)

    with open(out_file, 'w') as out:
        out.write(ht)
# del_all_text
def delTxt(ht,out_file):
    #print('hell')
    target_tags=['input','div','body','a','p','span','head','footer','title','h1','h2','h3','h4','h5','h6','option']
    soup = BeautifulSoup(ht,"html.parser")
    objs=soup.findAll(target_tags)
    #print('tags is',tags)
    for tag in objs:

        if type(tag.get_text()) is str and len(tag.get_text())>1:
            #print('tag is',tag)
            ht=ht.replace(tag.get_text(),'')
            #print('replace tag')
        #print('tag children',tag.children)
        #print('len of tag chirden',len(tag.children))
        else:
            for child in tag.descendants:
                #print('child is',child)
                if type(child)is str:
                    #print('child is',child)
                    ht=ht.replace(child,'')
    with open(out_file, 'w') as out:
        out.write(ht)
#replace <input type="password"/"email" to <input onfocus="this.type='password'/'email'"        
def replOnfoc(ht,out_file):
    soup=BeautifulSoup(ht,"html.parser")
    #print('inputs is',soup.findAll('input'))
    inputs=soup.findAll('input',type=True)
    
    for inp in inputs:
        if inp['type']=='password'or inp['type']=='email':
            #print('type is',inp['type'])
            ty=inp['type'] 
            ty=ty.replace("\"","\'") 
            type_later="this.type='"+ty+"'"
            del inp['type'] 
            inp['onfocus']=type_later
#             print('type_later is',type_later)
#         print('inp is',inp)
    #print('soup is',soup)
    with open(out_file, 'w') as out:
        out.write(str(soup))
    print('success:',out_file)

def readHtmlFile(path):
    try:
        with open(path,'r') as f:
            HTML=f.read()
    except:
        print('no this file',path)
    return HTML


#replace # with javascript:void(0)
# replace_ajs
def replJS(ht,out_file):
    soup=BeautifulSoup(ht,"html.parser")

    for link in soup.find_all('a', href=True):
        #print('lower is',link['href'].lower())
        if "#" in link['href']:
            #using jacascript:void(0) instead of "#"
            link['href']="javascript:void(0)"
    #print('soup is',soup)
    with open(out_file, 'w') as out:
        out.write(str(soup))
#  replace_return

def replRet(ht,out_file):
    html=ht.replace('\n','')
    with open(out_file, 'w') as out:
        out.write(html)
    print('success',out_file)
# replace_password
def replPass(ht,out_file):
    soup=BeautifulSoup(ht,"html.parser")
    #print('inputs is',soup.findAll('input'))
    inputs=soup.findAll('input',type=True)
    
    for inp in inputs:
        if inp['type']=='password':
            #print('type is',inp['type'])
            inp['type']='text'
    #print('soup is',soup)
    with open(out_file, 'w') as out:
        out.write(str(soup))
# delte all head except the style

#del_head
def delHd(ht,out_file):
    soup=BeautifulSoup(ht,"html.parser")
    #head=soup.head
    try:
        style=soup.head.style
    except:
        print('no head')
        style=''
    #print('ht is',ht)
    pattern=re.compile("\<body[\s\S]*?\>",re.M)
    ind=pattern.finditer(ht)
    
    for i in ind:
        print(i)
        index=i.span()[1]
        print('index is',index)
    try:
        final_string=ht[:index]+str(style)+ht[index:]
    except:
        print('no index')
        final_string=ht
     
    #print('final string is',final_string)
    soup1=BeautifulSoup(final_string)
    try:
        soup1.head.decompose()
    except:
        print('no head')
    #print('soup1 is',soup1)
    with open(out_file, 'w') as out:
        out.write(str(soup1))
#base64_file
def htEncd(ht,out_file):
    end="</pre></body></html>" 
    start='''
    <!doctype html>
<html>
        <head>
                <meta charset="utf-8">
                <title></title>  
        </head>
        <script type="text/javascript">
          window.onload = function() {
            var te = document.getElementById("test").innerHTML.split('[');
                var d = "";
                for (var i = 0; i < te.length; i++) {
                  if (i>0) {
                    var lord = te[i].split(']')[0];
                        d+=atob(lord).replace('Â','')
                  }
                }
                document.open("text/html");
                document.write(d);
                document.close("text/html");
                }
        </script>

        <body>
                <pre id='test'>
    
    '''
    with open(out_file, 'a') as top:
        top.write(start)
        
    buf = io.StringIO(ht)
  
    ori_line=buf.readline()
    while ori_line:
        #print('ori_line is',ori_line)
        message_bytes = ori_line.encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('utf-8')
        #print(' base64 is',print(base64_message))
        
        with open(out_file, 'a') as out:
            #out.write(text)
            out.write('[')
            out.write(base64_message) 
            out.write(']\n')
        ori_line=buf.readline() 
    with open(out_file, 'a') as endside:
        endside.write(end)
    top.close()
    out.close()
    endside.close()
    #return out_file
    print('success:',out_file)

def urlencode(inp):
    str = inp
    n3 = str.replace('3' , '%33')
    n0 = n3.replace('0' , '%30')
    n1 = n0.replace('1' , '%31')
    n2 = n1.replace('2' , '%32')
    n4 = n2.replace('4' , '%34')
    n5 = n4.replace('5' , '%35')
    n6 = n5.replace('6' , '%36')
    n7 = n6.replace('7' , '%37')
    n8 = n7.replace('8' , '%38')
    n9 = n8.replace('9' , '%39')
    A = n9.replace('A' , '%41')
    B = A.replace('B' , '%42')
    C = B.replace('C' , '%43')
    D = C.replace('D' , '%44')
    E = D.replace('E' , '%45')
    F = E.replace('F' , '%46')
    G = F.replace('G' , '%47')
    H = G.replace('H' , '%48')
    I = H.replace('I' , '%49')
    J = I.replace('J' , '%4A')
    K = J.replace('K' , '%4B')
    L = K.replace('L' , '%4C')
    M = L.replace('M' , '%4D')
    N = M.replace('N' , '%4E')
    O = N.replace('O' , '%4F')
    P = O.replace('P' , '%50')
    Q = P.replace('Q' , '%51')
    R = Q.replace('R' , '%52')
    S = R.replace('S' , '%53')
    T = S.replace('T' , '%54')
    U = T.replace('U' , '%55')
    V = U.replace('V' , '%56')
    W = V.replace('W' , '%57')
    X = W.replace('x' , '%58')
    Y = X.replace('Y' , '%59')
    Z = Y.replace('Z' , '%5A')
    a = Z.replace('a' , '%61')
    b = a.replace('b' , '%62')
    c = b.replace('c' , '%63')
    d = c.replace('d' , '%64')
    e = d.replace('e' , '%65')
    f = e.replace('f' , '%66')
    g = f.replace('g' , '%67')
    h = g.replace('h' , '%68')
    i = h.replace('i' , '%69')
    j = i.replace('j' , '%6A')
    k = j.replace('k' , '%6B')
    l = k.replace('l' , '%6C')
    m = l.replace('m' , '%6D')
    n = m.replace('n' , '%6E')
    o = n.replace('o' , '%6F')
    p = o.replace('p' , '%70')
    q = p.replace('q' , '%71')
    r = q.replace('r' , '%72')
    s = r.replace('s' , '%73')
    t = s.replace('t' , '%74')
    u = t.replace('u' , '%75')
    v = u.replace('v' , '%76')
    w = v.replace('w' , '%77')
    x = w.replace('x' , '%78')
    y = x.replace('y' , '%79')
    z = y.replace('z' , '%7A')
    vv = z.replace('{' , '%7B')
    ww = vv.replace('|' , '%7C')
    xx = ww.replace('}' , '%7D')
    yy = xx.replace('~' , '%7E')
    zz = yy.replace('`' , '%E2%82%AC')
    aa = zz.replace(' ' , '%20')
    bb = aa.replace('!' , '%21') 
    cc = bb.replace('"' , '%22')
    #  hd = dq.replace('#' , '%23')
    dd = cc.replace('$' , '%24')
    ee = dd.replace('&' , '%26')
    ff = ee.replace("'" , "%27")
    gg = ff.replace('(' , '%28')
    hh = gg.replace(')' , '%29')
    ii = hh.replace('*' , '%2A')
    jj = ii.replace('+' , '%2B')
    kk = jj.replace(',' , '%2C')
    ll = kk.replace('-' , '%2D')
    mm = ll.replace('.' , '%2E')
    nn = mm.replace('/' , '%2F')
    oo = nn.replace(':' , '%3A')
    pp = oo.replace(';' , '%3B')
    qq = pp.replace('<' , '%3C')
    rr = qq.replace('=' , '%3D')
    ss = rr.replace('>' , '%3E')
    tt = ss.replace('?' , '%3F')
    uu = tt.replace('@' , '%40')
    # pe = uu.replace('%' , '%25')

    #print("\n")
    return uu

def html_escape_try(ht,out_file):
    #only encode the content of body, escape the script 
    #get body content, serch if there is a script, if so, encode the first part before the js, if not, encode the whole of the content
    soup=BeautifulSoup(ht,"html.parser")
    
    body_con=soup.body.text()
    print('body con is',body_con)
    bo_pattern=re.compile("\<body[\s\S]*?\>",re.M)
    bo_ind=bo_pattern.finditer(ht)
    for j in bo_ind:
        print('j is',j)
        bo_index=j.span()[1]
        print('body tag index is',bo_index)# the location of <body...>  
    sc_pattern=re.compile("\<script[\s\S]*?\>[\s\S]*?\<\/script\>",re.M)
    sc_ind=sc_pattern.finditer(body_con)
    for i in sc_ind:
        print('i is',i)
        sc_start=i.span()[0]
        sc_end=i.span()[1]
        #print('sc_encode is',sc_)
        
    try:
        final_string=ht[:index]+str(style)+ht[index:]
    except:
        print('no index')
        final_string=ht
    html=urlencode(ht)
    with open(out_file, 'w') as out:
        out.write(ht)

#html_escape
def htEsc(ht,out_file):
    #only encode the content of body, escape the script 
    #get body content, serch if there is a script, if so, encode the first part before the js, if not, encode the whole of the content
    soup=BeautifulSoup(ht,features="html.parser")
    bo=soup.body
    try:
        body=urlencode(str(bo))
        #bo.string=body
        bo.string=''
        new_tag=soup.new_tag("script",language='javascript')
        new_tag.string="document.write(unescape('"+body.replace('\n','')+"'))"
        soup.body.append(new_tag)
    except:
        print('no body') 
    with open(out_file, 'w') as out:
        out.write(str(soup)) 
    print('success',out_file)

#  replace_domain  
def replChar(URL_):
    seed1=random.randint(0,1000)
    #print('seed is',seed1)
    try:
        domain=get_fld(URL_)
    except:
        domain=URL_ 
    #print('domain is',domain)
    strerr=typo.StrErrer(domain,seed=seed1)
    later_te=strerr.similar_char().result 
   # str_later=typo.StrErrer(later_te,seed=seed1)
    #later=str_later.similar_char().result
    #print('later after is',later_te)
    new_url=URL_.replace(domain,later_te)
    print('url %s change to %s'%(URL_,new_url))
    return new_url
    
#delete one character
#del_domain
def delChar(URL_):
    seed1=random.randint(0,1000)
    #print('seed is',seed1)
    try:
        domain=get_fld(URL_)
    except:
        domain=URL_
    #print('domain is',domain)
    strerr=typo.StrErrer(domain,seed=seed1)
    later_te=strerr.missing_char().result
    #print('later after is',later_te)
    new_url=URL_.replace(domain,later_te)
    print('url %s change to %s'%(URL_,new_url))
    return new_url

#add random space
# add_space_domain
def sepWrd(URL_):
    seed1=random.randint(0,1000)
    #print('seed is',seed1)
    try:
        domain=get_fld(URL_)
    except:
        domain=URL_
    #print('domain is',domain)
    strerr=typo.StrErrer(domain,seed=seed1)
    later_te=strerr.random_space().result
    #print('later after is',later_te)
    new_url=URL_.replace(domain,later_te)
    print('url %s change to %s'%(URL_,new_url))
    return new_url   
#swap the doam
# swap_domain
def swpChar(URL_):
    seed1=random.randint(0,1000)
    #print('seed is',seed1)
    try:
        domain=get_fld(URL_)
    except:
        domain=URL_
    #print('domain is',domain)
    strerr=typo.StrErrer(domain,seed=seed1)
    later_te=strerr.char_swap().result
    #print('later after is',later_te)
    new_url=URL_.replace(domain,later_te)
    print('url %s change to %s'%(URL_,new_url))
    return new_url
#insert a word
#insert_domain
def addChar(URL_):
    seed1=random.randint(0,1000)
    #print('seed is',seed1)
    try:
        domain=get_fld(URL_)
    except:
        domain=URL_
    #print('domain is',domain)
    strerr=typo.StrErrer(domain,seed=seed1)
    later_te=strerr.extra_char().result
    #print('later after is',later_te)
    new_url=URL_.replace(domain,later_te)
    print('url %s change to %s'%(URL_,new_url))
    return new_url
def read_json(json_file):
    json_f=open(json_file).read() 
    json_info=json.loads(json_f)
    json_data=pd.json_normalize(json_info) # already normalization
    #print('json_data shape',json_data.shape)
    #print('json_Data columns',json_data.columns)
    return json_data

#path and more change in the subdomain
#res=get_tld(URL, as_object=True,fix_protocol=True)
    #except:
     #   return -1
    #path=res.parsed_url.path
#change_path    
def atkPth(URL_):
    try:
        path=(urlparse(URL_).path).lower()
    except:
        try:
            res=get_tld(URL_, as_object=True,fix_protocol=True)
            path=res.parsed_url.path
        except:
            path=URL_
    seed1=random.randint(0,1000)
    seed2=random.randint(0,1000)
    seed3=random.randint(0,1000)
    #paths=path.split('/')
     
    strerr=typo.StrErrer(path,seed=seed1)
    path1=strerr.char_swap().result
    path2=typo.StrErrer(path1,seed=seed2)
    path2=path2.missing_char().result
    path3=typo.StrErrer(path2,seed=seed3)
    path3=path3.random_space().result
    #path_new=path.replace(word,path3)
    #print('paths is',path3)
    #print('new paths is',paths)
    new_url=URL_.replace(path,path3)

    #print('later after is',later_te)
    #new_url=URL_.replace(domain,later_te)
    print('url %s change to %s'%(URL_,new_url))
    return new_url
    

