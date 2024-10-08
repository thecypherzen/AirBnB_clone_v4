// $(".popover input:checkbox").css('margin-right', '10px');
$('document').ready(() => {
  const selected = {};
  // add listener to input of type checkbox
  $('input:checkbox').on('change', function () {
    const key = $(this).attr('data-id');
    if ($(this).is(':checked')) {
      selected[key] = $(this).attr('data-name');
    } else {
      delete selected[key];
    }
    // create is to of selected checkboxes
    let list = '';
    for (const value of Object.values(selected)) {
      if (list.length) {
        list += ', ';
      }
      list += value;
    }

    // append selected checkboxes to h4
    $('div.amenities h4').html(`${list}`);
  });

  // Update server status
  const apiBadge = $('#api_status');
  const url = 'http://0.0.0.0:5001/api/v1/status/';
  $.get(url, (res, xhrObj, stat) => {
    apiBadge.addClass('available');
  }).fail(err => {
    console.log(err);
    apiBadge.removeClass('available');
  });
});
