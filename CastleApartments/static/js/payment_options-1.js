function openChosenPaymentModal() {
    var selectedOption = document.getElementById("payment_option_select").value;
    var modalToOpen;

    if (selectedOption === "CREDIT_CARD") {
        modalToOpen = "credit_card_modal";
    } else if (selectedOption === "BANK_ACCOUNT") {
        modalToOpen = "bank_transfer_modal";
    } else if (selectedOption === "MORTGAGE") {
        modalToOpen = "mortgage_modal";
    }

    if (modalToOpen) {
        var modalElement = document.getElementById(modalToOpen);
        var modalInstance = new bootstrap.Modal(modalElement);
        modalInstance.show();
    }
}

function showSummary() {
    var selectedOption = document.getElementById("payment_option_select").value;
    var summaryDetails = document.getElementById("summary_details");

    // Tengiliðaupplýsingar
    var streetName = document.querySelector('[name="street_name"]').value;
    var city = document.querySelector('[name="city"]').value;
    var postalCode = document.querySelector('[name="postal_code"]').value;
    var country = document.querySelector('[name="country"]').value;
    var nationalId = document.querySelector('[name="national_id"]').value;

    // Setja tengiliðaupplýsingar í yfirlitið
    var contactInfo = `
        <h6 style="font-size: 1.25rem; font-weight: bold;">Tengiliðaupplýsingar</h6>
        <p><strong>Götuheiti:</strong> ${streetName}</p>
        <p><strong>Borg:</strong> ${city}</p>
        <p><strong>Póstnúmer:</strong> ${postalCode}</p>
        <p><strong>Land:</strong> ${country}</p>
        <p><strong>Kennitala:</strong> ${nationalId}</p>
        <br>
    `;

    // Greiðslumáti
    if (selectedOption === "CREDIT_CARD") {
        var cardName = document.querySelector('[name="card_name"]').value;
        var cardNumber = document.querySelector('[name="card_number"]').value;
        var expiry = document.querySelector('[name="expiry"]').value;
        var cvc = document.querySelector('[name="cvc"]').value;

        summaryDetails.innerHTML = `
            ${contactInfo}
            <h6 style="font-size: 1.25rem; font-weight: bold; margin-top: 1rem;">Kreditkortaupplýsingar</h6>
            <p><strong>Nafn á korti:</strong> ${cardName}</p>
            <p><strong>Kortanúmer:</strong> ${cardNumber}</p>
            <p><strong>Gildistími:</strong> ${expiry}</p>
            <p><strong>CVC:</strong> ${cvc}</p>
        `;
    } else if (selectedOption === "BANK_ACCOUNT") {
        var payerName = document.querySelector('[name="payer_name"]').value;
        var payerId = document.querySelector('[name="payer_id"]').value;
        var bankNumber = document.querySelector('[name="bank_number"]').value;
        var paymentDate = document.querySelector('[name="payment_date"]').value;

        summaryDetails.innerHTML = `
            ${contactInfo}
            <h6 style="font-size: 1.25rem; font-weight: bold; margin-top: 1rem;">Millifærsluupplýsingar</h6>
            <p><strong>Nafn greiðanda:</strong> ${payerName}</p>
            <p><strong>Kennitala:</strong> ${payerId}</p>
            <p><strong>Bankanúmer:</strong> ${bankNumber}</p>
            <p><strong>Dagsetning greiðslu:</strong> ${paymentDate}</p>
        `;
    } else if (selectedOption === "MORTGAGE") {
        var loanInstitution = document.querySelector('[name="loan_institution"]').value;
        var payerName = document.querySelector('[name="payer_name"]').value;
        var payerId = document.querySelector('[name="payer_id"]').value;

        summaryDetails.innerHTML = `
            ${contactInfo}
            <h6 style="font-size: 1.25rem; font-weight: bold; margin-top: 1rem;">Lánaupplýsingar</h6>
            <p><strong>Lánastofnun:</strong> ${loanInstitution}</p>
            <p><strong>Nafn greiðanda:</strong> ${payerName}</p>
            <p><strong>Kennitala greiðanda:</strong> ${payerId}</p>
        `;
    }
}

function submitFormAndOpenModal(event) {
    event.preventDefault();

    document.querySelector('form').submit();

    var summaryModal = bootstrap.Modal.getInstance(document.getElementById('summary_modal'));
    summaryModal.hide();

    var confirmationModal = new bootstrap.Modal(document.getElementById('confirmation_modal'));
    confirmationModal.show();
}