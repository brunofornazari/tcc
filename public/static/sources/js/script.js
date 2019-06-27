$(document).ready(function(){

   var socket = io.connect('http://127.0.0.1:5000');

   socket.on('connect', function(){
        socket.send('User has connected!');
   });
   socket.on('message', function(msg){
        if(msg !== '' && msg.length !== 0){
            $('#messages').html(msg);
        }

   });

   socket.on('user-creation-complete', function(msg){
        if(msg !== '' && msg.length !== 0){
            $('#messages').html(msg);
            $('.createUser-form').show();
        }

   });

   $('#createUser').on('click', function(){
        var sNome = $('#nome').val();
        if(sNome){
            socket.emit('register-user', sNome);
            $('.createUser-form').hide();
        } else {
            alert('O nome é obrigatório!')
        }


   });

});