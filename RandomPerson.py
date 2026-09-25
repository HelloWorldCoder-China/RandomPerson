import random as ra
import tkinter as tk
import threading as th
import time as ti
from tkinter import filedialog
import shutil as sh
import os
import yaml
from pathlib import Path
main=tk.Tk()
main.title("随机选人软件-初三4班出品 v2.2")

#region 配置管理
class config:
    def __init__(self,name,default:dict,rewriteaction:callable=None):
        self.name=name
        self.default=default
        self.rewriteaction=rewriteaction
        try:
            self.content=yaml.load(open(name,"r+"),Loader=yaml.SafeLoader)
        except:
            self.content=default
            yaml.dump(default,open(name,"w+"))
            try:
                rewriteaction(self)
            except:
                pass
    def reread(self):
        try:
            self.content=yaml.load(open(self.name,"r+"),Loader=yaml.SafeLoader)
        except:
            self.content=self.default
            yaml.dump(self.default,open(self.name,"w+"))
            try:
                self.rewriteaction(self)
            except:
                pass
    def write(self,target:dict):
        self.content=target
        yaml.dump(self.content,open(self.name,"w+"))
    def edit(self,content:dict):
        def searchreplace(path_content: dict, path_new: dict):
            for key in path_new.keys():
                if key in path_content:
                    if isinstance(path_new[key],dict) and isinstance(path_content[key],dict):
                        searchreplace(path_content[key],path_new[key])
                    else:
                        path_content[key]=path_new[key]
                else:
                    path_content[key]=path_new[key]
        searchreplace(self.content,content)
        yaml.dump(self.content,open(self.name,"w+"))
    def remove(self,key:list):
        target=self.content
        for i in key[:-1]:
            target=target[i]
        target.pop(key[-1])
        yaml.dump(self.content,open(self.name,"w+"))

#endregion 配置管理

#region 启动
os.makedirs("./config",exist_ok=True)
os.makedirs("./config/textlist",exist_ok=True)
def maincfgsetdefaultvalue(cfg):
    global mode,countnum,swidth,shight
    mode="number"
    countnum=1
    swidth=main.winfo_screenwidth()
    shight=main.winfo_screenheight()
maincfg=config("./config/main.cfg",{"mode":"number","count":1,"swidth":"auto","shight":"auto"},maincfgsetdefaultvalue)
mode=maincfg.content["mode"]
countnum=maincfg.content["count"]
if maincfg.content["swidth"]=="auto":
    swidth=main.winfo_screenwidth()
else:
    swidth=maincfg.content["swidth"]
if maincfg.content["shight"]=="auto":
    shight=main.winfo_screenheight()
else:
    shight=maincfg.content["shight"]
if swidth<=1920 or shight<=1580:
    main.geometry(f"{int(swidth/3)}x{int(shight/2.5)}+{int(swidth/3)}+{int(shight/2.5-shight/10)}")
main.geometry(f"{int(swidth/3)}x{int(shight/3)}+{int(swidth/3)}+{int(shight/3-shight/10)}")
main.resizable(False,False)
addboxregistry=[]
app=tk.Frame(main)
def percentwidth(percent):
    return int(swidth*percent/3/100)
def percentheight(percent):
    return int(shight*percent/3/100)
#endregion 启动

#region 数字输入框
def intboxup(entry):
    try:
        value=int(entry.get())
        entry.delete(0,tk.END)
        entry.insert(0,str(value+1))
    except ValueError:
        entry.delete(0,tk.END)
        entry.insert(0,"1")
def intboxdown(entry):
    try:
        value=int(entry.get())
        entry.delete(0,tk.END)
        entry.insert(0,str(value-1))
    except ValueError:
        entry.delete(0,tk.END)
        entry.insert(0,"0")
def intinput(defaultvalue,packside=tk.LEFT,anchor=tk.CENTER,app=main,width=4):
    frame=tk.Frame(app)
    frame.pack(side=packside,anchor=anchor)
    intdown=tk.Button(frame,text="-",font=("微软雅黑",15),command=lambda:intboxdown(box))
    intdown.pack(side=tk.LEFT)
    box=tk.Entry(frame,font=("微软雅黑",15),width=width)
    box.insert(0,str(defaultvalue))
    box.pack(side=tk.LEFT)
    intup=tk.Button(frame,text="+",font=("微软雅黑",15),command=lambda:intboxup(box))
    intup.pack(side=tk.LEFT)
    return box
#endregion 数字输入框

#region 随机抽取座号
def numbercfgsetdefaultvalue(cfg):
    global start,end
    start=1
    end=50
numbercfg=config("./config/number.cfg",{"start":1,"end":50},numbercfgsetdefaultvalue)
def numberrand():    
    global start,end,count,result,startbtn,numbercfg
    try:
        result.set("正在处理,请稍后......")
        getallready=[]
        if(int(end.get())-int(start.get())+1<int(count.get()) or int(end.get())<int(start.get())):
            result.set("输入错误,请检查抽取数量与范围")
            return
        numbercfg.edit({"start":int(start.get()),"end":int(end.get())})
        pool=ra.sample(range(int(start.get()),int(end.get())+1),int(count.get()))
        for i in range(len(pool)):
            if i!=0:
                result.set(result.get()+" ")
            else:
                result.set("")
            result.set(result.get()+str(pool[i]))
    except:
        result.set("输入错误,请检查抽取数量与范围")
def numbermode():
    global start,end,count,result,startbtn,modechooseframe,addboxregistry,numbercfg

    for box in addboxregistry:
        box.destroy()
    addboxregistry.clear()

    numbercfg.reread()
    startnum=numbercfg.content["start"]
    endnum=numbercfg.content["end"]

    rangeframe=tk.Frame(main)
    rangeframe.pack(pady=percentheight(2),after=modechooseframe)
    fromtxt=tk.Label(rangeframe,text="范围 从:",font=("微软雅黑",15))
    fromtxt.pack(side=tk.LEFT)
    start=intinput(startnum,app=rangeframe)
    totext=tk.Label(rangeframe,text="到:",font=("微软雅黑",15))
    totext.pack(side=tk.LEFT)
    end=intinput(endnum,app=rangeframe)
    addboxregistry.append(rangeframe)
#endregion 随机抽取座号

#region 随机抽取名字
def textrand():
    global cfgname,namelist,count,result,startbtn,cfgnamerd,namecfg
    try:
        result.set("正在处理,请稍后......")
        if(len(namelist)<int(count.get())):
            result.set("输入错误,请检查抽取数量与范围")
            return
        namecfg.edit({"cfgname":cfgname})
        choicelist=namelist.copy()
        for i in range(int(count.get())):
            namenow=ra.choice(choicelist)
            choicelist.remove(namenow)
            if i!=0:
                result.set(result.get()+" ")
            else:
                result.set("")
            result.set(result.get()+namenow)
    except Exception as e:
        result.set(e)
def textmode():
    global start,end,count,result,startbtn,modechooseframe,addboxregistry,cfgnamerd,cfgname,namelist,cfglistraw,textconfig,cfglist,namecfg
    for box in addboxregistry:
        box.destroy()
    addboxregistry.clear()

    def textcfgsetdefaultvalue(cfg):
        global cfgname
        cfgname="选择列表文件"
    namecfg=config("./config/text.cfg",{"cfgname":"选择列表文件"},textcfgsetdefaultvalue)
    cfgname=namecfg.content["cfgname"]

    cfgindex=config("./config/textlist/index.cfg",{"index":{}})
    cfglist=cfgindex.content["index"]
    namelist=[]
    def importcfg():
        global cfgname,textconfig
        filename=filedialog.askopenfilename(title="选择名单文件",filetypes=[("名单列表(换行分割名字)","*")])
        if not filename:
            result.set("用户已取消导入")
            return
        source=Path(filename)
        display_name=source.stem
        stored_name=source.name
        if display_name in cfglist:
            result.set("名单已存在,请勿重复导入")
            return
        sh.copy(filename,"./config/textlist/"+stored_name)
        cfgindex.edit({"index":{display_name:stored_name}})
        optionlist=cfgindex.content["index"].keys()
        cfgname=display_name
        textconfig.destroy()
        textconfig=tk.OptionMenu(textconfigframe,tk.StringVar(value=cfgname),*optionlist,command=readcfg)
        textconfig.pack(side=tk.LEFT,before=textconfigimportbtn)
        readcfg(cfgname)
    def removecfg():
        global cfgname,namelist,cfglistraw,textconfig,cfglist
        try:
            if cfgname!="选择列表文件":
                try:
                    removetarget=cfgindex.content["index"][cfgname]
                    cfgindex.remove(["index",cfgname])
                except:
                    result.set("删除索引失败")
                    ti.sleep(1)
                try:
                    os.remove("./config/textlist/"+removetarget)
                    result.set("删除文件成功")
                except:
                    pass
                cfgname="选择列表文件"
                namecfg.edit({"cfgname":cfgname})
                namelist=["恭喜你触发了彩蛋!","Copyright ©️2026 HelloWorldCoder","https://github.com/HelloWorldCoder-China/RandomPerson","电教其实是福瑞","http://greatthings.dragonhwc.com"]
                if not cfglist:
                    optionlist=[""]
                else:
                    optionlist=cfgindex.content["index"].keys()
                textconfig.destroy()
                textconfig=tk.OptionMenu(textconfigframe,tk.StringVar(value=cfgname),*optionlist,command=readcfg)
                textconfig.pack(side=tk.LEFT,before=textconfigimportbtn)
        except:
            result.set("删除失败,请检查文件是否存在")
    def readcfg(cfgnameinput):
        global namelist,cfgname
        cfgname=cfgnameinput
        cfgnameinput=cfgindex.content["index"][cfgnameinput]
        try:
            with open("./config/textlist/"+cfgnameinput,"r+") as file:
                cfg=file.read()
        except:
            result.set("名单文件不存在,请检查")
            namelist=["恭喜你触发了彩蛋!","Copyright ©️2026 HelloWorldCoder","https://github.com/HelloWorldCoder-China/RandomPerson","电教其实是福瑞","http://greatthings.dragonhwc.com"]
            return
        namelist=cfg.split("\n")
        try:
            namelist.remove("")
        except:
            pass
    
    if namecfg.content["cfgname"]!="选择列表文件":
        cfgname=namecfg.content["cfgname"]
        readcfg(cfgname)
    
    textconfigframe=tk.Frame(main)
    textconfigframe.pack(pady=percentheight(2),after=modechooseframe)
    if not cfglist:
        optionlist=[""]
    else:
        optionlist=cfgindex.content["index"].keys()
    textconfig=tk.OptionMenu(textconfigframe,tk.StringVar(value=cfgname),*optionlist,command=readcfg)
    textconfig.pack(side=tk.LEFT)
    textconfigimportbtn=tk.Button(textconfigframe,text="导入",font=("微软雅黑",15),command=importcfg)
    textconfigimportbtn.pack(side=tk.LEFT)
    textconfigremovebtn=tk.Button(textconfigframe,text="删除",font=("微软雅黑",15),command=removecfg)
    textconfigremovebtn.pack(side=tk.LEFT)
    addboxregistry.append(textconfigframe)
#endregion 随机抽取名字

#region 固定内容
title=tk.Label(main,text="随机选人软件-初三4班出品",font=("微软雅黑",25))
title.pack(pady=percentheight(4))

modechooseframe=tk.Frame(main)
modechooseframe.pack(pady=percentheight(2))
if mode=="number":
    boxvalue="座号模式"
elif mode=="text":
    boxvalue="名单模式"
modes=[
    "座号模式",
    "名单模式"
]
def modesswitch(value):
    global mode,swidth,maincfg
    if value=="座号模式":
        mode="number"
        numbermode()
    elif value=="名单模式":
        mode="text"
        textmode()
    maincfg.edit({"mode":mode})
modechoosebox=tk.OptionMenu(modechooseframe,tk.StringVar(value=boxvalue),*modes,command=modesswitch)
modechoosebox.pack()

timesframe=tk.Frame(main)
timesframe.pack(pady=percentheight(2))
timestext=tk.Label(timesframe,text="抽取数量:",font=("微软雅黑",15))
timestext.pack(side=tk.LEFT)
count=intinput(countnum,app=timesframe)

resultframe=tk.Frame(main)
resultframe.pack(pady=percentheight(2))
result=tk.StringVar()
result.set("抽取结果将在这里显示")
resultbox=tk.Entry(resultframe,font=("微软雅黑",15),width=int(percentwidth(90)/15),textvariable=result)
resultbox.pack()
resultscrollbar=tk.Scrollbar(resultframe,orient=tk.HORIZONTAL,command=resultbox.xview)
resultscrollbar.pack(fill=tk.X)
resultbox.config(xscrollcommand=resultscrollbar.set)

def startrand():
    startbtn.config(state=tk.DISABLED)
    if mode=="number":
        numberrand()
    elif mode=="text":
        textrand()
    startbtn.config(state=tk.NORMAL)
startbtn=tk.Button(main,text="开始抽取",font=("微软雅黑",15),command=lambda:th.Thread(target=startrand).start())
startbtn.pack(pady=percentheight(5))

if mode=="number":
    numbermode()
elif mode=="text":
    textmode()
#endregion

main.mainloop()