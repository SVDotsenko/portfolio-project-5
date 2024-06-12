const customAmountInput = document.getElementById('custom-amount');
const radioInputs = document.querySelectorAll('.form-check-input');

radioInputs.forEach(e => e.addEventListener('click', () =>
    customAmountInput.value = e.nextElementSibling.textContent.trim().replace('$', '')));

customAmountInput.addEventListener('input', () => radioInputs.forEach(radio =>
    radio.checked = radio.nextElementSibling.textContent.trim().replace('$', '') === customAmountInput.value));

customAmountInput.addEventListener('keypress', e => {
    const char = String.fromCharCode(e.which);
    (!(/[0-9]/.test(char)) || (customAmountInput.value.length === 0 && char === '0')) && e.preventDefault();
});

const collapsePersonalInfo = () => {
    if (['email', 'first-name', 'last-name'].reduce((acc, curr) => acc && document.getElementById(curr).value, true)) {
        setTimeout(() => new bootstrap.Collapse(document.getElementById('collapseOne'), {
            toggle: false
        }).hide(), 4000);
    }
}

const showCardNumberToast = () => {
    Toast.params.message = "The card number is 4242424242424242. The date and CVV are any future date and any three " +
        "digits, respectively";
    Toast.params.messageTags = "info";
    Toast.params.delay = 20;
    Toast.show();
}

const showSubscriptionToast = index => {
    const message = ["You have successfully subscribed to our newsletter!",
        "You have successfully unsubscribed from our newsletter!"];
    Toast.params.message = message[index];
    Toast.params.messageTags = "success";
    Toast.params.delay = 3;
    Toast.show();
}

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

const checkEmptyEmail = () => {
    const input = document.getElementById('email');
    const button = document.getElementById('subscribe-button');
    const pattern = new RegExp(input.getAttribute("pattern"));
    setTimeout(() => input.classList.remove('is-invalid', 'is-valid'), 3000);
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

window.onload = () => {
    collapsePersonalInfo();
    showCardNumberToast();
    subscribe();
};