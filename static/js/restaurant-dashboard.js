
// When a user clicks the edit button on a offer,
// the offer is hidden and the editable form is shown.
$(".edit-offer-btn").on("click", (evt) => {
    const offerId = evt.target.dataset.offerId;
    $(`#offer-${offerId}`).hide();
    $(`#editable-offer-${offerId}`).toggle();
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
