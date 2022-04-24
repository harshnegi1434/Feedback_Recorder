import tkinter as tk             
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from textblob import TextBlob
from textblob import Word
import nltk
import threading
import pyaudio
import wave
import sounddevice as sd 
import soundfile as sf
import speech_recognition as sr
import json
import requests

project = tk.Tk()

#Name of the  Application
project.title("FAI PROJECT")

#Voice Recording
class Voice_rec():
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 2
        fs = 44100

        frames = []
        def __init__(self):
            newWindow = Toplevel(project)
            newWindow.title("Audio")
            newWindow.geometry("240x240")
            self.isrecording = False
            self.button11 = tk.Button(newWindow, text='Start Recording',command=self.startrecording)
            self.button12 = tk.Button(newWindow, text='Stop Recording',command=self.stoprecording)
            self.button11.pack()
            self.button12.pack()

        def startrecording(self):
            
            self.p = pyaudio.PyAudio()  
            self.stream = self.p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
            self.isrecording = True
            messagebox.showinfo("Started", "Recording....")
            t = threading.Thread(target=self.record)
            t.start()

        def stoprecording(self):
                self.isrecording = False
                messagebox.showinfo("Success", "Your File Has Been Recorded !")
                user_inp = simpledialog.askstring(title="Saving", prompt="Save Your Filename As : ")
                self.filename = f"{user_inp}.wav"
                wf = wave.open(self.filename, 'wb')
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.p.get_sample_size(self.sample_format))
                wf.setframerate(self.fs)
                wf.writeframes(b''.join(self.frames))
                wf.close()
                messagebox.showinfo("Done", "Your Recording Is Saved !" )
                #Now The File Will Be Uploaded To Google Drive 
                headers = {"Authorization": "Bearer ya29.a0AfH6SMAm4nucuchXFEi1BUzp9d7GMtgIi4cr01JNBrxXTM9ETw70ysoX9Sk6UaAXjTIkkYzCoMnyjBbJMfs7eO7FQ89It2dvMWxEHlBlDfrEbtJ0Sj1_bRndLrP0DsSGUg04VobMrj4r-GKIpJvtuSSHP1ylTOU52Gd-UMipGaw"}
                para = {"name" : self.filename}
                files = {'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'), 'file': open(self.filename, "rb") }
                r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", headers=headers, files=files)
                messagebox.showinfo("Success !", "Your File Has Been Uploaded To Google Drive!")

        def record(self):
                while self.isrecording:
                    data = self.stream.read(self.chunk)
                    self.frames.append(data)
            
#Conversion Of Speech To Text
def Speech_To_Text():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=0)
    messagebox.showinfo("Greetings", "Thank You!, Press OK To Start Recording Your Response")
    messagebox.showinfo("Confirmation", "Press OK To Start Recording ")
    with mic as source:
        audio = r.listen(source)
        result = r.recognize_google(audio)
    messagebox.showinfo("Done" , "Thank You!, Your Feedback Is Recorded")
    obj = TextBlob(result)
    sentiment, subjectivity = obj.sentiment
    with open('Feedback_Form.txt',mode ='w') as file:
        file.write("Feedback : ")
        file.write("\n")
        if sentiment == 0:
                file.write("The Response Is  Neutral")
        elif sentiment > 0:
                file.write("The Response Is Positive")
        else:
                file.write("The Response Is Negative")
        file.write("\n")
        file.write("Response : ")
        file.write("\n")
        file.write(result)
    
    #Now The File Will Be Uploaded To Google Drive    
    headers = {"Authorization": "Bearer ya29.a0AfH6SMAm4nucuchXFEi1BUzp9d7GMtgIi4cr01JNBrxXTM9ETw70ysoX9Sk6UaAXjTIkkYzCoMnyjBbJMfs7eO7FQ89It2dvMWxEHlBlDfrEbtJ0Sj1_bRndLrP0DsSGUg04VobMrj4r-GKIpJvtuSSHP1ylTOU52Gd-UMipGaw"}
    para = {"name" : "Feedback_Form.txt",}
    files = {'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'), 'file': open("./Feedback_Form.txt", "rb") }
    R = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", headers=headers, files=files)
    messagebox.showinfo("Success !", "Your File Has Been Uploaded To Google Drive!")
    
#Opening a New Window For Choosing The Speech Option
def NewWindow_1():
    newWindow = Toplevel(project)
    newWindow.title("Speech Work")
    newWindow.geometry("240x240")
    button_3 = tk.Button(newWindow, text = "Record Audio" ,width=25, command = Voice_rec)
    button_4 = tk.Button(newWindow, text = "Record Response" ,width=25, command = Speech_To_Text)
    button_3.pack()
    button_4.pack()

#Canvas is Created
w = Canvas(project, width=300, height=150)

#Buttons Are Added
button_1 = tk.Button(project, text = "Start", width=25, command = NewWindow_1)
button_2 = tk.Button(project, text = "Quit" ,width=25, command = project.destroy)

w.pack()
button_1.pack()
button_2.pack()
project.mainloop() 



### IMPORTANT - The Google Drive Link Authorization Code Has To Be Regenerated Every Hour. It Can Be Solved By Using Python Quickstart. 
