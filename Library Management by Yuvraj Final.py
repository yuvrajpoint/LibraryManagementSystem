from datetime import date
import datetime
import mysql.connector
con = mysql.connector.connect(host='localhost', user='root', password='tiger') # Please enter password
cur = con.cursor()

cur.execute('create database if not exists test1')
cur.execute('use test1')
cur.execute('create table if not exists students(sid int primary key, sname varchar(15), pno bigint)')
cur.execute('create table if not exists books(bid int primary key, bname varchar(20), author varchar(15), total int)')
cur.execute('create table if not exists ir(bid int, sid int, doi date, dor date)')
con.commit()

today = datetime.datetime.now()
today_date = str(today.date())


def add_book():
    try:
        global j
        b = input('Enter book name : ').title()
        a = input('Enter author\'s name : ').title()
        t = int(input('Enter total number of books : '))
        cur.execute('select max(bid) from books')
        for i in cur:
            for j in i:
                pass
        if j == None:
            j = 1
        else:
            j = j+1
        d = (j, b, a, t)
        cur.execute("insert into books values(%s,%s,%s,%s)",d)
        con.commit()
        print('Book added')
        print('Book code of this book is : ',j)
        print('_'*90)
    except:
        print('Something went wrong !!!!')
        print('Try again....')
        add_book()


def add_student():
    try:
        global j
        n = input('Enter student\'s name : ').title()
        while 1:
            p = input('Enter phone number : ')
            if len(p) == 10 and p[0]  in ('9','8','7','6'):
                break
            else:
                print('Invalid phone no.')
                continue
        cur.execute('select max(sid) from students')
        for i in cur:
            for j in i:
                pass
        if j == None:
            j = 1
        else:
            j = j+1
        d = (j, n, int(p))
        cur.execute("insert into students values(%s,%s,%s)", d)
        con.commit()
        print('Student added')
        print('Reg. no of this student is : ', j)
        print('_'*90)
    except:
        print('Something went wrong !!!!')
        print('Try again....')
        add_student()


def issue_book():
    try:
        global stu
        sbid = []
        cur.execute('select bid from books where total > 0')
        for i in cur:
            sbid.append(i[0])
        ssid = []
        cur.execute('select sid from students')
        for i in cur:
            ssid.append(i[0])
        while 1:
            sid = int(input('Enter student\'s Reg. No. : '))
            if sid in ssid:
                break
            else:
                print('Invalid Reg. No. !!!')
                print('Try Again...')
                continue
        while 1:
            bid = int(input('Enter book code : '))
            if bid in sbid:
                break
            else:
                print('Invalid book code (either book is not available or this code invalid book code) !!!')
                print('Try Again...')
                continue
        idate = None
        s = ['-','/','\\',':']
        while 1:
            op = input('Enter date of issue (yyyy/mm/dd)\n[or Press T for today\'s date]\n\t\t\t--> ')
            if op.lower() == 't':
                idate = today_date
                break
            elif op[0:4].isdigit() and op[5:7].isdigit() and op[8:10].isdigit() and op[4] and op[7] in s and len(op)==10 and op[4]==op[7]:
                idate = op
                break
            else:
                print('Please enter correct date formate(YYYY/MM/DD) only!!!')
                continue
        cur.execute('insert into ir values(%s,%s,%s,null)',(bid,sid,idate))
        con.commit()           
        cur.execute('update books set total=total-1 where bid = %s',(bid,))
        con.commit()
        cur.execute('select sname from students where sid = %s',(sid,))
        for i in cur:
            stu = i[0]
        print('Book issued to',stu)
        print('Please return the book within 15 days to avoid late fee')
        print('Late fee for the extra days you keep the book after 15 days is 3 rs per day')
        print('_'*90)
    except:
        print('Something went wrong !!!!')
        print('Try again....')
        issue_book()


def submit_book():
    try:
        global idate
        stud = None
        ssid = []
        cur.execute('select sid from ir where dor is NULL')
        for i in cur:
            ssid.append(i[0])
        while 1:
            sid = int(input('Enter student\'s Reg. No. : '))
            if sid in ssid:
                break
            else:
                try:
                    print(sn(sid),'does not have any book.')
                except:
                    print('Invalid Reg. No. !!!')
                    print('Try Again...')
                    continue
        lbook = []
        lbid = []
        cur.execute('select bid from ir where sid = %s and dor is NULL',(sid,))
        for i in cur:
            lbid.append(i[0])
        for i in lbid:
            cur.execute('select bname from books where bid = %s', (i,))
            for j in cur:
                lbook.append(j[0])
        cur.execute('select sname from students where sid = %s', (sid,))
        for i in cur:
            stud = i[0]
        print('List of books', stud, ' have :')
        for i in range(len(lbook)):
            print(i+1, end='')
            print('. ', lbook[i])
        print('Enter which book', stud, 'want to return... ')
        ch = int(input())
        rbook = lbook[ch-1]
        bid = lbid[ch-1]
        cur.execute('update books set total=total+1 where bname=%s', (rbook,))
        con.commit()
        cur.execute('select doi from ir where sid=%s and bid=%s', (sid, bid))
        for i in cur:
            idate = i[0]
        print('Book issued on :', idate)
        diff = None
        rdate = None
        while 1:
            try:
                opn = input('Enter date of submission (yyyy/mm/dd)\n[or Press T for today\'s date]\n\t\t\t--> ')
                if opn.lower() == 't':
                    rdate = today_date
                    yi = int(str(idate)[0:4])
                    yr = int(rdate[0:4])
                    mi = int(str(idate)[5:7])
                    mr = int(rdate[5:7])
                    di = int(str(idate)[8:10])
                    dr = int(rdate[8:10])
                    datei = date(yi,mi,di)
                    dater = date(yr,mr,dr)
                    diff = (dater - datei).days
                    if diff >= 0:
                        break
                    else:
                        print('Date of submission should be after date of issue !')
                        print('Try again....')
                        continue
                else:
                    yi = int(str(idate)[0:4])
                    yr = int(opn[0:4])
                    mi = int(str(idate)[5:7])
                    mr = int(opn[5:7])
                    di = int(str(idate)[8:10])
                    dr = int(opn[8:10])
                    datei = date(yi,mi,di)
                    dater = date(yr,mr,dr)
                    diff = (dater - datei).days
                    if diff >= 0:
                        rdate = opn
                        break
                    else:
                        print('Date of submission should be after date of issue !')
                        print('Try again....')
                        continue
            except:
                print('Please enter valid and correct date formate(YYYY/MM/DD) only!!!')
        cur.execute('update ir set dor=%s where sid=%s and bid=%s',(rdate,sid,bid))
        con.commit()
        print('Book submitted.')
        print('No. of days', stud, 'kept the book :', diff)
        if diff <= 15:
            print('No fine!!!')
        elif diff > 15:
            print('Fine to be collected is : Rs', (diff-15)*3)
        else:
            pass
        print('_'*90)
    except:
        print('Something went wrong !!!!')
        print('Try again....')
        submit_book()
    

def remove_student():
    try:
        while 1:
            sid = int(input('Enter student Reg. No : '))
            cur.execute('select sid from students')
            l = []
            for i in cur:
                for j in i:
                    l.append(j)
            if sid not in l:
                print('This id in not valid please try again')
                pass
            else:
                break
        cur.execute('delete from students where sid = %s',(sid,))
        con.commit()
        print('Student removed')
        print('_'*90)
    except:
        print('Something went wrong !!!!')
        print('Try again....')
        remove_student()
    

def remove_book():
    try:
        global total
        while 1:
            bid = int(input('Enter book code : '))
            cur.execute('select bid from books')
            l = []
            for i in cur:
                for j in i:
                    l.append(j)
            if bid not in l:
                print('This book code in not valid please try again')
                pass
            else:
                break
        cur.execute('select total from books where bid = %s',(bid,))
        for i in cur:
            for total in i:
                pass

        while 1:
            print('Enter the no. of books you want to remove\n(or press a to remove all books)')
            t = input(' -> ').lower()
            if t == 'a':
                cur.execute('delete from books where bid = %s',(bid,))
                con.commit()
                print('Book removed')
                break
            elif int(t) <= total:
                cur.execute('update books set total = total-%s where bid = %s',(int(t),bid))
                con.commit()
                break
            else:
                print('Invalid input')
                print('Total no. of books are ', total,)
                print('Please enter valid input')
                pass
        print('_'*90)
    except:
        print('Something went wrong !!!!')
        print('Try again....')
        remove_book()


def display_books():
    print('+', end='')
    print('-' * 60, end='')
    print('+')
    print('| Book code | Book Name            | Author Name     | Total |')
    print('+', end='')
    print('-' * 60, end='')
    print('+')
    cur.execute('select * from books')
    for i in cur:
        print('|', end='')
        print('    ', end='')
        if len(str(i[0])) == 1:
            print('00'+str(i[0]), end='')
            print(' '*4, end='')
        elif len(str(i[0])) == 2:
            print('0'+str(i[0]), end='')
            print(' '*4, end='')
        else:
            print(i[0], end='')
            print(' '*(7 - len(str(i[0]))), end='')
        print('| ', end='')
        print(i[1], end='')
        l_n = 21 - len(i[1])
        print(' '*l_n, end='')
        print('| ', end='')
        print(i[2], end='')
        l_a = 16 - len(i[2])
        print(' '*l_a, end='')
        print('|  ', end='')
        print(i[3], end='')
        l_t = 5 - len(str(i[3]))
        print(' '*l_t, end='')
        print('|')
    print('+', end='')
    print('-' * 60, end='')
    print('+')


def display_students():
    print('+', end='')
    print('-' * 46, end='')
    print('+')
    print('|  Reg. No.  |  Student Name     |  Phone No.  |')
    print('+', end='')
    print('-' * 46, end='')
    print('+')
    cur.execute('select * from students')
    for i in cur:
        print('|     ',end='')
        if len(str(i[0])) == 1:
            print('0'+str(i[0]), end='')
            print(' '*5, end='')
        else:
            print(i[0], end='')
            print(' '*(7 - len(str(i[0]))), end='')
        print('|', end='')
        print('  ', end='')
        print(i[1],end='')
        l_n = 17-len(i[1])
        print(' '*l_n,end='')
        print('|  ',end='')
        print(i[2],end='')
        l_p = 10 - len(str(i[2]))
        print(' '*l_p, end='')
        print(' |') 
    print('+', end='')
    print('-' * 46, end='')
    print('+')


def sn(sid):
    con = mysql.connector.connect(host='localhost', user='root', password='tiger',database='test1') # Please enter password
    cur = con.cursor()
    cur.execute('select * from students')
    l = cur.fetchall()
    sn = None
    for i in l:
        if sid == i[0]:
            sn = i[1]
    return sn


def bn(bid):
    con = mysql.connector.connect(host='localhost', user='root', password='tiger',database='test1') # Please enter password
    cur = con.cursor()
    cur.execute('select * from books')
    l = cur.fetchall()
    bn = None
    for i in l:
        if bid == i[0]:
            bn = i[1]
    return bn


def pn(sid):
    con = mysql.connector.connect(host='localhost', user='root', password='tiger',database='test1') # Please enter password
    cur = con.cursor()
    cur.execute('select * from students')
    l = cur.fetchall()
    pn = None
    for i in l:
        if sid == i[0]:
            pn = i[2]
    return pn


def issue_records():
    con = mysql.connector.connect(host='localhost', user='root', password='tiger',database='test1') # Please enter password
    cur = con.cursor()
    print('+', end='')
    print('-' * 77, end='')
    print('+')
    print('| Reg. No. | Student Name    | Book Name            | Issue Date | Phone No.  |')
    print('+', end='')
    print('-' * 77, end='')
    print('+')
    cur.execute('select * from ir where dor is null')
    lst = cur.fetchall()
    for i in lst:
        print('|    ', end='')
        print(i[1], end='')
        l_i = 6 - len(str(i[1]))
        print(' '*l_i, end='')
        print('| ', end='')
        print(sn(i[1]), end='')
        l_r = 16 - len(sn(i[1]))
        print(' '*l_r, end='')
        print('| ', end='')
        print(bn(i[0]), end='')
        l_n = 21 - len(bn(i[0]))
        print(' '*l_n, end='')
        print('| ', end='')
        print(i[2], end='')
        l_d = 10 - len(str(i[2]))
        print(' '*l_d, end='')
        print(' | ', end='')
        print(pn(i[1]), end='')
        print(' |')
    print('+', end='')
    print('-' * 77, end='')
    print('+')    


def main():
    while True:
        print('''
                                            =========================
                                            WELCOME TO YUVRAJ LIBRARY
                                            _________________________
                                                 LIBRARY MANAGER
                                            -------------------------
                                            1. ADD BOOK
                                            2. ADD STUDENT
                                            3. ISSUE BOOK
                                            4. SUBMIT BOOK
                                            5. REMOVE STUDENT
                                            6. DELETE BOOK
                                            7. DISPLAY BOOKS
                                            8. DISPLAY STUDENTS
                                            9. ISSUE RSCORDS
                                            0. EXIT
                                            __________________________

        ''')
        ch = input('Enter Task No. -> ')
        if ch == '1':
            add_book()
        elif ch == '2':
            add_student()
        elif ch == '3':
            issue_book()
        elif ch == '4':
            submit_book()
        elif ch == '5':
            remove_student()
        elif ch == '6':
            remove_book()
        elif ch == '7':
            display_books()
        elif ch == '8':
            display_students()
        elif ch == '9':
            issue_records()
        elif ch == '0':
            break
        else:
            print('Invalid choice!!!')
            continue


def pswd():
    ps = input('Enter Password : ')
    if ps == '00':
        main()
    else:
        print('Wrong Password!!!')
        pswd()


pswd()

print('''
                                            Thank you for visiting our
                                            ========Library :)========''')








