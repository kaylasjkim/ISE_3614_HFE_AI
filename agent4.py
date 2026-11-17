
from datetime import datetime

# ==========================================================
# AGENT 4: INTERVIEW COACH
# Human-AI Collaboration - Interactive Prototype
# ==========================================================

# OPTIONAL FUTURE API CONFIGURATION
# Use only your institution-provided API key.
API_KEY = "PASTE_YOUR_INSTITUTION_API_KEY_HERE"

# No external API calls are made.

state = "IDLE"
selected_job = None
practice_history = []
current_questions = []

# Simulated job postings and interview intelligence
jobs = [
    {
        "id": 1,
        "title": "Human Factors Engineering Intern",
        "company": "AeroTech",
        "skills": ["usability", "research", "python"],
        "questions": [
            {
                "question": "How would you evaluate the "
                            "usability of a new interface?",
                "keywords": [
                    "users", "testing", "tasks", "feedback"
                ],
                "type": "Technical"
            },
            {
                "question": "Describe a time you improved "
                            "a design based on user feedback.",
                "keywords": [
                    "situation", "action", "result", "feedback"
                ],
                "type": "Behavioral"
            }
        ]
    },
    {
        "id": 2,
        "title": "UX Research Intern",
        "company": "DesignWorks",
        "skills": ["research", "interviews", "usability"],
        "questions": [
            {
                "question": "How would you conduct "
                            "a user interview?",
                "keywords": [
                    "questions", "participants",
                    "listening", "analysis"
                ],
                "type": "Technical"
            },
            {
                "question": "Describe a challenging "
                            "research project.",
                "keywords": [
                    "situation", "task", "action", "result"
                ],
                "type": "Behavioral"
            }
        ]
    },
    {
        "id": 3,
        "title": "Software Engineering Intern",
        "company": "CodeLabs",
        "skills": ["python", "javascript", "git"],
        "questions": [
            {
                "question": "How do you approach "
                            "debugging a software problem?",
                "keywords": [
                    "reproduce", "test", "debug", "solution"
                ],
                "type": "Technical"
            },
            {
                "question": "Describe a time you "
                            "collaborated on a coding project.",
                "keywords": [
                    "team", "communication",
                    "action", "result"
                ],
                "type": "Behavioral"
            }
        ]
    },
    {
        "id": 4,
        "title": "Human-AI Interaction Research Assistant",
        "company": "Research Institute",
        "skills": ["python", "research", "human-ai"],
        "questions": [
            {
                "question": "How would you evaluate "
                            "trust in a human-AI system?",
                "keywords": [
                    "trust", "users", "evaluation", "feedback"
                ],
                "type": "Technical"
            },
            {
                "question": "Describe a time you worked "
                            "with an unfamiliar technology.",
                "keywords": [
                    "situation", "action",
                    "learning", "result"
                ],
                "type": "Behavioral"
            }
        ]
    }
]

# Simulated information sources
sources = [
    "LinkedIn",
    "Handshake",
    "Glassdoor",
    "Reddit",
    "GitHub",
    "Company FAQ / Website",
    "Professional Communities"
]


def bot(message):
    print("\nAGENT 4:", message)


def set_state(new_state):
    global state
    state = new_state
    print("\n[SYSTEM STATE:", state + "]")


def ask(question):
    return input("\nYOU: " + question + "\n> ").strip()


def select_job():
    global selected_job, current_questions

    set_state("JOB_SELECTION")

    bot("Select a simulated job posting.")

    for job in jobs:
        print(f"\n{job['id']}. {job['title']}")
        print("Company:", job["company"])
        print("Skills:", ", ".join(job["skills"]))

    selection = ask("Enter job ID or B to cancel:")

    if selection.upper() == "B":
        set_state("READY")
        return

    if not selection.isdigit():
        bot("Invalid job ID.")
        return

    job = next(
        (j for j in jobs if j["id"] == int(selection)),
        None
    )

    if job is None:
        bot("Job not found.")
        return

    selected_job = job
    current_questions = []

    set_state("JOB_SELECTED")

    bot(f"Preparing for {job['title']} "
        f"at {job['company']}.")


def research_sources():
    if not selected_job:
        bot("Please select a job first.")
        return

    set_state("RESEARCHING_SOURCES")

    bot("Simulating research across the following sources:")

    for source in sources:
        print("-", source)

    bot("No live searches are performed.")
    bot("Interview questions are drawn from "
        "predefined example data.")

    set_state("RESEARCH_COMPLETE")


def generate_questions():
    global current_questions

    if not selected_job:
        bot("Select a job before generating questions.")
        return

    set_state("GENERATING_QUESTIONS")

    current_questions = selected_job["questions"].copy()

    bot(
        f"Generated {len(current_questions)} representative "
        "interview questions."
    )

    for i, question in enumerate(current_questions, 1):
        print(f"\n{i}. [{question['type']}]")
        print(question["question"])

    set_state("QUESTIONS_READY")


def view_guidance(question):
    bot("Suggested elements of a strong response:")

    for keyword in question["keywords"]:
        print("-", keyword.capitalize())

    if question["type"] == "Behavioral":
        bot("Consider using the STAR structure:")
        print("S - Situation")
        print("T - Task")
        print("A - Action")
        print("R - Result")

    bot("These are general coaching cues, "
        "not verified employer answer requirements.")


def evaluate_response(answer, question):
    set_state("EVALUATING_RESPONSE")

    if not answer.strip():
        bot("No response provided.")
        return None

    keywords = question["keywords"]

    matched = [
        keyword for keyword in keywords
        if keyword.lower() in answer.lower()
    ]

    score = round(
        100 * len(matched) / len(keywords)
    )

    print("\n" + "=" * 45)
    print("COACHING FEEDBACK")
    print("=" * 45)

    print("Keyword coverage:", str(score) + "%")
    print("Recognized concepts:", ", ".join(matched) or "None")

    missing = [
        keyword for keyword in keywords
        if keyword not in matched
    ]

    print("Concepts to consider:", ", ".join(missing) or "None")

    if score >= 75:
        bot("Your response includes many of the "
            "expected coaching concepts.")
    elif score >= 40:
        bot("Your response covers some relevant concepts. "
            "Consider adding specific examples.")
    else:
        bot("Your response may benefit from additional "
            "detail and clearer structure.")

    bot("This is a keyword-based coaching estimate, "
        "not a validated assessment of interview quality.")

    return score


def practice_interview():
    if not current_questions:
        bot("Generate questions before practicing.")
        return

    set_state("PRACTICE_SESSION")

    bot("Interview practice is beginning.")
    bot("Answer each question in your own words.")

    scores = []

    for index, question in enumerate(current_questions, 1):
        print("\n" + "=" * 48)
        print(f"QUESTION {index} OF {len(current_questions)}")
        print("Type:", question["type"])
        print(question["question"])

        answer = ask("Your answer:")

        score = evaluate_response(answer, question)

        if score is not None:
            scores.append(score)

            practice_history.append({
                "company": selected_job["company"],
                "role": selected_job["title"],
                "question": question["question"],
                "answer": answer,
                "score": score,
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            })

        guidance = ask(
            "Would you like coaching guidance? (yes/no):"
        )

        if guidance.lower() in ["yes", "y"]:
            view_guidance(question)

    set_state("SESSION_COMPLETE")

    if scores:
        average = round(sum(scores) / len(scores))
        bot(f"Practice session complete. "
            f"Average keyword coverage: {average}%")
    else:
        bot("Practice session completed without scored answers.")

    bot("You may repeat the session to practice again.")


def review_questions():
    if not current_questions:
        bot("No questions have been generated.")
        return

    set_state("REVIEWING_QUESTIONS")

    for i, question in enumerate(current_questions, 1):
        print(f"\n{i}. {question['question']}")
        print("Type:", question["type"])

    selection = ask(
        "Enter question number for coaching guidance, "
        "or B to return:"
    )

    if selection.upper() == "B":
        set_state("READY")
        return

    if not selection.isdigit():
        bot("Invalid selection.")
        return

    index = int(selection) - 1

    if 0 <= index < len(current_questions):
        view_guidance(current_questions[index])
    else:
        bot("Question not found.")

    set_state("READY")


def view_history():
    set_state("VIEWING_HISTORY")

    if not practice_history:
        bot("No practice sessions recorded.")
        return

    for i, record in enumerate(practice_history, 1):
        print("\n" + "-" * 45)
        print("Practice Record:", i)
        print("Company:", record["company"])
        print("Role:", record["role"])
        print("Question:", record["question"])
        print("Your Answer:", record["answer"])
        print("Keyword Coverage:", str(record["score"]) + "%")
        print("Date:", record["timestamp"])

    set_state("READY")


def main():
    bot("Welcome to Agent 4: Interview Coach.")
    bot("I can help you prepare for interviews, "
        "practice responses, and review coaching feedback.")
    bot("All research sources and interview intelligence "
        "are simulated.")

    while True:
        print("\n" + "=" * 48)
        print("AGENT 4 - INTERVIEW COACH")
        print("Current State:", state)
        print("=" * 48)

        print("1. Select a job posting")
        print("2. Research interview sources (simulation)")
        print("3. Generate interview questions")
        print("4. Review questions and coaching guidance")
        print("5. Start interview practice")
        print("6. View practice history")
        print("7. Exit")

        choice = ask("What would you like to do?")

        if choice == "1":
            select_job()
        elif choice == "2":
            research_sources()
        elif choice == "3":
            generate_questions()
        elif choice == "4":
            review_questions()
        elif choice == "5":
            practice_interview()
        elif choice == "6":
            view_history()
        elif choice == "7":
            set_state("SESSION_ENDED")
            bot("Goodbye, and good luck with your interview!")
            break
        else:
            bot("Invalid selection. Choose 1 through 7.")


if __name__ == "__main__":
    main()
