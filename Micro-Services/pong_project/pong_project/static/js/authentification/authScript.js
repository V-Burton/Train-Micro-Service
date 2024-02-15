import { get_cookie, div_handler } from '../utils.js';

document.addEventListener('DOMContentLoaded', function() {
	const csrftoken = get_cookie('csrftoken');
    const authFormContainer = document.getElementById('authFormContainer');
    const statusUser = document.getElementById('statusUser');
	console.log(csrftoken);



    authFormContainer.addEventListener('submit', function(event) {
		event.preventDefault(); // Prevent the default form submission
        if (event.target.id === 'registerForm') {
			sendRegisterForm(csrftoken);
        }

        if (event.target.id === 'loginForm') {
			sendLoginForm(csrftoken);
        }


    });
});

function sendLoginForm(csrftoken){

	const formData = new FormData(event.target); // Use the event target which is the form
	const username = formData.get('username');
	const password = formData.get('password');

	fetch('http://localhost:8002/login/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({ username, password }),
		credentials: 'include'
	})
	.then(response => response.json())
	.then(data => {
		if (data.token) {
			console.log(data.token);
			localStorage.setItem('jwt', data.token);
			console.log('login successful');
			fetch("../../../templates/home.html")
				.then(response => response.text())
                .then(html => {
                    document.getElementById('authFormContainer').innerHTML = html;
                });
		} else {
			console.error('Login failed')
		}
	})
	.catch(error => {
		console.error('Error:', error);
	});
}

function sendRegisterForm(csrftoken){
	const formData = new FormData(event.target); // Use the event target which is the form
	const username = formData.get('username');
	// const email = formData.get('email');
	const password1 = formData.get('password1');
	const password2 = formData.get('password2');

	fetch('http://localhost:8002/register/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({ username, password1, password2 }),
		credentials: 'include'
	})
	.then(response => response.text())
	.then(html => {
		authFormContainer.innerHTML = html;
		document.getElementById('authFormContainer').innerHTML = html;
	})
	.catch(error => {
		console.error('Error:', error);
	});
}