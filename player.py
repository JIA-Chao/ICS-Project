"""

Author: Jingxian Xu
Reminder: This player only supports windows system

"""

from tkinter import *
from win32com.client import Dispatch
import os
import pickle as pkl

 


  
def run(mood,username,index = [1]):
    root =Tk()
    wmp = Dispatch("WMPlayer.OCX")
    dict_path_name={}
    filedirs=[]
    global pwd
    pwd=os.getcwd()
    
    pwd += "\\" + mood
    print(pwd)
    os.chdir(pwd) #point to the folder that has music
    
    try:
        
        record_d = pkl.load(open(username + '_music.idx','rb'))
        refer_d = sorted(record_d, key=record_d.get,reverse=True)  #sort key(filepath) by its value(reference level)
        for key in refer_d:
            filedirs.append(key)
            dict_path_name[key.split("\\")[-1]] = key
        for files in os.listdir(pwd):
            if files.endswith('.mp3'):
                realdir = os.path.realpath(files)
                if realdir not in filedirs:  #if music files change, also need to add the new music filename to user record
                    filedirs.append(realdir)
                    dict_path_name[realdir.split("\\")[-1]]=realdir
                    record_d[realdir] = 0
                
    except:
        record_d={}             #store users' reference
        dict_path_name={}       #{filename:filepath}
        name=[]
        for files in os.listdir(pwd):
            if files.endswith('.mp3'):
                realdir = os.path.realpath(files)
                filedirs.append(realdir)
                dict_path_name[realdir.split("\\")[-1]]=realdir
                record_d[realdir] = 0
                
    #print(pwd,'start PWD1')
    l=pwd.split('\\')
    pwd = '\\'.join(l[:-1])  
    #print(pwd,'start PWD2')
    
    os.chdir(pwd)   #go back to player's directory
    
    
    #print(filedirs)
    #print(record_d,'********RECORD_D')
        
    if filedirs:
        for i in range(len(filedirs)):
            media = wmp.newMedia(filedirs[i])
            wmp.currentPlaylist.appendItem(media)
            
            print(filedirs[i])
            

    """Playing functions"""
            
    def play(event = None):
        wmp.controls.play()
    
    def stop():
        wmp.controls.stop()
        
    def pause(event = None):
        wmp.controls.pause()
        
    def exitit():
        global pwd
        stop()
        print(record_d)
        #print(pwd,'EXIT PWD1')
        pwd += '\\' + mood
        #print(pwd,'EXIT PWD2')
        os.chdir(pwd)
        pkl.dump(record_d, open(username + '_music.idx', 'wb'),0)
        l=pwd.split('\\')
        pwd = '\\'.join(l[:-1])
        #print(pwd,'EXIT PWD3')
        os.chdir(pwd)
        root.destroy()
        
    def Previous_it():
        media_dir = wmp.currentMedia.sourceURL
        media_name = wmp.currentMedia.name
        cur_pos = wmp.controls.currentPosition
        dur = wmp.currentMedia.duration
        if record_d[media_dir] > 0:
            record_d[media_dir] -= 1
        elif cur_pos < dur/2 :
            record_d[media_dir] = -2
        else:
            record_d[media_dir] = -1
        wmp.controls.previous()
        media_dir = wmp.currentMedia.sourceURL
        record_d[media_dir] += 1
        print(record_d)
        
        
    def Next_it():
       
        media_dir = wmp.currentMedia.sourceURL
        media_name = wmp.currentMedia.name
        cur_pos = wmp.controls.currentPosition
        dur = wmp.currentMedia.duration
        
        if record_d[media_dir] > 0:
            record_d[media_dir] -= 1
        elif cur_pos < dur/2 :
            record_d[media_dir] = -2
        else:
            record_d[media_dir] = -1
        
        print(record_d)
        wmp.controls.next()
        
    def Volume_ctr(none):
        wmp.settings.Volume = vio_scale.get()
        
    def Volume_add(i=[0]):
        wmp.settings.Volume =wmp.settings.Volume +5
        i.append(wmp.settings.Volume)
        vio_scale.set(wmp.settings.Volume)
        
    def Volume_minus(i=[0]):
        wmp.settings.Volume = wmp.settings.Volume -5
        i.append(wmp.settings.Volume)
        vio_scale.set(wmp.settings.Volume)
        
    def Scale_ctr(none):
        wmp.controls.currentPosition = var_scale.get()
        print(wmp.currentMedia.duration)
    
    def List_loop():
        wmp.settings.setMode("loop",True)
        play()
        
    def Thumbs_up():
        media_dir = wmp.currentMedia.sourceURL
        dur = wmp.currentMedia.duration
        record_d[media_dir] = 5
        print(record_d)
            
    
    
    """GUI"""
    modee_lab = LabelFrame(root,text = "play control")
    modee_lab.grid(row =0,column =0,rowspan =4,sticky = "wes")
    var_mode = IntVar()
    
    previous_play = Button(modee_lab,text = "last",width=5,height =1,command = Previous_it)
    previous_play.grid(row =0,column =2,rowspan =2,pady =5)
    next_play = Button(modee_lab,text = "next",width=5,height =1,command = Next_it)
    next_play.grid(row =0,column =3,rowspan =2,pady =5)
    thumbs_up = Button(modee_lab,text = "thumbs up",width=10,height =1,command = Thumbs_up)
    thumbs_up.grid(row =0,column =4,rowspan =2,pady=5)
  
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
    #mood='sad'  #for testing  
    #username='u'
    run(mood,username)
