import * as g from './pong/global.js';
import { session_create } from './pong/session.js';
import { get_cookie, div_handler } from './utils.js';

// export async function send_alias_request() {
// 	try {
// 		const alias = document.getElementById('alias').value;

// 		const response = await fetch('http://localhost:8002/alias_view', {
// 			method: 'POST',
// 			headers: {
// 				'Content-Type': 'application/json',
// 				'X-CSRFToken': get_cookie("csrftoken"),
// 			},
// 			credentials: 'include',
// 			body: JSON.stringify({ "alias": alias }),
// 		});

// 		if (!response.ok) {
// 			throw new Error('Network response was not ok: ' + response.statusText);
// 		} else {
// 			localStorage.setItem("jwt", response.token);
// 		}

// 		div_handler("game-menu-div");
// 	} catch (error) {
// 		console.error('Error:', error);
// 	}
// }

// export async function send_get_alias_request() {
// 	try {
// 		const response = await fetch('http://localhost:8002/alias_view', {
// 			method: 'GET',
// 			headers: {
// 				'Content-Type': 'application/json',
// 				'X-CSRFToken': get_cookie("csrftoken"),
// 			},
// 			credentials: 'include',
// 		});

// 		const data = await response.json();

// 		if (!response.ok) {
// 			div_handler("alias-div");
// 		} else {
// 			div_handler("game-menu-div");
// 			window.alias = data.alias;
// 		}
// 		console.log("alias = ", alias);
// 	} catch (error) {
// 		console.error('Error:', error);
// 	}
// }

export async function send_user_input(input, time) {

	const token = localStorage.getItem("jwt");
	console.log(token);
	try {
		if (window.game_session === null || window.game_session.id === 0)
			return;

		const response = await fetch(`http://localhost:8003/${window.game_session.id}/`, {
			method: 'PUT',
			headers: {
				'Authorization': `Bearer ${token}`,
				'Content-Type': 'application/json',
				'X-CSRFToken': get_cookie("csrftoken"),
			},
			credentials: 'include',
			body: JSON.stringify([input, time]),
		});

		if (!response.ok) {
			throw new Error('Network response was not ok: ' + response.statusText);
		}
	} catch (error) {
		console.error('Error sending input:', error);
	}
}

export async function send_game_creation_request() {

	const token = localStorage.getItem("jwt");
	console.log(token);
	try {
		const response = await fetch('http://localhost:8003/', {
			method: 'POST',
			headers: {
				'Authorization': `Bearer ${token}`,
				'Content-Type': 'application/json',
				'X-CSRFToken': get_cookie("csrftoken"),
			},
			credentials: 'include',
		});

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.error);
		}

		if (data) {
			console.log("data_id = ", data.id);
			session_create(data.id, g.TYPE_REMOTE);
		} else {
			console.error('Game creation failed');
		}
	} catch (error) {
		console.error('Error:', error);
	}
}
