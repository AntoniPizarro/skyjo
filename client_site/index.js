let ip = "192.168.1.34";
let port = "5505"

function logging() {
    let userName = document.getElementById("user-name").value;
    let userPass = document.getElementById("user-pass").value;
    if (userName != "" && userPass != "") {
        user = {
            name: userName,
            password: userPass
        };
        getData(user);

        let parameters = new URLSearchParams(window.location.search);
        parameters.append("name", userName);
        parameters.append("password", userPass);
        console.log(parameters.toString());
        let url = "index.html?name=" + userName + "&password=" + userPass;
        goURL(url);
    } else {
        alert("Faltan datos para loguearse.");
    }
}

function goURL(url) {
    window.location = url;
}

function getData(user) {
    fetch("http://" + ip + ":" + port + '/logging', {
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify(user),
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(jsonData => jsonData.json())
    .then(data => {
        console.log(data);
    });
}

function getPlayers() {
    fetch("http://" + ip + ":" + port + '/players', {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(jsonData => jsonData.json())
    .then(data => {
        console.log(data);
    });
}

function getSesion() {
    let parameters = new URLSearchParams(window.location.search);
    userName = parameters.get("name");
    userPass = parameters.get("password");

    return [userName, userPass];
}

function voteStart() {
    let sesion = getSesion();
    userName = sesion[0];
    userPass = sesion[1];
    console.log({vote: true, name: userName, password: userPass});
    fetch("http://" + ip + ":" + port + '/start', {
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify({vote: true, name: userName, password: userPass}),
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(jsonData => jsonData.json())
    .then(data => {
        console.log(data);
    });
}

function buildDeck() {
    
}

function getMazes() {
    let sesion = getSesion();
    userName = sesion[0];
    userPass = sesion[1]
    fetch("http://" + ip + ":" + port + '/decks', {
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify({name: userName, password: userPass}),
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(jsonData => jsonData.json())
    .then(data => {
        buildMazes(data);
    });
}

function buildMazes(mazes) {
    let mesa = document.getElementById("mesa");

    let ownDeck = document.createElement("div");
    ownDeck.className = "own";

    let othersDecks = document.createElement("div");
    othersDecks.className = "others";

    function createLine() {
        let line = document.createElement("div");
        line.className = "line";
        return line;
    }

    let cards = 0;
    let line = createLine();

    let cardID = 0;
    mazes["owner"].forEach(element => {
        cards++;
        let card = document.createElement("div");
        card.id = cardID;
        cardID++;
        card.innerHTML = "<h2 style=\"user-select: none;\">" + element + "</h2>";
        let cardType = 5;
        if (element < -2) {
            cardType = 5;
            card.innerHTML = "<h2 style=\"user-select: none;\">?</h2>";
        } else if (element >= -2 && element <= -1) {
            cardType = 0;
        } else if (element == 0) {
            cardType = 1;
        } else if (element >= 1 && element <= 4) {
            cardType = 2;
        } else if (element >= 5 && element <= 8) {
            cardType = 3;
        } else if (element >= 9) {
            cardType = 4;
        }

        card.className = "card-" + cardType;
        card.setAttribute("onclick", "acction(this)");

        line.appendChild(card.cloneNode(true));
        if (cards >= 4) {
            cards = 0;
            ownDeck.appendChild(line.cloneNode(true));
            line = createLine();
        }
    });

    cards = 0;
    line = createLine();
    for (let player in mazes["others"]) {
        othersDecks.innerHTML += "<h1 class=\"player-name\">" + player + "</h1>";
        mazes["others"][player].forEach(element => {
            cards++;
            let card = document.createElement("div");
            card.id = cardID;
            cardID++;
            card.innerHTML = "<h2 style=\"user-select: none;\">" + element + "</h2>";
            let cardType = 5;
            if (element < -2) {
                cardType = 5;
                card.innerHTML = "<h2 style=\"user-select: none;\">?</h2>";
            } else if (element >= -2 && element <= -1) {
                cardType = 0;
            } else if (element == 0) {
                cardType = 1;
            } else if (element >= 1 && element <= 4) {
                cardType = 2;
            } else if (element >= 5 && element <= 8) {
                cardType = 3;
            } else if (element >= 9) {
                cardType = 4;
            }
            card.className = "card-" + cardType;

            line.appendChild(card.cloneNode(true));
            if (cards >= 4) {
                cards = 0;
                othersDecks.appendChild(line.cloneNode(true));
                line = createLine();
            }
        });
    }
    mesa.innerHTML = "";
    mesa.appendChild(ownDeck);
    mesa.appendChild(othersDecks);
}

async function acction(card) {
    let sesion = getSesion();
    let userName = sesion[0];
    let userPass = sesion[1]
    let selectedCardID = "";
    let turn = await checkTurn();
    if (firstTurn()) {
        selectedCardID = card.id;
        revealCard(selectedCardID);
    }else if (turn.turn == userName) {
        alert("Es tu turno");
    }else {
        alert("Es el turno de " + turn.turn);
    }
    getMazes();
}

function revealCard(cardID) {
    let sesion = getSesion();
    userName = sesion[0];
    userPass = sesion[1];
    fetch("http://" + ip + ":" + port + '/reveal', {
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify({to_reveal: cardID, name: userName, password: userPass}),
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(jsonData => jsonData.json())
    .then(data => {
        console.log(data);
    });
}

function firstTurn() {
    let ownDeck = document.getElementById("mesa").querySelectorAll('.own')[0];
    let discarted = ownDeck.querySelectorAll('.card-5');
    let values = 0;
    discarted.forEach(element => {
        cardValue = element.firstChild.innerHTML;
        if (cardValue == '?') {
            values++;
        }
    });
    if (values > 10) {
        return true;
    }else{
        return false;
    }
}

function checkTurn() {
    let turn = fetch("http://" + ip + ":" + port + '/checkturn', {
        method: 'GET',
        mode: 'cors'
    })
    .then(jsonData => jsonData.json())
    .then(data => {return data});

    return turn;
}