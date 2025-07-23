document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("menu-toggle");
  const closeBtn = document.getElementById("close-sidebar");
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("overlay");

  // Open sidebar
  toggleBtn.addEventListener("click", () => {
    sidebar.classList.remove("-translate-x-full");
    overlay.classList.remove("hidden");
  });

  // Close sidebar via X
  closeBtn.addEventListener("click", () => {
    sidebar.classList.add("-translate-x-full");
    overlay.classList.add("hidden");
  });

  // Close sidebar via overlay
  overlay.addEventListener("click", () => {
    sidebar.classList.add("-translate-x-full");
    overlay.classList.add("hidden");
  });

  // Close sidebar jika klik di luar sidebar (selain sidebar & overlay)
  document.addEventListener("mousedown", (e) => {
    if (
      !sidebar.classList.contains("-translate-x-full") && // sidebar sedang terbuka
      !sidebar.contains(e.target) && // klik bukan di sidebar
      !toggleBtn.contains(e.target) && // klik bukan di tombol menu
      !overlay.contains(e.target) // klik bukan di overlay (karena overlay sudah handle sendiri)
    ) {
      sidebar.classList.add("-translate-x-full");
      overlay.classList.add("hidden");
    }
  });
});