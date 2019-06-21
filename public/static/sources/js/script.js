$(document).ready(function(){

   var socket = io.connect('http://127.0.0.1:5000');

   socket.on('connect', function(){
        socket.send('User has connected!');
   });
   socket.on('message', function(msg){
        if(msg !== '' && msg.length !== 0){
            $('#messages').html(msg);
            console.log('msg', msg);
        }

   });

   $('#sendButton').on('click', function(){
        socket.send($('#myMessage').val());
        $('#myMessage').val('');
   });

});