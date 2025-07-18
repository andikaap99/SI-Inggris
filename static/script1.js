document.addEventListener('DOMContentLoaded', () => {
    // --- FUNGSI SIDEBAR ---
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('close-sidebar');
    const overlay = document.getElementById('overlay');

    if (menuToggle && sidebar && closeSidebar && overlay) {
        const showSidebar = () => {
            sidebar.classList.remove('-translate-x-full');
            overlay.classList.remove('hidden');
        };
        const hideSidebar = () => {
            sidebar.classList.add('-translate-x-full');
            overlay.classList.add('hidden');
        };
        menuToggle.addEventListener('click', showSidebar);
        closeSidebar.addEventListener('click', hideSidebar);
        overlay.addEventListener('click', hideSidebar);
    }

    // --- FUNGSI PROFIL DROPDOWN & USERNAME ---
    const profileButton = document.getElementById('profile-button');
    const profileDropdown = document.getElementById('profile-dropdown');
    const usernameDisplay = document.getElementById('username-display');

    // Ambil dan tampilkan username dari localStorage
    try {
        const user = JSON.parse(localStorage.getItem("user"));
        if (user && user.username) {
            usernameDisplay.textContent = user.username;
        } else {
            usernameDisplay.textContent = "Guest"; // Teks cadangan jika tidak ada user
        }
    } catch (e) {
        console.error("Could not parse user from localStorage", e);
        usernameDisplay.textContent = "Guest";
    }

    // Tampilkan/sembunyikan dropdown saat tombol profil diklik
    if (profileButton && profileDropdown) {
        profileButton.addEventListener('click', (event) => {
            event.stopPropagation(); // Mencegah event 'click' dari window
            profileDropdown.classList.toggle('hidden');
        });
    }

    // Sembunyikan dropdown jika klik di luar area dropdown
    window.addEventListener('click', () => {
        if (profileDropdown && !profileDropdown.classList.contains('hidden')) {
            profileDropdown.classList.add('hidden');
        }
    });
    
    // Fungsi untuk logout
    const logoutButton = document.getElementById('logout-button');
    if(logoutButton) {
        logoutButton.addEventListener('click', (event) => {
            event.preventDefault(); // Mencegah link default
            // Hapus data user dari localStorage
            localStorage.removeItem('user');
            // Arahkan ke halaman login (ganti '/login' dengan URL halaman login Anda)
            window.location.href = '/login'; 
        });
    }
});

lucide.createIcons();

//*SCORE*//
window.onload = async function () {
    // --- FUNGSI PROFIL DROPDOWN & USERNAME ---
    const profileButton = document.getElementById('profile-button');
    const profileDropdown = document.getElementById('profile-dropdown');
    const usernameDisplay = document.getElementById('username-display');

    // Ambil dan tampilkan username dari localStorage
    try {
        const user = JSON.parse(localStorage.getItem("user"));
        if (user && user.username) {
            usernameDisplay.textContent = user.username;
        } else {
            usernameDisplay.textContent = "Guest";
        }
    } catch (e) {
        console.error("Could not parse user from localStorage", e);
        usernameDisplay.textContent = "Guest";
    }

    // Tampilkan/sembunyikan dropdown saat tombol profil diklik
    if (profileButton && profileDropdown) {
        profileButton.addEventListener('click', (event) => {
            event.stopPropagation();
            profileDropdown.classList.toggle('hidden');
        });
    }

    // Sembunyikan dropdown jika klik di luar area
    window.addEventListener('click', () => {
        if (profileDropdown && !profileDropdown.classList.contains('hidden')) {
            profileDropdown.classList.add('hidden');
        }
    });
    
    // Fungsi untuk logout
    const logoutButton = document.getElementById('logout-button');
    if(logoutButton) {
        logoutButton.addEventListener('click', (event) => {
            event.preventDefault();
            localStorage.removeItem('user');
            window.location.href = '/login'; // Ganti dengan URL login Anda
        });
    }

    // --- LOGIKA SKOR ---
    const type = new URLSearchParams(window.location.search).get("type") || "complete-sentence";

    let endpoint = "/complete-sentence/save-attempt/";
    if (type === "listening-word") {
        endpoint = "/listening-word/save-attempt/";
    } else if (type === "image-word") {
        endpoint = "/image-word/save-attempt/";
    } else if (type === "listening-sentence") {
        endpoint = "/listening-sentence/save-attempt/";
    }

    const attempt = JSON.parse(localStorage.getItem("complete_attempt"));
    if (!attempt) {
        document.getElementById("score-many").innerText = '0';
        document.getElementById("correct-answers").innerText = '0';
        document.getElementById("incorrect-answers").innerText = '0';
        document.getElementById("score-value").innerText = "0%";
        return;
    };

    const totalQuestions = attempt.questions.length;
    const correctAnswers = attempt.questions.filter(q => q.is_correct).length;
    const incorrectAnswers = totalQuestions - correctAnswers;
    const scorePercent = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;

    document.getElementById("score-many").innerText = totalQuestions;
    document.getElementById("correct-answers").innerText = correctAnswers;
    document.getElementById("incorrect-answers").innerText = incorrectAnswers;
    document.getElementById("score-value").innerText = scorePercent + "%";

    const circle = document.getElementById('progress-circle');
    const radius = circle.r.baseVal.value;
    const circumference = radius * 2 * Math.PI;
    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    const offset = circumference - scorePercent / 100 * circumference;
    circle.style.strokeDashoffset = offset;

    if (scorePercent > 70) {
        confetti({
            particleCount: 150,
            spread: 90,
            origin: { y: 0.6 }
        });
    }

    const retryButton = document.getElementById('retry-button');
    if (retryButton) {
        retryButton.onclick = () => {
            let practicePage = '/'; // Halaman default
            if (type === 'listening-word') practicePage = '/listening-word-word';
            // Tambahkan path lain jika perlu
            // else if (type === 'image-word') practicePage = '/image-word-practice';

            window.location.href = `${practicePage}?category=${attempt.category_id || ''}`;
        }
    }

    try {
        const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(attempt),
        });

        const result = await res.json();
        console.log("Attempt disimpan:", result.message);
        localStorage.removeItem("complete_attempt");
    } catch (err) {
        console.error("Gagal menyimpan attempt:", err);
    }
    };