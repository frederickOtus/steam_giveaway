$(document).ready(function(){
    bindFormActions();
    bindGiveawaysAct();
    bindGASelector();
});

function bindGASelector(){
    $('.keyedit-parent').on("change", "select", function(){
        var newga = $(this).val();
        var key = $(this).parent().attr('data-id');
        var oldparent = $(this).parent();
        var oldthis = $(this);
        $(this).attr('disabled','');
        $.get('/key/set_giveaway/' + key + '/' + newga, function(data){
            var cls = newga == "0" ? "free-key" : "bound-key";
            var html = "<li class='" + cls + "' data-id='" + key + "'>";
            oldthis.removeAttr('disabled');
            html += oldparent.html() + "</li>";
            if(cls == 'free-key'){
                $('ul','#free-keys').append(html);
                $('select', '#free-keys').val('0');
            }else{
                $('ul','#ga-' + newga).append(html);
                $('select', '#ga-' + newga).val(""+newga);
            }
            oldparent.remove();
        });//.error(function(){ alert("check with yo dev, this is bad"); });
    });
}

function bindGiveawaysAct(){
    
}

function bindFormActions(){
    $("#key-form").submit(function(){
        $('input','#key-form').attr('readonly','');
        $('button','#key-form').attr('disabled','');
        $('new-key').html("Submitting...");
        var name = $('#key-name').val();
        var key = $('#key').val();
        $.getJSON('/key/add/' + name + '/' + key, function(data){
            var id = data.id;
            $('input','#key-form').removeAttr('readonly');
            $('button','#key-form').removeAttr('disabled');
            $('new-key').html("New Key");
            $('#key-name').val('');
            $('#key').val('');
            var html = "<div class='free-key' data-id='" + id + "'>";
            html += name + " " + key + $('#sample-select').html() + "</div>";
            $('#free-keys').append(html);
        }).fail(function() {
            alert("Error, probs dupe key");
        })
        return false;
    });
    $("#ga-form").submit(function(){
        $('input','#ga-form').attr('readonly','');
        $('new-ga').html("Submitting...");
        var name = $('#ga-name').val();
        $.getJSON('/giveaway/add/' + name, function(data){
             location.reload(); 
        }).fail(function() {
            alert("Empty name?");
        })
        return false;
    });
}
