"""

Author: Jingxian Xu
"""
import os
import pickle as pkl

def get_report(username):
    msg = '********** Here is your music report **********\n\n'
    pwd=os.getcwd()
    moods=['not bad','sad','tired']
    for mood in moods:
        msg1 = "Here are you favorite songs when you are " + mood + ':\n'
        pwd += "\\" + mood
        #print(pwd)
        os.chdir(pwd)

        try:
            record_d = pkl.load(open(username + '_music.idx','rb'))
            top3=[]
            refer_l = sorted(record_d, key=record_d.get)
            for i in range(3):
                top3.append(refer_l.pop().split('\\')[-1][:-4])
            msg2=''
            for i in top3:
                msg2 += (i + '\n')
            msg += msg1
            msg += msg2
            
        except:
            msg += 'You never used safe and sound player before when you feel ' + mood +'.\n'
        msg += '\n'
        l = pwd.split('\\')
        pwd = '\\'.join(l[:-1])
        os.chdir(pwd)
    msg += '******** Thank you for your support :) ********\n'
    return msg

if __name__=="__main__":
    #username = 'u'
    print(get_report(username))
            
