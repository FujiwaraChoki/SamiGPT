document.addEventListener('DOMContentLoaded', () => {
    // Form
    const form = document.querySelector('form');
    let Text = '';
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        // Input
        const input = document.querySelector('.input');
        const inputValue = input.value;
        // Output
        const output = document.querySelector('.output');
        fetch('http://localhost:9000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'prompt': inputValue })
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                output.innerHTML = '';
                console.log(data['response']);
                // Set reponse to output, but with typewriter effect
                Text = data['response'];

                // Make typewriter effect
                for (let i = 0; i < Text.length; i++) {
                    setTimeout(() => {
                        output.innerHTML += Text[i];
                    }, 100 * i);
                }
            })
    })
})