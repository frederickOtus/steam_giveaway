$(document).ready(function(){
    $('#the-keys').on('click','.maybe',function(){
        var clicked = $(this);
        var id = clicked.attr('data-id');
        $('.maybe').html('--------------');
        $('.maybe').removeClass('.maybe');
        $.getJSON('/key/choose/' + id, function(data){
            clicked.html('Key: ' + data.key); 
        }).error(function(){ alert("well bugger. Try refreshing? Email me? \o.0/"); });
    });
});
