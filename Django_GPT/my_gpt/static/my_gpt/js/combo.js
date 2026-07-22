document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("combo-form");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const textarea = form.querySelector("textarea");
        const text = textarea.value.trim();
        const runUrl = form.dataset.runUrl;

        clearError();
        setLoading(form, true);

        try {
            const response = await fetch(runUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({
                    text: text,
                }),
            });

            const data = await response.json();

            if (!response.ok || !data.ok) {
                showError(
                    data.error
                    || "복합 분석 중 오류가 발생했습니다."
                );

                return;
            }

            showResult(data.result);

            if (data.history) {
                addLoginHistory(data.history);
            }
        } catch (error) {
            console.error(error);

            showError(
                "서버와 통신 중 오류가 발생했습니다. "
                + "잠시 후 다시 시도해 주세요."
            );
        } finally {
            setLoading(form, false);
        }
    });
});


function showResult(result) {
    const resultBox = document.getElementById("result-box");

    document.getElementById("sentiment-label").textContent =
        result.sentiment.label_ko;

    document.getElementById("sentiment-score").textContent =
        `${result.sentiment.score}%`;

    document.getElementById("toxicity-label").textContent =
        result.toxicity.top_label;

    document.getElementById("toxicity-score").textContent =
        `${result.toxicity.top_score}%`;

    renderToxicityLabels(result.toxicity.labels);
    renderSummary(result.summary);

    resultBox.style.display = "block";
}


function renderToxicityLabels(labels) {
    const labelsBox =
        document.getElementById("toxicity-labels");

    labelsBox.replaceChildren();

    labels.forEach((item) => {
        const paragraph = document.createElement("p");

        paragraph.textContent =
            `${item.label}: ${item.score}%`;

        labelsBox.appendChild(paragraph);
    });
}


function renderSummary(summary) {
    const summarySection =
        document.getElementById("summary-section");

    const summaryMessage =
        document.getElementById("summary-message");

    if (!summary) {
        summarySection.style.display = "none";
        summaryMessage.style.display = "block";
        return;
    }

    document.getElementById("original-length").textContent =
        `${summary.original_length}자`;

    document.getElementById("summary-length").textContent =
        `${summary.summary_length}자`;

    document.getElementById("compression-ratio").textContent =
        `${summary.compression_ratio}%`;

    document.getElementById("summary-text").textContent =
        summary.summary;

    summaryMessage.style.display = "none";
    summarySection.style.display = "block";
}


function showError(message) {
    const errorBox = document.getElementById("error-box");

    errorBox.textContent = message;
    errorBox.style.display = "block";
}


function clearError() {
    const errorBox = document.getElementById("error-box");

    errorBox.textContent = "";
    errorBox.style.display = "none";
}


function addLoginHistory(history) {
    const historyList = document.getElementById("login-history");

    if (!historyList) {
        return;
    }

    const emptyMessage =
        historyList.querySelector(".empty-history");

    if (emptyMessage) {
        emptyMessage.remove();
    }

    const article = createHistoryArticle(
        history.input,
        history.result,
        new Date(history.created_at)
    );

    historyList.prepend(article);

    const articles = historyList.querySelectorAll("article");

    if (articles.length > 5) {
        articles[articles.length - 1].remove();
    }
}


function createHistoryArticle(input, result, createdAt) {
    const article = document.createElement("article");

    appendHistoryRow(
        article,
        "입력: ",
        input.slice(0, 100)
    );

    appendHistoryRow(
        article,
        "감정: ",
        `${result.sentiment.label_ko} / `
        + `${result.sentiment.score}%`
    );

    appendHistoryRow(
        article,
        "유해 표현: ",
        `${result.toxicity.top_label} / `
        + `${result.toxicity.top_score}%`
    );

    if (result.summary) {
        appendHistoryRow(
            article,
            "요약: ",
            result.summary.summary.slice(0, 150)
        );
    }

    const timeParagraph = document.createElement("p");
    const small = document.createElement("small");

    small.textContent = createdAt.toLocaleString();
    timeParagraph.appendChild(small);
    article.appendChild(timeParagraph);

    return article;
}


function appendHistoryRow(article, title, value) {
    const paragraph = document.createElement("p");
    const strong = document.createElement("strong");

    strong.textContent = title;

    paragraph.appendChild(strong);
    paragraph.appendChild(
        document.createTextNode(value)
    );

    article.appendChild(paragraph);
}