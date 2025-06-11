document.addEventListener('DOMContentLoaded', function () {
    const portfolioChartCanvas = document.getElementById('stockChart');
    const graphFilter = document.getElementById('graphFilter');
    
    if (portfolioChartCanvas && graphFilter) {
        console.log('Chart canvas and filter found');
        const ctx = portfolioChartCanvas.getContext('2d');
        let chart;

        // Transaction data from window.transactionsData
        const transactions = window.transactionsData || [];
        console.log('Transactions data:', transactions);

        if (!transactions.length) {
            console.warn('No transaction data available');
            portfolioChartCanvas.parentElement.innerHTML += '<p class="text-center text-gray-600 mt-4">No transaction data to display.</p>';
            return;
        }

        const colors = ['#10B981', '#EF4444', '#3B82F6', '#F59E0B', '#8B5CF6'];

        function updateChart(symbol) {
            console.log('Updating chart for symbol:', symbol);
            const filteredData = symbol === 'all' 
                ? transactions 
                : transactions.filter(t => t.stock_symbol === symbol);

            console.log('Filtered data:', filteredData);

            if (!filteredData.length) {
                console.warn('No data for selected symbol:', symbol);
                if (chart) chart.destroy();
                ctx.canvas.parentElement.innerHTML += '<p class="text-center text-gray-600 mt-4">No data for selected symbol.</p>';
                return;
            }

            const datasets = {};
            filteredData.forEach(t => {
                if (!datasets[t.stock_symbol]) {
                    datasets[t.stock_symbol] = {
                        label: t.stock_symbol,
                        data: [],
                        borderColor: colors[Object.keys(datasets).length % colors.length],
                        backgroundColor: colors[Object.keys(datasets).length % colors.length] + '33',
                        tension: 0.3,
                        fill: true
                    };
                }
                datasets[t.stock_symbol].data.push({
                    x: t.transaction_date,
                    y: t.price_per_share
                });
            });

            console.log('Datasets:', datasets);

            if (chart) chart.destroy();
            chart = new Chart(ctx, {
                type: 'line',
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
                    },
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day',
                                tooltipFormat: 'MMM D, YYYY'
                            },
                            title: {
                                display: true,
                                text: 'Date'
                            }
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
            console.log('Chart rendered');
        }

        graphFilter.addEventListener('change', () => {
            updateChart(graphFilter.value);
        });

        // Initialize chart with all stocks
        updateChart('all');
    } else {
        console.error('Chart canvas or filter not found');
    }
});