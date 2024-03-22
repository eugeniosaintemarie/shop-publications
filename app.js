if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
        navigator.serviceWorker
            .register("https://eugeniosaintemarie.github.io/shop-publications/serviceWorker.js")
            .then(res => console.log("service worker registered"))
            .catch(err => console.log("service worker not registered", err))
    })
}

function isIOS() {
    return [
        'iPad Simulator',
        'iPhone Simulator',
        'iPod Simulator',
        'iPad',
        'iPhone',
        'iPod'
    ].includes(navigator.platform)
        || (navigator.userAgent.includes("Mac") && "ontouchend" in document);
}

function isSafari() {
    return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
}

function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

if (isIOS() && isSafari()) {
    var hasSeenPopup = getCookie('hasSeenPopup');
    if (!hasSeenPopup) {
        var popup = document.createElement("div");
        popup.style.position = "fixed";
        popup.style.bottom = "0";
        popup.style.width = "100%";
        popup.style.padding = "20px";
        popup.style.backgroundColor = "#ED1C24";
        popup.style.color = "white";
        popup.style.textAlign = "center";
        popup.innerHTML = "Para instalar HSBC Seguros Online, haz clic en el botón 'Compartir', y luego en 'Añadir a la pantalla de inicio' <button onclick='closePopup()'>Cerrar</button>";
        document.body.appendChild(popup);

        function closePopup() {
            document.body.removeChild(popup);
            setCookie('hasSeenPopup', true, 7);
        }
    }
}

Notification.requestPermission().then(function (result) {
    console.log(result);
});

const webpush = require('web-push');

const vapidKeys = {
    publicKey: process.env.PUBLIC_KEY,
    privateKey: process.env.PRIVATE_KEY
};

webpush.setVapidDetails(
    'mailto:e.saintemarie@outlook.com',
    vapidKeys.publicKey,
    vapidKeys.privateKey
);

const pushSubscription = {
    endpoint: process.env.SUBSCRIPTION_ENDPOINT,
    keys: {
        p256dh: process.env.P256DH_KEY,
        auth: process.env.AUTH_KEY
    }
};

const payload = JSON.stringify({
    title: 'Nuevo precio',
    body: 'El precio de una publicación cambio',
    icon: 'https://eugeniosaintemarie.github.io/shop-publications/image/icon/icon-72x72.png',
    badge: 'https://eugeniosaintemarie.github.io/shop-publications/image/icon/icon-72x72.png'
});

webpush.sendNotification(pushSubscription, payload).catch(error => {
    console.error(error.stack);
});