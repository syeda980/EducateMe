# from crypt import methods
from flask import Flask
from flask_mail import Mail , Message

from flask import render_template, make_response,request,session,redirect, url_for
import os

from model import *
from model.DbHandler import DBHandler

from flask_restful import  Api, Resource
from resources import  routes
from quiz import PopQuiz


app= Flask(__name__)
# app.config.from_object("config")
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'muhammadarsal236@gmail.com'
app.config['MAIL_PASSWORD'] = 'yqlphwspsdmswkuj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



api=Api(app)
routes.initialize_routes(api)

mail = Mail(app);
#myString="mysql+pymysql://root:arsalHussain#10@localhost/test"
def makeHandler():
        return DBHandler(host="educateme.chgckiwfcx1x.eu-north-1.rds.amazonaws.com",username="root",password="",db="educateme")





def getpageContent(courseName,pageName):

    completePageAddress="courses/"+courseName+"/"+pageName

    f = open(completePageAddress, "r")
    pageContent = f.readlines()
    return pageContent






@app.route("/")
def signin():
    # return render_template("cardslayout.html")
    return render_template("welcome.html")
     # return render_template("video.html")


@app.route("/signinPage",methods =["POST","GET"])
def signInPage():
    if request.method=="POST":
        choice=request.form["option"]
        print(choice)
        if choice=="user":
            print("here...")
            response = make_response(render_template("signin.html",msg=None,flag=False ,flag1=True))

            response.set_cookie("accountType", choice)
            return response
        elif choice=="Editor":
            response = make_response(render_template("adminSignIn.html"))
            response.set_cookie("accountType", choice)
            return response


@app.route("/validatesignin", methods=["POST","GET"])
def validateSignIn():
    print(request.method)
    if request.method =="POST":
        email=request.form['email']
        password=request.form['password']
        handler=makeHandler()
        accType=request.cookies.get('accountType')
        if accType=="user":
            if handler.checkUserExist(email,password,accType):
                name=handler.getUserName(email,accType)
                name=name[0]
                noOfCourses=handler.getUserCoursesCount(email,accType)
                noOfCourses=noOfCourses[0]
                print(noOfCourses)
                topCourses = handler.getPriorityCourses()
                if topCourses != -1:
                    response=make_response( render_template("home.html", userName=name, courses=topCourses))
                else:
                    response=make_response( render_template("home.html", userName=name, courses=-1))
                response.set_cookie("userEmail", email)
                response.set_cookie("userNoOfCourses",str(noOfCourses))
                response.set_cookie("userName",name)
                return response
            else:
                print("here")
                return render_template("signin.html",msg="Wrong email or password. Please Try Again",flag=True)
        elif accType=="Editor":
            if handler.checkUserExist(email,password,accType):
                print(accType)
                Id=handler.getEditorId(email)
                name=handler.getUserName(email,accType)
                phoneNo=handler.getEditorPhoneNo(email)
                name = name[0]
                print("here name is: ",name)
                phoneNo=phoneNo[0]
                noOfCourses = handler.getEditorCoursesCount(email)
                print("inside validate signin course count is ",noOfCourses)
                picture = handler.getEditorProfilePic(email)
                print(picture)
                response=make_response(render_template("admin.html",editorName=name,editorEmail=email,phoneNo=phoneNo,courses=None,profilePic=picture,noOfCourses=noOfCourses,Id=Id))
                response.set_cookie("editorId", str(Id))

                response.set_cookie("editorEmail", email)
                response.set_cookie("editorNoOfCourses", str(noOfCourses))
                response.set_cookie("editorUserName", name)
                print(phoneNo)
                response.set_cookie("editorContact",str(phoneNo))
                return response
            else:
                return render_template("adminSignIn.html",msg="Wrong email or password. Please Try Again",flag=True)


@app.route("/homescreen_logo")
def homeScreen_logo():
    email=request.cookies.get("userEmail")
    name=request.cookies.get("userName")
    if email:
        handler = makeHandler()
        topCourses = handler.getPriorityCourses()
        if topCourses != -1:
            return render_template("home.html", userName=name, courses=topCourses)
        else:
            return render_template("home.html", userName=name, courses=-1)
    return "you are not logged in"


@app.route("/homescreen")
def homeScreen():
    email=request.cookies.get("userEmail")
    name=request.cookies.get("userName")
    if email:
        handler=makeHandler()
        topCourses=handler.getPriorityCourses()
        if topCourses!=-1:
            return render_template("home.html",userName=name,courses=topCourses)
        else:
            return render_template("home.html",userName=name,courses=-1)

    else:
        return "you are not logged in"



@app.route("/courses")
def coursesScreen():
    email=request.cookies.get("userEmail")
    name=request.cookies.get("userName")
    if email:
        handler=makeHandler()
        courses=handler.getAllCourses()
        if courses:
            return render_template("courses.html",userName=name,courses=courses)
        else:
            courses=-1
            return render_template("courses.html",userName=name,courses=courses)

    else:
        return "you are not logged in"


@app.route("/aboutus")
def aboutUsScreen():
    email = request.cookies.get("userEmail")
    name = request.cookies.get("userName")
    if email:
        return render_template("aboutus.html", userName=name)
    else:
        return "you are not logged in"

@app.route("/progress")
def progressScreen():
    email = request.cookies.get("userEmail")
    name = request.cookies.get("userName")
    if email:
        handler=makeHandler()
        userId=handler.getUserId(email)
        courses=handler.getCoursesId(userId)
        progressPercent=[]
        print("here111111",courses)
        if courses!=-1:
            for courseId in courses:

                coursePagesCount=handler.getCoursePagesCount(courseId)
                pagesRead=handler.getCourseProgress(courseId,userId)
                if coursePagesCount!=0:
                    actualProgress=int( (pagesRead/coursePagesCount) *100)

                else:
                    actualProgress=0
                progressPercent.append(actualProgress)
                print("course page count",coursePagesCount)

            print(progressPercent)



            print("klajldja",courses)
        # if courses==-1:
        #     return render_template("progress.html",errormsg="you are not enrolled in any course")
        # else:
            userCourses=handler.getUserCourses(courses)
            print(userCourses)
            if userCourses==-1:
                return "You are currently not enrolled in any course. Visit our Courses Page"
            else:
                tempUserCourses=[]
                i=0
                for userCourse in userCourses:

                    tempTuple =(userCourse[0],userCourse[1],progressPercent[i])
                    tempUserCourses.append(tempTuple)
                    i+=1

                print(tempUserCourses)
                userCourses=tempUserCourses
                print("user courses: ",userCourses)

                return render_template("progress.html", userName=name,userCourses=userCourses,errormsg=None,progres=progressPercent)
        else:
                return render_template("progress.html",errormsg="you are not enrolled in any course")

    else:
        return "you are not logged in"

@app.route("/logout")
def logout():
    acctype = request.cookies.get("accountType")
    if acctype=="Editor":
        response=make_response(render_template("welcome.html"))
        response.delete_cookie("editorEmail")
        response.delete_cookie("editorUserName")
        response.delete_cookie("editorNoOfCourses")
        response.delete_cookie("editorContact")
        return response
    elif acctype=="user":
        response = make_response(render_template("welcome.html",msg=None,flag=False))
        response.delete_cookie("userEmail")
        response.delete_cookie("userName")
        response.delete_cookie("userNoOfCourses")
        return response





@app.route("/signup", methods=["POST","GET"])
def validateSignup():
    if request.method=="POST":
        name=request.form["userName"]
        email=request.form["userEmail"]
        password=request.form["userPassword"]

        handler=makeHandler()
        if handler.registerUser(name=name,email=email,password=password):
            return render_template("signin.html")
        else:
            return "Sorry your account registration was not successful"


@app.route('/forgotPassword')
def forgotPwd():
    return render_template('forgotPassword.html')


@app.route('/forgotPwd', methods=['POST','GET'])
def forgotPswd():
     print('heree')
     if request.method == "POST":
        email = request.form["email"]
        handler=makeHandler()
        acctype=request.cookies.get("accountType")
        if acctype=="user":

            res=handler.checkEmailExist(email,acctype)
            print(res)
            if res==True:
                return render_template("resetPassword.html",email=email)
            else:
                return "Email does not exist"
        elif acctype=="Editor":
            res = handler.checkEmailExist(email, acctype)
            print(res)
            if res == True:
                return render_template("resetPassword.html", email=email)
            else:
                return "Email does not exist"
@app.route('/resetPwd', methods=['POST','GET'])
def resetPwd():
     if request.method == "POST":
        pwd = request.form["pwd"]
        email = request.form["email"]
        acctype=request.cookies.get("accountType")
        handler = makeHandler()
        if acctype=="user":
            result=handler.resetPassword(email,pwd,acctype)
            if result==True:
                senderEmail=app.config['MAIL_USERNAME']
                msg = Message('Password Reset', sender=[senderEmail], recipients=[email])
                msg.body = "Your Password has been changed successfully"
                mail.send(msg)
                return render_template("signin.html")
            else:
                return "Sorry your new Password cannot be set at the moment please try again Thanks..."
        elif acctype=="Editor":
            result = handler.resetPassword(email, pwd, acctype)
            if result == True:
                senderEmail = app.config['MAIL_USERNAME']
                msg = Message('Password Reset', sender=[senderEmail], recipients=[email])
                msg.body = "Your Password has been changed successfully"
                mail.send(msg)
                return render_template("adminSignIn.html")
            else:
                return "Sorry your new Password cannot be set at the moment please try again Thanks..."

@app.route("/searchBar",methods=["POST","GET"])
def searchBar():
    if request.method=="POST":
        courseName=request.form["searchBar"]

        handler= makeHandler()
        cardInfo=handler.searchBar(courseName)
        if cardInfo!=-1:
            print(cardInfo[0])
            return render_template("card.html",course=cardInfo)
        else:
            return render_template("coursenotfound.html")


@app.route("/enrollnow" , methods=["POST","GET"])
def enrollNow():
    if request.method=="POST":
        courseName=request.form["enroll"]
        print("dsadsadsa")
        print(courseName)
        handler=makeHandler()
        courseId=handler.getCourseId(courseName)
        email=request.cookies.get("userEmail")
        userId= handler.getUserId(email)

        if handler.checkEnrollmentExist(userId[0],courseId)==-1: # if not enrolled than enroll him
            handler.enrollStudent(userId[0],courseId,email)
            userEmail=handler.getUserEmail(userId)


            return "Enrollment Successful"
        else:

            return "You are already enrolled in this course"


@app.route("/seemore", methods=["POST","GET"])
def seeMore():
    if request.method=="POST":
        courseName=request.form["submit"]
        fileName="courses/"+courseName+"/introduction.txt"
        f=open(fileName,"r")
        pageContent=f.readlines()

    return render_template("seemore.html",courseName=courseName,pageName="introduction",pageContent=pageContent)


@app.route("/suggestion_", methods=["POST","GET"])
def suggestion():
    # if request.method == "POST":
    #     print("hhgf")
    #     name = request.form["userName"]
    #     print(name)
    #     suggestion = request.form["suggestion"]
    #     print(suggestion)
    #     handler = makeHandler()
    #     email = request.cookies.get("userEmail")
    #     sugg = handler.registerSuggestion(suggestion,email)
        return render_template("suggestion.html")
    #     if sugg == True:
    #         return render_template("suggestion.html")
    #     else:
    #         return "not insert"
    # else:
    #     return "error"
@app.route("/suggestionform", methods=["POST","GET"])
def suggestionform():
    if request.method == "POST":
        print("hhgf")
        name = request.form["name"]
        print(name)
        suggestion = request.form["suggestion"]
        print(suggestion)
        handler = makeHandler()
        email = request.cookies.get("userEmail")
        sugg = handler.registerSuggestion(suggestion,email)
        if sugg == True:
            return "Thanks for the suggestion "
        else:
            return "Sorry your suggestion cannot be taken at the moment please try again Thanks..."

    else:
        return "error"

@app.route("/getCourseName")
def getCourseName():
    email = request.cookies.get("editorEmail")
    if email:
        return render_template("adminAddNewCourse.html")
    else:
        return render_template("backToAdminSignIn.html")


@app.route("/adminAddNewCourse" ,methods=["POST","GET"])
def adminAddNewCourse():
    email=request.cookies.get("editorEmail")
    if email:
        if request.method=="POST":
            email=request.cookies.get("editorEmail")
            courseName=request.form["courseName"]
            courseIntro=request.form["courseDescription"]
            print("here is",courseName,"  ",courseIntro)
            handler = makeHandler()
            Id=handler.getEditorId(email)
            print(Id)
            if len(courseIntro)<100:
                try:
                    if handler.checkIfCourseExist(courseName)==False:
                        if handler.registerCourses(courseName,0,0,Id,courseIntro):
                            parentDirectory="courses"
                            directory=courseName
                            path=parentDirectory+"/"+directory
                            print(path)
                            os.mkdir(path)
                            handler.incrementEditorCourse(email)
                            response=make_response(render_template("courseHomePage.html",courseName=courseName,pagesCount=0,pages=[]))
                            # response.set_cookie("courseName",courseName)
                            return response
                        else:
                            return "course registration failed"
                    else:
                        return "Course already exist"
                except Exception as e:
                    print(e)

            else:
                return "Enter course description less than 120 words"
    else:
        return render_template("backToAdminSignIn.html")

@app.route("/getNewPageName", methods=["POST","GET"])
def getNewPageName():
    email=request.cookies.get("editorEmail")
    
    if email:
        if request.method=="POST":
            courseName=request.form["submit"]
           
            # return render_template("getNewPageName.html",courseName=courseName)
            return render_template("insertText.html",courseName=courseName)
    else:
        return render_template("backToAdminSignIn.html")

    return "pages added successfully"
    




@app.route("/addNewPage", methods=["POST","GET"])
def addNewPage():
    email=request.cookies.get("editorEmail")
    if email:
        if request.method=="POST":
            pageName=request.form["pageName"]
            pageContent=request.form["pageContent"]
            # courseName=request.cookies.get("courseName")
            courseName=request.form["submit"]
            print(courseName)
            path="courses/"+courseName+"/"+pageName+".txt"
            f=open(path,"a")
            f.write(pageContent)
            handler=makeHandler()
            courseId=handler.getCourseId(courseName)
            print("courseid is: ",courseId)
            handler.addPage(courseId,pageName)
            pageCount=handler.countCoursePage(courseId)
            handler.incrementCoursePage(courseId, pageCount)
            # make increment user progress function

            pagesName=handler.getCoursePages(courseId)
            pagesName=reversed(pagesName)

            return render_template("courseHomePage.html", courseName=courseName, pages=pagesName, pagesCount=pageCount,pageNum=1)
    else:
        return render_template("backToAdminSignIn.html")

@app.route("/displayCourses")
def displayCourses():
    email=request.cookies.get("editorEmail")
    print(email)
    if email:
        try:
            handler=makeHandler()
            editorEmail=request.cookies.get("editorEmail")
            editorPicture=handler.getEditorProfilePic(editorEmail)
            editorCoursesCount=handler.getEditorCoursesCount(editorEmail)
            editorId=handler.getEditorId(editorEmail)
            courses=handler.getEditorCourses(editorId)
            print(editorId)
            print("courses are",len(courses))
            editorName=request.cookies.get("editorUserName")
            print(editorName)
            editorContact=request.cookies.get("editorContact")
            if len(courses)==0:
                displayCourses=False
                print(editorContact)
                return render_template("admin.html",editorName=editorName,editorEmail=editorEmail,phoneNo=editorContact,courses=courses,profilePic=editorPicture,noOfCourses=editorCoursesCount,Id=editorId,displayCourses=displayCourses)
            else:
                displayCourses=True
                return render_template("admin.html",editorName=editorName,editorEmail=editorEmail,phoneNo=editorContact,courses=courses,profilePic=editorPicture,noOfCourses=editorCoursesCount,Id=editorId,displayCourses=displayCourses)

        except Exception as e:
            print(e)
            return "exception thrown"
    else:
        return render_template("backToAdminSignIn.html")

@app.route("/viewCoursePages", methods=["GET", "POST"])
def viewCoursePages():
    email=request.cookies.get("editorEmail")
    if email:
        if request.method=="POST":
            courseName= request.form["submit"]
            response=make_response()
            # courseName=request.cookies.get("courseName")
            response.set_cookie("courseName", courseName)
            print(courseName)
            handler=makeHandler()

            courseId=handler.getCourseId(courseName)
            pagesName=handler.getCoursePages(courseId)
            pagesCount=handler.countCoursePage(courseId)
            if pagesCount ==-1:
                pagesCount=0
            return render_template("courseHomePage.html",courseName=courseName, pages=pagesName,pagesCount=pagesCount)
    else:
        return render_template("backToAdminSignIn.html")


@app.route("/editorHomePage")
def editorHomePage():
    email=request.cookies.get("editorEmail")
    if email:
        editorName=request.cookies.get("editorUserName")
        editorEmail=request.cookies.get("editorEmail")
        handler=makeHandler()
        noOfCourses=handler.getEditorCoursesCount(editorEmail)

        phoneNo=request.cookies.get("editorContact")
        editorId=request.cookies.get("editorId")
        print("sadnsad",editorId)
        picture=handler.getEditorProfilePic(editorEmail)

        response=make_response(render_template("admin.html", editorName=editorName, editorEmail=editorEmail, phoneNo=phoneNo, courses=None,
                            profilePic=picture, noOfCourses=noOfCourses, Id=editorId))
        response.delete_cookie("courseName")
        return  response
    else:
        return render_template("backToAdminSignIn.html")



@app.route("/getPageAddress", methods=["POST","GET"])
def showPageContent():
    email=request.cookies.get("editorEmail")
    if email:
        try:
            if request.method=="POST":
                pageAddress=request.form["submit"]
                print(pageAddress)
                tempPageAddress=pageAddress.split("/")
                completePageAddress="courses/"+pageAddress
                courseName=tempPageAddress[0]
                pageName=tempPageAddress[1]
                pageName=pageName.split(".txt")[0]
                f=open(completePageAddress,"r")
                pageContent=f.readlines()
                print(pageContent)
                return render_template("displayPageContentEditor.html", pageName=pageName, pageContent=pageContent,courseName=courseName)


        except Exception as e:
            print(e)
    else:
        return render_template("backTOAdminSignin.html")


@app.route("/continueCourse" ,methods=["POST","GET"])
def continueCourse():
    email = request.cookies.get("userEmail")
    if email:
        if request.method == "POST":
            courseName = request.form["submit"]
            # courseName=request.cookies.get("courseName")

            print(courseName)
            handler = makeHandler()

            courseId = handler.getCourseId(courseName)
            pagesName = handler.getCoursePages(courseId)
            pagesCount = handler.countCoursePage(courseId)
            response = make_response(render_template("viewcourseHomePageUser.html", courseName=courseName, pages=pagesName, pagesCount=pagesCount))
            response.set_cookie("courseName", courseName)

            if pagesCount == -1:
                pagesCount = 0
            return response
    else:
        return "you are not logged in"

@app.route("/getPageAddressUser", methods=["POST","GET"])
def showPageContentUser():
    email=request.cookies.get("userEmail")
    if email:
        try:
            if request.method=="POST":
                pageAddress=request.form["submit"]
                print(pageAddress)
                tempPageAddress=pageAddress.split("/")
                completePageAddress="courses/"+pageAddress
                courseName=tempPageAddress[0]
                pageName=tempPageAddress[1]
                f=open(completePageAddress,"r")
                pageContent=f.readlines()
                pageName=pageName.split('.')
                pageName=pageName[0]
                print('helo helo page name',pageName)
                return render_template("displayPageContentUser.html", pageName=pageName, pageContent=pageContent,courseName=courseName)


        except Exception as e:
            print(e)
    else:
        return render_template("home.html")


@app.route("/checkUserProgress", methods=["POST","GET"])
def checkUserProgress():
    try:
        if request.method=="POST":
            courseName=request.cookies.get("courseName")
            print(courseName, 'in check user')
            courseName=courseName
            userEmail=request.cookies.get("userEmail")
            handler=makeHandler()
            userId=handler.getUserId(userEmail)
            courseId=handler.getCourseId(courseName)
            pageName=request.form["submit"]
            pageName=pageName+'.txt'

            if handler.checkCompletedPage(courseId,userId,pageName)== True:
                if handler.insertUserProgress(courseId, userId, pageName) == True:
                    print("progress inserted in table successfully")


            else:
                print("you have already completed this page")


            pageContent=getpageContent(courseName,pageName)
            pageName=pageName.split('.')
            pageName=pageName[0]


            return render_template("displayPageContentUser.html", pageName=pageName, pageContent=pageContent,
                                   courseName=courseName)



    except Exception as e:
        print (e)

@app.route("/deleteCourse", methods=["POST","GET"])
def deleteCourse():
    try:
        if request.method=="POST":
            courseName=request.form["submit"]
            handler=makeHandler()
            editorEmail = request.cookies.get("editorEmail")
            handler.decrementEditorCourseCount(editorEmail)
            courseId = handler.getCourseId(courseName)
            print("courseId", courseId)
            userIds = handler.getuserIds(courseId)
            if userIds:
                print(userIds)
                for userId in userIds:
                    print(userId)
                    userEmail = handler.getUserEmail(userId[0])
                    handler.decrementUserCourse(userEmail)
                    print(userEmail)
            if handler.deleteCourse(courseName):

                print("course deleted")



            else:
                print("course not deleted")
        return "123"
    except Exception as e:
        print(e)


@app.route('/quiz/<courseName>')
def quiz(courseName):
    print('in quiz route',courseName)
    form = PopQuiz()
    if form.validate_on_submit():
        return redirect(url_for('passed'))
    return render_template('quiz.html',courseName=courseName)

@app.route('/passed')
def passed():
    return render_template('passed.html')

@app.route('/displayquiz/<quizdata>')
def quizData(quizdata):
    print('in quiz route',quizdata)
    quizData=quizdata.split('-')
    print(quizData[0])
    d=[]
    for q in quizData:
        d.append(q)
    d=d[:-1]

    
    return render_template("index.html",quizData=d)
    # form = PopQuiz()
    # if form.validate_on_submit():
    #     return redirect(url_for('passed'))
    # return render_template('quiz.html',courseName=courseName)





@app.route("/my/<courseName>" )
def my(courseName):
    handler=makeHandler()

    courseId=handler.getCourseId(courseName)
    pagesName=handler.getCoursePages(courseId)
    pagesCount=handler.countCoursePage(courseId)
    if pagesCount ==-1:
        pagesCount=0
        return render_template("courseHomePage.html",courseName=courseName, pages=pagesName,pagesCount=pagesCount)
    else:
        return render_template("courseHomePage.html",courseName=courseName, pages=pagesName,pagesCount=pagesCount)



if __name__=="__main__":
    app.run(debug=True)

