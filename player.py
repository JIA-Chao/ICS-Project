"""

Author: Jingxian Xu
(only supports windows system)

"""

from tkinter import *
from traceback import *
from win32com.client import Dispatch
import threading
import os
import time
  

  
def run(mood,index = [1]):
    root =Tk()
    wmp = Dispatch("WMPlayer.OCX")
    
    global total,name
    #name={}
    name=[]
    pwd=os.getcwd()
    pwd += "\\" + mood
    print(pwd)
    os.chdir(pwd)
    filenames=[]
    for files in os.listdir(pwd):
        if files.endswith('.mp3'):
            realdir = os.path.realpath(files)
            filenames.append(realdir)
    #print(filenames)
    if filenames:
        for i in range(len(filenames)):
            media = wmp.newMedia(filenames[i])
            wmp.currentPlaylist.appendItem(media)
            
            #print(filenames[i])
      
            
            
    def play(event = None):
  
        per_thread = threading.Thread(target = per)
        per_thread.daemnon = True
        wmp.controls.play()
        per_thread.start()
  
   
    
    def per():
        global total
        while wmp.playState !=1:
            progress_scal.set(int(wmp.controls.currentPosition))
            progress_scal.config(label = wmp.controls.currentPositionString)
            progress_scal.config(to = total,tickinterval = 50)
            time.sleep(1)
            root.title("%s" % wmp.currentMedia.name)
    
    def stop():
        wmp.controls.stop()
    def pause(event = None):
        wmp.controls.pause()
  
    
    def exitit():
        root.destroy()
    def Previous_it():
        wmp.controls.previous()
    def Next_it():
        wmp.controls.next()
    def Volume_ctr(none):
        wmp.settings.Volume = vio_scale.get()
    def Volume_add(i=[0]):
        wmp.settings.Volume =wmp.settings.Volume+5
        i.append(wmp.settings.Volume)
        vio_scale.set(wmp.settings.Volume)
    def Volume_minus(i=[0]):
        wmp.settings.Volume = wmp.settings.Volume -5
        i.append(wmp.settings.Volume)
        vio_scale.set(wmp.settings.Volume)
    def Scale_ctr(none):
  
        wmp.controls.currentPosition = var_scale.get()
        print(wmp.currentMedia.duration)
    def Clear_list():
        wmp.currentPlaylist.clear()
        list_name.delete(1.0,END)
        name = []
        index = []
    
    def List_loop():
        wmp.settings.setMode("loop",True)
        play()
    
    
  
  
  
    progress_lab = LabelFrame(root,text = "playing progress")
    progress_lab.grid(row =2,column =0,sticky = "we",rowspan = 2)
    var_scale = DoubleVar()
    progress_scal = Scale(progress_lab,orient = HORIZONTAL,showvalue = 0,length =180,variable = var_scale)
    progress_scal.bind("<Button-1>",pause)
    progress_scal.bind("")
    progress_scal.bind("<ButtonRelease-1>",play)
    progress_scal.grid(row =3,column =0)
  
    
    
    modee_lab = LabelFrame(root,text = "play control")
    modee_lab.grid(row =4,column =0,rowspan =4,sticky = "wes")
    var_mode = IntVar()
    
    previous_play = Button(modee_lab,text = "last",width=8,height =1,command = Previous_it)
    previous_play.grid(row =6,column =2,rowspan =2,pady =5)
    next_play = Button(modee_lab,text = "next",width=8,height =1,command = Next_it)
    next_play.grid(row =6,column =7,rowspan =2,pady =5)
  
    var_volume = IntVar()
    vioce_lab = LabelFrame(root,text = "volume control")
    vioce_lab.grid(row =8,column =0,sticky = "wes")
    vio_scale = Scale(vioce_lab,orient = HORIZONTAL,length =170,variable = var_volume,command =Volume_ctr)
    vio_scale.set(30)
    vio_scale.grid(row =8,column =0)
    vio_plus = Button(vioce_lab,width =8,text = "+",command =Volume_add)
    vio_plus.grid(row =9,column =0,sticky = "w")
    vio_minus = Button(vioce_lab,width =8,text ="-",command = Volume_minus)
    vio_minus.grid(row =9,column =0,sticky ="e")
  
    ctr_lab = LabelFrame(root,text = "player control",height =130)
    ctr_lab.grid(row =0,column =1,rowspan =12,sticky = "ns")
    btn_play = Button(ctr_lab,text ="play",width =10,command = play)
    btn_play.grid(row =1,column =1,pady =5)
    btn_stop = Button(ctr_lab,text ="stop",width =10,command = stop)
    btn_stop.grid(row =2,column =1,pady =5)
    btn_pause = Button(ctr_lab,text ="pause",width =10,command = pause)
    btn_pause.grid(row =3,column =1,pady =5)
    btn_pause = Button(ctr_lab,text ="exit",width =10,command = exitit)
    btn_pause.grid(row =4,column =1,pady =5)
    

  
    
  
  
    root.mainloop()

    
if __name__=='__main__':
    mood='not bad'
    run(mood)
