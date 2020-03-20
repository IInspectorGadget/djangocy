function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
// const forms = document.querySelector('form[name=filter]');
        // d = new URLSearchParams(new FormData(forms)).toString();



const clickMeButton = document.querySelector("#message_submit");




clickMeButton.addEventListener("click", function getMessage(){
    const user_id = document.querySelector(".profile__opinion").dataset.id
    $.ajax({
        
          type: 'POST',
        
          url: 'submit',
        
          data: {
                csrfmiddlewaretoken: CSRF_TOKEN,
                'id' : user_id,
                message : document.querySelector('#textarea').value,
               },
        
          success: function(response){
            alert($(".chat-messages"))
            $(".chat-messages").append('<div class="messages-item"><img src=' + response.image + ' alt=""><div><p>' + response.username + '</p><p>' + response.message.message + '</p></div></div>');
          },
        
         
        
        });
        
    


    // axios({
    //   method: 'post',
    //   url: "http://127.0.0.1:8000/profile/admin/chats/1/submit",
    //   data: {
    //     my : {
    //         id : user_id,
    //         message : document.querySelector('#textarea').value,
    //     }
        
    //   },
  
    // })
    //   .then((response) => {

    //     $(".chat-messages").append('<div class="messages-item"><img src=' + response.data.image + ' alt=""><div><p>' + response.data.username + '</p><p>' + response.data.message.message + '</p></div></div>');

    

    //   })
    //   .catch((response) => {
    //     alert('y');
    //   })
      
});



