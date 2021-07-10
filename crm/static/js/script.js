$(document).ready(function() {
  var editor = new MediumEditor('.editable');
  $('.question_answer').toggle();
  $('#dropdown').toggle();
  $('#dropdown2').toggle();
  $('.cover').toggle();
  $('.cover2').toggle();
  $("tbody").each(function() {
    if ($(this).children("tr").length > 7) {
      $(this).find('.moreload').css("display", "table-row");

    }
  });

  function MenuSizer() {
    if (window.localStorage.getItem("size") != null) {
      if (window.localStorage.getItem("size") == "small") {
        $(".undercontent").toggleClass('fullsize-sidebar');
        $('.navlink').toggleClass('smallnav');
        $('.nav__title').toggle(200);
        $('.top-bar__logo').toggle(200);
      }
    } else {
      window.localStorage.setItem("size", "big");
    }
  }

  MenuSizer()




  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
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
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });
  $(".question_title").click(function() {
    $(this).parents('.question').find('.question_answer').toggle();
    $(this).toggleClass("question_title--active")
  });
});



function toggleDropdown1() {
  $('#dropdown-trigger').toggleClass('top-bar__item--active');
  $('.cover').toggle();
  $('#dropdown-trigger').parent().find('#dropdown').toggle();
};

function toggleDropdown2() {
  $('#dropdown-trigger-2').toggleClass('top-bar__item--active');
  $('.cover2').toggle();
  $('#dropdown-trigger-2').find('#dropdown2').toggle();
};

function collapseNavigation() {
  $(".undercontent").toggleClass('fullsize-sidebar');
  $('.navlink').toggleClass('smallnav');
  $('.nav__title').toggle();
  $('.top-bar__logo').toggle();
  if (window.localStorage.getItem("size") == "big") {
    window.localStorage.setItem("size", "small");
  } else {
    window.localStorage.setItem("size", "big");
  };
};


$(document).on('click', '.markall', function(e) {
  // var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
  e.preventDefault();
  toggleDropdown1();
  var urlss = $(this).attr("data-href");
  console.log(urlss)
  $.ajax({
    type: 'POST',
    url: urlss,
    data: JSON.stringify({

      "pk": 13,

    }),

    success: (json) => {
      console.log('yaaay');


    },
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });

});



$(document).on('click', '.dropdown_notification', function(e) {
  // var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
  e.preventDefault();
  var pk = $(this).data("pk");
  var urlss = $(this).attr("data-href");
  $.ajax({
    type: 'POST',
    url: urlss,
    data: JSON.stringify({
      "pk": pk,
    }),

    success: (json) => {
      console.log('yaaay');
    },
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });

});


$(document).on('click', '.unopened', function(e) {
  var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
  e.preventDefault();
  var pk = $(this).attr("data-id");
  var urlss = $(this).attr("data-href");



  // console.log($(this).find("input[name='type"+i+"']:checked").val());
  $.ajax({
    type: 'POST',
    url: urlss,
    data: JSON.stringify({
      "pk": pk,
      // "csrfmiddlewaretoken": csrftoken,
      // "action": 'post'
    }),

    success: (json) => {
      $(this).removeClass("unopened");
      $(this).parents(".Ccard").removeClass("unopened");


    },
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
});

$(document).ready(function() {
  $('.moreload').click(function() {
    $(this).parents('tbody').find('tr').css("display", "table-row");
    $(this).toggle();
  });
});
