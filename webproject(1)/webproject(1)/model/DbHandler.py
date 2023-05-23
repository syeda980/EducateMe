from ast import Try
from cgitb import handler
from logging import handlers
import queue
from turtle import update
import pymysql
from pymysql import connections, cursors
# from sqlalchemy import false
from datetime import date

class DBHandler:
    def __init__(self,host,username,password,db):
        self.host=host
        self.username=username
        self.password=password
        self.db=db
        self.connection= pymysql.Connect(host=self.host,user=self.username,password=self.password,database=self.db)

    def checkUserExist(self, email,password,acctype):
        try:
            cur = self.connection.cursor()
            if acctype=="user":
                query = "select * from users where user_email = %s and user_password = %s";
                args = (email,password)
                cur.execute(query, args)
                rows = cur.fetchall()
                if rows:
                    return True
                return False
            elif acctype=="Editor":
                query = "select * from editors where editor_email = %s and editor_password = %s";
                args = (email, password)
                cur.execute(query, args)
                rows = cur.fetchall()
                if rows:
                    return True
                return False
        except Exception as e:
            print (e)
        finally:
            if cur!=None:
                cur.close()

    def checkUserAccountAlreadyExist(self,email):
        try:
            cur = self.connection.cursor()
            query = "select * from users where user_email = %s ";
            args = (email)
            cur.execute(query, args)
            rows = cur.fetchall()
            if rows:
                return False
            return True
        except Exception as e:
            print (e)
        finally:
            if cur!=None:
                cur.close()



    def registerUser(self,name,email,password):
        try:
            if self.checkUserAccountAlreadyExist(email=email)==False:
                return False
            cur=self.connection.cursor()
            query="Insert into users (user_name, user_email,user_password) values (%s,%s,%s)"
            args=(name,email,password)
            cur.execute(query,args)
            self.connection.commit()
            self.connection.close()
            cur.close()
            return True
        except Exception as e:
            print(e)
            cur.close()
            self.connection.close()
            return False
    def registerEditor(self,name,email,password,contact):
        try:
            cur=self.connection.cursor()
            noOfCourses=0
            query="Insert into editors (editor_name, editor_email,editor_password,editor_contact,editor_courses) values(%s,%s,%s,%s,%s) "
            args=(name,email,password,contact,noOfCourses)
            cur.execute(query,args)
            self.connection.commit()
            self.connection.close()
            cur.close()
            return True
        except Exception as e:
            print(e)
            self.connection.close()
            cur.close()
            return False

    def registerCourses(self,c_name,c_pages,c_students,e_id,courseIntro):
        try:
            cur=self.connection.cursor()
            query="Insert into courses (course_name,course_pages,students_enrolled,editor_id,course_intro) values(%s,%s,%s,%s,%s)"
            args=(c_name,c_pages,c_students,e_id,courseIntro)
            cur.execute(query,args)
            self.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(e)
            cur.close()
            return False



    def registerSuggestion(self,text,email):
        try:
            id=self.getUserId(email)
            id=id[0]
            cur=self.connection.cursor()
            if id!=-1:
                query=" insert into suggestions (suggestion_date, suggestion_text, user_id) values (%s,%s,%s)"
                currentDate=date.today()
                args=(currentDate, text,id)
                cur.execute(query,args)
                self.connection.commit()
                return True
            else:
                cur.close()
                self.connection.close()
                return False
        except Exception as e:
            print("Error suggestion not uploaded",e)

            return False
    def getUserId(self, email):
        try:
            cur=self.connection.cursor()
            query="select user_id from users where user_email=%s"
            args=(email)
            cur.execute(query,args)
            row=cur.fetchone()
            if row:
                return row
            else:
                cur.close()
                return -1
        except Exception as e:
            print(e)

            return -1

    def getUserName(self, email,acctype):
        try:
            cur = self.connection.cursor()
            if acctype=="user":
                query = "select user_name from users where user_email=%s"
                args = (email)
                cur.execute(query, args)
                row = cur.fetchone()
                if row:
                    return row
                else:
                    cur.close()
                    self.connection.close()
                    return -1
            elif acctype=="Editor":
                query = "select editor_name from editors where editor_email=%s"
                args = (email)
                cur.execute(query, args)
                row = cur.fetchone()
                if row:
                    return row
                else:
                    cur.close()
                    self.connection.close()
                    return -1
        except Exception as e:
            print(e)

            return -1

    def getUserCoursesCount(self, userEmail,acctype):
        try:
            cur = self.connection.cursor()
            if acctype=="user":
                query = "select user_courses from users where user_email=%s"
                args = (userEmail)
                cur.execute(query, args)
                row = cur.fetchone()
                if row:
                    return row
                else:
                    cur.close()
                    return -1
            elif acctype=="Editor":
                query = "select editor_courses from editors where editor_email=%s"
                args = (userEmail)
                cur.execute(query, args)
                row = cur.fetchone()
                if row:
                    return row
                else:
                    cur.close()
                    return -1

        except Exception as e:
            print(e)

            return -1




    def getStudentsEnrolled(self,c_id):
        try:
            cur=self.connection.cursor()
            query="select students_enrolled from courses where course_id= %s"
            args=(c_id)
            row=cur.execute(query,args)
            rows=cur.fetchone()
            if rows:
                cur.close()
                return rows[0]
            else:

                cur.close()
                return -1
        except Exception as e :
            print(e)
            return -1

    def incrementStudent(self,c_id):
        coursesCount =self.getStudentsEnrolled(c_id)
        coursesCount=coursesCount+1

        try:
            cur=self.connection.cursor()
            query="update courses set students_enrolled=%s where course_id=%s;"
            args=(coursesCount,c_id)
            result=cur.execute(query,args)
            if result==1:
                self.connection.commit()
                cur.close()
                return True
            else:
                return False

        except Exception as e:
            print(e)
            self.connection.close()
            cur.close()

    # editor_courses count update
    def getEditorCoursesCount(self, e_email):
        try:
            print(type(e_email))
            print(e_email)
            cur=self.connection.cursor()
            query=" select editor_courses from editors where editor_email = %s ;"
            args=(e_email)
            cur.execute(query,args)
            courseCount=cur.fetchone()
            print("courses count", courseCount)
            return courseCount[0]

        except Exception as e:
            print(e)
    def incrementEditorCourse(self,e_email):

        try:
            cur=self.connection.cursor()
            coursesCount = self.getEditorCoursesCount(e_email)
            coursesCount = coursesCount + 1
            query="update editors set editor_courses=%s where editor_email=%s;"
            args=(coursesCount,e_email)
            cur.execute(query,args)
            self.connection.commit()
            return True

        except Exception as e:
            print(e)
            return False



    def searchBar(self,courseName):
            try:
                cur = self.connection.cursor()
                query = "Select course_name, course_intro from courses where course_name=%s"
                arg=(courseName)
                cur.execute(query,arg)
                rows= cur.fetchone()

                self.connection.close()
                cur.close()
                if rows:
                    print(rows)
                    return rows
                else:
                    return -1
            except Exception as e:
                print(e)
                self.connection.close()
                cur.close()
                return False

    def getAllCourses(self):
        try:
            cur=self.connection.cursor()
            query="select course_name, course_intro from courses"
            cur.execute(query)
            rows=cur.fetchall()
            print(rows[0])
            self.connection.close()
            cur.close()
            return rows

        except Exception as e:
            print(e)

    def getCoursesId(self,userId):
        try:
            cur=self.connection.cursor()
            query=" select course_id from enrollment where user_id =%s"
            args=(userId)
            cur.execute(query,args)
            rows=cur.fetchall()
            cur.close()
            if rows:
                return rows
            else:
                return -1
        except Exception as e:
            print(e)

    def getUserCourses(self,coursesIds):
        try:
            cur=self.connection.cursor()
            list=[]
            i=0
            for id in coursesIds:
                print("id is:",id)
                realId=id[0]

                query=" Select course_name, course_intro from courses where course_id= %s;"
                args=(realId)
                cur.execute(query,args)
                row=cur.fetchone()
                print(row)
                list.append(row)


            print(list)
            if list:
                return list
            else:
                return -1
        except Exception as e:
            print(e,"in exception")

    def checkEnrollmentExist(self, userId, course_id):
        try:
            cur = self.connection.cursor()
            query = "Select course_id, user_id from enrollment where course_id = %s and user_id=%s"
            args = (course_id, userId)
            res = cur.execute(query, args)
            print("userId: ",userId)
            print("courseid: ", course_id)

            rows = cur.fetchall()
            print(rows)
            cur.close()
            if rows:
                return rows
            else:
                return -1
        except Exception as e:
            print (e)

    def getPriorityCourses(self):
        try:
            cur=self.connection.cursor()
            studentsEnrolled=-1
            query="select  course_name,course_intro,students_enrolled from courses ORDER BY students_enrolled desc LIMIT 3;"
            # args=(studentsEnrolled)
            cur.execute(query)
            rows= cur.fetchall()
            print(rows)
            cur.close()
            if rows:
                return rows
            else:
                return -1

        except Exception as e:
            print(e)

    # def enroll(self, userEmail):
    #     try:
    #         userId = self.getUserId(userEmail)
    #         self.checkEnrollmentExist()
    #         cur = self.connection.cursor()
    #         query =
    #
    #     except Exception as e:
    #         print (e)


    def getCourseId(self, courseName):
        try:
            cur=self.connection.cursor()
            query=" select course_id from courses where course_name= %s;"
            args=(courseName)
            cur.execute(query,args)
            rows=cur.fetchone()
            cur.close()
            print( "row", rows[0])
            return rows[0];


        except Exception as e:
            print(e)

    def enrollStudent(self,userId,courseId,userEmail):
        try:
            cur=self.connection.cursor()
            #make and call progress function
            query="Insert into enrollment (user_id,course_id, pages_read ) values(%s,%s,%s);"
            pagesRead=0
            args=(userId,courseId,pagesRead)
            cur.execute(query,args)
            self.connection.commit()
            self.incrementUserCourse(userEmail)
            studentsEnrolled= self.getStudentsEnrolled(courseId)
            print("here",studentsEnrolled)
            res=self.incrementStudent(courseId)
            print(res)

            #write increment students enrolled func
            cur.close()


        except Exception as e:
            print(e)

    def checkEmailExist(self,email,acctype): #for reset password purpose return true if email exist
        try:
            if self.connection!=None:
                cur = self.connection.cursor()
                if acctype=="user":
                    query="select user_email from users where user_email=%s"
                    args=(email)
                    cur.execute(query, args)
                    rows=cur.fetchone()
                    print("here rows is: ",rows)
                    if rows:
                        cur.close()
                        return True
                    else:
                        return False
                elif acctype=="Editor":
                    query = "select editor_email from editors where editor_email=%s"
                    args = (email)
                    cur.execute(query, args)
                    rows = cur.fetchone()
                    print("here rows is: ", rows)
                    if rows:
                        cur.close()
                        return True
                    else:
                        return False
        except Exception as e:
            print(e)

    def resetPassword(self,email,pwd,acctype):
        try:
            if self.connection!=None:
                cur=self.connection.cursor()
                if acctype=="user":
                    query='update users set user_password=%s where user_email=%s'
                    args=(pwd,email)
                    res=cur.execute(query,args)
                    if res==1:
                        cur.close()
                        self.connection.commit()
                        return True
                    else:
                        return False
                elif acctype=="Editor":
                    query = 'update editors set editor_password=%s where editor_email=%s'
                    args = (pwd, email)
                    res = cur.execute(query, args)
                    if res == 1:
                        cur.close()
                        self.connection.commit()
                        return True
                    else:
                        return False

        except Exception as e:
            print(str(e))

    def incrementUserCourse(self,userEmail):
        coursesCount =self.getUserCourseCount(userEmail)
        coursesCount=coursesCount[0]
        coursesCount=coursesCount+1
        print(coursesCount)

        try:
            cur=self.connection.cursor()
            query="update users set user_courses =%s where user_email=%s;"
            args=(coursesCount,userEmail)
            result=cur.execute(query,args)
            self.connection.commit()
            if result==1:
                return True
            else:
                return False

        except Exception as e:
            print(e)
            self.connection.close()
            cur.close()

    def checkIfCourseExist(self, courseName):
        try:
            cur=self.connection.cursor()
            query=" select course_name from courses where course_name= %s"
            args=(courseName)
            cur.execute(query,args)
            row=cur.fetchone()
            cur.close()
            if row:
                return True
            else:
                return False



        except Exception as e:
            cur.close()
            print(e)


    def checkIfCourseExistEditor(self, courseName,editorId):
        try:
            cur=self.connection.cursor()
            query=" select course_name from courses where course_name= %s and editor_id=%s "
            args=(courseName,editorId)
            cur.execute(query,args)
            row=cur.fetchone()
            cur.close()
            if row:
                return True
            else:
                return False



        except Exception as e:
            cur.close()
            print(e)

    def insertQuestion(self,courseName,question,correctOption,option1,option2,option3,option4):
        try:
            cur=self.connection.cursor();
            courseId=self.getCourseId(courseName=courseName)

            query="insert into quizzes (course_id,question,option1,option2,option3,option4,correct_answer) values(%s,%s,%s,%s,%s,%s,%s);"
            args=(courseId,question,option1,option2,option3,option4,correctOption)
            result=cur.execute(query,args)
            if result==1:
                self.connection.commit()
                return True;
            else:
                print('Question not added')
                return False


        except Exception as e:
            print('Question not added')
            print(e);
            return False


    def getEditorPhoneNo(self,email):
        try:
            cur=self.connection.cursor()
            query = "select editor_contact from editors where editor_email=%s"
            args = (email)
            cur.execute(query, args)
            row = cur.fetchone()
            if row:
                return row
            else:
                cur.close()
                self.connection.close()
                return -1
        except Exception as e :
            print(str(e))
            cur.close()

    def getEditorId(self,email):
        try:
            cur=self.connection.cursor()
            query = "select editor_id from editors where editor_email=%s"
            args = (email)
            cur.execute(query, args)
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                cur.close()
                self.connection.close()
                return -1
        except Exception as e :
            print(str(e))
            cur.close()

    def getEditorCourses(self,editorId):
        try:
            cur=self.connection.cursor()
            print(editorId)
            query="select course_id, course_name, course_pages, students_enrolled from courses where editor_id=%s"
            args=(editorId)
            cur.execute(query,args)
            rows=cur.fetchall()
            cur.close()
            if rows:
                return rows
            else:
                return rows

        except Exception as e:
            print(e)

    def getEditorProfilePic(self,email):
        try:
                cur=self.connection.cursor()
                query = "select editor_picture from editors where editor_email=%s"
                args = (email)
                cur.execute(query, args)
                row = cur.fetchone()
                if row:
                    return row[0]
                else:
                    cur.close()
                    self.connection.close()
                    return -1
        except Exception as e :
                print(str(e))
                cur.close()

    def addPage(self, courseId, pageName):
        try:
            cur=self.connection.cursor()
            print("hereee coursename and page name is: ", courseId,"    ",pageName)
            query=" INSERT INTO COURSEPAGES (course_id, page_name) VALUES (%s,%s)"
            args=(courseId,pageName)
            cur.execute(query,args)
            self.connection.commit()
            print("page added in database also")
            cur.close()

        except Exception as e:
            print(e)

    def countCoursePage(self,courseId):
        try:
            cur=self.connection.cursor()
            query= " select COUNT(course_id) from coursepages where course_id = %s"
            args=(courseId)
            cur.execute(query,args)
            pageCount=cur.fetchone()
            print(pageCount)
            return pageCount[0]

        except Exception as e:
            print(e)

    def incrementCoursePage(self,courseId,pageCount):
        try:
            cur=self.connection.cursor()
            query="update courses set course_pages=%s where course_id=%s; "
            args=(pageCount,courseId)
            cur.execute(query,args)
            self.connection.commit()
            print("course pages incremented successfully")


        except Exception as e:
            print(e)

    def getCoursePages(self,courseId):
        try:
            cur=self.connection.cursor()
            query="select page_name from coursepages where course_id = %s"
            args=(courseId)
            cur.execute(query,args)
            pagesName=cur.fetchall()
            cur.close()
            if pagesName:
                return pagesName
            else:
                return -1
        except Exception as e:
            print(e)

    def checkCompletedPage(self,courseId,userId,pageName):
        try:
            cur=self.connection.cursor()
            query=" SELECT * from userprogress where course_id=%s and user_id = %s and page_name = %s ;"
            args=(courseId, userId, pageName)

            cur.execute(query, args)
            row= cur.fetchone()
            cur.close()
            if row:
                return False
            else:
                return True

        except Exception as e:
            print(e)

    def insertUserProgress(self,courseId, userId,pageName):
        try:
            cur=self.connection.cursor()
            userId=userId[0]
            query="INSERT INTO userprogress (user_id, course_id, page_name) VALUES (%s,%s,%s) ;"
            args=(userId,courseId,pageName)
            cur.execute(query,args)
            self.connection.commit()

            coursePagesCount=self.getCoursePagesCount(courseId)
            pagesRead=self.getCourseProgress(courseId,userId)
            if coursePagesCount!=0:
                actualProgress=int( (pagesRead/coursePagesCount) *100)

            else:
                    actualProgress=0

            actualProgress=str(actualProgress)+'%'
            self.updatePageRead(userId,courseId,pagesRead,actualProgress)


            cur.close()
            return True

        except Exception as e:
            print(e)
            return False
    

    def getCourseProgress(self,courseId, userId):
        try:
            cur=self.connection.cursor()
            query="SELECT COUNT(*) FROM userprogress where course_id = %s and user_id = %s ;"
            args=(courseId, userId)
            cur.execute(query,args)
            count=cur.fetchone()
            return count[0]

        except Exception as e:
            print(e)

    def getCoursePagesCount(self,courseId):
        try:
            cur=self.connection.cursor()
            query="SELECT course_pages from courses where course_id = %s"
            args=(courseId)
            cur.execute(query,args)
            count=cur.fetchone()
            return count[0]
        except Exception as e:
            print(e)

    def decrementEditorCourseCount(self,e_email):

        try:
            cur=self.connection.cursor()
            coursesCount = self.getEditorCoursesCount(e_email)
            coursesCount = coursesCount - 1
            query="update editors set editor_courses=%s where editor_email=%s;"
            args=(coursesCount,e_email)
            cur.execute(query,args)
            self.connection.commit()
            return True

        except Exception as e:
            print(e)
            return False

    def deleteCourse(self,courseName):
        try:
            cur=self.connection.cursor()
            query=" DELETE from courses where course_name= %s"
            args=(courseName)
            cur.execute(query,args)
            self.connection.commit()
            cur.close()
            return True

        except Exception as e:
            print(e)
            return False

    def getuserIds(self,courseId):
        try:
            cur = self.connection.cursor()
            query = " select DISTINCT user_id from enrollment where course_id =%s"
            args = (courseId)
            cur.execute(query, args)
            rows = cur.fetchall()
            cur.close()
            if rows:
                return rows
            else:
                return -1

        except Exception as e:
            print(e)
            return -1

    def decrementUserCourse(self,userEmail):
        coursesCount =self.getUserCourseCount(userEmail)
        coursesCount=coursesCount[0]
        coursesCount=coursesCount-1
        print(coursesCount)

        try:
            cur=self.connection.cursor()
            query="update users set user_courses =%s where user_email=%s;"
            args=(coursesCount,userEmail)
            result=cur.execute(query,args)
            self.connection.commit()
            if result==1:
                return True
            else:
                return False

        except Exception as e:
            print(e)
            self.connection.close()
            cur.close()

    def getUserEmail(self, userId):
        try:
            cur=self.connection.cursor()
            query="select user_email from users where user_id=%s"
            args=(userId)
            cur.execute(query,args)
            row=cur.fetchone()
            if row:
                return row
            else:
                cur.close()
                return -1
        except Exception as e:
            print(e)

            return -1

    def getUserCourseCount(self, u_email):
        try:
            print(type(u_email))
            print(u_email)
            cur=self.connection.cursor()
            query=" select user_courses from users where user_email = %s ;"
            args=(u_email)
            cur.execute(query,args)
            courseCount=cur.fetchone()
            print("courses count", courseCount)
            return courseCount

        except Exception as e:
            print(e)

    def updatePageRead(self,userId,courseId,pagesRead,progress):
        try:
            cur=self.connection.cursor()
            print(userId,"in page read")
            print(courseId,"in page read")
            print(pagesRead,"in page read")
            print(progress,"in page read")

            query="update enrollment set pages_read=%s, progress= %s where course_id = %s and user_id= %s; "



            # query=" insert into enrollment (pages_read, progress)  values (%s,%s) where course_id = %s and user_id= %s;"
            args=(pagesRead,progress,courseId,userId)
            result=cur.execute(query,args)
            self.connection.commit()
            


        except Exception as e:
            print(e)

    def getQuiz(self,courseName):
        try:
            cur=self.connection.cursor()
            courseId=self.getCourseId(courseName)
            print(courseId,'in db')

            print(courseName,'in db')
            query="select * from quizzes where course_id =%s"
            args=(courseId)
            cur.execute(query,args)
            rows=cur.fetchall()
            print(rows)
            return rows

        except Exception as e:
            print(e)






