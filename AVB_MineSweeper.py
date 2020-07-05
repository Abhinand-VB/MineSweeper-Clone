import tkinter as tk
from functools import partial
from array import *
import random
from tkinter import *
from pygame import mixer
import time
import threading
import tkinter.messagebox
import unicodedata
import os

mixer.init()
t=tk.Tk()
t.title("Mine Sweeper")
t.iconbitmap(r'img\\pirateflag.ico')

pathm = 'text\\AboutM.rtf'
pathe = 'text\\AboutE.rtf'

mixer.music.load("SFX\\\SSJ3-Goku_Theme.mp3.") #Loading File Into Mixer   #bgm
win_sound = mixer.Sound("SFX\\\Ovation.wav")
loose_sound = mixer.Sound("SFX\\\BigBomb.wav")
imbatman = mixer.Sound("SFX\\\imbatman.wav")
snap = mixer.Sound("SFX\\\BigBomb.wav")

pbm = PhotoImage(file = r"img\\bombm.png")
pbm = pbm.subsample(10,10)
pbh = PhotoImage(file = r"img\\bombh.png")
pbh = pbh.subsample(33,33)
pd = PhotoImage(file = r"img\\danger.png")
pd = pd.subsample(16,16)
pc = PhotoImage(file = r"img\\congratulations.png")
pc = pc.subsample(16,16)
pfp = PhotoImage(file = r"img\\face _palm.png")
pfp = pfp.subsample(20,20)
pto = PhotoImage(file = r"img\\toungue_out.png")
pto = pto.subsample(14,14)
pqm = PhotoImage(file = r"img\\question_mark2.png")
pqm = pqm.subsample(20,20)
pwpa = PhotoImage(file = r"img\\blackpause.png")
pwpa = pwpa.subsample(10,10)
pwpl = PhotoImage(file = r"img\\blackplay.png")
pwpl = pwpl.subsample(10,10)
pwso = PhotoImage(file = r"img\\blacksoundon.png")
pwso = pwso.subsample(10,10)
pwsf = PhotoImage(file = r"img\\blacksoundoff.png")
pwsf = pwsf.subsample(11,9)
pbpa = PhotoImage(file = r"img\\whitepause.png")
pbpa = pbpa.subsample(10,10)
pbpl = PhotoImage(file = r"img\\whiteplay.png")
pbpl = pbpl.subsample(10,10)
pbso = PhotoImage(file = r"img\\whitesoundon.png")
pbso = pbso.subsample(10,10)
pbsf = PhotoImage(file = r"img\\whitesoundoff.png")
pbsf = pbsf.subsample(11,9)
pbs = PhotoImage(file = r"img\\batsymbol.png")
INTRO= PhotoImage(file = r"img\\INTRO.png")
INTROM= PhotoImage(file = r"img\\INTROM.png")

xg=0#click row
yg=0#click colomn
o=0;#opened
event= list()
button = list()
rows, cols = (5, 5)#size default
n=3.3;#difficulty 30% default
d=rows*cols//n#no of bombs
d=int(d)
be= [[0 for i in range(cols)] for j in range(rows)]#inside 1 for bomb 2 for opened
fe= [[0 for i in range(cols)] for j in range(rows)]#outside
f= [[0 for i in range(cols)] for j in range(rows)]#outside_rightclick
nf=d#no of flags
st=0#size tracker
dt=0#difficuilty tracker
#mixer.music.set_volume(.5)#Default volume
sound=1#sound on
pause=0#not paused
thanu=1#not called
wol=0#for win or loose but gets changed to 1 in reset
theme=0#default white
lang=1#default language english
cheat=0#no cheat default

def english():
    global l,soundbutton,playbutton,d,di,lang,wol,cheatbut,cheat
    lang=1
    if(wol==0) :
        reset()
    if(thanu) :
        l['text']="Mind those {} mines".format(d)
    else :
        l['text']="Mind those {} mines".format(di)
    soundbutton['text']='Sound'
    playbutton['text']='BGM'
    menubar.entryconfigure(1, label='File')
    menubar.entryconfigure(2, label='Theme')
    menubar.entryconfigure(3, label='Language')
    menubar.entryconfigure(4, label='Help')
    file.entryconfigure(0, label='Activate THANOS')
    file.entryconfigure(2, label='CheatButton')
    file.entryconfigure(3, label='Kill CheatButton')
    file.entryconfigure(4, label='Exit')
    thememenu.entryconfigure(0, label='Batman')
    thememenu.entryconfigure(1, label='Goku')
    helpmenu.entryconfigure(0, label='Guide')
    if(cheat) :
        cheatbut['text']='1 question will be answered'

def malayalam():
    global l,soundbutton,playbutton,d,di,lang,wol,cheatbut,cheat
    lang=0
    if(wol==0) :
        reset()
    s=u'ബോംബുകളെ സൂക്ഷിക്കുക'
    b=s.encode('utf-8').decode('utf-8')
    if(thanu) :
        l['text']=str(d)+b
    else :
        l['text']=str(di)+b

    s=u'ശബ്ദം'
    b=s.encode('utf-8').decode('utf-8')
    soundbutton['text']=b

    s=u'മ്യൂസിക്'
    b=s.encode('utf-8').decode('utf-8')
    playbutton['text']=b

    s=u'ഫയൽ'
    b=s.encode('utf-8').decode('utf-8')
    menubar.entryconfigure(1, label=b)

    s=u'പതിപ്പ്'
    b=s.encode('utf-8').decode('utf-8')
    menubar.entryconfigure(2, label=b)

    s=u'ഭാഷ'
    b=s.encode('utf-8').decode('utf-8')
    menubar.entryconfigure(3, label=b)
    
    s=u'സഹായം'
    b=s.encode('utf-8').decode('utf-8')
    menubar.entryconfigure(4, label=b)

    s=u'താനോസീസിനെ വിളിക്കൂ'
    b=s.encode('utf-8').decode('utf-8')
    file.entryconfigure(0, label=b)

    s=u'ചതിയൻ ബട്ടൺ'
    b=s.encode('utf-8').decode('utf-8')
    file.entryconfigure(2, label=b)

    s=u'ചതിയൻ ബട്ടണെകൊല്ലുക'
    b=s.encode('utf-8').decode('utf-8')
    file.entryconfigure(3, label=b)

    s=u'നിർത്താം'
    b=s.encode('utf-8').decode('utf-8')
    file.entryconfigure(4, label=b)

    s=u'ബാറ്റ്മാൻ'
    b=s.encode('utf-8').decode('utf-8')
    thememenu.entryconfigure(0, label=b)

    s=u'ഗോകു'
    b=s.encode('utf-8').decode('utf-8')
    thememenu.entryconfigure(1, label=b)
    
    s=u'മാർ‌ഗ്ഗനിർ‌ദ്ദേശങ്ങൾ'
    b=s.encode('utf-8').decode('utf-8')
    helpmenu.entryconfigure(0, label=b)
    
    if(cheat) :
        s=u'ഒരു ചോദ്യം ഒരു ഉത്തരം'
        b=s.encode('utf-8').decode('utf-8')
        cheatbut['text']=b
def guide():
    global lang
    if(lang):
        os.startfile(pathe)
    else :
        os.startfile(pathm)

  
def normaltheme():
    global theme
    theme=0
    if(sound):
        play()
    reset()

def blacktheme():
    global theme
    theme=1
    if(sound):
        mixer.Sound.play(imbatman)
        play()
    reset()

def batman():
    global cols,rows,cheat
    for i in range(rows*rows+3):
            button[i]['bg']='black'
            button[i]['fg']='white'
    fl['bg']='black'
    fl['fg']='white'
    l['bg']='black'
    l['fg']='white'
    timed['bg']='black'
    timed['fg']='white'
    soundbutton['bg']='black'
    soundbutton['fg']='white'
    playbutton['bg']='black'
    playbutton['fg']='white'
    if(cheat) :
        cheatbut['bg']='black'
        cheatbut['fg']='white'
    button[rows*rows]['image']=pbs

def thanosi():
    global rows,cols,nf,o,d,n,button,l,lang,di
    if(sound):
        mixer.Sound.play(snap)
    b= [0 for i in range((rows*cols)//2)]#50percent thanos goal
    i=0
    di=d
    nf=d-nf#storing used no of flags
    while(i<(rows*cols)//2):
        b[i]=random.randrange(0, rows*cols, 1)
        for j in range(i) :
            if b[j]==b[i]:
                i=i-1
        i=i+1
    for i in range((rows*cols)//2) :
          x,y=divmod(b[i],cols)
          if(be[x][y]==1) :
              di-=1
              button[x*rows+y]['state']=tk.DISABLED
              button[x*rows+y]['relief'] = "sunken"
              button[x*rows+y]['bg']='grey'
          elif(be[x][y]==2) :
              button[x*rows+y]['state']=tk.DISABLED
              button[x*rows+y]['relief'] = "sunken"
              button[x*rows+y]['bg']='grey'
              button[x*rows+y]['text']=fe[x][y]
          else :
              button[x*rows+y]['state']=tk.DISABLED
              button[x*rows+y]['relief'] = "sunken"
              button[x*rows+y]['bg']='grey'
          if (f[x][y]==1):
              nf=nf-1
          be[x][y]=3
          o+=1
    nf=di-nf#storing new flags remaining
    flagrefresh()
    if (lang):
        l['text']="Mind those {} mines".format(di)
    else :
        s=u'ബോംബ് കളെ സൂക്ഷിക്കുക'
        b=s.encode('utf-8').decode('utf-8')
        l['text']=str(di)+b

def cheatz() :
    global rows,cols
    for i in range (rows) :
        for j in range (cols) :
            if(f[i][j]==2 and be[i][j]==0) :
                leftklick(i,j)
                return
def killcheat():
    global cheat
    cheat=0
    forget()
    reset()

def cheatbutton() :
    global rows,cols,lang,theme ,cheatbut ,cheat
    cheat=1
    cheatbut=tk.Button(t,font=("Helvetica", 12),command=cheatz)
    cheatbut.grid(column=0,row=rows+3,columnspan=cols,sticky="wens")
    if(lang) :
        cheatbut['text']='1 question will be answered'
    else :
        s=u'ഒരു ചോദ്യം ഒരു ഉത്തരം'
        b=s.encode('utf-8').decode('utf-8')
        cheatbut['text']=b
    if (theme)  :
        cheatbut['bg']='black'
        cheatbut['fg']='white'
    else :
        cheatbut['bg']='white'
        cheatbut['fg']='black'

def fifty() :
    global rows,cols,n,nf,d
    n=2
    d=rows*cols//n
    d=int(d)
    nf=d
    reset()

def thanos():
    global thanu,wol,lang
    if(thanu):
        thanosi()
    else :
        if(lang) :
            tkinter.messagebox.showerror('THOR',' I went for the head' )
        else :
            s=u'എപ്പോഴും എപ്പോഴും ഇങ്ങനെ കുമ്പിട്ട് നിൽക്കാൻ പറ്റില്ല പഴയ ജിംനാസിയാണ്'
            b=s.encode('utf-8').decode('utf-8')
            s1=u'താനോസ്'
            b1=s1.encode('utf-8').decode('utf-8')
            tkinter.messagebox.showerror(b1,b)
    thanu=0

def on_closing():
    global lang
    if(lang) :
        exitfunc()
    else :
        s1=u'ഷമ്മി തൽസമയം പറയുന്നു'
        b1=s1.encode('utf-8').decode('utf-8')
        s=u'ഡാ മോനെ അത് ലോക്കാ ഇങ്ങു പോര്'
        b=s.encode('utf-8').decode('utf-8')
        tkinter.messagebox.showerror(b1,b)

def exitfunc():
    mixer.music.stop()
    t.destroy()

def rightloose():
    global lang
    if(lang) :
        tkinter.messagebox.showinfo('For Your Information','Right Click is for creating FLAGS not REATH')
    else :
        s1=u'താങ്കളുടെ അറിവിനു വേണ്ടി'
        b1=s1.encode('utf-8').decode('utf-8')
        s=u'ഇത് ഫ്ലാഗ് വെക്കാനുള്ള ബട്ടൺ ആണ് റീത്ത് വയ്ക്കാനുള്ളതല്ല'
        b=s.encode('utf-8').decode('utf-8')
        tkinter.messagebox.showerror(b1,b)

def leftloose():
    global lang
    if(lang) :
        tkinter.messagebox.showinfo('Black Panther Says','We dont do that here')
    else :
        s=u'ശവത്തിൽ കുത്താതെ'
        b=s.encode('utf-8').decode('utf-8')
        s1=u'മനസ്സാക്ഷി പറയുന്നു'
        b1=s1.encode('utf-8').decode('utf-8')
        tkinter.messagebox.showwarning('SHAMMI',b)

def play():
    global soundbutton,sound,pause
    if(theme):
        mixer.music.load("SFX\\\Batmanbgm.mp3")
        soundbutton['image']=pbsf
    else :
        mixer.music.load("SFX\\\SSJ3-Goku_Theme.mp3.") #Loading File Into Mixer   #bgm
        soundbutton['image']=pwsf
    mixer.music.play(-1) #Playing It In The Whole Device
    soundbutton['command']=stop
    soundbutton.bind("<Button-3>",lambda event2:stop())
    sound=1
    if(pause==1):
        paused()

def stop():
    global soundbutton,sound
    if(theme):
        soundbutton['image']=pbso
    else :
        soundbutton['image']=pwso
    soundbutton['command']=play
    soundbutton.bind("<Button-3>",lambda event2:play())
    sound=0
    mixer.music.stop()

def unpause():
    global playbutton,pause
    mixer.music.unpause()
    if(theme):
        playbutton['image']=pbpa
    else :
        playbutton['image']=pwpa
    playbutton['command']=paused
    playbutton.bind("<Button-3>",lambda event2:paused())
    pause=0

def paused():
    global playbutton,pause
    mixer.music.pause()
    if(theme):
        playbutton['image']=pbpl
    else :
        playbutton['image']=pwpl
    playbutton['command']=unpause
    playbutton.bind("<Button-3>",lambda event2:unpause())
    pause=1

def forget() :
    global rows,cols
    for button in t.grid_slaves():
           button.grid_forget()
    for i in range(cols) :
        t.grid_columnconfigure(i,weight=0,minsize=0)
    for i in range(rows+3) :
        t.grid_rowconfigure(i,weight=0,minsize=0)


def size():
    global rows,cols,st,n,nf,d
    forget()
    if (st==0):
        rows, cols = (7, 7)#size
        st=1
    elif (st==1):
        rows, cols = (9, 9)#size
        st=2
    else :
       rows, cols = (5, 5)#size
       st=0
    d=rows*cols//n
    d=int(d)
    nf=d
    reset()

def diff() :#difficulty
    global rows,cols,dt,n,nf,d
    if (dt==0):
        n=2.5
        dt=1
    elif (dt==1):
        n=6.6
        dt=2
    else :
        n=3.3
        dt=0
    d=rows*cols//n
    d=int(d)
    nf=d
    reset()

def gameset():
    global be,d,rows,cols,fe
    b= [0 for i in range(d)]#bomb
    i=0
    while(i<d):
        f=random.randrange(0, rows*cols, 1)
        b[i]=f
        for j in range(i) :
            if b[j]==f :
                i=i-1 #checks if same then ignore
        i=i+1
    for i in range(d) :
      x,y=divmod(b[i],cols)
      be[x][y]=1
    for i in range(rows):
        for j in range(cols):
            f=0
            x=max(i-1,0)
            while (x<=min(i+1,rows-1)):
                y=max(j-1,0)
                while (y<=min(j+1,cols-1)):
                    if (x==i and y==j):
                        y=y+1
                        continue
                    f=f+be[x][y]
                    y=y+1
                x=x+1
            fe[i][j]=f
            j=j+1
        i=i+1

def flagrefresh():
    global f1
    fl['text']="Flags :{}".format(nf)


def timer ():
    global timed,wol
    t=0
    while(wol):
        i=0
        (mins,secs)=divmod(t,60)
        timeformat='{:02d}:{:02d}'.format(mins,secs)
        timed['text']=timeformat
        while(wol and i<50):
            time.sleep(0.02)
            i+=1
        t+=1
    return

def reset():
    global rows,cols,nf,be,fe,f,o,d,n,button,l,click,wol,thanu,fl,theme,cheat
    click=1
    thanu=1
    del button
    button = list()
    for i in range(cols) :
        t.grid_columnconfigure(i,weight=1,minsize=70)
        t.grid_rowconfigure(i,weight=1,minsize=60)
    t.grid_rowconfigure(rows,weight=1,minsize=60)
    for i in range(rows):
        for j in range(cols):
           button.append(tk.Button(font=("Helvetica", 12),bg='white',command=partial(klik,i,j)))
           button[-1].grid(row=i,column=j,sticky="wens")
           button[i*rows+j].bind("<Button-3>",lambda event1:right_click(event1))
           button[i*rows+j].bind("<Button-1>",lambda event1:left_click(event1))

    button.append(tk.Button(image=pto,bg='white',command=lambda :reset())) #rows*rows
    button[-1].grid(row=rows,column=2,sticky="wens",columnspan=rows-4)
    button[rows*rows].bind("<Button-3>",lambda event1:reset())

    button.append(tk.Button(text='{}X{}'.format(rows,cols),font=("Helvetica", 12),fg='black',bg='white',command=lambda :size()))#rows*rows+1
    button[-1].grid(row=rows,column=rows-2,sticky="wens")
    button[rows*rows+1].bind("<Button-3>",lambda event1:size())

    button.append(tk.Button(text='{}%'.format(int(100//n)),font=("Helvetica", 12),fg='black',bg='white',command=lambda :diff()))#rows*rows+2
    button[-1].grid(row=rows,column=rows-1,sticky="wens")
    button[rows*rows+2].bind("<Button-3>",lambda event1:diff())
    nf=d
    be= [[0 for i in range(cols)] for j in range(rows)]#inside
    fe= [[0 for i in range(cols)] for j in range(rows)]#outside
    f= [[0 for i in range(cols)] for j in range(rows)]#outside_rightclick
    fl=tk.Label(t,text="Flags :{}".format(nf),font=("Helvetica", 12),fg='black',bg='white')
    fl.grid(row=rows,column=0,sticky="wens",columnspan=2)
    o=0
    gameset()
    l=tk.Label(t,text="Mind those {} mines".format(d),font=("Helvetica", 12),fg='black',bg='white')
    l.grid(row=rows+1,column=0,sticky="wens",columnspan=cols)
    fixed_buttons()
    if(cheat)   :
        cheatbutton()
    if(wol):
        wol=0
        time.sleep(0.02)#buffer to fix double timer
    wol=1
    if (lang==0) :
        malayalam()
    if(theme):
        batman()
    #(i,j)=(0,4)
    #button[i*rows+j]['text']=i*rows+j

def fixed_buttons():
    global rows,cols,playbutton,soundbutton,sound,pause,timed
    soundbutton=tk.Button(t,bg='white',text='Sound',compound=RIGHT)
    soundbutton.grid(row=rows+2,column=0,sticky="wens",columnspan=2)
    playbutton=tk.Button(t,bg='white',text='BGM',compound=RIGHT)
    playbutton.grid(row=rows+2,column=cols-2,sticky="wens",columnspan=2)
    timed=tk.Label(t,text='00:00',font=("Helvetica", 12),fg='black',bg='white')
    timed.grid(row=rows+2,column=2,sticky="wens",columnspan=rows-4)
    if(pause) :
        paused()
    else :
        unpause()
    if(sound):
       if(theme):
            soundbutton['image']=pbsf
       else :
            soundbutton['image']=pwsf
       soundbutton['command']=stop

    else :
       stop()

def left_click(event1):
    global f,event
    event =event1

def right_click(event1):
    global f,event,nf
    event =event1
    #event1.widget.config(relief = "sunken")
    #t.update_idletasks()
    event.widget.invoke()
    #event.widget.config(relief = "raised")
    if (be[xg][yg]==2):
        return
    if (f[xg][yg]==1):
        button[xg*rows+yg]['image']=pqm    #question_mark
        nf=nf+1
    elif (f[xg][yg]==2):
        button[xg*rows+yg]['image']=""
    else :
        button[xg*rows+yg]['image']=pd      #danger
        nf=nf-1
    f[xg][yg]=f[xg][yg]+1;
    if(f[xg][yg]>2):
        f[xg][yg]=0
    flagrefresh()

def lose():
    global cols,f,xg,yg,sound,l,wol,thanu,lang
    thanu=0
    wol=0
    if(sound):
        mixer.Sound.play(loose_sound)
    for i in range(rows):
            for j in range(cols):
                    button[i*rows+j].bind("<Button-3>",lambda event2:rightloose())
                    if (be[i][j]==1):
                        button[i*rows+j]['activebackground']='white'
                        button[i*rows+j]['command']=lambda :leftloose()
                        button[i*rows+j]['image'] =pbm
                        button[i*rows+j]['relief']="sunken"
                        if(f[i][j]==1):
                            button[i*rows+j]['bg']='yellow'
                        else :
                            button[i*rows+j]['bg']='white'
                    elif(be[i][j]==0):
                        button[i*rows+j]['state']=tk.DISABLED
                        button[i*rows+j]['text'] = fe[i][j]
    if(lang):
        l['text']="Better Luck Next Time"
    else :
        s=u'അടുത്ത തവണ ജയിക്കാം'
        b=s.encode('utf-8').decode('utf-8')
        l['text']=b
    button[xg*rows+yg]['activebackground']='red'
    button[xg*rows+yg]['bg']='red'
    button[xg*rows+yg]['image'] =pbh
    button[rows*rows]['image'] = pfp

def win():
    global cols,sound,l,wol,lang
    thanu=0
    wol=0
    if(sound):
        mixer.Sound.play(win_sound)
    button[rows*rows]['image']=pc
    if(lang):
        l['text']="Congratulations"
    else :
        s=u'അഭിനന്ദനങ്ങൾ താങ്കൾ ജയിച്ചിരിക്കുന്നു'
        b=s.encode('utf-8').decode('utf-8')
        l['text']=b
    for i in range(rows):
        for j in range(cols):
            if(be[i][j]==1):
                button[i*rows+j]['state']=tk.DISABLED
                button[i*rows+j]['image']=pbm

def leftklick(i,j):

    global o,d,nf,f,rows,cols
    button[i*rows+j]['image']=""
    if (be[i][j]==1):
        lose()

    else :
        if (f[i][j]==1):
            nf=nf+1
            flagrefresh()
        be[i][j]=2
        o=o+1
        if (fe[i][j]==0):
            button[i*rows+j]['state']=tk.DISABLED
            button[i*rows+j]['bg']='green'
            button[i*rows+j]['relief']='sunken'
            jackpot(i,j)

        elif (fe[i][j]==1):
            button[i*rows+j]['state']=tk.DISABLED
            button[i*rows+j]['bg']='cyan'
            button[i*rows+j]['relief']='sunken'
            button[i*rows+j]['text']=fe[i][j]
            button[i*rows+j]['disabledforeground']="black"
        elif (fe[i][j]==2):
            button[i*rows+j]['state']=tk.DISABLED
            button[i*rows+j]['bg']='yellow'
            button[i*rows+j]['relief']='sunken'
            button[i*rows+j]['text']=fe[i][j]
            button[i*rows+j]['disabledforeground']="black"

        elif (fe[i][j]==3):
            button[i*rows+j]['state']=tk.DISABLED
            button[i*rows+j]['bg']='blue'
            button[i*rows+j]['relief']='sunken'
            button[i*rows+j]['text']=fe[i][j]
            button[i*rows+j]['disabledforeground']="white"

        else :
            button[i*rows+j]['state']=tk.DISABLED
            button[i*rows+j]['bg']='red'
            button[i*rows+j]['relief']='sunken'
            button[i*rows+j]['text']=fe[i][j]
            button[i*rows+j]['disabledforeground']="white"

    if(o==rows*cols-d):
       win()

def jackpot(i,j):
    x=max(i-1,0)
    while (x<=min(i+1,rows-1)):
        y=max(j-1,0)
        while (y<=min(j+1,cols-1)):
            if ((x==i and y==j)or be[x][y]==2 or be[x][y]==3 ):
                y=y+1
                continue
            leftklick(x,y)
            y=y+1
        x=x+1

def klik(i,j):
    global xg,yg,event,click
    if(click):
        t1=threading.Thread(target=timer)
        t1.start()
        click=0
    xg=i
    yg=j
    if(event.num==3):
         return
    leftklick(i,j)

def create_menu():
    global menubar,file,thememenu,language,helpmenu
    menubar=tk.Menu(t)
    t.config(menu=menubar)

    file=tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label='File',menu=file)
    file.add_command(label='Activate THANOS',command=thanos)
    file.add_command(label='50%',command=fifty)
    file.add_command(label='CheatButton',command=cheatbutton)
    file.add_command(label='Kill CheatButton',command=killcheat)
    file.add_command(label='Exit',command=exitfunc)

    thememenu=tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label='Theme',menu=thememenu)
    thememenu.add_command(label='Batman',command=blacktheme)
    thememenu.add_command(label='Goku',command=normaltheme)

    language=tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label='Language',menu=language)
    language.add_command(label='English',command=english)
    s=u'മലയാളം'
    b=s.encode('utf-8').decode('utf-8')
    language.add_command(label=b,command=malayalam)
    
    helpmenu=tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label='Help',menu=helpmenu)
    helpmenu.add_command(label='Guide',command=guide)
def mainfunctions():
    create_menu()
    reset()

def displayintro():
    mixer.music.play(-1) #Playing It In The Whole Device
    t.grid_columnconfigure(0,weight=1,minsize=70)
    t.grid_rowconfigure(0,weight=1,minsize=60)
    l=tk.Label(t,image=INTRO)
    l.grid(row=0,column=0,sticky="wens",columnspan=1)
    time.sleep(2)
    l['image']=INTROM
    time.sleep(2)
    forget()
    mainfunctions()

t1=threading.Thread(target=displayintro)
t1.start()
t.protocol("WM_DELETE_WINDOW", on_closing)
t.mainloop()


