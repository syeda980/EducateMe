from cgitb import handler
from dataclasses import dataclass
from flask import request, Response, jsonify,render_template
from flask_restful import Resource


from model.DbHandler import DBHandler
# class VehiclesApi(Resource):
#     def get(self):
#
#         buses=Vehicle.objects().to_json()
#         return Response(buses, mimetype="application/json", status=200)
#     def post(self):
#         body=request.get_json()
#         #veh=Vehicle(**body).save()
#         veh = Vehicle(reg=body["reg"],model=body["model"]).save()
#         id=veh.id
#         return {'id':str(id)},200
#
# class VehicleApi(Resource):
#     def get(self,id):
#         veh=Vehicle.objects.get(id=id).to_json()
#         return Response(veh,mimetype="application/json",status=200)
#     def put(self,id):
#         body=request.get_json()
#         Vehicle.objects.get(id=id).update(**body)
#         return {'id':str(id)},200
#     def delete(self,id):
#         Vehicle.objects.get(id=id).delete()
#
#
# class Test(Resource):
#     def get(self):
#         return jsonify({"msg":"Hello World"})
#
#     def post(self):
#         data = request.get_json()  # status code
#         print(data)
#         data.update(name="Sanam")
#         data.update(magic=78952369841)
#         data.update(sep="operator")
#         return data, 201



def makeHandler():
        return DBHandler(host="localhost",username="root",password="arsalHussain#10",db="educateme")

class suggestionsApi(Resource):
    def post(self):
        data = request.get_json()  # status code
        print(data)
        print("inm post api")
        print(data["name"])
        name=data["name"]
        text=data["suggestion"]
        handler=DBHandler(host="localhost",username="root",password="arsalHussain#10",db="educateme")
        email = request.cookies.get("userEmail")
        print("emain in api",email)

        handler.registerSuggestion(email=email,text=text)


class createPageFileApi(Resource):
    def post(self):
        data=request.get_json()
        pageName=data['pagename']
        courseName=data['coursename']
        pageContent=data['pagecontent']
        path = "courses/" + courseName + "/" + pageName + ".txt"
        f = open(path, "a")
        f.write(pageContent)
        handler = makeHandler()
        courseId = handler.getCourseId(courseName)
        handler.addPage(courseId, pageName)
        pageCount = handler.countCoursePage(courseId)
        handler.incrementCoursePage(courseId, pageCount)
        # make increment user progress function

        pagesName = handler.getCoursePages(courseId)
        pagesName = reversed(pagesName)

class viewCourseApi(Resource):
    def post(self):
        data=request.get_json()
        courseName=data['courseName']

    
        handler=makeHandler()

        courseId=handler.getCourseId(courseName)
        pagesName=handler.getCoursePages(courseId)
        pagesCount=handler.countCoursePage(courseId)
        print(courseName,'in apiii')

        print(pagesName,'in apiii')
        print(pagesCount,'in apiii')

        return{'courseName':courseName, 'pageName':pagesName,'pageCount':pagesCount}


       




class insertTextApi(Resource):
    def post(self):
        print("inside api")
        data=request.get_json()
        print(data)
        courseName=data["1"];
        print((data["1"]))
        courseName=courseName.split("-")
        courseName=courseName[1]
        pageName=data["2"]
        pageName=pageName.split("-")
        pageName=pageName[1]

        print("coursename",courseName)
        print("pagename", pageName)


        path = "courses/" + courseName + "/" + pageName + ".txt"
        f = open(path, "a")
        pageContent=[]
        for i,v in data.items()  :
            if i>"3"  :
                tag=v.split("-")
                openingtag= "<"+ tag[0]+">"
                tagText=tag[1]
                closingTag="</"+tag[0]+">"
                completeText=openingtag+tagText+closingTag
                f.write(completeText)
                f.write('\n');


        # print(pageContent)
        # tup_dict = dict(pageContent)  # {'hi': 'bye', 'one': 'two'}
        # tup_dict.pop('courseName')
        # tup_dict.pop('pageName')
        # print(tup_dict)

        # f.write(pageContent)
        handler = makeHandler()
        courseId = handler.getCourseId(courseName)
        handler.addPage(courseId, pageName)
        pageCount = handler.countCoursePage(courseId)
        handler.incrementCoursePage(courseId, pageCount)
        # make increment user progress function

        pagesName = handler.getCoursePages(courseId)
        pagesName = reversed(pagesName)
        return {'courseName':courseName}
        str=""




class deleteCourseApi(Resource):
    def post(self):
        data = request.get_json()  # status code
        courseName=data["courseName"]

        handler=DBHandler(host="localhost",username="root",password="arsalHussain#10",db="educateme")
        editorEmail = request.cookies.get("editorEmail")
        handler.decrementEditorCourseCount(editorEmail)
        courseId = handler.getCourseId(courseName)
        print("courseId", courseId)
        userIds = handler.getuserIds(courseId)
        print('user idsssss',userIds)
        if userIds!=-1:
            for userId in userIds:
                print(userId)
                userEmail = handler.getUserEmail(userId[0])
                handler.decrementUserCourse(userEmail)
                print(userEmail)
        if handler.deleteCourse(courseName):

            print("course deleted")
            return {"msg":"true"};
        else:
            return {"msg":"false"}





class EnrollApi(Resource):
    def post(self):
        data=request.get_json()
        print('inenroll api',data);

        courseName=data['courseName'];
        handler = makeHandler()
        courseId = handler.getCourseId(courseName)
        email = request.cookies.get("userEmail")
        print(email)
        userId = handler.getUserId(email)


        if handler.checkEnrollmentExist(userId[0], courseId) == -1:  # if not enrolled than enroll him
            handler.enrollStudent(userId[0], courseId, email)
            userEmail = handler.getUserEmail(userId)

            return jsonify({"msg":"True"})
        else:

            return jsonify({"msg":"False"})


class EditorViewCoursesApi(Resource):
    def post(self):
        print('editor email in api');

        editorEmail=request.get_json()
        editorEmail=editorEmail['email']
        print('editor email in api',editorEmail)

        handler=DBHandler(host="localhost",username="root",password="arsalHussain#10",db="educateme")
        editorPicture=handler.getEditorProfilePic(editorEmail)
        editorCoursesCount=handler.getEditorCoursesCount(editorEmail)
        editorId=handler.getEditorId(editorEmail)
        courses=handler.getEditorCourses(editorId)
        print('in api',courses)
        return courses;
 
        # ab db handler se function call krna hau

class checkCourseExistEditor(Resource):
    def post(self):
        data=request.get_json()
        courseName=data['courseName']
        editorEmail=data['editorEmail']
        handler=DBHandler(host="localhost",username="root",password="arsalHussain#10",db="educateme")
        editorId=handler.getEditorId(editorEmail)
        flag= handler.checkIfCourseExistEditor(courseName,editorId)
        if flag == True:
            return {'msg':1}
        else:
            return {'msg':0}

class insertQuestion(Resource):
    def post(self):
        data=request.get_json();
        courseName=data['courseName'];
        question=data['question'];
        correctOption=data['correctOption'];
        option1  =data['option1'];
        option2=data['option2'];
        option3=data['option3'];
        option4=data['option4'];

        handler=DBHandler(host="localhost",username="root",password="arsalHussain#10",db="educateme")

        flag=handler.insertQuestion(courseName,question,correctOption,option1,option2,option3,option4)

        if flag==True:
            return {'msg':1}
        else:
            return {'msg':0}

class takeQuiz(Resource):
    def post(self):
        print('in take quiz api')
        data=request.get_json()
        courseName=data['courseName']
        # progress=data['progress']
        handler=DBHandler(host="localhost",username="root",password="arsalHussain#10",db="educateme")
        rows=handler.getQuiz(courseName)

        return {'quiz':rows}
    










