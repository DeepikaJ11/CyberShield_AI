// Import Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, updateProfile } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";

// Firebase configuration
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

// Elements
const registerForm = document.getElementById("registerForm");
const username = document.querySelector("input[name='username']");
const email = document.querySelector("input[name='email']");
const password = document.querySelector("input[name='password']");
const confirmPassword = document.querySelector("input[name='confirm-password']");
const spinnerOverlay = document.getElementById("spinner-overlay");

// Handle registration
registerForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  if (password.value !== confirmPassword.value) {
    alert("❌ Passwords do not match!");
    return;
  }

  try {
    // Show spinner
    spinnerOverlay.style.display = "flex";

    const userCredential = await createUserWithEmailAndPassword(auth, email.value, password.value);
    const user = userCredential.user;

    // Save display name
    await updateProfile(user, { displayName: username.value });

    // Wait 2 seconds with spinner
    setTimeout(() => {
      spinnerOverlay.style.display = "none";
      window.location.href = "login.html";
    }, 2000);

  } catch (error) {
    spinnerOverlay.style.display = "none"; // hide spinner if error
    alert("❌ " + error.message);
  }
});
