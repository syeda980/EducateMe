
           <script src="https://code.jquery.com/jquery-3.6.1.min.js" integrity="sha256-o88AwQnZB+VDvE9tvIXrMQaPlFFSUTR+nldQm1LuPXQ=" crossorigin="anonymous"></script>

        function getCourseName(courseName){
        alert(courseName);

        }

        function fun(e){
            console.log(e);

            var courseName =e['value'];
            console.log(courseName);



            var data={}
        data["courseName"]=courseName
        courseName=JSON.stringify(data)
        console.log('in enroll script',courseName);




        $.ajax({
                url: '/api/enroll', // url where to submit the request
                type : "post", // type of action POST || GET

                data : courseName, // post data || get data
                dataType : 'json',
                contentType: "application/json; charset=utf-8",

                success : function(result) {
                    // you can see the result from the console
                    // tab of the developer tools
                    console.log(result)

                    result=result['msg']
                    if (result=="True")
                    {
                        alert("Enrollment Successful")
                    }
                    else{
                        alert("You are already enrolled in this course")


                    }
                },
                error: function(xhr, resp, text) {
                    console.log("error idhr");
                    console.log(xhr, resp, text);
                    alert("Enrollment Failed")
                }
            })




        $(document).ready(function(){
        // click on button submit
        $("#submit").on('click', function(e){
        	e.preventDefault();
            // send ajax
            console.log('in script');






        });
    });

    }





