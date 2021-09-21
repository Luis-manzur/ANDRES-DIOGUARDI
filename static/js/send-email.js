window.onload = () => {
    const contactForm = document.getElementById('contact-form')
    contactForm.onsubmit = (e) => {
        e.preventDefault()
        const name = document.getElementById('name').value
        const email = document.getElementById('email').value
        const number = document.getElementById('number').value
        const message = document.getElementById('message').value
        fetch('https://luismanzur.herokuapp.com/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, number, message })
        }).then(x => x.json())
        contactForm.reset()
        alert('Email Enviado con exito')
    }
    
}