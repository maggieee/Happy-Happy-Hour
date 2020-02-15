
// When a user clicks the edit button on a offer,
// the offer is hidden and the editable form is shown.
$(".edit-offer-btn").on("click", (evt) => {
    const offerId = evt.target.dataset.offerId;
    $(`#offer-${offerId}`).hide();
    $(`#editable-offer-${offerId}`).show();
});

// When a user clicks the cancel button, editable form is hidden
// and the offer is shown without any changes.
$(".cancel-edit-btn").on("click", (evt) => {
    evt.preventDefault();
    const offerId = evt.target.dataset.offerId;
    $(`#offer-${offerId}`).show();
    $(`#editable-offer-${offerId}`).hide();
});

// When a user clicks the delete button, they're asked if they
// want to delete the offer. If so, offer is deleted in database
// and page is relaoded to reflect change.
$(".delete-offer-btn").on("click", (evt) => {
    result = window.confirm("Are you sure you want to delete this offer?");

    if (result) {
        const offerId = evt.target.dataset.offerId;
        $.post("/restaurant/delete/offer", { offer: offerId }, () => {
            location.reload(true);
        });
    };
});
