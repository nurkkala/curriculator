// Javascript for the Knowledge Areas page

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

(function(){
  var course_pk = undefined;
  var outcome_pk = undefined;

  $('#add-outcome-to-course').on('show.bs.modal', function(e) {
    outcome_pk = e.relatedTarget.dataset.outcome;
  });

  $('#add-button').click(function(e) {
    course_pk = $('#chosen-course option:selected')[0].value;
    console.log("Course %o gets outcome %o", course_pk, outcome_pk);

    $.post("/cs2013/add-outcome/",
	   { course_pk: course_pk,
	     outcome_pk: outcome_pk,
	     csrfmiddlewaretoken: getCookie('csrftoken') },
	  function() {
	    $('#add-outcome-to-course').modal('hide');
	    location.reload();
	  });

  });
}());

