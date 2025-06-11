document.addEventListener('DOMContentLoaded', function () {
    // Mobile Menu Toggle
    const menuBtn = document.getElementById('menuBtn');
    const sidebar = document.getElementById('sidebar');
    
    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // Form Validation for Transaction Form
    const transactionForm = document.querySelector('form');
    if (transactionForm) {
        transactionForm.addEventListener('submit', function (e) {
            const quantityInputs = document.querySelectorAll('input[name="quantity[]"], input[name="quantity"]');
            const priceInputs = document.querySelectorAll('input[name="price[]"], input[name="price_per_share"]');
            for (let i = 0; i < quantityInputs.length; i++) {
                const qty = quantityInputs[i].value;
                const price = priceInputs[i].value;
                if (qty <= 0 || price <= 0) {
                    e.preventDefault();
                    alert('Quantity and price must be positive numbers.');
                    return;
                }
            }
        });
    }

    // Dynamic Transaction Rows for Average Price Calculator
    const addRowBtn = document.getElementById('addRow');
    const transactionsContainer = document.getElementById('transactionsContainer');
    
    if (addRowBtn && transactionsContainer) {
        addRowBtn.addEventListener('click', () => {
            const newRow = document.createElement('div');
            newRow.className = 'transaction-row flex space-x-4 items-end';
            newRow.innerHTML = `
                <div class="flex-1">
                    <label class="block text-gray-700 font-medium mb-1">Quantity</label>
                    <input type="number" name="quantity[]" class="w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none" required>
                </div>
                <div class="flex-1">
                    <label class="block text-gray-700 font-medium mb-1">Price per Share (₹)</label>
                    <input type="number" step="0.01" name="price[]" class="w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none" required>
                </div>
                <button type="button" class="remove-row bg-red-600 text-white p-3 rounded-lg hover:bg-red-700 transition-colors">
                    <i class="fas fa-trash"></i>
                </button>
            `;
            transactionsContainer.appendChild(newRow);
            updateRemoveButtons();
        });

        function updateRemoveButtons() {
            const removeButtons = document.querySelectorAll('.remove-row');
            removeButtons.forEach(button => {
                button.addEventListener('click', () => {
                    if (transactionsContainer.querySelectorAll('.transaction-row').length > 1) {
                        button.parentElement.remove();
                    } else {
                        alert('At least one transaction row is required.');
                    }
                });
            });
        }

        updateRemoveButtons();
    }
});