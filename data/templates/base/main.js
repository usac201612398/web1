$(document).ready(function() {
    $('.add').click(function() { return !$('#initialServers option:selected').remove().appendTo('#actualServers'); });  
    $('.remove').click(function() { return !$('#actualServers option:selected').remove().appendTo('#initialServers'); });
    //$('.submit').click(function() { $('#actualServers option').prop('selected', 'selected'); });
     
    $('.submit').click(function() {
        var serversVal = "";
        var serversText = "";
        $('#actualServers option').each(function(){
            serversVal = serversVal + $(this).val() + "--";
            serversText = serversText + $(this).text() + "--";
        });
        alert(serversVal);
        alert(serversText);
    });

  
    $("#filtro").on("input",function(){
        $('#initialServers option').each(function(){
            if($(this).text().indexOf($("#filtro").val()) == -1){
                  $(this).prop("selected", false);
                  $(this).fadeOut();
              }else{
                  $(this).prop("selected", false);
                $(this).fadeIn();
                }
        });
      });
           
});
