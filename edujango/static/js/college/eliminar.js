// Script para eliminar
$(document).ready(function(){
    $('.eliminar').click(function(){
        var id = $(this).attr('id');
        $('#m'+ id).modal('hide');
        var url = $(this).attr('href');
        $.getJSON(url, function(data){
            
        });
        toggleDiv('f'+id);
        return false;
    });
});
function toggleDiv(trId) {
    $("#"+trId).toggle(500);
}