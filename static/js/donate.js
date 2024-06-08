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

window.onload = () => {
    if (document.getElementById('email').value) {
        setTimeout(() => new bootstrap.Collapse(document.getElementById('collapseOne'), {
            toggle: false
        }).hide(), 4000);
    }

    navigator.clipboard.writeText('4242424242424242').then(() => {
        Toast.params.message = "Card number copied to clipboard, paste it in the input field. The date and CVV are any future date and any three digits, respectively";
        Toast.params.messageTags = "info";
        Toast.params.delay = 10;
        Toast.show();
    }, () => {
        Toast.params.message = "Failed to copy card number to clipboard, type it manually 4242424242424242. The date and CVV are any future date and any three digits, respectively";
        Toast.params.messageTags = "error";
        Toast.params.delay = 10;
        Toast.show();
    });
};