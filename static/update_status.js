$(document).ready(function() {
    $('#checkAll').change(function() {
        var isChecked = $(this).prop('checked');
        $('.offer-checkbox').prop('checked', isChecked);
        $('.offer-checkbox').each(function() {
            var offerId = $(this).data('id');
            updateOfferStatus(offerId, isChecked);
        });
    });

    $('.offer-checkbox').change(function() {
        updateCheckStatus();
        var offerId = $(this).data('id');
        var isChecked = $(this).prop('checked');
        updateOfferStatus(offerId, isChecked);
    });

    function updateCheckStatus() {
        var allChecked = true;
        $('.offer-checkbox').each(function() {
            if (!$(this).prop('checked')) {
                allChecked = false;
                return false; // Break each loop
            }
        });
        $('#checkAll').prop('checked', allChecked);
    }

    function updateOfferStatus(offerId, isChecked) {
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
    }
});
