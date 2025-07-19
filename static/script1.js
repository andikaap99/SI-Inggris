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
