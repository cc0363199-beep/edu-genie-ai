const task =
    document.getElementById("task");

const input =
    document.getElementById("input");

const levelWrap =
    document.getElementById("levelWrap");

const level =
    document.getElementById("level");

const run =
    document.getElementById("run");

const clear =
    document.getElementById("clear");

const copy =
    document.getElementById("copy");

const result =
    document.getElementById("result");

const loading =
    document.getElementById("loading");

const status =
    document.getElementById("status");



const placeholders = {

    qa:
        "Example: What is an operating system?",

    explain:
        "Example: Explain Python functions with a simple example.",

    quiz:
        "Example: Python basics",

    summarize:
        "Paste the learning material you want to summarize.",

    prerequisites:
        "Example: Python programming",

    learn:
        "Example: Web development"

};



/*
--------------------------------------------------
Task Change
--------------------------------------------------
*/

task.addEventListener(
    "change",
    () => {

        levelWrap.classList.toggle(
            "hidden",
            task.value !== "learn"
        );

        input.placeholder =
            placeholders[task.value] || "";

    }
);



/*
--------------------------------------------------
API Health Check
--------------------------------------------------
*/

async function checkHealth() {

    try {

        const response =
            await fetch("/health");

        const data =
            await response.json();

        if (data.status === "ok") {

            status.textContent =
                "API Online";

        } else {

            status.textContent =
                "API Problem";

        }

    } catch {

        status.textContent =
            "API Offline";

    }

}


checkHealth();



/*
--------------------------------------------------
Display Text
--------------------------------------------------
*/

function showText(text) {

    result.textContent =
        text || "No result returned.";

}



/*
--------------------------------------------------
Quiz Renderer
--------------------------------------------------
*/

function renderQuiz(data) {

    if (
        !data.questions ||
        !data.questions.length
    ) {

        showText(
            data.message ||
            "No quiz questions were returned."
        );

        return;

    }


    result.innerHTML = "";


    const title =
        document.createElement("h3");

    title.textContent =
        data.title || "Quiz";

    result.appendChild(title);


    const form =
        document.createElement("div");


    data.questions.forEach(
        (question, index) => {

            const box =
                document.createElement("div");

            box.className =
                "quiz-question";


            const heading =
                document.createElement("strong");

            heading.textContent =
                `${index + 1}. ${question.question}`;

            box.appendChild(heading);


            question.options.forEach(
                (option, optionIndex) => {

                    const label =
                        document.createElement("label");

                    label.className =
                        "quiz-option";


                    label.innerHTML =
                        `
                        <input
                            type="radio"
                            name="q${index}"
                            value="${optionIndex}"
                        >

                        ${escapeHtml(option)}
                        `;


                    box.appendChild(label);

                }
            );


            const feedback =
                document.createElement("div");

            feedback.className =
                "feedback";


            box.appendChild(feedback);


            form.appendChild(box);

        }
    );


    const submit =
        document.createElement("button");

    submit.className =
        "quiz-submit";

    submit.textContent =
        "Check Answers";


    submit.onclick = () => {

        let score = 0;


        data.questions.forEach(
            (question, index) => {

                const selected =
                    form.querySelector(
                        `input[name="q${index}"]:checked`
                    );


                const box =
                    form.children[index];


                const feedback =
                    box.querySelector(
                        ".feedback"
                    );


                box
                    .querySelectorAll(
                        ".quiz-option"
                    )
                    .forEach(
                        option => {

                            option.classList.remove(
                                "correct",
                                "wrong"
                            );

                        }
                    );


                if (
                    selected &&
                    Number(selected.value) ===
                    question.answer
                ) {

                    score++;


                    selected
                        .closest(
                            ".quiz-option"
                        )
                        .classList.add(
                            "correct"
                        );


                    feedback.textContent =
                        "Correct.";

                } else {

                    if (selected) {

                        selected
                            .closest(
                                ".quiz-option"
                            )
                            .classList.add(
                                "wrong"
                            );

                    }


                    feedback.textContent =
                        `Answer: ${
                            question.options[
                                question.answer
                            ]
                        }. ${
                            question.explanation || ""
                        }`;

                }

            }
        );


        submit.textContent =
            `Score: ${score}/${data.questions.length}`;

    };


    result.appendChild(form);

    result.appendChild(submit);

}



/*
--------------------------------------------------
HTML Escape
--------------------------------------------------
*/

function escapeHtml(value) {

    return String(value)
        .replace(
            /[&<>"']/g,
            character => ({

                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#039;"

            }[character])
        );

}



/*
--------------------------------------------------
Run
--------------------------------------------------
*/

run.addEventListener(
    "click",
    async () => {

        const value =
            input.value.trim();


        if (!value) {

            showText(
                "Please enter a topic, question, or content first."
            );

            return;

        }


        loading.classList.remove(
            "hidden"
        );

        run.disabled = true;


        try {

            let endpoint =
                `/${task.value}`;

            let body;


            if (task.value === "quiz") {

                body = {

                    topic: value,

                    count: 3

                };

            }

            else if (
                task.value === "learn"
            ) {

                endpoint =
                    "/learn/recommendations";


                body = {

                    topic: value,

                    level: level.value

                };

            }

            else {

                body = {

                    text: value

                };

            }


            const response =
                await fetch(
                    endpoint,
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(body)

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Request failed."
                );

            }


            if (
                task.value === "quiz"
            ) {

                renderQuiz(
                    data.result
                );

            } else {

                showText(
                    data.result
                );

            }

        }

        catch (error) {

            showText(
                `Error: ${error.message}`
            );

        }

        finally {

            loading.classList.add(
                "hidden"
            );

            run.disabled = false;

        }

    }
);



/*
--------------------------------------------------
Clear
--------------------------------------------------
*/

clear.addEventListener(
    "click",
    () => {

        input.value = "";

        showText(
            "Your response will appear here."
        );

    }
);



/*
--------------------------------------------------
Copy
--------------------------------------------------
*/

copy.addEventListener(
    "click",
    async () => {

        try {

            await navigator.clipboard.writeText(
                result.innerText
            );


            copy.textContent =
                "Copied";


            setTimeout(
                () => {

                    copy.textContent =
                        "Copy";

                },
                1200
            );

        }

        catch {

            copy.textContent =
                "Copy failed";

        }

    }
);