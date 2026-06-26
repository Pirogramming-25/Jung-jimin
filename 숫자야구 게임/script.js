let answer = [];
let attempts = 9;

function makeAnswer() {
    while (answer.length < 3) {
        let randomNumber = Math.floor(Math.random() * 10);

        if (!answer.includes(randomNumber)) {
            answer.push(randomNumber);
        }
    }
}

function check_numbers() {
    const input1 = document.getElementById("number1").value;
    const input2 = document.getElementById("number2").value;
    const input3 = document.getElementById("number3").value;

    if (input1 === "" || input2 === "" || input3 === "") {
        clearInputs();
        return;
    }

    const userNumbers = [Number(input1), Number(input2), Number(input3)];

    let strike = 0;
    let ball = 0;

    for (let i = 0; i < 3; i++) {
        if (userNumbers[i] === answer[i]) {
            strike++;
        } else if (answer.includes(userNumbers[i])) {
            ball++;
        }
    }

    let resultHTML;

    if (strike === 0 && ball === 0) {
        resultHTML = `<span class="out num-result">O</span>`;
    } else {
    resultHTML = `
        <span>${strike}</span> 
        <span class="strike num-result">S</span>
        <span>${ball}</span>
        <span class="ball num-result">B</span>
        `;
    }

    const resultDiv = document.createElement("div");
    resultDiv.classList.add("check-result");

    resultDiv.innerHTML = `
    <span class="left">${userNumbers.join(" ")}</span>
    <span>:</span>
    <span class="right">${resultHTML}</span>
    `;

    document.getElementById("results").appendChild(resultDiv);

    attempts--;
    document.getElementById("attempts").innerText = attempts;

    if (strike === 3) {
        document.getElementById("game-result-img").src = "success.png";
        document.querySelector(".submit-button").disabled = true;
        clearInputs();
        return;
    }

    if (attempts === 0) {
        document.getElementById("game-result-img").src = "fail.png";
        document.querySelector(".submit-button").disabled = true;
        clearInputs();
        return;
    }

    clearInputs();
}

makeAnswer();
document.getElementById("attempts").innerText = attempts;