// Javascript for the Knowledge Areas page

// Pick out a cookie with the given name; from the Django documentation.
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

  // Add an outcome to a course. Uses a modal.
  var course_pk = undefined;
  var outcome_pk = undefined;

  $('#add-outcome-to-course').on('show.bs.modal', function(e) {
    // When the modal pops up, the button that caused the pop has a data-outcome attribute
    // containing the primary key of the outcome.
    outcome_pk = e.relatedTarget.dataset.outcome;
  });

  $('#add-button').click(function(e) {
    // Clicking on the add button grabs the primary key of the selected course from the
    // list of courses.
    course_pk = $('#chosen-course option:selected')[0].value;
    console.log("Course %o gets outcome %o", course_pk, outcome_pk);

    // Post back to the server to add the outcome to the course. Must pass the CSRF token
    // to avoid a 403 (Forbidden) from the view. Upon completion, reload the page so that
    // it reflects the newly added outcome.
    $.post("/cs2013/add-outcome/",
	   { course_pk: course_pk,
	     outcome_pk: outcome_pk,
	     csrfmiddlewaretoken: getCookie('csrftoken') },
	  function() {
	    $('#add-outcome-to-course').modal('hide');
	    location.reload();
	  });
  });

}());				// IIFE

