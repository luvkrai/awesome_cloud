    $(document).ready(function(){
      $('#container_menu').hover(function() {
      $('#navbarDropdown').dropdown('toggle').stop(true, true).delay(200).fadeIn(200);
    }, function() {
      $('#navbarDropdown').dropdown('toggle').stop(true, true).delay(200).fadeIn(200);
    });
    $('#account_menu').hover(function() {
      $('#navprofileDropdown').dropdown('toggle').stop(true, true).delay(200).fadeIn(200);
    }, function() {
      $('#navprofileDropdown').dropdown('toggle').stop(true, true).delay(200).fadeIn(200);
    });
});

function flashMessage(data) {
html = '';
for (i=0; i<data.length; i++) {
    html += '<div class="alert alert-' + data[i]['type'] + '"><a href="#" class="close" data-dismiss="alert">&times;</a>' + data[i].message + '</div>';
}
return html;
}

function nav_toggle(){

}


function get_exited() {
    var docker_exited = new Array();
    var data = new Array();
    var response_status = new Array();
    $("input:checked").each(function() {
        data.push($(this).val());
        });
    var selected_containers = data.toString();
    console.log("start");
    $.ajax({
    type: "POST",
    url: "/delete_container/"+selected_containers,
    data:"hhh",
    dataType:'text',
    beforeSend:function(){
     $('#submit').toggle();
     $('#loader').toggle();
     $('#t01').find('*').prop('disabled',true);
     return confirm("Are you sure?");
    },
    success: function(data){
        console.log("success")
        //$("#ttt").html(data);
        //var $bodyContent = $('#t01 tbody').children();
        response = $.parseJSON(data);
        console.log(response);
        var $table = $('#t01');
        $('#t01 tr').not(function(){ return !!$(this).has('th').length; }).remove();
            $.each(response.table, function(i, item) {
            var $tr = $('<tr>').append(
            $('<td>').text(item.name),
            $('<td>').text(item.container_id),
            $('<td>').text(item.image),
            $('<td>').text(item.status),
			$('<td>').text(item.date),
            $('<td>').html('<input type="checkbox" name="docker_exited[]" id="docker_exited" value="'+item.container_id+'">')
            ).appendTo('#t01');
            //console.log($tr.wrap('<p>').html());
            });

        //$("#ttt").html(row);
        //$table.find('tbody').empty().append(row);
        $table.trigger('reflow');
        if (response.success){
            response_status.push('[{"type": "success", "message": "Successfully deleted containers"}]');
            }
        else{
            response_status.push('[{"type": "danger", "message": "Ooops! an error occurred"}]');
            }
        $('#flash').append(flashMessage(JSON.parse(response_status)));

        }}).always(function() {
            $('#t01').find('*').prop('disabled',false);
            $('#loader').toggle();
            $('#submit').toggle();
        })
    ;}

