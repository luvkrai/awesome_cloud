 $(document).ready(function(){
      $('#container_menu').hover(function() {
      $('#navbarDropdown').dropdown('toggle');
    }, function() {
      $('#navbarDropdown').dropdown('toggle');
    });
    $('#account_menu').hover(function() {
      $('#navprofileDropdown').dropdown('toggle');
    }, function() {
      $('#navprofileDropdown').dropdown('toggle');
    });
});