const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    auth.signInWithEmailAndPassword(email, password)
    .then(userCredential => {
        const user = userCredential.user;
        console.log('User signed in:', user);
        document.getElementById('loginMessage').textContent = 'Login successful!';
        document.querySelectorAll('.hidden').forEach(link => link.classList.remove('hidden'));
    })
    .catch(error => {
        console.error('Error signing in:', error);
        document.getElementById('loginMessage').textContent = 'Login failed: ' + error.message;
    });
});
