document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("summarize-form");

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
                    data.error || "요약 중 오류가 발생했습니다."
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

    document.getElementById("original-length").textContent =
        `${result.original_length}자`;

    document.getElementById("summary-length").textContent =
        `${result.summary_length}자`;

    document.getElementById("compression-ratio").textContent =
        `${result.compression_ratio}%`;

    document.getElementById("summary-text").textContent =
        result.summary;

    resultBox.style.display = "block";
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

    const inputParagraph = document.createElement("p");
    const inputTitle = document.createElement("strong");

    inputTitle.textContent = "입력: ";
    inputParagraph.appendChild(inputTitle);
    inputParagraph.appendChild(
        document.createTextNode(input.slice(0, 100))
    );

    const resultParagraph = document.createElement("p");
    const resultTitle = document.createElement("strong");

    resultTitle.textContent = "요약: ";
    resultParagraph.appendChild(resultTitle);
    resultParagraph.appendChild(
        document.createTextNode(result.summary.slice(0, 150))
    );

    const timeParagraph = document.createElement("p");
    const small = document.createElement("small");

    small.textContent = createdAt.toLocaleString();
    timeParagraph.appendChild(small);

    article.appendChild(inputParagraph);
    article.appendChild(resultParagraph);
    article.appendChild(timeParagraph);

    return article;
}