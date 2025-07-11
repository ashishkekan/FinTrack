document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const menuBtn = document.getElementById('menuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            mobileMenu.classList.toggle('active');
        });
    }

    // Portfolio Chart
    const portfolioChartCanvas = document.getElementById('stockChart');
    const graphFilter = document.getElementById('graphFilter');
    if (portfolioChartCanvas && graphFilter) {
        const ctx = portfolioChartCanvas.getContext('2d');
        let chart;

        const transactions = window.transactionsData || [];
        console.log("Transactions Data:", transactions); // Debug: Verify data received

        if (!window.Chart) {
            console.error("Chart.js is not loaded");
            const parent = ctx.canvas.parentElement;
            parent.innerHTML = '<p class="text-center text-red-600 mt-4">Error: Chart.js not loaded. Please check dependencies.</p>';
            return;
        }

        const colors = ['#10B981', '#EF4444', '#3B82F6', '#F59E0B', '#8B5CF6', '#EC4899', '#6B7280', '#14B8A6', '#F97316', '#8B5CF6'];

        function updateChart(symbol) {
            const filteredData = symbol === 'all' 
                ? transactions 
                : transactions.filter(t => t.stock_symbol === symbol);

            console.log("Filtered Data for", symbol, ":", filteredData); // Debug: Verify filtered data

            if (!filteredData.length) {
                if (chart) chart.destroy();
                const parent = ctx.canvas.parentElement;
                parent.innerHTML = '<p class="text-center text-gray-600 mt-4">No data for selected symbol.</p>';
                parent.appendChild(ctx.canvas);
                return;
            }

            // Check if all transactions are on the same day
            const dates = [...new Set(filteredData.map(t => t.transaction_date))];
            const chartType = dates.length > 1 ? 'line' : 'bar';

            // Group data by stock symbol
            const datasets = {};
            filteredData.forEach(t => {
                if (!datasets[t.stock_symbol]) {
                    datasets[t.stock_symbol] = {
                        label: t.stock_symbol,
                        data: [],
                        borderColor: colors[Object.keys(datasets).length % colors.length],
                        backgroundColor: colors[Object.keys(datasets).length % colors.length] + '33',
                        tension: chartType === 'line' ? 0.3 : 0,
                        fill: chartType === 'line'
                    };
                }
                datasets[t.stock_symbol].data.push({
                    x: chartType === 'line' ? t.transaction_date : t.stock_symbol,
                    y: t.price_per_share
                });
            });

            // Sort data by date for line chart
            if (chartType === 'line') {
                Object.values(datasets).forEach(dataset => {
                    dataset.data.sort((a, b) => new Date(a.x) - new Date(b.x));
                });
            }

            console.log("Chart Type:", chartType, "Datasets:", datasets); // Debug: Verify chart type and datasets

            if (chart) chart.destroy();
            try {
                chart = new Chart(ctx, {
                    type: chartType,
                    data: {
                        datasets: Object.values(datasets)
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top',
                            },
                            title: {
                                display: true,
                                text: symbol === 'all' ? 'Top 10 Stocks Price Trends' : `Price Trend for ${symbol}`,
                            }
                        },
                        scales: {
                            x: {
                                type: chartType === 'line' ? 'time' : 'category',
                                time: chartType === 'line' ? {
                                    unit: 'day',
                                    tooltipFormat: 'MMM d, yyyy'
                                } : undefined,
                                title: {
                                    display: true,
                                    text: chartType === 'line' ? 'Date' : 'Stock Symbol'
                                },
                                labels: chartType === 'bar' ? Object.keys(datasets) : undefined
                            },
                            y: {
                                beginAtZero: false,
                                title: {
                                    display: true,
                                    text: 'Price per Share (₹)'
                                }
                            }
                        }
                    }
                });
            } catch (error) {
                console.error("Chart.js Error:", error);
                const parent = ctx.canvas.parentElement;
                parent.innerHTML = '<p class="text-center text-red-600 mt-4">Error rendering chart: ' + error.message + '</p>';
                parent.appendChild(ctx.canvas);
            }
        }

        graphFilter.addEventListener('change', () => {
            console.log("Graph Filter Changed to:", graphFilter.value); // Debug: Verify filter change
            updateChart(graphFilter.value);
        });

        updateChart('all');
    } else {
        console.error("Chart canvas or filter element not found");
    }

    // Average Price Calculator Dynamic Rows
    const addRowBtn = document.getElementById('addRow');
    const container = document.getElementById('transactionsContainer');
    if (addRowBtn && container) {
        addRowBtn.addEventListener('click', () => {
            const row = document.createElement('div');
            row.className = 'transaction-row flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 items-end mt-4';
            row.innerHTML = `
                <div class="flex-1">
                    <label class="block text-gray-700 font-medium mb-2">Quantity</label>
                    <input type="number" name="quantity[]" class="w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none" min="1" required>
                </div>
                <div class="flex-1">
                    <label class="block text-gray-700 font-medium mb-2">Price per Share (₹)</label>
                    <input type="number" step="0.01" name="price[]" class="w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none" min="0.01" required>
                </div>
                <button type="button" class="remove-row bg-red-600 text-white p-3 rounded-lg hover:bg-red-700 transition-colors">
                    <i class="fas fa-trash"></i>
                </button>
            `;
            container.appendChild(row);
        });

        container.addEventListener('click', (e) => {
            if (e.target.closest('.remove-row')) {
                const row = e.target.closest('.transaction-row');
                if (container.querySelectorAll('.transaction-row').length > 1) {
                    row.remove();
                }
            }
        });
    }
});