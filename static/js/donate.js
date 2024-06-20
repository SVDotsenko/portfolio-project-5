/**
 * Gets the custom amount input element and all radio input elements.
 * Adds an event listener to each radio input element to update the custom amount input value when clicked.
 * Adds an event listener to the custom amount input element to update the checked status of radio inputs when its value
 * is changed.
 */
const customAmountInput = document.getElementById('custom-amount');
const radioInputs = document.querySelectorAll('.form-check-input');

radioInputs.forEach(e => e.addEventListener('click', () =>
    customAmountInput.value = e.nextElementSibling.textContent.trim().replace('$', '')));

customAmountInput.addEventListener('input', () => radioInputs.forEach(radio =>
    radio.checked = radio.nextElementSibling.textContent.trim().replace('$', '') === customAmountInput.value));

/**
 * Collapses the personal information section if all required fields are filled.
 */
const collapsePersonalInfo = () => {
    if (['email', 'first-name', 'last-name'].reduce((acc, curr) => acc && document.getElementById(curr).value, true)) {
        setTimeout(() => new bootstrap.Collapse(document.getElementById('collapseOne'), {
            toggle: false
        }).hide(), 2000);
    }
}

/**
 * Shows a toast with card number information and sets up an event listener to collapse the personal information section
 * when the toast is hidden.
 */
const showCardNumberToast = () => {
    Toast.params.message = "The card number is 4242424242424242. The date and CVV are any future date and any three " +
        "digits, respectively";
    Toast.params.messageTags = "info";
    Toast.params.delay = 20;
    Toast.show();

    $(Toast.params.element).on('hide.bs.toast', function () {
        collapsePersonalInfo();
        $(this).off('hide.bs.toast');
    });
}

/**
 * Shows a toast with subscription status message.
 * @param {number} index - The index of the message to show. 0 for subscription success, 1 for unsubscription success.
 */
const showSubscriptionToast = index => {
    const message = ["You have successfully subscribed to our newsletter!",
        "You have successfully unsubscribed from our newsletter!"];
    Toast.params.message = message[index];
    Toast.params.messageTags = "success";
    Toast.params.delay = 3;
    Toast.show();
}

/**
 * Sets up the subscribe button to toggle subscription status when clicked.
 */
const subscribe = () => {
    const subscribeButton = document.getElementById('subscribe-button');
    subscribeButton.textContent = localStorage.getItem('subscribed') === 'true' ? 'Unsubscribe' : 'Subscribe';
    subscribeButton.addEventListener('click', () => {
        const isSubscribed = localStorage.getItem('subscribed') === 'true';
        showSubscriptionToast(+isSubscribed)
        localStorage.setItem('subscribed', !isSubscribed);
        subscribeButton.textContent = isSubscribed ? 'Subscribe' : 'Unsubscribe';
    });
}

/**
 * Checks if the email input value is valid and updates its class and the disabled status of the subscribe button
 * accordingly.
 */
const checkEmptyEmail = () => {
    const input = document.getElementById('email');
    const button = document.getElementById('subscribe-button');
    const pattern = new RegExp(input.getAttribute("pattern"));
    setTimeout(() => input.classList.remove('is-invalid', 'is-valid'), 2000);
    if (pattern.test(input.value)) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        button.disabled = false;
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        button.disabled = true;
    }
}

/**
 * Sets up the page to show the card number toast and subscribe when loaded.
 */
window.onload = () => {
    showCardNumberToast();
    subscribe();
};