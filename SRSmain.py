from tkinter import *
from tkinter import  messagebox
import datetime
import ttk
from tkinter import filedialog
import os
from PIL import ImageTk,Image
import sqlite3
from PIL import ImageGrab
import time

Institution_Name="Government College Of Engineering & Ceramic Technology, Kolkata"
KEY= -1
PermissionForUpdateOrDelete="Denied"

def downloadRegCard(regRoot, width, height, userPHOTO):
    global KEY, PermissionForUpdateOrDelete
    screen_width=regRoot.winfo_screenwidth()
    screen_height=regRoot.winfo_screenheight()
    x_coordinate=(screen_width/2)-(width/2)
    y_coordinate=(screen_height/2)-(height/2)-40
    lastX=x_coordinate+width
    lastY=y_coordinate+height
    picName=userPHOTO[9:]
    img=ImageGrab.grab(bbox=(x_coordinate+10, y_coordinate+80, lastX+6, lastY+30))
    img.save("FinalRegistrationCards\\"+picName)
    responce=messagebox.askyesno("DISPLAY REGISTRATION CARD???", "Wanna See Your Registration Card?")
    if responce==1:
        img.show()
        time.sleep(3)
    messagebox.showinfo("SUCCESSFULLY DOWNLOADED!!!", "Your Registration Card is here:\nFinalRegistrationCards\\"+picName)
    KEY, PermissionForUpdateOrDelete=-1, "Denied"
    regRoot.destroy()

def regCardClicked(root):
    global KEY, PermissionForUpdateOrDelete, Institution_Name
    if PermissionForUpdateOrDelete=="Granted":
        width=550
        height=350
        
        regRoot=Toplevel()
        screen_width=regRoot.winfo_screenwidth()
        screen_height=regRoot.winfo_screenheight()
        x_coordinate=(screen_width/2)-(width/2)
        y_coordinate=(screen_height/2)-(height/2)-40
        regRoot.geometry("%dx%d+%d+%d" % (width, height, x_coordinate, y_coordinate))
        regRoot.minsize(width,height)
        regRoot.maxsize(width,height)
        regRoot.title("REGISTRATION CARD")
        regRoot.iconbitmap("images\icon.ico")
        regRoot.configure(background='#01e779')
        #===============================Get Data===================================================
        conn=sqlite3.connect("database\StudentDetails.db")
        c=conn.cursor()
        c.execute("SELECT *, oid FROM details")
        records=c.fetchall()
        for record in records:
            if record[7]==KEY:
                userREG=record[0]
                userROLL=record[1]
                userFNAME=record[2]
                userLNAME=record[3]
                userPHOTO=record[4]
                userSESSION=record[5]
                userADDRESS=record[6]
                break
        conn.commit()
        conn.close()
        
        #===============================Download Button===================================
        b=Button(regRoot, text="DOWNLOAD", font=("arial b", 15), bg="#0183f8", cursor="hand2",
                 command=lambda:downloadRegCard(regRoot, width, height, userPHOTO))
        b.pack(pady=(5,0))

        #================================Top Frame | Reg Card Download==========================
        tFrame=LabelFrame(regRoot, bg="#7cd0ba")
        tFrame.pack(pady=(20,0))
        label=Label(tFrame, text="Registration Card", font=("arial b", 30), bg="#7cd0ba")
        label.pack(pady=(10,0), padx=20)
        institutionLabel=Label(tFrame, text=Institution_Name, bg="#7cd0ba", font=("arial b", 13))
        institutionLabel.pack(pady=(0,10), padx=15)
     
        #================================Middle Left Frame | Reg Card Download==========================
        mlFrame=Frame(regRoot, bg='#01e779')
        mlFrame.pack(side=LEFT, padx=(25,0))
        
        img=ImageTk.PhotoImage(Image.open(userPHOTO))
        panel=Label(mlFrame, image=img, bg='#01e779')
        panel.pack()
        
        #================================Middle Right Frame | Reg Card Download==========================
        mrFrame=Frame(regRoot, bg='#01e779')
        mrFrame.pack(side=RIGHT, padx=(0,25))

        mrlFrame=Frame(mrFrame, bg='#01e779')
        mrlFrame.pack(side=LEFT, padx=(25,0))
        nameL=Label(mrlFrame, text="NAME", font=("arial", 17), bg='#01e779').pack()
        regL=Label(mrlFrame, text="REG. NO.", font=("arial", 17), bg='#01e779').pack()
        rollL=Label(mrlFrame, text="ROLL NO.", font=("arial", 17), bg='#01e779').pack()
        addL=Label(mrlFrame, text="ADDRESS", font=("arial", 17), bg='#01e779').pack()
        sessL=Label(mrlFrame, text="SESSION", font=("arial", 17), bg='#01e779').pack()

        mrrFrame=Frame(mrFrame, bg='#01e779')
        mrrFrame.pack(side=RIGHT, padx=(5,30))
        name=Label(mrrFrame, text=userFNAME+" "+userLNAME, font=("arial", 17), bg='#01e779').pack()
        reg=Label(mrrFrame, text=userREG, font=("arial", 17), bg='#01e779').pack()
        roll=Label(mrrFrame, text=userROLL, font=("arial", 17), bg='#01e779').pack()
        add=Label(mrrFrame, text=userADDRESS, font=("arial", 17), bg='#01e779').pack()
        sess=Label(mrrFrame, text=userSESSION, font=("arial", 17), bg='#01e779').pack()
        
        
        regRoot.mainloop()        
        #KEY, PermissionForUpdateOrDelete=-1, "Denied"
    else:
        messagebox.showwarning("WARNING!!!", "Please Specify The Data By Clicking The Display Button")

def updateClicked(root, regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr,sessionE, addressE, display, tEntityE, variable):
    global KEY, PermissionForUpdateOrDelete
    if PermissionForUpdateOrDelete=="Granted":
        #==============================Fetching Previous Data======================================
        conn=sqlite3.connect("database\StudentDetails.db")
        c=conn.cursor()
        c.execute("SELECT *, oid FROM details")
        records=c.fetchall()
        for record in records:
            if record[7]==KEY:
                preREG=record[0]
                preROLL=record[1]
                preFNAME=record[2]
                preLNAME=record[3]
                prePHOTO=record[4]
                preSESSION=record[5]
                preADDRESS=record[6]
                break
        conn.commit()
        conn.close()
        #=================================New Data=========================================
        photoPathEntry.config(state=NORMAL)
        sessionE.config(state="normal")
        
        newREG=regE.get().strip()
        newROLL=rollE.get().strip()
        newFNAME=fnameE.get().strip()
        newLNAME=lnameE.get().strip()
        newSESSION=sessionE.get().strip()
        newADDRESS=addressE.get().strip()
        #===========Make the virtual databased address===================================
        realSession=variable.get()
        reelSession=realSession[:4]+"-"+realSession[5:]
        image = Image.open(photoPathEntry.get())
        reelAddress=addressE.get().strip().split()
        finalReelAddress=""
        for i in range(len(reelAddress)):
            finalReelAddress+=reelAddress[i]
            if i!=len(reelAddress)-1:
                finalReelAddress+="-"
        newPHOTO="database\{}_{}_{}{}_{}_{}.png".format(regE.get().strip(),
                                                          rollE.get().strip(),
                                                          fnameE.get().strip(),
                                                          lnameE.get().strip(),
                                                          reelSession,
                                                          finalReelAddress
                                                          )        
        photoPathEntry.config(state=DISABLED)
        sessionE.config(state="readonly")
        #===============Checking for uniqueness============================
        if preREG==newREG and preROLL==newROLL and preFNAME==newFNAME and preLNAME==newLNAME and newPHOTO==photoPathEntry.get() and preSESSION==newSESSION and preADDRESS==newADDRESS:
            #Nothing has changed!!!
            messagebox.showwarning("WARNING!!!", "The Data Is Already In The Database!!!")
        else:
            #user has changed something
            conn=sqlite3.connect("database\StudentDetails.db")
            c=conn.cursor()
            record_id=KEY
            c.execute("""UPDATE details SET
            regNumber= :Regnumber,   
            rollNumber= :Rollnumber,
            fName= :Fname,
            lName= :Lname,
            photoPath= :Photopath,
            session= :Session,
            address= :Address
            WHERE oid= :oid""",
            {
                'Regnumber': newREG,
                'Rollnumber' : newROLL,
                'Fname':newFNAME,
                'Lname':newLNAME,
                'Photopath':newPHOTO,
                'Session':newSESSION,
                'Address':newADDRESS,

                'oid':record_id
            })
            conn.commit()
            conn.close()
            image.save(newPHOTO)
            if newPHOTO!=prePHOTO:
                os.remove(prePHOTO)
            KEY, PermissionForUpdateOrDelete=-1, "Denied"
            messagebox.showinfo("SUCCESSFULLY UPDATED!!!", "Your Data Is Been Successfully Updated!!!")
            resetClicked(root, regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr, sessionE, addressE, display, tEntityE)
    else:
        messagebox.showwarning("WARNING!!!", "Please Specify The Data By Clicking The Display Button")

def deleteClicked(root, regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr,sessionE, addressE, display, tEntityE):
    global KEY, PermissionForUpdateOrDelete
    if PermissionForUpdateOrDelete=="Granted":
        responce=messagebox.askyesno("Are You Sure?","Delete It?")
        if responce==1:
            conn=sqlite3.connect("database\StudentDetails.db")
            c=conn.cursor()
            c.execute("SELECT *, oid FROM details")
            records=c.fetchall()
            for record in records:
                if record[7]==KEY:
                    photoPath=record[4]
                    os.remove(photoPath)
                    break
            conn.commit()
            conn.close()
            
            conn=sqlite3.connect("database\StudentDetails.db")
            c=conn.cursor()
            c.execute("DELETE from details WHERE oid=" + str(KEY))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("DELETED!!!", "Successfully Deleted!!!")
            KEY=-1
            PermissionForUpdateOrDelete="Denied"
            resetClicked(root, regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr, sessionE, addressE, display, tEntityE)
    else:
        messagebox.showwarning("WARNING!!!", "Please Specify The Data By Clicking The Display Button")

def searchClicked(root, regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr,sessionE, addressE, display, tEntityE):
    userGivenInfo=[]
    if regE.get().strip()!="":
        userGivenInfo.append(regE.get().strip())
    else:
        userGivenInfo.append("NaN")
    if rollE.get().strip()!="":
        userGivenInfo.append(rollE.get().strip())
    else:
        userGivenInfo.append("NaN")
    if fnameE.get().strip()!="":
        userGivenInfo.append(fnameE.get().strip())
    else:
        userGivenInfo.append("NaN")
    if lnameE.get().strip()!="":
        userGivenInfo.append(lnameE.get().strip())
    else:
        userGivenInfo.append("NaN")
    photoPathEntry.config(state=NORMAL)
    if photoPathEntry.get()!="126px x 126px png":
        userGivenInfo.append(photoPathEntry.get())
    else:
        userGivenInfo.append("NaN")
    photoPathEntry.config(state=DISABLED)
    sessionE.config(state="normal")
    sessionInfo=sessionE.get()
    sessionE.config(state="readonly")
    userGivenInfo.append(sessionInfo)
    if addressE.get().strip()!="":
        userGivenInfo.append(addressE.get().strip())
    else:
        userGivenInfo.append("NaN")
    conn=sqlite3.connect("database\StudentDetails.db")
    c=conn.cursor()
    c.execute("SELECT *, oid FROM details")
    records=c.fetchall()
    finalIDs=[]
    for record in records:
        for i in range(7):
            if userGivenInfo[i]!="NaN":
                if userGivenInfo[i]!=record[i]:
                    break
                else:
                    pass
        else:
            finalIDs.append(record[7])
    conn.commit()
    conn.close()
    if len(finalIDs)==0:
        messagebox.showwarning("WARNING!!!", "No Such Parameter Is In The Dataset!!!")
        resetClicked(root, regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr, sessionE, addressE, display, tEntityE)
    else:
        conn=sqlite3.connect("database\StudentDetails.db")
        c=conn.cursor()
        c.execute("SELECT *, oid FROM details")
        records=c.fetchall()
        finalTexts=[]
        lineNumber=1
        for eachID in finalIDs:
            for record in records:
                if eachID==record[7]:
                    text=str(lineNumber)+"     "+record[0]+"     "+record[1]+"     "+record[2]+"_"+record[3]+"     "+record[5]+"     "+record[6]+"     "+record[4]+"     "+str(record[7])
                    finalTexts.append(text)
                    lineNumber+=1
                    break
        while display.get(0)!="":
            display.delete(0)
        lineCount=1
        for eachText in finalTexts:
            display.insert(lineCount, eachText)
            lineCount+=1
        conn.commit()
        conn.close()

def displayClicked(root, regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr,sessionE, addressE, display, tEntityE):
    global KEY, PermissionForUpdateOrDelete
    try:
        lineID=display.curselection()[0]
        tempText=display.get(lineID).split()
        mainID=int(tempText[-1])
        KEY=mainID
        resetClicked(root, regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr, sessionE, addressE, display, tEntityE)

        conn=sqlite3.connect("database\StudentDetails.db")
        c=conn.cursor()
        c.execute("SELECT *, oid FROM details")
        records=c.fetchall()
        for record in records:
            if record[7]==KEY:
                regE.insert(0, record[0])
                rollE.insert(0, record[1])
                fnameE.insert(0, record[2])
                lnameE.insert(0, record[3])
                photoPathEntry.config(state=NORMAL)
                photoPathEntry.delete(0, END)
                photoPathEntry.insert(0, record[4])
                photoPathEntry.config(state=DISABLED)
                sessionE.config(state="normal")
                sessionE.delete(0, END)
                sessionE.insert(0, record[5])
                sessionE.config(state="readonly")
                addressE.insert(0, record[6])
                PermissionForUpdateOrDelete="Granted"
                conn.commit()
                conn.close()
                break
        
    except:
        messagebox.showwarning("WARNING!!!", "Please Select A Line From The Existing Dataset!!!")
    
def addClicked(root, regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr, variable, sessionE, addressE, tEntityE, display):
    sessionE.config(state="normal")
    result=sessionE.get()
    sessionE.config(state="readonly")
    if  result=="NaN":
        messagebox.showerror("ERROR!!!", "Please Enter A Valid Session")
    else:
        if regE.get().strip()!="" and rollE.get().strip()!="" and fnameE.get().strip()!="" and lnameE.get().strip()!="" and addressE.get().strip()!="":
            if ("-" not in addressE.get().strip()) and ("/" not in addressE.get().strip()) and ('\\' not in addressE.get().strip()):
                try:
                    conn=sqlite3.connect("database\StudentDetails.db")
                    c=conn.cursor()
                    c.execute("SELECT *, oid FROM details")
                    records=c.fetchall()
                    if len(records)==0:
                        realSession=variable.get()
                        reelSession=realSession[:4]+"-"+realSession[5:]
                        image = Image.open(photoPathEntry.get())
                        reelAddress=addressE.get().strip().split()
                        finalReelAddress=""
                        for i in range(len(reelAddress)):
                            finalReelAddress+=reelAddress[i]
                            if i!=len(reelAddress)-1:
                                finalReelAddress+="-"
                        path="database\{}_{}_{}{}_{}_{}.png".format(regE.get().strip(),
                                                                          rollE.get().strip(),
                                                                          fnameE.get().strip(),
                                                                          lnameE.get().strip(),
                                                                          reelSession,
                                                                          finalReelAddress
                                                                          )
                        image.save(path)
                        c.execute("INSERT INTO details VALUES (:regNumber, :rollNumber, :fName, :lName, :photoPath, :session, :address)",
                                {
                                'regNumber':regE.get().strip(),
                                'rollNumber':rollE.get().strip(),
                                'fName':fnameE.get().strip(),
                                'lName':lnameE.get().strip(),
                                'photoPath':path,
                                'session':variable.get(),
                                'address':addressE.get().strip()
                                }
                          )
                        messagebox.showinfo("SUCCESSFULLY ADDED!!!", "The Data Is Successfully Added To The Database!!!")
                        conn.commit()
                        conn.close()
                        tEntityE.config(state=NORMAL)
                        tEntityE.delete(0, END)
                        tEntityE.config(state=DISABLED)
                        
                        regE.delete(0, END)
                        rollE.delete(0, END)
                        fnameE.delete(0, END)
                        lnameE.delete(0, END)
                        photoPathEntry.config(state=NORMAL)
                        photoPathEntry.delete(0, END)
                        photoPathEntry.insert(0, "126px x 126px png")
                        photoPathEntry.config(state=DISABLED)
                        sessionE.config(state="normal")
                        sessionE.current(4)
                        sessionE.config(state="readonly")
                        addressE.delete(0, END)
                    else:
                        for record in records:
                            if record[0]==regE.get().strip() and record[1]==rollE.get().strip() and record[2]==fnameE.get().strip() and record[3]==lnameE.get().strip() and record[5]==variable.get() and record[6]==addressE.get().strip():
                                messagebox.showerror("ERROR!!!", "The Data Is Already In The Database!!!")
                                conn.commit()
                                conn.close()
                                break
                        else:
                            realSession=variable.get()
                            reelSession=realSession[:4]+"-"+realSession[5:]
                            image = Image.open(photoPathEntry.get())
                            reelAddress=addressE.get().strip().split()
                            finalReelAddress=""
                            for i in range(len(reelAddress)):
                                finalReelAddress+=reelAddress[i]
                                if i!=len(reelAddress)-1:
                                    finalReelAddress+="-"
                            path="database\{}_{}_{}{}_{}_{}.png".format(regE.get().strip(),
                                                                              rollE.get().strip(),
                                                                              fnameE.get().strip(),
                                                                              lnameE.get().strip(),
                                                                              reelSession,
                                                                              finalReelAddress
                                                                              )
                            image.save(path)
                            c.execute("INSERT INTO details VALUES (:regNumber, :rollNumber, :fName, :lName, :photoPath, :session, :address)",
                                    {
                                    'regNumber':regE.get().strip(),
                                    'rollNumber':rollE.get().strip(),
                                    'fName':fnameE.get().strip(),
                                    'lName':lnameE.get().strip(),
                                    'photoPath':path,
                                    'session':variable.get(),
                                    'address':addressE.get().strip()
                                    }
                              )
                            messagebox.showinfo("SUCCESSFULLY ADDED!!!", "The Data Is Successfully Added To The Database!!!")
                            tEntityE.config(state=NORMAL)
                            tEntityE.delete(0, END)
                            tEntityE.config(state=DISABLED)
                            conn.commit()
                            conn.close()
                        regE.delete(0, END)
                        rollE.delete(0, END)
                        fnameE.delete(0, END)
                        lnameE.delete(0, END)
                        photoPathEntry.config(state=NORMAL)
                        photoPathEntry.delete(0, END)
                        photoPathEntry.insert(0, "126px x 126px png")
                        photoPathEntry.config(state=DISABLED)
                        sessionE.config(state="normal")
                        sessionE.current(4)
                        sessionE.config(state="readonly")
                        addressE.delete(0, END)
                except:
                    messagebox.showerror("ERROR!!!", "Please Provide A 126px X 126px Photo!!!")
            else:
                messagebox.showwarning("WARNING!!!", "Please Provide The Address Without Any Hyphen ('-') Or Slash ('/') Or Backslash ('\\') Symbols!!!")
        else:
            messagebox.showerror("ERROR!!!", "Please provide all the Information!!!")
        conn=sqlite3.connect("database\StudentDetails.db")
        c=conn.cursor()
        c.execute("SELECT *, oid FROM details")
        records=c.fetchall()
        tEntityE.config(state=NORMAL)
        tEntityE.delete(0, END)
        tEntityE.insert(0, str(len(records)))
        tEntityE.config(state=DISABLED)
        conn.commit()
        conn.close()
        #########################LISTBOX##########################
        conn=sqlite3.connect("database\StudentDetails.db")
        c=conn.cursor()
        c.execute("SELECT *, oid FROM details")
        records=c.fetchall()
        alreadyText=display.get(0)
        while display.get(0)!="":
            display.delete(0)
        lineCount=1
        for record in records:
            reelAddress=record[6].split()
            finalReelAddress=""
            for i in range(len(reelAddress)):
                finalReelAddress+=reelAddress[i]
                if i!=len(reelAddress)-1:
                    finalReelAddress+="-"
            finalText=str(lineCount)+"     "+record[0]+"     "+record[1]+"     "+record[2]+"_"+record[3]+"     "+record[5]+"     "+finalReelAddress+"     "+record[4]+"     "+str(record[7])
            display.insert(lineCount, finalText)
            lineCount+=1
        conn.commit()
        conn.close()

def resetClicked(root, regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr, sessionE, addressE, display, tEntityE):
    if regE.get().strip()!="":
        regE.delete(0, END)
    if rollE.get().strip()!="":
        rollE.delete(0, END)
    if fnameE.get().strip()!="":
        fnameE.delete(0, END)
    if lnameE.get().strip()!="":
        lnameE.delete(0, END)
    photoPathEntry.config(state=NORMAL)
    photoPathEntry.delete(0, END)
    photoPathEntry.insert(0, "126px x 126px png")
    photoPathEntry.config(state=DISABLED)
    sessionE.config(state="normal")
    sessionE.current(4)
    sessionE.config(state="readonly")
    if addressE.get().strip()!="":
        addressE.delete(0, END)
    conn=sqlite3.connect("database\StudentDetails.db")
    c=conn.cursor()
    c.execute("SELECT *, oid FROM details")
    records=c.fetchall()
    while display.get(0)!="":
            display.delete(0)
    lineCount=1
    for record in records:
        reelAddress=record[6].split()
        finalReelAddress=""
        for i in range(len(reelAddress)):
            finalReelAddress+=reelAddress[i]
            if i!=len(reelAddress)-1:
                finalReelAddress+="-"
        finalText=str(lineCount)+"     "+record[0]+"     "+record[1]+"     "+record[2]+"_"+record[3]+"     "+record[5]+"     "+finalReelAddress+"     "+record[4]+"     "+str(record[7])
        display.insert(lineCount, finalText)
        lineCount+=1
    tEntityE.config(state=NORMAL)
    tEntityE.delete(0, END)
    tEntityE.insert(0, str(len(records)))
    tEntityE.config(state=DISABLED)
    conn.commit()
    conn.close()

def browseButtonClicked(root, photoPathEntry):
    currentDir=os.getcwd()
    root.filename=filedialog.askopenfilename(initialdir=currentDir, title="Select a 126x126 png file", filetypes=(("png files","*.png"),("all files","*.*")))
    try:
        image = Image.open(root.filename)
        width, height = image.size
        if root.filename.endswith(".png") and width==126 and height==126:
            photoPathEntry.config(state=NORMAL)
            photoPathEntry.delete(0, END)
            photoPathEntry.insert(0, root.filename)
            photoPathEntry.config(state=DISABLED)
        else:
            messagebox.showerror("ERROR!!!", "Please select a PNG file of size 126px x 126px")
            photoPathEntry.config(state=NORMAL)
            photoPathEntry.delete(0, END)
            photoPathEntry.insert(0, "126px x 126px png")
            photoPathEntry.config(state=DISABLED)
    except:
        photoPathEntry.config(state=NORMAL)
        result=photoPathEntry.get()
        if result=="126px x 126px png":
            if not(root.filename.endswith(".png")) and len(root.filename)!=0:
                messagebox.showerror("ERROR!!!", "Please select a PNG file of size 126px x 126px")
                photoPathEntry.config(state=DISABLED)
            else:
                photoPathEntry.config(state=DISABLED)
                photoPathEntry.config(state=NORMAL)
                photoPathEntry.delete(0, END)
                photoPathEntry.insert(0, "126px x 126px png")
                photoPathEntry.config(state=DISABLED)
        else:
            try:
                prevPath=photoPathEntry.get()
                image = Image.open(prevPath)
                if not(root.filename.endswith(".png")) and len(root.filename)!=0:
                    messagebox.showerror("ERROR!!!", "Please select a PNG file of size 126px x 126px")
            except:
                messagebox.showerror("ERROR!!!", "Please select a PNG file of size 126px x 126px")
        photoPathEntry.config(state=DISABLED)

def exitClicked(root):
    result=messagebox.askquestion("EXIT!!!", "Are you want to exit???")
    if result=="yes":
        root.destroy()

def main():
    root=Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),root.winfo_screenheight()))
    root.title("STUDENTS' REGISTRATION SYSTEM")
    root.config(bg="cadet blue")
    root.iconbitmap("images\icon.ico")
    
    conn=sqlite3.connect("database\StudentDetails.db")
    c=conn.cursor()
    '''
    c.execute("""CREATE TABLE details(
                regNumber text,
                rollNumber text,
                fName text,
                lName text,
                photoPath text,
                session text,
                address text
                )""")
    '''
    conn.commit()
    conn.close()
    #===========================================top frame========================================
    topFrame=LabelFrame(root, bg="cadet blue")
    topFrame.pack(side=TOP, pady=(20,0))
    label=Label(topFrame,
                text="STUDENTS'  REGISTRATION  SYSTEM",
                font=("arial b", 30), bg="cadet blue")
    label.pack(padx=20)
    #============================================middle frame======================================
    mFrame=Frame(root, bg="cadet blue")
    mFrame.pack(pady=30)
    #=============================================middle left========================================
    inputFrame=Frame(mFrame, bg="cadet blue")
    inputFrame.pack(side=LEFT, pady=(10,0))
    reg=Label(inputFrame, text="REG. NO   ", font=("arial b", 30), bg="cadet blue").grid(row=0, column=0)
    roll=Label(inputFrame, text="ROLL NO   ", font=("arial b", 30), bg="cadet blue").grid(row=1, column=0, pady=(20,0))
    fname=Label(inputFrame, text="FIRST NAME   ", font=("arial b", 30), bg="cadet blue").grid(row=2, column=0, pady=(20,0))
    lname=Label(inputFrame, text="LAST NAME   ", font=("arial b", 30), bg="cadet blue").grid(row=3, column=0, pady=(20,0))
    photo=Label(inputFrame, text="PHOTO   ", font=("arial b", 30), bg="cadet blue").grid(row=4, column=0, pady=(20,0))
    session=Label(inputFrame, text="SESSION   ", font=("arial b", 30), bg="cadet blue").grid(row=5, column=0, pady=(20,0))
    address=Label(inputFrame, text="ADDRESS   ", font=("arial b", 30), bg="cadet blue").grid(row=6, column=0, pady=(20,0))
    regE=Entry(inputFrame, font=("arial", 25))
    regE.focus_set()
    regE.grid(row=0, column=1)
    rollE=Entry(inputFrame, font=("arial", 25))
    rollE.grid(row=1, column=1, pady=(20,0))
    fnameE=Entry(inputFrame, font=("arial", 25))
    fnameE.grid(row=2, column=1, pady=(20,0))
    lnameE=Entry(inputFrame, font=("arial", 25))
    lnameE.grid(row=3, column=1, pady=(20,0))
    pEntryFrame=Frame(inputFrame, bg="cadet blue")
    pEntryFrame.grid(row=4, column=1, pady=(20,0))
    photoPathEntry=Entry(pEntryFrame, font=("arial", 25), width=15)
    photoPathEntry.insert(0, "126px x 126px png")
    photoPathEntry.config(state=DISABLED)
    photoPathEntry.pack(side=LEFT)
    browseB=Button(pEntryFrame, text="Browse", font=("Courier b", 16), bg="#a3a8a7", cursor="hand2",
                   command=lambda:browseButtonClicked(root, photoPathEntry))
    browseB.pack(side=RIGHT)
    now=datetime.datetime.now()
    currentYear=now.year
    firstAttr=[str(currentYear-4),
               str(currentYear-3),
               str(currentYear-2),
               str(currentYear-1),
               str(currentYear)]
    lastAttr=[]
    for i in range(len(firstAttr)):
        lastAttr.append(str(int(firstAttr[i][2:])+1))
    finalAttr=[]
    for i in range(len(firstAttr)):
        finalAttr.append(firstAttr[i]+'/'+lastAttr[i])
    finalAttr.append("NaN") #should not be selected while adding data
    variable = StringVar()
    sessionE = ttk.Combobox(inputFrame,
                     state="readonly",
                     font=("arial", 25),
                     textvariable=variable,
                     values=finalAttr,
                     width=19)
    sessionE.current(4) 
    sessionE.grid(row=5, column=1, pady=(20,0))
    addressE=Entry(inputFrame, font=("arial", 25))
    addressE.grid(row=6, column=1, pady=(20,0))
    #===========================================middle right=======================================
    displayFrame=Frame(mFrame, bg="cadet blue")
    displayFrame.pack(side=RIGHT, pady=(10,0), padx=(50,0))
    tEntity=Label(displayFrame, text="TOTAL ENTITIES", font=("arial b", 30), bg="cadet blue").grid(row=0, column=0)
    tEntityE=Entry(displayFrame, font=("arial", 25), width=3)
    conn=sqlite3.connect("database\StudentDetails.db")
    c=conn.cursor()
    c.execute("SELECT *, oid FROM details")
    records=c.fetchall()
    tEntityE.config(state=NORMAL)
    tEntityE.insert(0 ,str(len(records)))
    tEntityE.config(state=DISABLED)
    tEntityE.grid(row=0, column=1)
    conn.commit()
    conn.close()
    textFrame=Frame(displayFrame, bg="cadet blue")
    textFrame.grid(row=1,column=0, columnspan=2, pady=(20,0))
    yscrollbar = Scrollbar(textFrame)
    yscrollbar.pack(side=RIGHT, fill=Y, pady=(9,0))
    #============================================LISTBOX============================================
    display=Listbox(textFrame,
                 font=("Courier b", 15),
            yscrollcommand=yscrollbar.set,
                    width=51, height=16
                 )
    display.pack(pady=(9,0))
    yscrollbar.config(command=display.yview)
    conn=sqlite3.connect("database\StudentDetails.db")
    c=conn.cursor()
    c.execute("SELECT *, oid FROM details")
    records=c.fetchall()
    lineCount=1
    for record in records:
        reelAddress=record[6].split()
        finalReelAddress=""
        for i in range(len(reelAddress)):
            finalReelAddress+=reelAddress[i]
            if i!=len(reelAddress)-1:
                finalReelAddress+="-"
        finalText=str(lineCount)+"     "+record[0]+"     "+record[1]+"     "+record[2]+"_"+record[3]+"     "+record[5]+"     "+finalReelAddress+"     "+record[4]+"     "+str(record[7])
        display.insert(lineCount, finalText)
        lineCount+=1
    conn.commit()
    conn.close()
   #=========================================lower frame====================================
    LFrame=Frame(root, bg="cadet blue")
    LFrame.pack()
    
    resetB=Button(LFrame, text="RESET", font=("Courier b", 20), bg="#01e779", cursor="hand2",
                  command=lambda:resetClicked(root,
                                              regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr, sessionE, addressE, display,
                                              tEntityE
                                              )).grid(row=0,column=0)
    
    addB=Button(LFrame, text="ADD", font=("Courier b", 20), bg="#0183f8", cursor="hand2",
                command=lambda:addClicked(root,
                                          regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr, variable, sessionE, addressE,
                                          tEntityE, display
                                          )).grid(row=0,column=1, padx=(25,0))

    displayB=Button(LFrame, text="DISPLAY", font=("Courier b", 20), bg="#a3a8a7", cursor="hand2",
                   command=lambda:displayClicked(root,
                                                 regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr,sessionE, addressE, display,
                                                 tEntityE
                                                 )).grid(row=0,column=2, padx=(25,0))
    
    searchB=Button(LFrame, text="SEARCH", font=("Courier b", 20), bg="#b69444", cursor="hand2",
                   command=lambda:searchClicked(root,
                                                regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr,sessionE, addressE, display,
                                                tEntityE
                                                )).grid(row=0,column=3, padx=(25,0))
    
    updateB=Button(LFrame, text="UPDATE", font=("Courier b", 20), bg="yellow", cursor="hand2",
                   command=lambda:updateClicked(root,
                                                regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr,sessionE, addressE, display,
                                                tEntityE, variable
                                                )).grid(row=0,column=4, padx=(25,0))
    
    deleteB=Button(LFrame, text="DELETE", font=("Courier b", 20), bg="#7cd0ba", cursor="hand2",
                   command=lambda:deleteClicked(root,
                                                regE, rollE, fnameE, lnameE, photoPathEntry, finalAttr,sessionE, addressE, display,
                                                tEntityE
                                                )).grid(row=0,column=5, padx=(25,0))
    
    regCardB=Button(LFrame, text="GENERATE REG. CARD", font=("Courier b", 20), bg="#c873b6", cursor="hand2",
                    command=lambda:regCardClicked(root)).grid(row=0,column=6, padx=(25,0))
    
    exitB=Button(LFrame, text="EXIT", font=("Courier b", 20), bg="#e36753", cursor="hand2",
                 command=lambda:exitClicked(root)).grid(row=0,column=7, padx=(25,0))
    
    root.mainloop()

if __name__=="__main__":
    main()
