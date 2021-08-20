#importing libraries
from tkinter import *
import tkinter.messagebox
from PIL import ImageTk, Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
import mysql.connector
import random
from decouple import config

#creating window
window = Tk()
window.title("Sentiment Analysis")
window.geometry("500x700+400+25")
window.iconbitmap('C:/Users/Acer PC/Desktop/Python/-sentiment-very-satisfied_89968.ico')
window.resizable(FALSE,FALSE)

Result = ""
ss = "SENTIMENT ANALYSIS TOOL"
count = 0
txt = ""

#Connecting to database
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = config('passwd'),
    database = config('database'),
)

#creating a cursor
my_cursor = mydb.cursor()

'''
colors = ['green','gold','red','black']
#Slidercolor function
def slidercolor():
    fg = random.choice(colors)
    l1.config(fg=fg)
    l1.after(2,slidercolor)
'''
#Slidertext function
def slider():
    global count,txt
    if(count>=len(ss)):
        count = 0
        txt = ""
        l1.config(text=txt)
    else:
        txt = txt+ss[count]
        l1.config(text=txt)
        count += 1
    l1.after(200,slider)

#clear text function
def Clear():
    m1=text.get(1.0, END)
    if len(m1)==1:
        tkinter.messagebox.showinfo("Warning", "Enter text first")
    else:
        text.delete(1.0, END)

#get text function
def get_text():
    global Result
    m2=text.get(1.0, END)
    if len(m2)==1:
        tkinter.messagebox.showinfo("Warning", "Enter text to perform analysis")
    else:
        t1.delete(1.0, END)
        t2.delete(1.0, END)
        t3.delete(1.0, END)
        Textvar = text.get(1.0, END)
        Lower = Textvar.lower()
        cleaned = Lower.translate(str.maketrans('','',string.punctuation))
        score = SentimentIntensityAnalyzer().polarity_scores(cleaned)
        t1.insert(1.0, score['pos'])
        t2.insert(1.0, score['neu'])
        t3.insert(1.0, score['neg'])
        comp = score['compound']
        if comp >= 0.05:
            l5.config(text="Above text has a POSITIVE sentiment")
            Result = "POSITIVE"
        elif comp <= -0.05:
            l5.config(text="Above text has a NEGATIVE sentiment")
            Result = "NEGATIVE"
        else:
            l5.config(text="Above text has a NEUTRAL sentiment")
            Result = "NEUTRAL"

#save results function
def Save_db():
    m3=text.get(1.0, END)
    if len(m3)==1:
        tkinter.messagebox.showinfo("Warning", "Enter text to save")
    else:
        sql_command = "INSERT INTO analysis (review, pos_score, neg_score, neu_score, sentiment) VALUES (%s, %s, %s, %s, %s)"
        values = (text.get(1.0, END), t1.get(1.0, END), t3.get(1.0, END), t2.get(1.0, END), Result)
        my_cursor.execute(sql_command, values)
        mydb.commit()
        tkinter.messagebox.showinfo("", "Saved Sucessfully")

#header
l1 = Label(window, text=ss, font="ArialBlack 22 bold")
l1.grid(row=0,column=0)
slider()
#slidercolor()
c1 = Canvas(window, width=500, height=2, bg="grey").grid(row=1,column=0)

#main review frame
frame = LabelFrame(window,text="Write your text here")
frame.grid(row=2,column=0,padx=10,pady=10,sticky="nsew")
text = Text(frame,width=55,height=12,borderwidth=3,wrap="word",bg="light cyan")
text.grid(row=0,column=0,columnspan=2,padx=5,pady=5)

#adding buttons
pallete = LabelFrame(window,text="Buttons")
pallete.grid(row=3,column=0,padx=10,pady=10,sticky="nsew")
btn1 = Button(pallete,height=3,width=20,text="Perform Analysis",command=get_text)
btn1.grid(row=0,column=0,padx=5,pady=10,sticky="nsew")

btn2 = Button(pallete,height=3,width=20,text="Clear text",command=Clear)
btn2.grid(row=0,column=1,padx=5,pady=10,sticky="nsew")

btn3 = Button(pallete,height=3,width=20,text="Save results",command=Save_db)
btn3.grid(row=0,column=2,padx=5,pady=10,sticky="nsew")

#result frame
Analyze = LabelFrame(window,text="Result")
Analyze.grid(row=4,column=0,padx=10,pady=5,sticky="nsew")
l3 = Label(Analyze, text="Emotion Scores:",font="Arialblack 10")
l3.grid(row=0,column=0,columnspan=3,sticky="nsew")

#adding images
im1 = Image.open("C:/Users/Acer PC/Downloads/pst.jpg")
resize1 = im1.resize((100,100), Image.ANTIALIAS)
new1 = ImageTk.PhotoImage(resize1)

im2 = Image.open("C:/Users/Acer PC/Downloads/neu.jpg")
resize2 = im2.resize((100,100), Image.ANTIALIAS)
new2 = ImageTk.PhotoImage(resize2)

im3 = Image.open("C:/Users/Acer PC/Downloads/neg.jpg")
resize3 = im3.resize((100,100), Image.ANTIALIAS)
new3 = ImageTk.PhotoImage(resize3)

#adding frames
f1 = LabelFrame(Analyze,text="Positive")
f1.grid(row=1,column=0,padx=15,pady=10,sticky="nsew")
l2 = Label(f1,image=new1)
l2.grid(row=0,column=0,padx=10,sticky="nsew")

f2 = LabelFrame(Analyze,text="Neutral")
f2.grid(row=1,column=1,padx=15,pady=10,sticky="nsew")
l3 = Label(f2,image=new2)
l3.grid(row=0,column=0,padx=10,sticky="nsew")

f3 = LabelFrame(Analyze,text="Negative")
f3.grid(row=1,column=2,padx=15,pady=10,sticky="nsew")
l4 = Label(f3,image=new3)
l4.grid(row=0,column=0,padx=10,sticky="nsew")

#adding texts
t1 = Text(f1,width=6,height=1,borderwidth=1)
t1.grid(row=1,column=0,pady=5)
t2 = Text(f2,width=6,height=1,borderwidth=1)
t2.grid(row=1,column=0,pady=5)
t3 = Text(f3,width=6,height=1,borderwidth=1)
t3.grid(row=1,column=0,pady=5)
l5 = Label(Analyze,text="",font="15")
l5.grid(row=2,column=0,columnspan=3,pady=5)

#adding scrollbar
scroll = Scrollbar(frame,command=text.yview)
text['yscroll'] = scroll.set
scroll.grid(row=0,column=2,sticky="ns")

window.mainloop()