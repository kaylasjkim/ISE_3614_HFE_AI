
import json
from datetime import datetime

# ============================================================
# AGENT 1: JOB SEARCH
# Human-AI Collaboration System - Interactive Prototype
# ============================================================

# OPTIONAL API CONFIGURATION
# Paste your institution-provided API key below if needed
# for a future API-connected version.
API_KEY = "PASTE_YOUR_INSTITUTION_API_KEY_HERE"

# This version uses simulated job listings and does not
# make external API calls.

# -----------------------------
# SYSTEM STATES
# -----------------------------

agent_state = "IDLE"
application_history = []

user_profile = {
    "skills": [],
    "preferred_roles": [],
    "preferred_location": "",
    "minimum_match": 50
}

# -----------------------------
# SIMULATED JOB FEED
# -----------------------------

jobs = [
    {
        "id": 1,
        "title": "Human Factors Engineering Intern",
        "company": "AeroTech",
        "platform": "Handshake",
        "location": "Remote",
        "skills": ["python", "usability", "research"],
        "description": "Support usability testing and human-centered design."
    },
    {
        "id": 2,
        "title": "UX Research Intern",
        "company": "DesignWorks",
        "platform": "LinkedIn",
        "location": "New York",
        "skills": ["research", "interviews", "usability"],
        "description": "Conduct user interviews and evaluate interfaces."
    },
    {
        "id": 3,
        "title": "Software Engineering Intern",
        "company": "CodeLabs",
        "platform": "Glassdoor",
        "location": "Remote",
        "skills": ["python", "javascript", "git"],
        "description": "Develop and test software applications."
    },
    {
        "id": 4,
        "title": "Human-AI Interaction Research Assistant",
        "company": "Research Institute",
        "platform": "GitHub",
        "location": "Virginia",
        "skills": ["python", "research", "human-ai"],
        "description": "Study collaboration between humans and AI."
    },
    {
        "id": 5,
        "title": "Ergonomics Analyst Intern",
        "company": "WorkSafe",
        "platform": "LinkedIn",
        "location": "Remote",
        "skills": ["ergonomics", "research", "data analysis"],
        "description": "Analyze workplace systems and human performance."
    }
]

# -----------------------------
# CHATBOT FEEDBACK
# -----------------------------

def bot(message):
    print("\nAGENT 1:", message)


def set_state(new_state):
    global agent_state
    agent_state = new_state
    print("[SYSTEM STATE:", agent_state + "]")


def get_input(prompt):
    return input("\nYOU: " + prompt + "\n> ").strip()


# -----------------------------
# USER PROFILE
# -----------------------------

def configure_profile():
    set_state("PROFILE_CONFIGURATION")

    bot("Let's configure your job-search preferences.")

    skills = get_input(
        "Enter your skills separated by commas:"
    )

    roles = get_input(
        "Enter your preferred job titles separated by commas:"
    )

    location = get_input(
        "Enter your preferred location (or Remote):"
    )

    user_profile["skills"] = [
        skill.strip().lower()
        for skill in skills.split(",")
        if skill.strip()
    ]

    user_profile["preferred_roles"] = [
        role.strip().lower()
        for role in roles.split(",")
        if role.strip()
    ]

    user_profile["preferred_location"] = location.lower()

    bot("Your preferences have been saved for this session.")

    set_state("READY")


# -----------------------------
# JOB MATCHING
# -----------------------------

def calculate_match(job):
    if not user_profile["skills"]:
        return 0

    matched = set(user_profile["skills"]).intersection(
        set(job["skills"])
    )

    score = len(matched) / len(job["skills"]) * 100

    return round(score)


def search_jobs():
    if not user_profile["skills"]:
        bot("Please configure your profile before searching.")
        return

    set_state("SEARCHING")
    bot("Searching simulated job feeds...")

    results = []

    for job in jobs:
        score = calculate_match(job)

        if score >= user_profile["minimum_match"]:
            results.append((job, score))

    results.sort(key=lambda result: result[1], reverse=True)

    set_state("RESULTS_AVAILABLE")

    if not results:
        bot("No jobs met your current match threshold.")
        bot("You can update your skills or lower the threshold.")
        return

    bot(f"Found {len(results)} potentially relevant jobs.")

    for job, score in results:
        print(
            f"\n[{job['id']}] {job['title']}"
            f"\nCompany: {job['company']}"
            f"\nPlatform: {job['platform']}"
            f"\nLocation: {job['location']}"
            f"\nSkill Match: {score}%"
        )

    review_job()


# -----------------------------
# JOB REVIEW
# -----------------------------

def review_job():
    while True:
        selection = get_input(
            "Enter a job ID to review, or B to return:"
        )

        if selection.lower() == "b":
            set_state("READY")
            return

        if not selection.isdigit():
            bot("Please enter a valid job ID.")
            continue

        job = next(
            (j for j in jobs if j["id"] == int(selection)),
            None
        )

        if job is None:
            bot("Job not found.")
            continue

        set_state("JOB_REVIEW")

        score = calculate_match(job)

        bot(
            f"Reviewing {job['title']} at {job['company']}."
        )

        print("\nJOB DESCRIPTION:", job["description"])
        print("REQUIRED SKILLS:", ", ".join(job["skills"]))
        print("YOUR MATCH SCORE:", str(score) + "%")

        matched = set(user_profile["skills"]).intersection(
            set(job["skills"])
        )

        missing = set(job["skills"]) - set(
            user_profile["skills"]
        )

        print("MATCHED SKILLS:", ", ".join(sorted(matched)) or "None")
        print("UNMATCHED SKILLS:", ", ".join(sorted(missing)) or "None")

        bot("Would you like to proceed with this opportunity?")

        print("\n1. Approve application")
        print("2. Reject recommendation")
        print("3. Return to results")

        decision = get_input("Choose an option:")

        if decision == "1":
            approve_application(job)
        elif decision == "2":
            bot("Recommendation rejected. No application submitted.")
            set_state("RESULTS_AVAILABLE")
        elif decision == "3":
            set_state("RESULTS_AVAILABLE")
        else:
            bot("Invalid selection. No action was taken.")


# -----------------------------
# HUMAN APPROVAL
# -----------------------------

def approve_application(job):
    set_state("AWAITING_HUMAN_CONFIRMATION")

    bot(
        "You are about to authorize a SIMULATED application "
        f"for {job['title']} at {job['company']}."
    )

    confirmation = get_input(
        "Type CONFIRM to simulate submission, or CANCEL:"
    )

    if confirmation.upper() != "CONFIRM":
        bot("Application canceled. No changes were made.")
        set_state("RESULTS_AVAILABLE")
        return

    submit_application(job)


# -----------------------------
# SIMULATED APPLICATION
# -----------------------------

def submit_application(job):
    set_state("SIMULATING_SUBMISSION")

    record = {
        "job_id": job["id"],
        "job_title": job["title"],
        "company": job["company"],
        "status": "SIMULATED_SUBMISSION",
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    application_history.append(record)

    set_state("APPLICATION_RECORDED")

    bot(
        "Simulation complete! Your application decision "
        "has been recorded."
    )

    bot(
        "No real application was sent to the employer."
    )


# -----------------------------
# APPLICATION HISTORY
# -----------------------------

def view_history():
    set_state("VIEWING_HISTORY")

    if not application_history:
        bot("No simulated applications have been recorded.")
    else:
        bot("Here is your application history:")

        for record in application_history:
            print(
                f"\n{record['job_title']} - {record['company']}"
                f"\nStatus: {record['status']}"
                f"\nTime: {record['timestamp']}"
            )

    set_state("READY")


# -----------------------------
# SETTINGS
# -----------------------------

def change_threshold():
    value = get_input(
        "Enter minimum skill-match percentage (0-100):"
    )

    try:
        threshold = int(value)

        if 0 <= threshold <= 100:
            user_profile["minimum_match"] = threshold
            bot(f"Match threshold updated to {threshold}%.")
        else:
            bot("Please enter a value between 0 and 100.")

    except ValueError:
        bot("Invalid input. Please enter a whole number.")


# -----------------------------
# MAIN CHATBOT INTERFACE
# -----------------------------

def main():
    bot(
        "Welcome to Agent 1: Job Search.\n"
        "I can help identify relevant jobs, explain skill "
        "matches, and simulate application decisions."
    )

    bot(
        "This is a prototype. All job listings and "
        "application submissions are simulated."
    )

    while True:
        print("\n" + "=" * 45)
        print("AGENT 1 - JOB SEARCH")
        print("Current State:", agent_state)
        print("=" * 45)

        print("1. Configure my profile")
        print("2. Search for jobs")
        print("3. View application history")
        print("4. Change match threshold")
        print("5. View my profile")
        print("6. Exit")

        choice = get_input("What would you like to do?")

        if choice == "1":
            configure_profile()

        elif choice == "2":
            search_jobs()

        elif choice == "3":
            view_history()

        elif choice == "4":
            change_threshold()

        elif choice == "5":
            bot("Your current profile:")
            print(
                json.dumps(user_profile, indent=4)
            )

        elif choice == "6":
            set_state("SESSION_ENDED")
            bot("Thank you for using Agent 1. Goodbye!")
            break

        else:
            bot(
                "I didn't recognize that selection. "
                "Please choose a number from 1 to 6."
            )


if __name__ == "__main__":
    main()
