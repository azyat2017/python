#les packages utilisés
from tkinter import  *
from tkinter import filedialog
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
#data frame emty sera rempli de données de fichier csv
dfa=None
#variables globales
varbs=[]
names=[]
#parent interface
root=Tk()
root.title("Data Visulation")
bg_image=PhotoImage(file="bckg2.gif")
w=bg_image.width()
h=bg_image.height()
root.geometry("%dx%d+0+0" % (w, h))
panel1 = Label(root, image=bg_image)
panel1.place(x=0,y=0,relwidth=1,relheight=1)
Tops=Entry(panel1,state='disabled')
Tops.pack(side=TOP,padx=100,pady=10)
Tops.focus_set()
#frames
f1=Frame(panel1,width=90,height=10,relief=SUNKEN)
f1.pack(side=TOP,padx=100,pady=50)
f1.focus_set()
f2=Frame(panel1,width=90,height=10,relief=SUNKEN)
f2.pack(side=TOP)
f2.focus_set()
f3=Frame(panel1,width=90,height=10,relief=SUNKEN)
f3.pack(side=BOTTOM)
f3.focus_set()
#Heading de homepage: Data Visulation
lblinfo=Label(Tops,font=('aria',30,'italic'),text="Data Visulation",fg="forest green")
lblinfo.rowconfigure(0,weight=1)
lblinfo.columnconfigure(1,weight=1)
lblinfo.pack(side=TOP,padx=100,pady=5,fill="both")
#ce fonction est responsable de l'affichage de données sous forme d'un tableau organisé
def popup_bonus(df):
    #toplevel permet d'afficher une fentre au dessous d'autre "pop up window"
    win=Toplevel()
    win.wm_title("Window")
    """
    canvas = Canvas(win)
    f2 = Frame(canvas)
    scrollbar = Scrollbar(canvas, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=RIGHT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas_frame = canvas.create_window((0, 0), window=f2, anchor=N + W)
    """
    f2=Frame(win)
    f2.pack()
    tree=ttk.Treeview(f2)
    tree["columns"]=("1","2","3","4","5")
    for x in range(len(df.columns)):
        tree.column("#"+str((x+1)), stretch=YES)
    l=0
    #les titres de chaque colonne
    for col in df.columns:
        tree.heading("#"+str((l+1)),text=col,anchor=E)
        l+=1
    count = len(df.index)
    print(count)
    #inserez ligne par ligne
    for i in range(count):
        row=df.iloc[i]
        listie=[]
        for j in range(5):
            listie.append(row[j])
        tree.insert('','end',text="item"+str(i),values=(listie[0],listie[1],listie[2],listie[3],listie[4]))
    tree.grid(row=4,columnspan=4,sticky='nsew')
    
#ce fonction supprime les variables non checké dans fonction doAnalysis, variable qui reste on applique sur lui les fonction de statistique      
def swimingPool():
    j=0
    for var in varbs:
        if(var.get()==0):
            del names[j]
        j+=1
    
    
    root=Toplevel()
    root.wm_title("Window")
    win=Frame(root)
    win.pack(side=RIGHT)
    Label(win, text="Max:").grid(row=0, sticky=W)
    Label(win, text=dfa[names[0]].max(),borderwidth=2,relief="solid").grid(row=0,column=1, sticky=W)
    Label(win, text="Min:").grid(row=1, sticky=W)
    Label(win, text=dfa[names[0]].min(),borderwidth=2,relief="solid").grid(row=1,column=1, sticky=W)
    Label(win, text="Somme:").grid(row=2, sticky=W)
    Label(win, text=dfa[names[0]].sum(),borderwidth=2,relief="solid").grid(row=2,column=1, sticky=W)
    Label(win, text="Mean:").grid(row=3, sticky=W)
    Label(win, text=dfa[names[0]].mean(),borderwidth=2,relief="solid").grid(row=3,column=1, sticky=W)
    Label(win, text="Mode:").grid(row=4, sticky=W)
    Label(win, text=dfa[names[0]].mode(),borderwidth=2,relief="solid").grid(row=4,column=1, sticky=W)
    Label(win, text="Standard deviation(écart:").grid(row=5, sticky=W)
    Label(win, text=dfa[names[0]].std(),borderwidth=2,relief="solid").grid(row=5,column=1, sticky=W)
    f1=Frame(root)
    f1.pack(side="right")
    #affiche des graphes grace aux fonctions de matplotlib
    figure = plt.Figure(figsize=(6,5), dpi=100)
    plt.xticks(dfa["Year"])
    ax = figure.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure, f1)
    chart_type.get_tk_widget().pack()
    df2=dfa[['Year','Value']].groupby('Year').sum()
    df2.plot(kind='line',legend=True,color='r',marker='o',fontsize=10,ax=ax)
#on lire le fichier csv et on applique fonction popupbonus pour l'organiser sous un tableau    
def getCSV():
    global dfa
    file_path=filedialog.askopenfilename()
    dfa=pd.read_csv(file_path,encoding="ISO-8859-1",sep=",",squeeze=True)
    popup_bonus(dfa)
#ce fonction affiche un window avec des variables quantitatives pour choisir le quel on veut traiter
def doAnalysis():
    global dfa
    if(dfa is None):
        file_path=filedialog.askopenfilename()
        dfa=pd.read_csv(file_path,encoding="ISO-8859-1",sep=",")
        win=Toplevel()
        win.wm_title("Window")
        Label(win, text="Choose a variable:").grid(row=0, sticky=W)
        i=1
        global varbs
        global names
        names.clear()
        varbs.clear()
        for col in dfa.columns:
            if(dfa[col].dtype==np.float64 or dfa[col].dtype==np.int64):
                var1 = IntVar()
                Checkbutton(win, text=col, variable=var1).grid(row=i, sticky=W)
                varbs.append(var1)
                names.append(col)
                i+=1
        Button(win, text='Validate', command=swimingPool).grid(row=i, sticky=W, pady=4)
        Button(win, text='Cancel', command=win.destroy).grid(row=i,column=1, sticky=W, pady=4)
#les buttons "load csv" "show statistics"
btnload = Button(f1, fg="black", padx=90,pady=10,font=('ariel', 20, 'bold'), text="Load csv", width=10,height=2,command=getCSV)
btnload.grid(row=0,column=0)
btnTwo = Button(f2, padx=90, pady=10, fg="black", font=('ariel', 20, 'bold'), text="Show Statistics",  width=10,height=2,command=doAnalysis)
btnTwo.grid(row=1,column=0)
btnT = Button(f3,text="Exit",fg="red")
btnT["bg"]="white"
btnT["border"]="0"
btnT["width"]=10
btnT["height"]=2
btnT.grid(row=1,column=0)
#action
root.mainloop()