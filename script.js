document.getElementById('creditForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Collect form data
    const formData = {
        income: parseFloat(document.getElementById('income').value),
        debt: parseFloat(document.getElementById('debtinc').value),
        credit_score: parseFloat(document.getElementById('credit_score').value),
        age: parseFloat(document.getElementById('age').value),
        loan_amount: parseFloat(document.getElementById('education').value)
    };

    try {
        // Send POST request
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        const resultDiv = document.getElementById('result');

        if (result.prediction) {
            resultDiv.innerText = `Prediction: ${result.prediction}`;
            resultDiv.classList.remove('error');
        } else {
            resultDiv.innerText = `Error: ${result.error}`;
            resultDiv.classList.add('error');
        }
    } catch (error) {
        document.getElementById('result').innerText = `Error: ${error.message}`;
        document.getElementById('result').classList.add('error');
    }
});