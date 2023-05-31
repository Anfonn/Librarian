document.getElementById('submit').addEventListener('click', function() {
    const query = document.getElementById('query').value;
    const loading = document.getElementById('loading');
    loading.style.display = 'block';  // Show the loading indicator

    fetch('http://localhost:5001/get_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({query: query})
    })
    .then(response => response.json())
    .then(data => {
        loading.style.display = 'none';
        if (data.output_text) {
            let output = data.output_text.replace("\\n", "\n");
            let formatted = output.replace("SOURCE:", "\nsource:");
            document.getElementById('output').innerText = formatted;
        } else {
            document.getElementById('output').innerText = "Error: Response does not contain 'output_text'";
        }
    })
    .catch(error => {
        loading.style.display = 'none';
        console.error('Error:', error);
        document.getElementById('output').innerText = "Error: " + error;
    });
});