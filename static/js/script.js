$(document).ready(function(){
    var answer = null;    
    var username;
    var socket = undefined;

    $('#name-text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            socket = io.connect('/race');
            
            name = $('#name-text').val();
            username = name;

            socket.on('newQuestion', function(data) {
                $("#answer").val("");
                $("#race-input").fadeOut(250, () => {
                    $("#race-input").fadeIn(250);
                    $("#answer").focus();
                });
                $("#number-1").text(data.num1);
                $("#number-2").text(data.num2);
                $("#action").text(data.action);
        
                answer = data.answer;
            });
        
            socket.on('updateBoard', function(data) {
                $(".board").html("");
                data.forEach(e => {
                    $(".board").append(`
                    <div class="board-user">
                            <div class="name">${e['name']}</div>
                            <div class="points">${e['points']}</div>
                    </div>`);
                });
            });

            socket.on('disconnect', () => {
                // socket.emit('unjoined', {sid: username});
                // socket.emit('getBoard');
            })

            socket.emit('joined', {name: name}, () => {
                $("#name-input").fadeOut(() => {
                    $('.leaderboard').fadeIn(250);
                    socket.emit('question');
                    $("#answer").focus();
                });
            });
            
        }
    });

    $("#answer").keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            youranswer = parseInt($("#answer").val());
            if (answer == youranswer) {
                socket.emit('increaseRank');
                socket.emit('question');
            } else {
                $(".input-container").effect("shake", 500);
            }
        }
    });
   
}); 