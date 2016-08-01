$(function(){

$('.datepicker').pickadate({
  selectMonths: true, // Creates a dropdown to control month
  selectYears: 15
})

$('select').material_select();

function validateEmail(email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  return emailReg.test( email );
}

//for csrf_token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrf_token = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

$("#download-button").on("click", function(event){
    event.preventDefault();

    $('#start_date').removeClass('datepicker invalid').addClass('datepicker');
    $('#end_date').removeClass('datepicker invalid').addClass('datepicker');
    $('#email').removeClass('validate invalid').addClass('validate');

    $('#feedback_message').remove()

    var start_date = $('#start_date').val()
    var end_date = $('#end_date').val()
    var email = $('#email').val()
    var category = $('#category').val()

    var d = new Date();

    if (!start_date){
      $('#start_date').addClass('datepicker invalid');
    }
    if (!end_date){
      $('#end_date').addClass('datepicker invalid');
    }
    if (start_date > end_date){
      $('#start_date').addClass('datepicker invalid');
      $('#end_date').addClass('datepicker invalid');
    }

    if(Date.parse(end_date) > d){
      $('#end_date').addClass('datepicker invalid');
    }

    if (!email || !validateEmail(email)){
      $('#email').addClass('validate invalid');
    }

    if (start_date && end_date && email && (category.length != 0) && (start_date <= end_date)
        && (Date.parse(end_date) <= d) && validateEmail(email)){
      $.ajax({
        url: "/",
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data:JSON.stringify({
          start_date: start_date,
          end_date: end_date,
          email: email,
          category: category
        })

      })

      $('#main_content').append("<div class='row center' id='feedback_message'><h7 class='header col s12 light'>Email will be sent soon</h7></div>");
      $('#feedback_message').delay(5000).fadeOut('slow');

    }


})

})
