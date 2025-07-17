document.addEventListener('DOMContentLoaded', () => {
    // --- LOGIKA KUIS  ---
    let currentId;
    let currentCategory = new URLSearchParams(window.location.search).get("category") || "Default";

    // Fungsi untuk menampilkan pesan feedback (pengganti alert)
    function showFeedbackMessage(message, isCorrect) {
        const feedbackEl = document.getElementById('feedback-message');
        feedbackEl.textContent = message;
        feedbackEl.classList.remove('text-green-600', 'text-red-600', 'font-semibold');
        
        // Jika isCorrect adalah boolean, gunakan warna hijau/merah
        if (typeof isCorrect === 'boolean') {
            feedbackEl.classList.add(isCorrect ? 'text-green-600' : 'text-red-600', 'font-semibold');
        } else {
            // Jika tidak (misalnya untuk menampilkan skor), gunakan warna netral
            feedbackEl.classList.add('text-gray-700', 'font-semibold');
        }

        feedbackEl.classList.remove('opacity-0', '-translate-y-2');
        feedbackEl.classList.add('opacity-100', 'translate-y-0');

        setTimeout(() => {
            feedbackEl.classList.remove('opacity-100', 'translate-y-0');
            feedbackEl.classList.add('opacity-0', '-translate-y-2');
        }, 2500); // Tampilkan pesan lebih lama
    }

    async function loadQuestion(id) {
        const url = id ? `/listening-sentence/${id}/` : `/listening-sentence/start/${encodeURIComponent(currentCategory)}`;
        try {
            const res = await fetch(url);
            const data = await res.json();
            if (data.error) {
                showFeedbackMessage(data.error, false);
                return;
            }
            currentId = data.id_ls;
            document.getElementById("audio").src = data.audio_url;
        } catch (error) {
            console.error("Failed to load question:", error);
            showFeedbackMessage("Failed to load question.", false);
        }
    }

    async function evaluateAnswer() {
        const answerInput = document.getElementById("answer");
        const answer = answerInput.value;
        if (!answer.trim()) {
            showFeedbackMessage("Please type your answer first!", false);
            return;
        }

        try {
            const res = await fetch("/listening-sentence/answer/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id_ls: currentId, student_answer: answer }),
            });
            const result = await res.json();

            // Menggunakan feedback baru, bukan alert
            showFeedbackMessage("Your Score: " + result.final_score, null); // null karena ini bukan true/false

            if (result.next_id) {
                setTimeout(() => {
                    loadQuestion(result.next_id);
                    answerInput.value = "";
                }, 1500);
            } else {
                // Tidak ada soal lagi, bisa arahkan ke halaman skor jika ada
                showFeedbackMessage("Quiz finished! No more questions.", null);
                setTimeout(() => {
                    // Arahkan ke halaman menu atau home, karena tidak ada halaman skor khusus untuk tipe ini
                        window.location.href = "/listening-sentence";
                }, 2500);
            }
        } catch (error) {
            console.error("Failed to evaluate answer:", error);
            showFeedbackMessage("Could not submit answer.", false);
        }
    }
    
    function playAudio() {
        const audio = document.getElementById("audio");
        const speakerBtn = document.getElementById('speaker-btn');
        audio.volume = 0.5;
        audio.play();
        
        speakerBtn.classList.add('playing');
        audio.onended = () => {
            speakerBtn.classList.remove('playing');
        };
    }

    document.getElementById("evaluateBtn").onclick = evaluateAnswer;
    document.getElementById("speaker-btn").onclick = playAudio;
    document.getElementById("answer").addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            evaluateAnswer();
        }
    });

    // Memuat soal pertama
    loadQuestion();
});
