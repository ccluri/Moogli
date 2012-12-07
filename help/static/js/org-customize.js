var customize_toc = function(){
  // Change the table of contents' ul style
  var toc_text = $('#text-table-of-contents ul').attr("class", "nav nav-list bs-docs-sidenav affix");
  $('.bs-docs-sidebar').append(toc_text);

  // Make the li element active when clicked upon
  $('li', toc_text).click( function(evt) {
    $(this).siblings().attr('class', '');
    $(this).attr('class', 'active');
  });

  // Hide TOC header
  $('#table-of-contents').remove();


};

var hide_postamble = function () {
  $('#postamble').hide()
};

// Call whatever needs to be called, onload
$(document).ready(function(evt) {
  customize_toc();
  hide_postamble();
});
