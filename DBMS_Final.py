from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import messagebox
from matplotlib import pyplot as pyp
import random
from datetime import datetime
import Database

def ctransac(cu,fracc, toacc, trtyp, amt):
    id = random.randint(1000, 2000)
    x = datetime.now()
    dat = str(x.strftime('%Y-%m-%d'))
    tim = x.time()
    Database.cursor.execute(
        '''INSERT INTO TRANSACTIONS(TR_ID,C_ID,FRM_ACC,TO_ACC,TR_TYPE,AMT,DT,TM) VALUES(%s,%s,%s,%s,'%s',%s,'%s','%s')''' % (id, cu, fracc, toacc, trtyp, amt, dat, tim))
    Database.dbase.commit()

def customer(cu1):
    c_name = Database.cursor.execute('''SELECT C_NAME FROM CUSTOMER WHERE C_ID=?''', (cu1,))
    for i in c_name:
        cname = i[0]

    c_acc = Database.cursor.execute('''SELECT C_ACCNO FROM CUSTOMER WHERE C_ID=?''', (cu1,))
    for j in c_acc:
        cacc = j[0]

    window2 = Tk()
    window2.title("Customer Page")
    window2.configure(background='pink')
    window2.geometry('1500x700')

    frame5 = Frame(window2, bg='blue')
    frame5.place(relx=0, rely=0, relwidth=1, relheight=0.34)
    frame6 = Frame(window2, bg='blue')
    frame6.place(relx=0, rely=0.34, relwidth=0.2, relheight=0.66)

    load = Image.open(r"D:\Study Stuff\College\4th Sem\Projects\DBMS-Python\Main files\logo2.jpg")
    photo = ImageTk.PhotoImage(load)
    img = Label(window2, image=photo)
    img.image = photo
    img.place(x=340, y=-2)

    frame = Frame(window2, bg='white')
    frame.place(relx=0.19, rely=0, relwidth=0.06, relheight=0.211)
    frame2 = Frame(window2, bg='white')
    frame2.place(relx=0.75, rely=0, relwidth=0.06, relheight=0.211)

    accn = StringVar()
    amt = StringVar()

    def transfer():
        comp.place_forget()

        taccn = accn.get()
        tamt = amt.get()

        if accn.get() == "" and amt.get() == "":
            messagebox.showerror("Error", "Enter Account Number and Amount!")
        elif accn.get() == "":
            messagebox.showerror("Error", "Enter Account Number!")
        elif amt.get() == "":
            messagebox.showerror("Error", "Enter Amount!")

        else:
            frm = Database.cursor.execute('''SELECT C_ACCNO FROM Customer WHERE C_ID=?''', (cu1,))
            for p in frm:
                frmacc = p[0]

            if int(taccn)==int(frmacc):
                messagebox.showerror("Error", "Enter a different account number!")
            else:
                tbal = Database.cursor.execute('''SELECT C_ACCBAL FROM CUSTOMER WHERE C_ID=?''', (cu1,))

                for k in tbal:
                    bal = k[0]
                balance = bal - int(tamt)

                if balance <= 0:
                    messagebox.showerror("Error", "Insufficient balance!")
                else:
                    Database.cursor.execute('''UPDATE CUSTOMER SET C_ACCBAL=? WHERE C_ID=?''', (balance, cu1,))

                    tbal2 = Database.cursor.execute('''SELECT C_ACCBAL FROM CUSTOMER WHERE C_ACCNO=?''', (taccn,))
                    flag = 0

                    for l in tbal2:
                        flag = 1
                        bal2 = l[0]

                    if flag == 1:
                        balance2 = bal2 + int(tamt)
                        Database.cursor.execute('''UPDATE CUSTOMER SET C_ACCBAL=? WHERE C_ACCNO=?''', (balance2, taccn,))

                    comp.place(x=535, y=525)
                    Database.dbase.commit()

                    st1 = 'Fund Transfer  '
                    ctransac(cu1,frmacc, taccn, st1, tamt)

    frmdat = StringVar()
    todat = StringVar()

    def gt_st():
        if frmdat.get() == "" or todat.get() == "":
            messagebox.showerror("Error", "Enter date first!")
            statement()
        else:
            frame7.place_forget()
            frame8.place_forget()
            frame9.place_forget()
            frame14.place_forget()
            frame16.place_forget()
            frame17.place_forget()
            frame18.place_forget()
            list.delete(0,END)
            list.place_forget()

            frame15.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

            scrbar.pack(side=RIGHT, fill=Y)
            scrbar.config(command=list.yview)

            tl1 = Label(frame15, text="TR ID", font=("Times New Roman", 9), width=11, height=3)
            tl1.place(x=25, y=20)
            tl2 = Label(frame15, text="FROM ACCOUNT", font=("Times New Roman", 9), width=14, height=3)
            tl2.place(x=170, y=20)
            tl3 = Label(frame15, text="TO ACCOUNT", font=("Times New Roman", 9), width=14, height=3)
            tl3.place(x=325, y=20)
            tl4 = Label(frame15, text="TR TYPE", font=("Times New Roman", 9), width=14, height=3)
            tl4.place(x=450, y=20)
            tl5 = Label(frame15, text="AMOUNT", font=("Times New Roman", 9), width=11, height=3)
            tl5.place(x=645, y=20)
            tl6 = Label(frame15, text="DATE", font=("Times New Roman", 9), width=11, height=3)
            tl6.place(x=825, y=20)

            frmdat1 = frmdat.get()
            todat1 = todat.get()
            frm2 = Database.cursor.execute('''SELECT C_ACCNO FROM Customer WHERE C_ID=?''', (cu1,))

            for r in frm2:
                frmaccn = r[0]

            stment=Database.cursor.execute('''SELECT * FROM TRANSACTIONS WHERE TR_ID IN (SELECT TR_ID FROM TRANSACTIONS WHERE FRM_ACC=? OR TO_ACC=?) AND DT BETWEEN '%s' AND '%s' ''' % (frmdat1,todat1),(frmaccn,frmaccn) )

            for s in stment:
                trid = s[0]
                frmacc = s[3]
                if str(frmacc)=='None':
                    frmacc='       None'
                toacc = s[4]
                if str(toacc)=='None':
                    toacc='       None'
                trtyp = s[5]
                amt = str(s[6])
                amt=amt.rjust(8,'0')
                dat = s[7]

                list.insert(END,"    " +str(trid)+"               " + str(frmacc)+"         " + str(toacc)+"        " + str(trtyp)+"           " + amt+"             " + str(dat))
                list.place(x=20, y=80)

    frame7 = Frame(window2, bg='pink')
    frame8 = Frame(window2, bg='pink')
    frame9 = Frame(window2, bg='pink')
    frame14 = Frame(window2, bg='pink')
    frame15 = Frame(window2, bg='pink')
    frame16 = Frame(window2, bg='pink')
    frame17 = Frame(window2, bg='pink')
    frame18 = Frame(window2, bg='pink')

    scrbar = Scrollbar(frame15)
    list = Listbox(frame15, yscrollcommand=scrbar.set, font=("Arial", 15), width=85, height=15)
    comp = Label(window2, text="Fund Successfully Transfered", font=("Times New Roman", 18), width=30, height=2)

    def funds():
        frame8.place_forget()
        frame9.place_forget()
        frame14.place_forget()
        frame15.place_forget()
        frame16.place_forget()
        frame17.place_forget()
        frame18.place_forget()

        comp.place_forget()

        frame7.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        f1 = Label(frame7, text="Transfer to account:", font=("Times New Roman", 18), width=15, height=2)
        f1.place(x=240, y=50)
        txtf1 = Entry(frame7, textvariable=accn, font=("Times New Roman", 18))
        txtf1.place(x=490, y=55, width=250, height=50)
        f2 = Label(frame7, text="Amount:", font=("Times New Roman", 18), width=15, height=2)
        f2.place(x=240, y=130)
        txtf2 = Entry(frame7, textvariable=amt, font=("Times New Roman", 18))
        txtf2.place(x=490, y=130, width=250, height=50)
        btf3 = Button(frame7, text="Proceed transfer", font=("Times New Roman", 15), width=15, height=1, command=transfer)
        btf3.place(x=525, y=210)

    def check_bal():
        frame7.place_forget()
        frame9.place_forget()
        frame14.place_forget()
        frame15.place_forget()
        frame16.place_forget()
        frame17.place_forget()
        frame18.place_forget()

        comp.place_forget()

        frame8.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        balval = Database.cursor.execute('''SELECT C_ACCBAL FROM CUSTOMER WHERE C_ID=?''', (cu1,))
        for m in balval:
            balvalue = m[0]

        cb1 = Label(frame8, text="Account balance is", font=("Times New Roman", 18), width=15, height=2)
        cb1.place(x=240, y=50)
        txtcb1 = Label(frame8, font=("Times New Roman", 18), width=15, height=2)
        txtcb1.place(x=490, y=55, width=250, height=50)
        txtcb1.configure(text=balvalue)

    def statement():
        frame7.place_forget()
        frame8.place_forget()
        frame14.place_forget()
        frame15.place_forget()
        frame16.place_forget()
        frame17.place_forget()
        frame18.place_forget()

        comp.place_forget()

        frame9.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        s1 = Label(frame9, text="From date:", font=("Times New Roman", 18), width=15, height=2)
        s1.place(x=240, y=50)
        txts1 = Entry(frame9, textvariable=frmdat, font=("Times New Roman", 18))
        txts1.place(x=490, y=55, width=250, height=50)
        s2 = Label(frame9, text="To date:", font=("Times New Roman", 18), width=15, height=2)
        s2.place(x=240, y=130)
        txts2 = Entry(frame9, textvariable=todat, font=("Times New Roman", 18))
        txts2.place(x=490, y=130, width=250, height=50)
        bts3 = Button(frame9, text="Get statement", font=("Times New Roman", 15), width=15, height=1, command=gt_st)
        bts3.place(x=525, y=210)

    def loan_transfer():
        lnid = random.randint(4000, 5000)
        ltype = n.get()
        ltime = int(m.get())
        lamt = int(amt1.get())

        interest = (lamt * 0.1 * ltime)
        finalamt = lamt + interest

        Database.cursor.execute('''INSERT INTO LOAN VALUES(?,?,?,?,10,?,?)''',(lnid,ltype,cu1, ltime,lamt,finalamt,))
        comp2 = Label(frame17, text="Loan Submitted Successfully", font=("Times New Roman", 18), width=30, height=2)
        comp2.place(x=300, y=300)
        Database.dbase.commit()

    def loans():
        frame7.place_forget()
        frame8.place_forget()
        frame9.place_forget()
        frame14.place_forget()
        frame15.place_forget()
        frame17.place_forget()
        frame18.place_forget()

        comp.place_forget()

        frame16.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        bt40 = Button(frame16, text="Loan Details", font=("Times New Roman", 30), width=16, height=2,command= current_loan)
        bt40.place(x=120, y=80)
        bt41 = Button(frame16, text="Apply Loan", font=("Times New Roman", 30), width=16, height=2,command=apply_loan)
        bt41.place(x=590, y=80)

    def apply_loan():
        frame7.place_forget()
        frame8.place_forget()
        frame9.place_forget()
        frame14.place_forget()
        frame15.place_forget()
        frame16.place_forget()
        frame18.place_forget()

        frame17.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        ttk.Label(frame17, text="Select the Loan Type :",font=("Times New Roman", 18)).grid(column=240, row=50, padx=2, pady=25)
        loanchosen = ttk.Combobox(frame17, width=40, textvariable=n)
        loanchosen['values'] = ('Home Loan','Education Loan','Car Loan','Gold Loan','Personal Loan')
        loanchosen.grid(column=250, row=50, padx=2, pady=25)
        loanchosen.current()

        ttk.Label(frame17, text="Select the Loan Time :",font=("Times New Roman", 18)).grid(column=240, row=60, padx=2, pady=25)
        timechosen = ttk.Combobox(frame17, width=40, textvariable=m)
        timechosen['values'] = ('2','5','7','10',)
        timechosen.grid(column=250, row=60, padx=2, pady=25)
        timechosen.current()

        f27 = Label(frame17, text="Amount:", font=("Times New Roman", 18), width=10, height=1)
        f27.place(x=0, y=188)
        txtf27 = Entry(frame17, textvariable=amt1, font=("Times New Roman", 18))
        txtf27.place(x=150, y=188, width=200, height=30)

        btf37 = Button(frame17, text="Submit", font=("Times New Roman", 15), width=15, height=1, command=loan_transfer)
        btf37.place(x=100, y=270)

    amt1 = StringVar()
    n = tk.StringVar()
    m = tk.StringVar()

    def current_loan():
        frame7.place_forget()
        frame8.place_forget()
        frame9.place_forget()
        frame14.place_forget()
        frame15.place_forget()
        frame16.place_forget()
        frame17.place_forget()
        list1.delete(0, END)
        list1.place_forget()

        frame18.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        scrbar1.pack(side=RIGHT, fill=Y)
        scrbar1.config(command=list1.yview)

        a1 = Label(frame18, text="Loan id", font=("Times New Roman", 12), width=12, height=2)
        a1.place(x=25, y=20)
        a2 = Label(frame18, text="Loan Type", font=("Times New Roman", 12), width=12, height=2)
        a2.place(x=160, y=20)
        a3 = Label(frame18, text="Years", font=("Times New Roman", 11), width=8, height=2)
        a3.place(x=285, y=20)
        a4 = Label(frame18, text="ROI", font=("Times New Roman", 11), width=8, height=2)
        a4.place(x=363, y=20)
        a5 = Label(frame18, text="Amount", font=("Times New Roman", 12), width=12, height=2)
        a5.place(x=443, y=20)
        a6 = Label(frame18, text="Final Amount", font=("Times New Roman", 12), width=12, height=2)
        a6.place(x=605, y=20)

        stment2 = Database.cursor.execute('''SELECT * FROM LOAN WHERE C_ID =?  ''' , (cu1,))

        for s in stment2:
            loanid = s[0]
            loantype = s[1]
            loantime3 = s[3]
            interestrate = s[4]
            amt10 = s[5]
            final = s[6]

            list1.insert(END, "    " + str(loanid) + "               " + str(loantype) + "         " + str(loantime3) + "        " + str(interestrate) + "           " + str(amt10) + "             " + str(final))
            list1.place(x=20, y=80)

    scrbar1 = Scrollbar(frame18)
    list1 = Listbox(frame18, yscrollcommand=scrbar1.set, font=("Arial", 15), width=85, height=15)

    def display1():
        frame7.place_forget()
        frame8.place_forget()
        frame9.place_forget()
        frame15.place_forget()
        frame16.place_forget()
        frame17.place_forget()
        frame18.place_forget()

        comp.place_forget()

        frame14.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        detail = Database.cursor.execute('''SELECT C_ADD, C_GEN, C_DOB, C_PHONE, C_EMAIL FROM CUSTOMER WHERE C_ID=?''',(cu1,))

        for q in detail:
            add1 = q[0]
            gen1 = q[1]
            dob1 = q[2]
            phone1 = q[3]
            email1 = q[4]

        add = Label(frame14, text="Address:", font=("Times New Roman", 18), width=15, height=2)
        add.place(x=70, y=20)
        txtadd = Label(frame14, text=add1, font=("Times New Roman", 15), width=18, height=2)
        txtadd.place(x=300, y=23)
        gen = Label(frame14, text="Gender:", font=("Times New Roman", 18), width=15, height=2)
        gen.place(x=70, y=100)
        txtgen = Label(frame14, text=gen1, font=("Times New Roman", 15), width=18, height=2)
        txtgen.place(x=300, y=103)
        dob = Label(frame14, text="Date of Birth:", font=("Times New Roman", 18), width=15, height=2)
        dob.place(x=70, y=180)
        txtdob = Label(frame14, text=dob1, font=("Times New Roman", 15), width=18, height=2)
        txtdob.place(x=300, y=183)
        phone = Label(frame14, text="Contact No:", font=("Times New Roman", 18), width=15, height=2)
        phone.place(x=70, y=260)
        txtphone = Label(frame14, text=phone1, font=("Times New Roman", 15), width=18, height=2)
        txtphone.place(x=300, y=263)
        email = Label(frame14, text="Email ID:", font=("Times New Roman", 18), width=15, height=2)
        email.place(x=70, y=340)
        txtemail = Label(frame14, text=email1, font=("Times New Roman", 15), width=18, height=2)
        txtemail.place(x=300, y=343)

    def destroy2():
        window2.destroy()
        start()

    profile1 = Button(window2, text="Profile", font=("Times New Roman", 15), width=22, height=2, command=display1).place(x=0,y=245)
    ft = Button(window2, text="Fund Transfer", font=("Times New Roman", 15), width=22, height=2, command=funds).place(x=0, y=315)
    cb = Button(window2, text="Check Balance", font=("Times New Roman", 15), width=22, height=2, command=check_bal).place(x=0,y=385)
    st = Button(window2, text="Your Statement", font=("Times New Roman", 15), width=22, height=2, command=statement).place(x=0,y=455)
    ln = Button(window2, text="Loans", font=("Times New Roman", 15), width=22, height=2, command=loans).place(x=0, y=525)
    lg = Button(window2, text="Logout", font=("Times New Roman", 15), width=22, height=2, command=destroy2).place(x=0, y=595)

    c_name = Label(window2, text="Customer Name:", font=("Times New Roman", 18), width=15, height=2).place(x=0, y=165)
    c_name2 = Label(window2, text=cname, font=("Times New Roman", 18), width=15, height=2).place(x=220, y=165)
    c_id = Label(window2, text="Customer Id:", font=("Times New Roman", 18), width=15, height=2).place(x=440, y=165)
    c_id2 = Label(window2, text=cu1, font=("Times New Roman", 18), width=15, height=2).place(x=660, y=165)
    acc_no = Label(window2, text="Account No:", font=("Times New Roman", 18), width=15, height=2).place(x=880, y=165)
    acc_no2 = Label(window2, text=cacc, font=("Times New Roman", 18), width=17, height=2).place(x=1100, y=165)

def manager(eu1):
    e_namem = Database.cursor.execute('''SELECT E_NAME FROM EMPLOYEE WHERE E_ID=?''', (eu1,))
    for ii in e_namem:
        enamem = ii[0]

    window3m = Tk()
    window3m.title("Manager Page")
    window3m.configure(background='pink')
    window3m.geometry('1500x700')

    frame5m = Frame(window3m, bg='blue')
    frame5m.place(relx=0, rely=0, relwidth=1, relheight=0.34)
    frame6m = Frame(window3m, bg='blue')
    frame6m.place(relx=0, rely=0.34, relwidth=0.2, relheight=0.66)

    load = Image.open(r"D:\Study Stuff\College\4th Sem\Projects\DBMS-Python\Main files\logo2.jpg")
    photo = ImageTk.PhotoImage(load)
    img = Label(window3m, image=photo)
    img.image = photo
    img.place(x=340, y=-2)

    frame = Frame(window3m, bg='white')
    frame.place(relx=0.19, rely=0, relwidth=0.06, relheight=0.211)
    frame2 = Frame(window3m, bg='white')
    frame2.place(relx=0.75, rely=0, relwidth=0.06, relheight=0.211)

    id_em11= StringVar()
    accn2mxx = StringVar()
    accn3mxx = StringVar()
    id_emxx = StringVar()
    id_em2xx = StringVar()
    add1empxx = StringVar()
    gen1empxx = StringVar()
    dob1empxx = StringVar()
    phone1empxx = StringVar()
    email1empxx = StringVar()
    sal1empxx = StringVar()
    dept1empxx = StringVar()
    desig1empxx = StringVar()
    hdate1empxx = StringVar()
    name1empxx = StringVar()
    pass1empxx = StringVar()
    accn21m = StringVar()

    accn2mcc = StringVar()
    accnbalcc = StringVar()
    id_cc = StringVar()
    id_2cc = StringVar()
    add1cc = StringVar()
    gen1cc = StringVar()
    dob1cc = StringVar()
    phone1cc = StringVar()
    email1cc = StringVar()
    dept1cc = StringVar()
    desig1cc = StringVar()
    name1cc = StringVar()
    pass1cc = StringVar()

    frame12manemp = Frame(window3m, bg='pink')
    frame12addemp = Frame(window3m, bg='pink')
    frame12rememp = Frame(window3m, bg='pink')
    frame13m = Frame(window3m, bg='pink')
    frame12addcust = Frame(window3m, bg='pink')
    frame12remcust = Frame(window3m, bg='pink')
    frame12mancust = Frame(window3m, bg='pink')
    frameda= Frame(window3m, bg='pink')
    frame13 = Frame(window3m, bg='pink')
    frame13cc = Frame(window3m, bg='pink')

    comp3m = Label(window3m, text="Employee Added Successfully", font=("Times New Roman", 18), width=30, height=2)
    comp4m = Label(window3m, text="Customer Added Successfully", font=("Times New Roman", 18), width=30, height=2)

    comp1m = Label(window3m, text="Employee Successfully Removed", font=("Times New Roman", 18), width=30, height=2)
    comp2m = Label(window3m, text="Customer Successfully Removed", font=("Times New Roman", 18), width=30, height=2)
    comp5m = Label(window3m, text="Enter details correctly!", font=("Arial", 18), width=30, height=2)




    def updateemp():
        accn2m = accn2mxx.get()
        accn3m = accn3mxx.get()
        id_em2 = id_em2xx.get()
        add1emp = add1empxx.get()
        comp5m.place_forget()



        gen1emp = gen1empxx.get()



        dob1emp = dob1empxx.get()
        phone1emp = phone1empxx.get()


        email1emp = email1empxx.get()


        sal1emp = sal1empxx.get()

        dept1emp = dept1empxx.get()

        desig1emp = desig1empxx.get()

        hdate1emp = hdate1empxx.get()
        name1emp = name1empxx.get()


        pass1emp = pass1empxx.get()
        Database.cursor.execute('''INSERT INTO EMPLOYEE(E_PASS,E_NAME,E_ID,E_ADD,E_GEN,E_DOB,E_PHONE,E_EMAIL,E_SAL,E_DEPT,E_DESIG,E_HDATE) VALUES('%s','%s',%s,'%s','%s','%s',%s,'%s',%s,'%s','%s','%s')''' % (pass1emp, name1emp, id_em2, add1emp, gen1emp, dob1emp, phone1emp, email1emp, sal1emp, dept1emp,desig1emp,hdate1emp))
        Database.dbase.commit()
        comp3m.place(x=535, y=525)

    def enteremp():
        frame12manemp.place_forget()
        frame12addemp.place_forget()
        frame13m.place_forget()
        frame12addcust.place_forget()
        frame12remcust.place_forget()
        frame12mancust.place_forget()
        frame13cc.place_forget()

        comp3m.place_forget()
        comp4m.place_forget()
        comp5m.place_forget()

        comp1m.place_forget()
        comp2m.place_forget()

        frame13.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        nameemp = Label(frame13, text="Name:", font=("Times New Roman", 18), width=15, height=1)
        nameemp.place(x=70, y=20)
        txtnameemp = Entry(frame13, textvariable=name1empxx, font=("Times New Roman", 15))
        txtnameemp.place(x=300, y=23,  width=250, height=25)
        genemp = Label(frame13, text="Gender:", font=("Times New Roman", 18), width=15, height=1)
        genemp.place(x=70, y=75)
        txtgenemp = Entry(frame13, textvariable=gen1empxx, font=("Times New Roman", 15))
        txtgenemp.place(x=300, y=78, width=250, height=25)
        dobemp = Label(frame13, text="Date of Birth:", font=("Times New Roman", 18), width=15, height=1)
        dobemp.place(x=70, y=130)
        txtdobemp = Entry(frame13, textvariable=dob1empxx, font=("Times New Roman", 15) )
        txtdobemp.place(x=300, y=133, width=250, height=25)
        phoneemp = Label(frame13, text="Contact No:", font=("Times New Roman", 18), width=15, height=1)
        phoneemp.place(x=70, y=185)
        txtphoneemp = Entry(frame13, textvariable=phone1empxx, font=("Times New Roman", 15))
        txtphoneemp.place(x=300, y=188, width=250, height=25)
        emailemp = Label(frame13, text="EMail ID:", font=("Times New Roman", 18), width=15, height=1)
        emailemp.place(x=70, y=240)
        txtemailemp = Entry(frame13, textvariable=email1empxx, font=("Times New Roman", 15))
        txtemailemp.place(x=300, y=243, width=250, height=25)
        salemp = Label(frame13, text="Salary:", font=("Times New Roman", 18), width=15, height=1)
        salemp.place(x=570, y=20)
        txtsalemp = Entry(frame13, textvariable=sal1empxx, font=("Times New Roman", 15))
        txtsalemp.place(x=800, y=23, width=250, height=25)
        deptemp = Label(frame13, text="Department:", font=("Times New Roman", 18), width=15, height=1)
        deptemp.place(x=570, y=75)
        txtdeptemp = Entry(frame13, textvariable=dept1empxx, font=("Times New Roman", 15))
        txtdeptemp.place(x=800, y=78, width=250, height=25)
        desigemp = Label(frame13, text="Designation:", font=("Times New Roman", 18), width=15, height=1)
        desigemp.place(x=570, y=130)
        txtdesigemp = Entry(frame13, textvariable=desig1empxx, font=("Times New Roman", 15))
        txtdesigemp.place(x=800, y=133, width=250, height=25)
        hdateemp = Label(frame13, text="Hire Date:", font=("Times New Roman", 18), width=15, height=1)
        hdateemp.place(x=570, y=185)
        txthdateemp = Entry(frame13, textvariable=hdate1empxx, font=("Times New Roman", 15))
        txthdateemp.place(x=800, y=188, width=250, height=25)
        addemp = Label(frame13, text="Address:", font=("Times New Roman", 18), width=15, height=1)
        addemp.place(x=570, y=240)
        txtaddemp = Entry(frame13, textvariable=add1empxx, font=("Times New Roman", 15))
        txtaddemp.place(x=800, y=243, width=250, height=25)
        passemp = Label(frame13, text="Password:", font=("Times New Roman", 18), width=15, height=1)
        passemp.place(x=70, y=295)
        txtpassemp = Entry(frame13, show="*", textvariable=pass1empxx, font=("Times New Roman", 15))
        txtpassemp.place(x=300, y=298, width=250, height=25)
        updatempadd= Button(frame13, text="Add Employee", font=("Times New Roman", 18), width=17, height=1, command=updateemp)
        updatempadd.place(x=700, y=300)

    def delemp():
        xxx =id_em11.get()

        temp1=Database.cursor.execute('''SELECT E_NAME FROM Employee WHERE E_ID =?''', (xxx,))
        flag3=0

        for t in temp1:
            flag3=1

        if flag3==1:
            Database.cursor.execute('''DELETE FROM Employee WHERE E_ID =?''', (xxx,))
            Database.dbase.commit()
            comp1m.place(x=535, y=525)
        else:
            messagebox.showerror("Error", "Employee not found!")

    def rememp():
        frame12manemp.place_forget()
        frame12addemp.place_forget()
        frame13m.place_forget()
        frame12addcust.place_forget()
        frame12remcust.place_forget()
        frame12mancust.place_forget()
        frame13cc.place_forget()
        frame13.place_forget()

        comp3m.place_forget()
        comp4m.place_forget()
        comp5m.place_forget()

        comp1m.place_forget()
        comp2m.place_forget()

        frame12rememp.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        ckd1rememp = Label(frame12rememp, text="Employee ID:", font=("Times New Roman", 18), width=22, height=2)
        ckd1rememp.place(x=145, y=50)
        txtckd1rememp = Entry(frame12rememp, textvariable=id_em11, font=("Times New Roman", 18))
        txtckd1rememp.place(x=490, y=53, width=250, height=50)
        btckd3rememp = Button(frame12rememp, text="Remove Employee", font=("Times New Roman", 15), width=15, height=1,command=delemp)
        btckd3rememp.place(x=525, y=220)

    def addemp():
        frame12manemp.place_forget()
        frame12rememp.place_forget()
        frame13m.place_forget()
        frame12addcust.place_forget()
        frame12remcust.place_forget()
        frame12mancust.place_forget()
        frame13cc.place_forget()
        frame13.place_forget()

        comp3m.place_forget()
        comp4m.place_forget()
        comp5m.place_forget()

        comp1m.place_forget()
        comp2m.place_forget()

        frame12addemp.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        ckd1addemp = Label(frame12addemp, text="Employee ID:", font=("Times New Roman", 18), width=22, height=2)
        ckd1addemp.place(x=145, y=50)
        txtckd1addemp = Entry(frame12addemp, textvariable=id_em2xx, font=("Times New Roman", 18))
        txtckd1addemp.place(x=490, y=53, width=250, height=50)
        btckd3addemp = Button(frame12addemp, text="Add Employee", font=("Times New Roman", 15), width=15, height=1,command=enteremp)
        btckd3addemp.place(x=525, y=220)

    def manemp():
        frame12rememp.place_forget()
        frame12addemp.place_forget()
        frame13m.place_forget()
        frame12addcust.place_forget()
        frame12remcust.place_forget()
        frame12mancust.place_forget()
        frame13cc.place_forget()
        frame13.place_forget()
        frameda.place_forget()

        comp3m.place_forget()
        comp4m.place_forget()
        comp5m.place_forget()

        comp1m.place_forget()
        comp2m.place_forget()

        frame12manemp.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        ckd1manemp = Button(frame12manemp, text="Add Employee", font=("Times New Roman", 18), width=22, height=2,command=addemp)
        ckd1manemp.place(x=145, y=50)
        ckd2manemp = Button(frame12manemp, text="Remove Employee", font=("Times New Roman", 18), width=22, height=2,command=rememp)
        ckd2manemp.place(x=145, y=130)

    def updatecust():
        accn2nocc = accn2mcc.get()
        accn2balcc = accnbalcc.get()


        id_cc2 = id_cc.get()


        add2cc = add1cc.get()


        gen2cc = gen1cc.get()


        dob2cc = dob1cc.get()
        phone2cc = phone1cc.get()


        email2cc = email1cc.get()



        name2cc = name1cc.get()



        pass2cc = pass1cc.get()
        Database.cursor.execute('''INSERT INTO Customer(C_PASS,C_NAME,C_ID,C_ADD,C_GEN,C_DOB,C_PHONE,C_EMAIL,C_ACCBAL,C_ACCNO) VALUES('%s','%s',%s,'%s','%s','%s',%s,'%s',%s,'%s')''' % (pass2cc, name2cc, id_cc2, add2cc, gen2cc, dob2cc, phone2cc, email2cc, accn2balcc, accn2nocc))
        Database.dbase.commit()
        comp4m.place(x=535, y=525)

    def entercust():
        frame12manemp.place_forget()
        frame12addemp.place_forget()
        frame13m.place_forget()
        frame12addcust.place_forget()
        frame12remcust.place_forget()
        frame12mancust.place_forget()
        frame13.place_forget()

        comp3m.place_forget()
        comp4m.place_forget()
        comp5m.place_forget()

        comp1m.place_forget()
        comp2m.place_forget()

        frame13cc.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        namecc = Label(frame13cc, text="Name:", font=("Times New Roman", 18), width=15, height=1)
        namecc.place(x=70, y=20)
        txtnamecc = Entry(frame13cc, textvariable=name1cc, font=("Times New Roman", 15))
        txtnamecc.place(x=300, y=23, width=250, height=25)
        gencc = Label(frame13cc, text="Gender:", font=("Times New Roman", 18), width=15, height=1)
        gencc.place(x=70, y=75)
        txtgencc = Entry(frame13cc, textvariable=gen1cc, font=("Times New Roman", 15))
        txtgencc.place(x=300, y=78, width=250, height=25)
        dobcc = Label(frame13cc, text="Date of Birth:", font=("Times New Roman", 18), width=15, height=1)
        dobcc.place(x=70, y=130)
        txtdobcc = Entry(frame13cc, textvariable=dob1cc, font=("Times New Roman", 15) )
        txtdobcc.place(x=300, y=133, width=250, height=25)
        phonecc = Label(frame13cc, text="Contact No:", font=("Times New Roman", 18), width=15, height=1)
        phonecc.place(x=70, y=185)
        txtphonecc = Entry(frame13cc, textvariable=phone1cc, font=("Times New Roman", 15))
        txtphonecc.place(x=300, y=188, width=250, height=25)
        emailcc = Label(frame13cc, text="EMail ID:", font=("Times New Roman", 18), width=15, height=1)
        emailcc.place(x=70, y=240)
        txtemailcc = Entry(frame13cc, textvariable=email1cc, font=("Times New Roman", 15))
        txtemailcc.place(x=300, y=243, width=250, height=25)
        salcc = Label(frame13cc, text="Account Bal:", font=("Times New Roman", 18), width=15, height=1)
        salcc.place(x=570, y=20)
        txtsalcc = Entry(frame13cc, textvariable=accnbalcc, font=("Times New Roman", 15))
        txtsalcc.place(x=800, y=23, width=250, height=25)
        deptcc = Label(frame13cc, text="Customer ID:", font=("Times New Roman", 18), width=15, height=1)
        deptcc.place(x=570, y=75)
        txtdeptcc = Entry(frame13cc, textvariable=id_cc, font=("Times New Roman", 15))
        txtdeptcc.place(x=800, y=78, width=250, height=25)
        addcc = Label(frame13cc, text="Address:", font=("Times New Roman", 18), width=15, height=1)
        addcc.place(x=570, y=130)
        txtaddcc = Entry(frame13cc, textvariable=add1cc, font=("Times New Roman", 15))
        txtaddcc.place(x=800, y=133, width=250, height=25)
        passcc = Label(frame13cc, text="Password:", font=("Times New Roman", 18), width=15, height=1)
        passcc.place(x=570, y=185)
        txtpasscc = Entry(frame13cc, show="*", textvariable=pass1cc, font=("Times New Roman", 15))
        txtpasscc.place(x=800, y=188, width=250, height=25)
        updatempcc= Button(frame13cc, text="Add Customer", font=("Times New Roman", 18), width=17, height=1, command=updatecust)
        updatempcc.place(x=700, y=250)


    def delcust():
        daccnm = accn21m.get()

        temp2=Database.cursor.execute('''SELECT C_ID FROM Customer WHERE C_ACCNO =?''',(daccnm,))
        flag4=0

        for u in temp2:
            flag4=1

        if flag4==1:
            Database.cursor.execute('''DELETE FROM Customer WHERE C_ACCNO =?''',(daccnm,))
            Database.dbase.commit()
            comp2m.place(x=535, y=525)
        else:
            messagebox.showerror("Error", "Customer not found!")

    def remcust():
        frame12manemp.place_forget()
        frame12addemp.place_forget()
        frame13m.place_forget()
        frame12addcust.place_forget()
        frame12rememp.place_forget()
        frame12mancust.place_forget()
        frame13cc.place_forget()
        frame13.place_forget()

        comp3m.place_forget()
        comp4m.place_forget()
        comp5m.place_forget()

        comp1m.place_forget()
        comp2m.place_forget()

        frame12remcust.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        ckd1remcust = Label(frame12remcust, text="Customer AccNo:", font=("Times New Roman", 18), width=22, height=2)
        ckd1remcust.place(x=145, y=50)
        txtckd1remcust = Entry(frame12remcust, textvariable=accn21m, font=("Times New Roman", 18))
        txtckd1remcust.place(x=490, y=53, width=250, height=50)
        btckd3remcust = Button(frame12remcust, text="Remove Customer", font=("Times New Roman", 15), width=15, height=1,command=delcust )
        btckd3remcust.place(x=525, y=220)

    def addcust():
        frame12manemp.place_forget()
        frame12addemp.place_forget()
        frame13m.place_forget()
        frame12rememp.place_forget()
        frame12remcust.place_forget()
        frame12mancust.place_forget()
        frame13cc.place_forget()
        frame13.place_forget()

        comp3m.place_forget()
        comp4m.place_forget()
        comp5m.place_forget()

        comp1m.place_forget()
        comp2m.place_forget()

        frame12addcust.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        ckd1addcust = Label(frame12addcust, text="Customer AccNo:", font=("Times New Roman", 18), width=22, height=2)
        ckd1addcust.place(x=145, y=50)
        txtckd1addcust = Entry(frame12addcust, textvariable=accn2mcc, font=("Times New Roman", 18))
        txtckd1addcust.place(x=490, y=53, width=250, height=50)
        btckd3addcust = Button(frame12addcust, text="Add Customer", font=("Times New Roman", 15), width=15, height=1,command=entercust)
        btckd3addcust.place(x=525, y=220)

    def mancust():
        frame12manemp.place_forget()
        frame12addemp.place_forget()
        frame13m.place_forget()
        frame12addcust.place_forget()
        frame12remcust.place_forget()
        frame12rememp.place_forget()
        frame13cc.place_forget()
        frame13.place_forget()
        frameda.place_forget()

        comp3m.place_forget()
        comp4m.place_forget()
        comp5m.place_forget()

        comp1m.place_forget()
        comp2m.place_forget()

        frame12mancust.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        ckd1mancust = Button(frame12mancust, text="Add customer", font=("Times New Roman", 18), width=22, height=2,command=addcust)
        ckd1mancust.place(x=145, y=50)
        ckd2mancust = Button(frame12mancust, text="Remove customer", font=("Times New Roman", 18), width=22, height=2,command=remcust)
        ckd2mancust.place(x=145, y=130)

    def displaym():
        frame12manemp.place_forget()
        frame12addemp.place_forget()
        frame12rememp.place_forget()
        frame12addcust.place_forget()
        frame12remcust.place_forget()
        frame12mancust.place_forget()
        frame13cc.place_forget()
        frame13.place_forget()
        frameda.place_forget()

        comp3m.place_forget()
        comp4m.place_forget()
        comp5m.place_forget()

        comp1m.place_forget()
        comp2m.place_forget()

        frame13m.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        detailm = Database.cursor.execute('''SELECT E_ADD, E_GEN, E_DOB, E_PHONE, E_EMAIL, E_SAL, E_DEPT, E_DESIG, E_HDATE FROM EMPLOYEE WHERE E_ID=?''',(eu1,))

        for pp in detailm:
            add1m = pp[0]
            gen1m = pp[1]
            dob1m = pp[2]
            phone1m = pp[3]
            email1m = pp[4]
            sal1m = pp[5]
            dept1m = pp[6]
            desig1m = pp[7]
            hdate1m = pp[8]

        addm = Label(frame13m, text="Address:", font=("Times New Roman", 18), width=15, height=2)
        addm.place(x=70, y=20)
        txtaddm = Label(frame13m, text=add1m, font=("Times New Roman", 15), width=18, height=2)
        txtaddm.place(x=300, y=23)
        genm = Label(frame13m, text="Gender:", font=("Times New Roman", 18), width=15, height=2)
        genm.place(x=70, y=100)
        txtgenm = Label(frame13m, text=gen1m, font=("Times New Roman", 15), width=18, height=2)
        txtgenm.place(x=300, y=103)
        dobm = Label(frame13m, text="Date of Birth:", font=("Times New Roman", 18), width=15, height=2)
        dobm.place(x=70, y=180)
        txtdobm = Label(frame13m, text=dob1m, font=("Times New Roman", 15), width=18, height=2)
        txtdobm.place(x=300, y=183)
        phonem = Label(frame13m, text="Contact No:", font=("Times New Roman", 18), width=15, height=2)
        phonem.place(x=70, y=260)
        txtphonem = Label(frame13m, text=phone1m, font=("Times New Roman", 15), width=18, height=2)
        txtphonem.place(x=300, y=263)
        emailm = Label(frame13m, text="EMail ID:", font=("Times New Roman", 18), width=15, height=2)
        emailm.place(x=70, y=340)
        txtemailm = Label(frame13m, text=email1m, font=("Times New Roman", 15), width=18, height=2)
        txtemailm.place(x=300, y=343)
        salm = Label(frame13m, text="Salary:", font=("Times New Roman", 18), width=15, height=2)
        salm.place(x=570, y=60)
        txtsalm = Label(frame13m, text=sal1m, font=("Times New Roman", 15), width=18, height=2)
        txtsalm.place(x=800, y=63)
        deptm = Label(frame13m, text="Department:", font=("Times New Roman", 18), width=15, height=2)
        deptm.place(x=570, y=140)
        txtdeptm = Label(frame13m, text=dept1m, font=("Times New Roman", 15), width=18, height=2)
        txtdeptm.place(x=800, y=143)
        desigm = Label(frame13m, text="Designation:", font=("Times New Roman", 18), width=15, height=2)
        desigm.place(x=570, y=220)
        txtdesigm = Label(frame13m, text=desig1m, font=("Times New Roman", 15), width=18, height=2)
        txtdesigm.place(x=800, y=223)
        hdatem = Label(frame13m, text="Hire Date:", font=("Times New Roman", 18), width=15, height=2)
        hdatem.place(x=570, y=300)
        txthdatem = Label(frame13m, text=hdate1m, font=("Times New Roman", 15), width=18, height=2)
        txthdatem.place(x=800, y=303)

    def da_bal():
        da= Database.cursor.execute('''SELECT C_NAME, C_ACCBAL FROM CUSTOMER ''')
        da_f=da.fetchall()

        l_n=[]
        l_b=[]
        for i in da_f:
            l_n.append(i[0])
            l_b.append(i[1])
        pyp.bar(l_n,l_b)
        pyp.xlabel('Name Of Customer')
        pyp.ylabel('Balance')
        pyp.title('Balance of each customer')
        pyp.show()


    def da_tra():
        da2= Database.cursor.execute('''SELECT C_ACCNO, C_NAME FROM CUSTOMER''')
        da2_f=da2.fetchall()

        l_acc=[]
        l_c=[]
        for i in da2_f:
            l_acc.append(i[1])
            count=0
            da2_c=Database.cursor.execute('''SELECT COUNT(TR_ID) FROM TRANSACTIONS WHERE FRM_ACC=? OR TO_ACC=?''',(i[0],i[0],))
            da2_cf=da2_c.fetchall()
            count=count+da2_cf[0][0]
            l_c.append(count)
        pyp.pie(l_c,labels=l_acc, autopct='%1.2f%%')
        pyp.title('No. of Transactions By Each Customer')
        pyp.show()


    def data_ana():
        frame12rememp.place_forget()
        frame12addemp.place_forget()
        frame13m.place_forget()
        frame12addcust.place_forget()
        frame12remcust.place_forget()
        frame12mancust.place_forget()
        frame13cc.place_forget()
        frame13.place_forget()
        frameda.place_forget()

        comp3m.place_forget()
        comp4m.place_forget()
        comp5m.place_forget()

        comp1m.place_forget()
        comp2m.place_forget()

        Button(frameda, text='Balance BarGraph', font=("Times New Roman", 18), width=22, height=2,command=da_bal).place(x=145, y=50)
        Button(frameda, text='No. of Transaction Pie Chart', font=("Times New Roman", 18), width=22, height=2, command=da_tra).place(x=540,y=50)
        frameda.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)


    def destroy3m():
        window3m.destroy()
        start()

    profilem = Button(window3m, text="Profile", font=("Times New Roman", 15), width=22, height=2, command=displaym).place(x=0,y=265)
    c_depm = Button(window3m, text="Manage Customer", font=("Times New Roman", 15), width=22, height=2, command=mancust).place(x=0,y=335)
    c_widm = Button(window3m, text="Manage Employee", font=("Times New Roman", 15), width=22, height=2, command=manemp).place(x=0,y=405)
    da_man = Button(window3m, text='Data Analysis',font=("Times New Roman", 15), width=22, height=2, command=data_ana).place(x=0, y=475)
    lgm = Button(window3m, text="Logout", font=("Times New Roman", 15), width=22, height=2, command=destroy3m).place(x=0, y=545)

    c_namem = Label(window3m, text="Manager Name:", font=("Times New Roman", 18), width=17, height=2).place(x=90, y=165)
    c_name2m = Label(window3m, text=enamem, font=("Times New Roman", 18), width=17, height=2).place(x=350, y=165)
    c_idm = Label(window3m, text="Manager Id:", font=("Times New Roman", 18), width=17, height=2).place(x=740, y=165)
    c_id2m = Label(window3m, text=eu1, font=("Times New Roman", 18), width=17, height=2).place(x=1000, y=165)

def etransac1(eu,toacc, trtyp, amt):
    id = random.randint(2000, 3000)
    x = datetime.now()
    dat = str(x.strftime('%Y-%m-%d'))
    tim = x.time()
    Database.cursor.execute('''INSERT INTO TRANSACTIONS(TR_ID,E_ID,TO_ACC,TR_TYPE,AMT,DT,TM) VALUES(%s,%s,%s,'%s',%s,'%s','%s')''' % (id, eu, toacc, trtyp, amt, dat, tim))
    Database.dbase.commit()

def etransac2(eu,fracc, trtyp, amt):
    id = random.randint(3000, 4000)
    x = datetime.now()
    dat = str(x.strftime('%Y-%m-%d'))
    tim = x.time()
    Database.cursor.execute('''INSERT INTO TRANSACTIONS(TR_ID,E_ID,FRM_ACC,TR_TYPE,AMT,DT,TM) VALUES(%s,%s,%s,'%s',%s,'%s','%s')''' % (id, eu, fracc, trtyp, amt, dat, tim))
    Database.dbase.commit()

def employee(eu1):
    e_name = Database.cursor.execute('''SELECT E_NAME FROM EMPLOYEE WHERE E_ID=?''', (eu1,))
    for i in e_name:
        ename = i[0]

    window3 = Tk()
    window3.title("Employee Page")
    window3.configure(background='pink')
    window3.geometry('1500x700')

    frame5 = Frame(window3, bg='blue')
    frame5.place(relx=0, rely=0, relwidth=1, relheight=0.34)
    frame6 = Frame(window3, bg='blue')
    frame6.place(relx=0, rely=0.34, relwidth=0.2, relheight=0.66)

    load = Image.open(r"D:\Study Stuff\College\4th Sem\Projects\DBMS-Python\Main files\logo2.jpg")
    photo = ImageTk.PhotoImage(load)
    img = Label(window3, image=photo)
    img.image = photo
    img.place(x=340, y=-2)

    frame = Frame(window3, bg='white')
    frame.place(relx=0.19, rely=0, relwidth=0.06, relheight=0.211)
    frame2 = Frame(window3, bg='white')
    frame2.place(relx=0.75, rely=0, relwidth=0.06, relheight=0.211)

    accn2 = StringVar()
    amt2 = StringVar()

    def deposit():
        comp1.place_forget()

        daccn = accn2.get()
        damt = amt2.get()

        if accn2.get() == "" and amt2.get() == "":
            messagebox.showerror("Error", "Enter Account Number and Amount!")
        elif accn2.get() == "":
            messagebox.showerror("Error", "Enter Account Number!")
        elif amt2.get() == "":
            messagebox.showerror("Error", "Enter Amount!")

        else:
            dbal = Database.cursor.execute('''SELECT C_ACCBAL FROM CUSTOMER WHERE C_ACCNO=?''', (daccn,))
            flag2 = 0

            for n in dbal:
                flag2=1
                bal = n[0]

            if flag2==1:
                balance = bal + int(damt)
                Database.cursor.execute('''UPDATE CUSTOMER SET C_ACCBAL=? WHERE C_ACCNO=? ''', (balance, daccn,))

                comp1.place(x=535, y=525)
                Database.dbase.commit()

                st2 = 'Fund Deposit  '
                etransac1(eu1,daccn, st2, damt)
            else:
                messagebox.showerror("Error", "Invalid Account Number!")

    accn3 = StringVar()
    amt3 = StringVar()

    def withdraw():
        comp2.place_forget()

        waccn = accn3.get()
        wamt = amt3.get()

        if accn3.get() == "" and amt3.get() == "":
            messagebox.showerror("Error", "Enter Account Number and Amount!")
        elif accn3.get() == "":
            messagebox.showerror("Error", "Enter Account Number!")
        elif amt3.get() == "":
            messagebox.showerror("Error", "Enter Amount!")

        else:
            wbal = Database.cursor.execute('''SELECT C_ACCBAL FROM CUSTOMER WHERE C_ACCNO=?''', (waccn,))
            flag1 = 0

            for o in wbal:
                flag1 = 1
                bal = o[0]

            if flag1 == 1:
                balance = bal - int(wamt)
                if balance <= 0:
                    messagebox.showerror("Error", "Insufficient balance!")
                else:
                    Database.cursor.execute('''UPDATE CUSTOMER SET C_ACCBAL=? WHERE C_ACCNO=? ''', (balance, waccn,))

                    comp2.place(x=535, y=525)
                    Database.dbase.commit()

                    st3 = 'Fund Withdraw'
                    etransac2(eu1,waccn, st3, wamt)
            else:
                messagebox.showerror("Error", "Invalid Account Number!")

    frame10 = Frame(window3, bg='pink')
    frame11 = Frame(window3, bg='pink')
    frame12 = Frame(window3, bg='pink')
    frame13 = Frame(window3, bg='pink')

    comp1 = Label(window3, text="Amount Successfully Deposited", font=("Times New Roman", 18), width=30, height=2)
    comp2 = Label(window3, text="Amount Successfully Withdrawn", font=("Times New Roman", 18), width=30, height=2)

    def c_deposit():
        frame11.place_forget()
        frame12.place_forget()
        frame13.place_forget()

        comp1.place_forget()
        comp2.place_forget()

        frame10.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        csd1 = Label(frame10, text="Customer's account number:", font=("Times New Roman", 18), width=22, height=2)
        csd1.place(x=145, y=50)
        txtcsd1 = Entry(frame10, textvariable=accn2, font=("Times New Roman", 18))
        txtcsd1.place(x=490, y=53, width=250, height=50)
        csd2 = Label(frame10, text="Amount:", font=("Times New Roman", 18), width=15, height=2)
        csd2.place(x=240, y=130)
        txtcsd2 = Entry(frame10, textvariable=amt2, font=("Times New Roman", 18))
        txtcsd2.place(x=490, y=133, width=250, height=50)
        btcsd3 = Button(frame10, text="Deposit", font=("Times New Roman", 15), width=15, height=1, command=deposit)
        btcsd3.place(x=525, y=220)

    def c_withdraw():
        frame10.place_forget()
        frame12.place_forget()
        frame13.place_forget()

        comp1.place_forget()
        comp2.place_forget()

        frame11.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        wd1 = Label(frame11, text="Customer's account number:", font=("Times New Roman", 18), width=22, height=2)
        wd1.place(x=145, y=50)
        txtwd1 = Entry(frame11, textvariable=accn3, font=("Times New Roman", 18))
        txtwd1.place(x=490, y=53, width=250, height=50)
        wd2 = Label(frame11, text="Amount:", font=("Times New Roman", 18), width=15, height=2)
        wd2.place(x=240, y=130)
        txtwd2 = Entry(frame11, textvariable=amt3, font=("Times New Roman", 18))
        txtwd2.place(x=490, y=133, width=250, height=50)
        btwd3 = Button(frame11, text="Withdraw", font=("Times New Roman", 15), width=15, height=1, command=withdraw)
        btwd3.place(x=525, y=220)

    def chk_deposit():
        frame10.place_forget()
        frame11.place_forget()
        frame13.place_forget()

        comp1.place_forget()
        comp2.place_forget()

        frame12.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        ckd1 = Label(frame12, text="Deposit to account number:", font=("Times New Roman", 18), width=22, height=2)
        ckd1.place(x=145, y=50)
        txtckd1 = Entry(frame12, textvariable=accn2, font=("Times New Roman", 18))
        txtckd1.place(x=490, y=53, width=250, height=50)
        ckd2 = Label(frame12, text="Amount:", font=("Times New Roman", 18), width=15, height=2)
        ckd2.place(x=240, y=130)
        txtckd2 = Entry(frame12, textvariable=amt2, font=("Times New Roman", 18))
        txtckd2.place(x=490, y=133, width=250, height=50)
        btckd3 = Button(frame12, text="Deposit", font=("Times New Roman", 15), width=15, height=1, command=deposit)
        btckd3.place(x=525, y=220)

    def display2():
        frame10.place_forget()
        frame11.place_forget()
        frame12.place_forget()

        comp1.place_forget()
        comp2.place_forget()

        frame13.place(relx=0.2, rely=0.34, relwidth=0.8, relheight=0.7)

        detail = Database.cursor.execute('''SELECT E_ADD, E_GEN, E_DOB, E_PHONE, E_EMAIL, E_SAL, E_DEPT, E_DESIG, E_HDATE FROM EMPLOYEE WHERE E_ID=?''',(eu1,))

        for p in detail:
            add1 = p[0]
            gen1 = p[1]
            dob1 = p[2]
            phone1 = p[3]
            email1 = p[4]
            sal1 = p[5]
            dept1 = p[6]
            desig1 = p[7]
            hdate1 = p[8]

        add = Label(frame13, text="Address:", font=("Times New Roman", 18), width=15, height=2)
        add.place(x=70, y=20)
        txtadd = Label(frame13, text=add1, font=("Times New Roman", 15), width=18, height=2)
        txtadd.place(x=300, y=23)
        gen = Label(frame13, text="Gender:", font=("Times New Roman", 18), width=15, height=2)
        gen.place(x=70, y=100)
        txtgen = Label(frame13, text=gen1, font=("Times New Roman", 15), width=18, height=2)
        txtgen.place(x=300, y=103)
        dob = Label(frame13, text="Date of Birth:", font=("Times New Roman", 18), width=15, height=2)
        dob.place(x=70, y=180)
        txtdob = Label(frame13, text=dob1, font=("Times New Roman", 15), width=18, height=2)
        txtdob.place(x=300, y=183)
        phone = Label(frame13, text="Contact No:", font=("Times New Roman", 18), width=15, height=2)
        phone.place(x=70, y=260)
        txtphone = Label(frame13, text=phone1, font=("Times New Roman", 15), width=18, height=2)
        txtphone.place(x=300, y=263)
        email = Label(frame13, text="EMail ID:", font=("Times New Roman", 18), width=15, height=2)
        email.place(x=70, y=340)
        txtemail = Label(frame13, text=email1, font=("Times New Roman", 15), width=18, height=2)
        txtemail.place(x=300, y=343)
        sal = Label(frame13, text="Salary:", font=("Times New Roman", 18), width=15, height=2)
        sal.place(x=570, y=60)
        txtsal = Label(frame13, text=sal1, font=("Times New Roman", 15), width=18, height=2)
        txtsal.place(x=800, y=63)
        dept = Label(frame13, text="Department:", font=("Times New Roman", 18), width=15, height=2)
        dept.place(x=570, y=140)
        txtdept = Label(frame13, text=dept1, font=("Times New Roman", 15), width=18, height=2)
        txtdept.place(x=800, y=143)
        desig = Label(frame13, text="Designation:", font=("Times New Roman", 18), width=15, height=2)
        desig.place(x=570, y=220)
        txtdesig = Label(frame13, text=desig1, font=("Times New Roman", 15), width=18, height=2)
        txtdesig.place(x=800, y=223)
        hdate = Label(frame13, text="Hire Date:", font=("Times New Roman", 18), width=15, height=2)
        hdate.place(x=570, y=300)
        txthdate = Label(frame13, text=hdate1, font=("Times New Roman", 15), width=18, height=2)
        txthdate.place(x=800, y=303)

    def destroy3():
        window3.destroy()
        start()

    profile2 = Button(window3, text="Profile", font=("Times New Roman", 15), width=22, height=2, command=display2).place(x=0,y=265)
    c_dep = Button(window3, text="Cash Deposit", font=("Times New Roman", 15), width=22, height=2, command=c_deposit).place(x=0,y=335)
    c_wid = Button(window3, text="Cash Withdraw", font=("Times New Roman", 15), width=22, height=2, command=c_withdraw).place(x=0, y=405)
    cq_d = Button(window3, text="Cheque Deposit", font=("Times New Roman", 15), width=22, height=2, command=chk_deposit).place(x=0, y=475)
    lg = Button(window3, text="Logout", font=("Times New Roman", 15), width=22, height=2, command=destroy3).place(x=0, y=545)

    c_name = Label(window3, text="Employee Name:", font=("Times New Roman", 18), width=18, height=2).place(x=90, y=165)
    c_name2 = Label(window3, text=ename, font=("Times New Roman", 18), width=17, height=2).place(x=350, y=165)
    c_id = Label(window3, text="Employee Id:", font=("Times New Roman", 18), width=18, height=2).place(x=740, y=165)
    c_id2 = Label(window3, text=eu1, font=("Times New Roman", 18), width=17, height=2).place(x=1000, y=165)


def start():
    window = Tk()
    window.title("Banking System")
    window.configure(background='blue')

    username = StringVar()
    password = StringVar()

    def check_cust():

        u1 = username.get()
        p1 = password.get()

        cpa = Database.cursor.execute('''SELECT C_PASS FROM CUSTOMER WHERE C_ID=?''', (u1,))

        pwd = -1
        for record in cpa:
            pwd = record[0]

        if p1 == pwd:
            window.destroy()
            customer(u1)
        elif username.get() == "" and password.get() == "":
            messagebox.showerror("Error", "Enter Username and password!")
        elif username.get() == "":
            messagebox.showerror("Error", "Enter Username!")
        elif password.get() == "":
            messagebox.showerror("Error", "Enter Password!")
        else:
            messagebox.showerror("Error", "Invalid Username or Password!")

    def check_emp():
        u1 = username.get()
        p1 = password.get()

        epa = Database.cursor.execute('''SELECT E_PASS,E_DESIG FROM EMPLOYEE WHERE E_ID=?''', (u1,))

        des = -2
        pwd = -1
        for record in epa:
            pwd = record[0]
            des = record[1]

        if p1 == pwd:
            if des == 'Manager':
                window.destroy()
                manager(u1)
            else:
                window.destroy()
                employee(u1)
        elif username.get() == "":
            messagebox.showerror("Error", "Enter Username!")
        elif password.get() == "":
            messagebox.showerror("Error", "Enter Password!")
        else:
            messagebox.showerror("Error", "Invalid Username or Password!")

    frame3 = Frame(window, bg='sky blue')
    frame4 = Frame(window, bg='sky blue')


    def login_cust():
        frame1.place_forget()

        frame3.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.8)

        cl = Label(frame3, text="Customer Login", font=("Times New Roman", 30), width=20, height=2)
        cl.place(x=320, y=60)
        cl1 = Label(frame3, text="Username:", font=("Times New Roman", 20), width=15, height=2)
        cl1.place(x=290, y=190)
        cl2 = Label(frame3, text="Password:", font=("Times New Roman", 20), width=15, height=2)
        cl2.place(x=290, y=270)
        ctxt1 = Entry(frame3, textvariable=username, font=("Times New Roman", 18))
        ctxt1.place(x=550, y=200, width=250, height=50)
        ctxt2 = Entry(frame3, textvariable=password, show="*", font=("Times New Roman", 18))
        ctxt2.place(x=550, y=278, width=250, height=50)
        cbt3 = Button(frame3, text="Login", font=("Times New Roman", 15), width=15, height=1, command=check_cust)
        cbt3.place(x=590, y=370)
        back = Button(frame3, text="Back", font=("Times New Roman", 15), width=10, height=1, command=main)
        back.place(x=70, y=60)

    def login_emp():
        frame1.place_forget()

        frame4.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.8)

        el = Label(frame4, text="Employee Login", font=("Times New Roman", 30), width=20, height=2)
        el.place(x=320, y=60)
        el1 = Label(frame4, text="Username:", font=("Times New Roman", 20), width=15, height=2)
        el1.place(x=290, y=190)
        el2 = Label(frame4, text="Password:", font=("Times New Roman", 20), width=15, height=2)
        el2.place(x=290, y=270)
        etxt1 = Entry(frame4, textvariable=username, font=("Times New Roman", 18))
        etxt1.place(x=550, y=200, width=250, height=50)
        etxt2 = Entry(frame4, textvariable=password, show="*", font=("Times New Roman", 18))
        etxt2.place(x=550, y=278, width=250, height=50)
        ebt3 = Button(frame4, text="Login", font=("Times New Roman", 15), width=15, height=1, command=check_emp)
        ebt3.place(x=590, y=370)
        back = Button(frame4, text="Back", font=("Times New Roman", 15), width=10, height=1, command=main)
        back.place(x=70, y=60)

    frame1 = Frame(window, bg='sky blue')

    def main():
        frame3.place_forget()
        frame4.place_forget()

        frame1.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.8)

        load = Image.open(r"D:\Study Stuff\College\4th Sem\Projects\DBMS-Python\Main files\logo2.jpg")
        photo = ImageTk.PhotoImage(load)
        img = Label(window, image=photo)
        img.image = photo
        img.place(x=305, y=0)

        frame = Frame(window, bg='white')
        frame.place(relx=0.1, rely=0, relwidth=0.14, relheight=0.2077)
        frame2 = Frame(window, bg='white')
        frame2.place(relx=0.777, rely=0, relwidth=0.123, relheight=0.2077)

        bt1 = Button(frame1, text="Customer", font=("Times New Roman", 30), width=16, height=2, activebackground='blue',command=login_cust)
        bt1.place(x=120, y=160)
        bt2 = Button(frame1, text="Employee", font=("Times New Roman", 30), width=16, height=2, activebackground='blue',command=login_emp)
        bt2.place(x=590, y=160)
        window.geometry('1280x720')
        window.mainloop()

    main()

start()