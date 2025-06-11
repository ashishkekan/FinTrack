document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            const quantity = document.querySelector('input[name="quantity"]');
            const price = document.querySelector('input[name="price_per_share"]');
            if (quantity && price) {
                if (quantity.value <= 0 || price.value <= 0) {
                    e.preventDefault();
                    alert('Quantity and price must be positive numbers.');
                }
            }
        });
    }
});