from .resources import EnrollApi, checkCourseExistEditor, deleteCourseApi, insertQuestion, insertTextApi, suggestionsApi,EditorViewCoursesApi, takeQuiz, viewCourseApi

def initialize_routes(api):
    # api.add_resource(VehiclesApi, '/api/buses')
    # api.add_resource(Test, "/api/test")
    # api.add_resource(VehicleApi, "/api/bus/<id>")
    api.add_resource(suggestionsApi, '/api/registerSuggestion')
    api.add_resource(EditorViewCoursesApi,'/api/displayEditorCourses')
    api.add_resource(EnrollApi,'/api/enroll')
    api.add_resource(deleteCourseApi,'/api/deletecourseapi')
    api.add_resource(insertTextApi,'/api/inserttextapi')
    api.add_resource(viewCourseApi,'/api/viewcourseapi')
    api.add_resource(checkCourseExistEditor,'/api/checkcourseexisteditor')
    api.add_resource(insertQuestion,'/api/insertquestion')
    api.add_resource(takeQuiz,'/api/takequiz')

    #api.add_resource(Square, '/square/<int:num>')