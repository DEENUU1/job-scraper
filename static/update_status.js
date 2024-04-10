$(document).ready(function() {
    $('input[type="checkbox"]').change(function() {
      var offerId = $(this).data('id');
      var isChecked = $(this).prop('checked');

      $.ajax({
        url: '/offer_status',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({offer_id: offerId, status: isChecked}),
        success: function(response) {
          console.log(response);
        },
        error: function(xhr, status, error) {
          console.error(error);
        }
      });
    });
});
