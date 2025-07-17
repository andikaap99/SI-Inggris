// --- LOGIKA KUIS (DARI FILE ASLI ANDA) ---
let currentId;
let currentCategory = new URLSearchParams(window.location.search).get("category") || "Default";

// Fungsi untuk menampilkan pesan feedback (pengganti alert)
function showFeedbackMessage(message, isCorrect) {
    const feedbackEl = document.getElementById('feedback-message');
    feedbackEl.textContent = message;
    feedbackEl.classList.remove('text-green-600', 'text-red-600', 'font-semibold');
    feedbackEl.classList.add(isCorrect ? 'text-green-600' : 'text-red-600', 'font-semibold');
    feedbackEl.classList.remove('opacity-0', '-translate-y-2');
    feedbackEl.classList.add('opacity-100', 'translate-y-0');

    setTimeout(() => {
        feedbackEl.classList.remove('opacity-100', 'translate-y-0');
        feedbackEl.classList.add('opacity-0', '-translate-y-2');
    }, 2000);
}

async function loadQuestion(id) {
    const url = id ? `/complete-sentence/${id}/` : `/complete-sentence/start/${encodeURIComponent(currentCategory)}`;
    try {
        const res = await fetch(url);
        const data = await res.json();
        if (data.error) {
            showFeedbackMessage(data.error, false);
            return;
        }
        currentId = data.id_cs;
        // Mengganti placeholder ___ dengan span yang bisa di-style
        const formattedQuestion = data.question.replace('___', '<span class="blank"></span>');
        document.getElementById("question").innerHTML = formattedQuestion;
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
        const res = await fetch("/complete-sentence/answer/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_cs: currentId, student_answer: answer }),
        });
        const result = await res.json();

        // Menggunakan feedback baru, bukan alert
        showFeedbackMessage(result.correct ? "Correct! Great job!" : "Incorrect. Let's try the next one.", result.correct);

        window.attemptAnswers = window.attemptAnswers || [];
        window.attemptAnswers.push({
            id_cs: currentId,
            answer: answer,
            is_correct: result.correct
        });

        if (result.next_id) {
            setTimeout(() => {
                loadQuestion(result.next_id);
                answerInput.value = "";
            }, 1500);
        } else {
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
                // Arahkan ke halaman hasil yang benar
                window.location.href = "/result?type=complete-sentence";
            }, 1500);
        }
    } catch (error) {
        console.error("Failed to evaluate answer:", error);
        showFeedbackMessage("Could not submit answer.", false);
    }
}

document.getElementById("evaluateBtn").onclick = evaluateAnswer;
document.getElementById("answer").addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        evaluateAnswer();
    }
});

// Memuat soal pertama
loadQuestion();