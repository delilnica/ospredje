function odpri_prijavo(ne_zapri=true)
{
	let o  = document.getElementById("prijava_okvir");

	if (ne_zapri) {
		o.style.display = "block";
	} else {
		o.style.display  = "none";
	}
}

function odjavi()
{
	document.cookie = "zeton=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
	document.cookie = "zeton=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/fragment;";
	document.cookie = "vzdevek=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
	document.cookie = "vzdevek=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/fragment;";
	location.reload();
}

function oddaj_fragment()
{
	let odg = document.getElementById("odgovor");

	let ime      = document.getElementById("ime").value;
	let besedilo = document.getElementById("besedilo").value;
	let zaseben  = document.querySelector("#zaseben").checked ? 1 : 0;
	let datoteka = document.querySelector('input[type="file"]').files[0];

	var params = {
		"ime": ime,
		"besedilo": besedilo,
		"zaseben": zaseben
	}

	var reader = new FileReader();

	if (datoteka) {
		reader.readAsDataURL(datoteka);
	}
	setTimeout(function(){
		if (datoteka) {
			params["datoteka"] = reader.result;
		}
		console.log(params);

		let uspeh = false;
		var headers = new Headers();
		headers.append("Authorization", getCookie("zeton"));

		fetch("http://localhost:81/fragment.php", {
			method: "POST",
			body: JSON.stringify(params),
			headers: headers
		}).then(function(response) {
			uspeh = (response.status == 201)
			return response.json();
		}).then(function(j) {
			console.log(j);
			if (uspeh) {
				odg.className = "obvestilo uspeh";
				odg.innerHTML = "Fragment je bil uspešno dodan. Dosegljiv je pod oznako <a href='/fragment/" + j["response"] + "'>" + j["response"] + "</a>";
			} else {
				odg.className = "obvestilo napaka";
				odg.innerHTML = j["response"];
			}
			odg.style.display = "block";

		}).catch(function(err) {
			console.log(err);
			alert("Napaka, podrobnosti v konzoli.");
		})
	}, 100);
}

function prijavi_uporabnika(reload=true, vzdevek=null, geslo=null)
{
	let odg = document.getElementById("odgovor");

	if (vzdevek == null) {
		var vzdevek = document.getElementById("vzdevek").value;
		var geslo   = document.getElementById("geslo").value;
	}

	const params = {
		"vzdevek": vzdevek,
		"geslo": geslo
	}

	let uspeh = false;

	fetch("http://localhost:81/login.php", {
		method: "POST",
		body: JSON.stringify(params)
	}).then(function(response) {
		uspeh = (response.status == 200)
		return response.json();
	}).then(function(j) {
		// console.log(j);
		if (!uspeh) {
			odg.className = "obvestilo napaka";
			odg.innerHTML = j["response"];
			odg.style.display = "block";
		} else {
			// odpri_prijavo(false);
			odg.style.display = "none";
			document.cookie = "zeton=" + j["response"];
			document.cookie = "vzdevek=" + vzdevek;
			if (reload) {
				location.reload();
			} else {
				location.replace("/");
			}
		}

	}).catch(function(err) {
		console.log(err);
		alert("Napaka, podrobnosti v konzoli.");
	})
}

function registriraj_uporabnika()
{
	let odg = document.getElementById("odgovor");

	let vzdevek = document.getElementById("reg_vzdevek").value;
	let enaslov = document.getElementById("reg_enaslov").value;
	let geslo   = document.getElementById("reg_geslo").value;

	const params = {
		"vzdevek": vzdevek,
		"enaslov": enaslov,
		"geslo": geslo
	}

	let uspeh = false;

	fetch("http://localhost:81/register.php", {
		method: "POST",
		body: JSON.stringify(params)
	}).then(function(response) {
		uspeh = (response.status == 201)
		if (!uspeh) {
			return response.json();
		}
		prijavi_uporabnika(false, vzdevek, geslo);
	}).then(function(j) {
		if (uspeh) {
			return;
		}
		console.log(j);
			odg.className = "obvestilo napaka";
			odg.innerHTML = j["response"];
			odg.style.display = "block";

	}).catch(function(err) {
		console.log(err);
		alert("Napaka, podrobnosti v konzoli.");
	})
}

function izbris_fragmenta(id)
{
	var headers = new Headers();
	headers.append("Authorization", getCookie("zeton"));

	const params = {
		"izbris": true,
		"id": id
	}

	fetch("http://localhost:81/fragment.php", {
		method: "POST",
		body: JSON.stringify(params),
		headers: headers,
	}).then(function(response) {
		location.reload();
	}).catch(function(err) {
		console.log(err);
		alert("Napaka, podrobnosti v konzoli.");
	})
}

function izbris_uporabnika(id)
{
	var headers = new Headers();
	headers.append("Authorization", getCookie("zeton"));

	const params = {
		"izbris": true,
		"id": id
	}

	fetch("http://localhost:81/admin.php", {
		method: "POST",
		body: JSON.stringify(params),
		headers: headers,
	}).then(function(response) {
		location.reload();

	}).catch(function(err) {
		console.log(err);
		alert("Napaka, podrobnosti v konzoli.");
	})
}

function uporabnik_admin(id)
{
	var headers = new Headers();
	headers.append("Authorization", getCookie("zeton"));

	const params = {
		"id": id,
		"admin": true // obrne vrednost
	}

	fetch("http://localhost:81/admin.php", {
		method: "POST",
		body: JSON.stringify(params),
		headers: headers,
	}).then(function(response) {
		// console.log(response);
		location.reload();

	}).catch(function(err) {
		console.log(err);
		alert("Napaka, podrobnosti v konzoli.");
	})
}

// https://www.w3schools.com/js/js_cookies.asp
function getCookie(cname) {
	let name = cname + "=";
	let ca = document.cookie.split(';');
	for(let i = 0; i < ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}
