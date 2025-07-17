let currentId;
// Mengambil kategori dari URL. Jika tidak ada, gunakan "Default".
let currentCategory = new URLSearchParams(window.location.search).get("category") || "Default";

// Fungsi untuk menampilkan pesan feedback (pengganti alert)
function showFeedbackMessage(message, isCorrect) {
    const feedbackEl = document.getElementById('feedback-message');
    feedbackEl.textContent = message;
    
    // Hapus kelas warna sebelumnya
    feedbackEl.classList.remove('text-green-600', 'text-red-600', 'font-semibold');
    
    // Tambahkan kelas warna berdasarkan status jawaban
    if (isCorrect) {
        feedbackEl.classList.add('text-green-600', 'font-semibold');
    } else {
        feedbackEl.classList.add('text-red-600', 'font-semibold');
    }

    // Tampilkan pesan
    feedbackEl.classList.remove('opacity-0', '-translate-y-2');
    feedbackEl.classList.add('opacity-100', 'translate-y-0');

    // Sembunyikan pesan setelah beberapa detik
    setTimeout(() => {
        feedbackEl.classList.remove('opacity-100', 'translate-y-0');
        feedbackEl.classList.add('opacity-0', '-translate-y-2');
    }, 2000); // Pesan akan hilang setelah 2 detik
}

// Fungsi untuk memuat pertanyaan dari server
async function loadQuestion(id) {
// Tentukan URL berdasarkan apakah ini pertanyaan pertama atau lanjutan
const url = id ? `/listening-word/${id}/` : `/listening-word/start/${encodeURIComponent(currentCategory)}`;
try {
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data = await res.json();

    if (data.error) {
        showFeedbackMessage(data.error, false);
        return;
    }
    // Simpan ID soal saat ini dan set sumber audio
    currentId = data.id_lw;
    document.getElementById("audio").src = data.audio_url;
} catch (error) {
    console.error("Failed to load question:", error);
    showFeedbackMessage("Failed to load the next question. Please check your connection.", false);
}
}

// Fungsi untuk mengevaluasi jawaban siswa
async function evaluateAnswer() {
const answerInput = document.getElementById("answer");
const answer = answerInput.value;

// Jangan lakukan apa-apa jika tidak ada jawaban
if (!answer.trim()) {
    showFeedbackMessage("Please type your answer first!", false);
    return;
}

try {
    const res = await fetch("/listening-word/answer/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_lw: currentId, student_answer: answer }),
    });
    if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
    }
    const result = await res.json();

    // new alert
    showFeedbackMessage(result.correct ? "Correct! Great job!" : "Incorrect, try the next one!", result.correct);

    // Simpan riwayat jawaban
    window.attemptAnswers = window.attemptAnswers || [];
    window.attemptAnswers.push({
        id_lw: currentId,
        answer: answer,
        is_correct: result.correct
    });

    // Jika ada soal berikutnya, muat soal tersebut setelah jeda singkat
    if (result.next_id) {
        setTimeout(() => {
            loadQuestion(result.next_id);
            answerInput.value = ""; // Kosongkan input
        }, 1500); // Tunggu 1.5 detik sebelum memuat soal baru
    } else {
        // Jika tidak ada soal lagi, proses hasil akhir
        setTimeout(() => {
            const user = JSON.parse(localStorage.getItem("user"));
            const username = user?.username;
            const category = new URLSearchParams(window.location.search).get("category");

            const completeAttempt = {
            student_id: username,
            category_id: category,
            questions: window.attemptAnswers
            };

            localStorage.setItem("complete_attempt", JSON.stringify(completeAttempt));

            // Arahkan ke halaman hasil
            window.location.href = "/result?type=listening-word"; 
        }, 1500); // Tunggu 1.5 detik sebelum redirect
    }
} catch(error) {
    console.error("Failed to evaluate answer:", error);
    showFeedbackMessage("Could not submit your answer. Please try again.", false);
}
}

// Fungsi untuk memutar audio
function playAudio() {
const audio = document.getElementById("audio");
const speakerBtn = document.getElementById('speaker-btn');
audio.volume = 0.5;
audio.play();

// Tambahkan animasi saat audio diputar
speakerBtn.classList.add('playing');
audio.onended = () => {
    speakerBtn.classList.remove('playing');
};
}

// Menambahkan event listener ke tombol
document.getElementById("evaluateBtn").onclick = evaluateAnswer;
document.getElementById("speaker-btn").onclick = playAudio;
// Memungkinkan submit dengan menekan tombol Enter
document.getElementById("answer").addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        evaluateAnswer();
    }
});

// Memuat pertanyaan pertama saat halaman dibuka
loadQuestion();