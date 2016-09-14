$(document).ready(function(){
    $('.toggle').click(function(e){
        var id = $(this).attr('data-id');
        var elm = $(this);
        $.get('/wl-toggle/' + id, function(data){
           if(elm.html() == 'Whitelist'){
                elm.html('Blacklist');
           } 
           else{
                elm.html('Whitelist');
           }
        }).error(function(){ alert("Whoops!"); });
    });
});

