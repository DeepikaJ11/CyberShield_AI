// Import Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";

// ✅ Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDFqoJ0cxZRj6Gf_Q4h5awQa_7xTilR7AM",
  authDomain: "bully-block-ai-39bf7.firebaseapp.com",
  databaseURL: "https://bully-block-ai-39bf7-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "bully-block-ai-39bf7",
  storageBucket: "bully-block-ai-39bf7.firebasestorage.app",
  messagingSenderId: "1029684496192",
  appId: "1:1029684496192:web:ea9e7f5f8a5e5022ca5ca5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Form elements
const loginForm = document.getElementById("loginForm");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const errorMsg = document.getElementById("error-msg");
const spinnerOverlay = document.getElementById("spinnerOverlay");

// Handle login
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const email = emailInput.value;
  const password = passwordInput.value;

  signInWithEmailAndPassword(auth, email, password)
    .then(() => {
      errorMsg.textContent = "";
      spinnerOverlay.style.display = "flex"; // show spinner

      setTimeout(() => {
        window.location.href = "dashboard.html"; // redirect after 2 sec
      }, 2000);
    })
    .catch((error) => {
      spinnerOverlay.style.display = "none"; // hide spinner if error
      errorMsg.textContent = "❌ " + error.message;
    });
});
