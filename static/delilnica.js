// let vzd = getCookie("vzdevek");
//
// if (vzd != "") {
// 	// document.getElementById("prijava_uporabnik").innerHTML = vzd;
// 	document.getElementById("odjavi").style.display = "block";
// 	document.getElementById("prijavi").style.display = "none";
// 	document.getElementById("prijava_uporabnik").innerHTML = "Prijavljen kot " + vzdevek;
// }

function odpri_prijavo(ne_zapri=true)
{
	let o  = document.getElementById("prijava_okvir");
	// let p  = document.getElementById("prijavi");
	// let od = document.getElementById("odjavi");

	if (ne_zapri) {
		o.style.display = "block";
		// p.style.display = "none";
	} else {
		o.style.display  = "none";
		// od.style.display = "none";
		// p.style.display  = "block";
	}
}

function odjavi()
{
	document.cookie = "zeton=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
	document.cookie = "vzdevek=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
	location.reload();
}

function prijavi_uporabnika(reload=true, vzdevek=null, geslo=null)
{
	// let obr = document.getElementById("prijava_obrazec");
	let odg = document.getElementById("odgovor");

	if (vzdevek == null) {
		let vzdevek = document.getElementById("vzdevek").value;
		let geslo   = document.getElementById("geslo").value;
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
		// let odgovor = response.json();
		// console.log(odgovor);
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
		// let odgovor = response.json();
		// console.log(odgovor);
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

			// odpri_prijavo(false);
			// odg.style.display = "none";
			// document.cookie = "zeton=" + j["response"];
			// document.cookie = "vzdevek=" + vzdevek;

	}).catch(function(err) {
		console.log(err);
		alert("Napaka, podrobnosti v konzoli.");
	})

}

// https://www.w3schools.com/js/js_cookies.asp
// function getCookie(cname) {
// 	let name = cname + "=";
// 	let ca = document.cookie.split(';');
// 	for(let i = 0; i < ca.length; i++) {
// 		let c = ca[i];
// 		while (c.charAt(0) == ' ') {
// 			c = c.substring(1);
// 		}
// 		if (c.indexOf(name) == 0) {
// 			return c.substring(name.length, c.length);
// 		}
// 	}
// 	return "";
// }
