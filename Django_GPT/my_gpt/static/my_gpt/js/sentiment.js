const guestHistory = [];


document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("sentiment-form");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const textarea = form.querySelector("textarea");
        const text = textarea.value.trim();
        const runUrl = form.dataset.runUrl;
        const isAuthenticated =
            form.dataset.authenticated === "true";

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
                    data.error || "분석 중 오류가 발생했습니다."
                );
                return;
            }

            showResult(data.result);

            if (isAuthenticated && data.history) {
                addLoginHistory(data.history);
            } else {
                addGuestHistory(text, data.result);
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
    const label = document.getElementById("result-label");
    const score = document.getElementById("result-score");

    label.textContent = result.label_ko;
    score.textContent = `${result.score}%`;
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


function addGuestHistory(input, result) {
    guestHistory.unshift({
        input: input,
        result: result,
        createdAt: new Date(),
    });

    if (guestHistory.length > 5) {
        guestHistory.pop();
    }

    renderGuestHistory();
}


function renderGuestHistory() {
    const historyList = document.getElementById("guest-history");

    if (!historyList) {
        return;
    }

    historyList.replaceChildren();

    guestHistory.forEach((history) => {
        const article = createHistoryArticle(
            history.input,
            history.result,
            history.createdAt
        );

        historyList.appendChild(article);
    });
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
        document.createTextNode(input)
    );

    const resultParagraph = document.createElement("p");
    const resultTitle = document.createElement("strong");

    resultTitle.textContent = "결과: ";
    resultParagraph.appendChild(resultTitle);
    resultParagraph.appendChild(
        document.createTextNode(
            `${result.label_ko} / ${result.score}%`
        )
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