function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(";") : [];

    for (const cookieItem of cookies) {
        const cookie = cookieItem.trim();

        if (cookie.startsWith(`${name}=`)) {
            return decodeURIComponent(
                cookie.substring(name.length + 1)
            );
        }
    }

    return null;
}


function setLoading(form, isLoading) {
    const button = form.querySelector("button[type='submit']");
    const textarea = form.querySelector("textarea");
    const loading = form.querySelector(".loading");

    if (button) {
        if (!button.dataset.originalText) {
            button.dataset.originalText = button.textContent.trim();
        }

        button.disabled = isLoading;
        button.textContent = isLoading
            ? "처리 중..."
            : button.dataset.originalText;
    }

    if (textarea) {
        textarea.readOnly = isLoading;
    }

    if (loading) {
        loading.style.display = isLoading ? "block" : "none";
    }
}