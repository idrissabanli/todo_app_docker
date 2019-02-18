
    var formData = $("#review_form");
    var loc2 = '{% url 'task:change_task' task.slug %}';
    var message = $("#id_review");
    var chatHolder = $("#chat-item");
    var user = "{{ request.user }}";

    var endpoint2 = wsStart + loc.host + loc2;
    console.log(endpoint);
    console.log(endpoint2);
    var socket2 = new ReconnectingWebSocket(endpoint2);
    var textalign = "text-align: left";
    socket2.onmessage = function(e){
        console.log("message", e);
        var chatDataMsg = JSON.parse(e.data);
        if(user === chatDataMsg.username){
            textalign = "right";
        }else{
            textalign = "left";
        }
        chatHolder.append("<li style ='margin: 6px 0px; text-align: "+ textalign + "'><span class='comment'>" + chatDataMsg.message + " via " + chatDataMsg.username + "</span></li>");
    };

    socket2.onopen = function(e){
        console.log("open", e);
        formData.submit(function (event) {
            event.preventDefault();
            var msgText = message.val();
            // chatHolder.append("<li>" + msgText + " via " + me + "</li>")
            var finalData = {
                'message': msgText
            };
            socket2.send(JSON.stringify(finalData));
            formData[0].reset();
        });
    };
    socket2.onerror = function(e){
        console.log("error", e)
    };
    socket2.onclose = function(e){
        console.log("close", e)
    };
