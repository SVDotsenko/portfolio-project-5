const customAmountInput = document.getElementById('custom-amount');
const radioInputs = document.querySelectorAll('.form-check-input');

radioInputs.forEach(e => e.addEventListener('click', () =>
    customAmountInput.value = e.nextElementSibling.textContent.trim().replace('$', '')));

customAmountInput.addEventListener('input', () => radioInputs.forEach(radio =>
    radio.checked = radio.nextElementSibling.textContent.trim().replace('$', '') === customAmountInput.value));