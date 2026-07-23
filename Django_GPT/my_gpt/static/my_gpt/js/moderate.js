document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("moderate-form");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        clearError();
        setLoading(form, true);

        const text =
            form.querySelector("textarea").value.trim();

        try {

            const response = await fetch(
                form.dataset.runUrl,
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json",
                        "X-CSRFToken":
                            getCookie("csrftoken"),
                    },
                    body: JSON.stringify({
                        text,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok || !data.ok) {
                showError(data.error);
                return;
            }

            showResult(data.result);

            addLoginHistory(data.history);

        } catch {

            showError("서버 오류가 발생했습니다.");

        } finally {

            setLoading(form, false);

        }

    });

});

function clearError() {
    const errorBox = document.getElementById("error-box");

    if (!errorBox) return;

    errorBox.textContent = "";
    errorBox.style.display = "none";
}


function showError(message) {
    const errorBox = document.getElementById("error-box");

    if (!errorBox) return;

    errorBox.textContent = message;
    errorBox.style.display = "block";
}


function showResult(result) {
    const resultBox = document.getElementById("result-box");
    const topLabel = document.getElementById("top-label");
    const topScore = document.getElementById("top-score");
    const allLabels = document.getElementById("all-labels");

    if (
        !resultBox
        || !topLabel
        || !topScore
        || !allLabels
    ) {
        return;
    }

    topLabel.textContent = result.top_label;
    topScore.textContent = `${result.top_score}%`;

    allLabels.replaceChildren();

    result.labels.forEach((item) => {
        const paragraph = document.createElement("p");

        paragraph.textContent =
            `${item.label}: ${item.score}%`;

        allLabels.appendChild(paragraph);
    });

    resultBox.style.display = "block";
}


function addLoginHistory(history) {
    if (!history) return;

    const historyList =
        document.getElementById("login-history");

    if (!historyList) return;

    const emptyHistory =
        historyList.querySelector(".empty-history");

    if (emptyHistory) {
        emptyHistory.remove();
    }

    const article = document.createElement("article");

    article.innerHTML = `
        <p>
            <strong>입력:</strong>
            ${history.input.slice(0, 100)}
        </p>

        <p>
            <strong>가장 높은 항목:</strong>
            ${history.result.top_label}
        </p>

        <p>
            <strong>점수:</strong>
            ${history.result.top_score}%
        </p>

        <p>
            <small>
                ${new Date(
                    history.created_at
                ).toLocaleString()}
            </small>
        </p>
    `;

    historyList.prepend(article);

    const articles =
        historyList.querySelectorAll("article");

    if (articles.length > 5) {
        articles[articles.length - 1].remove();
    }
}