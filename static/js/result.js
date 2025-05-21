const ctx = document.getElementById('expenseChart').getContext('2d');
const expenseChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: chartLabels, // Array of categories (e.g. ['Food', 'Transport'])
    datasets: [{
      label: 'Total per Category',
      data: chartValues,  // Corresponding amounts (e.g. [50000, 30000])
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Amount (Rp)' // Y-axis title
        }
      }
    }
  }
});
