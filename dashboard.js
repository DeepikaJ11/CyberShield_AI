import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";

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

// ✅ Protect page: redirect to login if not authenticated
onAuthStateChanged(auth, (user) => {
  if (!user) {
    window.location.href = "login.html";
  }
});

// ✅ Logout functionality
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    signOut(auth)
      .then(() => {
        window.location.href = "login.html";
      })
      .catch((error) => {
        alert("Error signing out: " + error.message);
      });
  });
}

// ✅ Fetch live stats from Flask backend
async function loadStats() {
  try {
    const res = await fetch("http://127.0.0.1:5000/stats");
    const data = await res.json();

    document.getElementById("totalMessages").innerText = data.total;
    document.getElementById("highAlerts").innerText = data.high;
    document.getElementById("flaggedUsers").innerText = data.flagged;

    console.log("✅ Stats loaded:", data);
  } catch (error) {
    console.error("❌ Error loading stats:", error);
  }
}

// Load once on page open
loadStats();

// Refresh every 5 seconds
setInterval(loadStats, 5000);
