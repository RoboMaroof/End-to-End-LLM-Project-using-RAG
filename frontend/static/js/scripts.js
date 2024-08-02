document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let query = document.getElementById('query').value;

    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(data => {
            let results = document.getElementById('results');
            results.innerHTML = '';
            data.forEach(item => {
                let li = document.createElement('li');
                li.textContent = `Filename: ${item.filename}, Summary: ${item.summary}, Similarity: ${item.similarity}`;
                results.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
});
