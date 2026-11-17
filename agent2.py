
from datetime import datetime
from pathlib import Path
import textwrap

# ==========================================================
# AGENT 2: RESUME AND COVER LETTER TAILOR
# Human-AI Collaboration - Interactive Prototype
# ==========================================================

# OPTIONAL FUTURE API CONFIGURATION
# Only use your institution-provided API key.
API_KEY = "PASTE_YOUR_INSTITUTION_API_KEY_HERE"

# No external API calls are made in this version.

state = "IDLE"
profile = {}
current_job = None
resume_draft = ""
letter_draft = ""
approved = False
revision_count = 0
history = []

# Simulated job postings
jobs = [
    {
        "id": 1,
        "title": "Human Factors Engineering Intern",
        "company": "AeroTech",
        "skills": ["python", "usability", "research"],
        "focus": "usability testing and human-centered design"
    },
    {
        "id": 2,
        "title": "UX Research Intern",
        "company": "DesignWorks",
        "skills": ["research", "interviews", "usability"],
        "focus": "user interviews and interface evaluation"
    },
    {
        "id": 3,
        "title": "Software Engineering Intern",
        "company": "CodeLabs",
        "skills": ["python", "javascript", "git"],
        "focus": "software development and testing"
    },
    {
        "id": 4,
        "title": "Human-AI Interaction Research Assistant",
        "company": "Research Institute",
        "skills": ["python", "research", "human-ai"],
        "focus": "human-AI collaboration research"
    }
]


def bot(message):
    print("\nAGENT 2:", message)


def set_state(new_state):
    global state
    state = new_state
    print("\n[SYSTEM STATE:", state + "]")


def ask(question):
    return input("\nYOU: " + question + "\n> ").strip()


def pause():
    input("\nPress Enter to continue...")


def configure_profile():
    global profile, approved
    set_state("PROFILE_CONFIGURATION")
    bot("Enter your actual qualifications. Do not include "
        "sensitive personal information.")

    name = ask("Your name:")
    education = ask("Education or degree:")
    skills = ask("Skills (comma-separated):")
    experience = ask("Relevant experience (one or more sentences):")
    achievements = ask("Achievements (one or more sentences):")

    if not name or not education or not skills:
        bot("Name, education, and skills are required.")
        return

    profile = {
        "name": name,
        "education": education,
        "skills": [
            s.strip() for s in skills.split(",") if s.strip()
        ],
        "experience": experience,
        "achievements": achievements
    }

    approved = False
    bot("Profile saved for this session.")
    set_state("READY")


def select_job():
    global current_job, approved
    set_state("JOB_SELECTION")

    print("\nSIMULATED JOB POSTINGS")
    for job in jobs:
        print(f"\n{job['id']}. {job['title']}")
        print("Company:", job["company"])
        print("Required skills:", ", ".join(job["skills"]))

    selection = ask("Select a job ID, or B to cancel:")

    if selection.upper() == "B":
        set_state("READY")
        return

    if not selection.isdigit():
        bot("Invalid job ID.")
        return

    selected = next(
        (j for j in jobs if j["id"] == int(selection)),
        None
    )

    if selected is None:
        bot("Job not found.")
        return

    current_job = selected
    approved = False
    bot(f"Selected {selected['title']} at "
        f"{selected['company']}.")
    set_state("JOB_SELECTED")


def analyze_match():
    if not profile or not current_job:
        bot("Configure a profile and select a job first.")
        return [], []

    set_state("ANALYZING_QUALIFICATIONS")

    user_skills = {
        s.lower() for s in profile["skills"]
    }
    required = current_job["skills"]

    matched = [
        s for s in required if s.lower() in user_skills
    ]
    unmatched = [
        s for s in required if s.lower() not in user_skills
    ]

    score = round(100 * len(matched) / len(required))

    bot(f"Skill overlap: {score}%")
    print("Matched:", ", ".join(matched) or "None")
    print("Not demonstrated:", ", ".join(unmatched) or "None")

    bot("This is a simple skill-overlap measure, "
        "not an assessment of hiring eligibility.")

    set_state("ANALYSIS_COMPLETE")
    return matched, unmatched


def generate_documents():
    global resume_draft, letter_draft, approved
    global revision_count

    if not profile or not current_job:
        bot("Please configure your profile and select a job.")
        return

    matched, unmatched = analyze_match()
    set_state("GENERATING_DRAFTS")

    name = profile["name"]
    title = current_job["title"]
    company = current_job["company"]

    # Preserve all user-provided skills, prioritizing
    # exact matches with the posting.
    ordered_skills = [
        s for s in profile["skills"]
        if s.lower() in current_job["skills"]
    ]
    ordered_skills += [
        s for s in profile["skills"]
        if s.lower() not in current_job["skills"]
    ]

    experience = profile["experience"] or "Not provided"
    achievements = profile["achievements"] or "Not provided"

    resume_draft = f"""RESUME - TAILORED DRAFT

{name}

TARGET POSITION
{title} | {company}

EDUCATION
{profile['education']}

RELEVANT SKILLS
{', '.join(ordered_skills)}

EXPERIENCE
{experience}

ACHIEVEMENTS
{achievements}
"""

    skill_sentence = (
        ", ".join(matched)
        if matched else "the skills described in my resume"
    )

    letter_draft = f"""COVER LETTER - TAILORED DRAFT

Dear Hiring Team at {company},

I am writing to express my interest in the
{title} position.

My educational background in
{profile['education']} and my experience
have motivated me to pursue this opportunity.

My relevant qualifications include {skill_sentence}.
I am particularly interested in your posting's
focus on {current_job['focus']}.

Relevant experience:
{experience}

Relevant achievements:
{achievements}

I would welcome the opportunity to discuss
how my background aligns with this position.

Sincerely,
{name}
"""

    approved = False
    revision_count = 0
    set_state("AWAITING_HUMAN_REVIEW")

    bot("Both drafts have been generated.")
    bot("All qualifications originate from your profile. "
        "Please verify the wording before approval.")

    if unmatched:
        bot("The following job requirements were not "
            "demonstrated by your listed skills:")
        print(", ".join(unmatched))


def display_documents():
    if not resume_draft:
        bot("No drafts are available. Generate them first.")
        return

    set_state("DOCUMENT_REVIEW")

    print("\n" + "=" * 55)
    print(resume_draft)
    print("=" * 55)
    print(letter_draft)
    print("=" * 55)

    set_state(
        "APPROVED" if approved else "AWAITING_HUMAN_REVIEW"
    )


def revise_documents():
    global resume_draft, letter_draft
    global approved, revision_count

    if not resume_draft:
        bot("Generate documents before requesting revisions.")
        return

    set_state("REVISION_REQUESTED")

    bot("Choose a revision action.")
    print("1. Add a verified accomplishment")
    print("2. Change the cover letter emphasis")
    print("3. Regenerate drafts from the profile")
    print("4. Cancel")

    choice = ask("Choose an option:")

    if choice == "1":
        accomplishment = ask(
            "Enter an accurate accomplishment:"
        )
        if not accomplishment:
            bot("No changes made.")
            return

        resume_draft += (
            "\nADDITIONAL ACCOMPLISHMENT\n"
            + accomplishment + "\n"
        )
        letter_draft = letter_draft.replace(
            "Sincerely,",
            "An additional accomplishment I would "
            "like to highlight is: "
            + accomplishment + "\n\nSincerely,"
        )

    elif choice == "2":
        emphasis = ask(
            "Enter a truthful area of interest to emphasize:"
        )
        if not emphasis:
            bot("No changes made.")
            return

        letter_draft = letter_draft.replace(
            "I would welcome the opportunity",
            "I am especially interested in "
            + emphasis + ".\n\n"
            "I would welcome the opportunity"
        )

    elif choice == "3":
        generate_documents()
        bot("Drafts regenerated.")
        return

    elif choice == "4":
        bot("Revision canceled.")
        return

    else:
        bot("Invalid selection.")
        return

    approved = False
    revision_count += 1
    set_state("AWAITING_HUMAN_REVIEW")
    bot("Revision complete. Please review the updated drafts.")


def approve_documents():
    global approved

    if not resume_draft:
        bot("No documents are available for approval.")
        return

    display_documents()
    set_state("AWAITING_CONFIRMATION")

    confirmation = ask(
        "Type APPROVE to approve both drafts, "
        "or CANCEL:"
    )

    if confirmation.upper() == "APPROVE":
        approved = True
        set_state("APPROVED")
        bot("Both documents approved for prototype use.")
        bot("No application has been submitted.")
    else:
        approved = False
        set_state("AWAITING_HUMAN_REVIEW")
        bot("Approval canceled. No documents exported.")


def export_documents():
    if not approved:
        bot("Human approval is required before exporting.")
        return

    set_state("EXPORTING")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = Path("agent2_exports")

    try:
        folder.mkdir(exist_ok=True)

        resume_file = folder / f"resume_{timestamp}.txt"
        letter_file = folder / f"cover_letter_{timestamp}.txt"

        resume_file.write_text(
            resume_draft, encoding="utf-8"
        )
        letter_file.write_text(
            letter_draft, encoding="utf-8"
        )

        history.append({
            "job": current_job["title"],
            "company": current_job["company"],
            "revisions": revision_count,
            "status": "EXPORTED",
            "time": timestamp
        })

        set_state("EXPORTED")
        bot("Documents saved successfully.")
        print("Resume:", resume_file)
        print("Cover letter:", letter_file)
        bot("No documents were sent to an employer.")

    except OSError as error:
        set_state("EXPORT_FAILED")
        bot(f"Unable to save files: {error}")
        bot("You can still review the drafts on screen.")


def view_history():
    set_state("VIEWING_HISTORY")

    if not history:
        bot("No documents have been exported.")
    else:
        for record in history:
            print("\nJob:", record["job"])
            print("Company:", record["company"])
            print("Revisions:", record["revisions"])
            print("Status:", record["status"])
            print("Time:", record["time"])

    set_state("READY")


def main():
    bot("Welcome to Agent 2: Resume and Cover Letter Tailor.")
    bot("I can tailor draft documents using your verified "
        "qualifications and simulated job postings.")
    bot("This is a rule-based prototype, not a live AI model.")

    while True:
        print("\n" + "=" * 48)
        print("AGENT 2 - RESUME & COVER LETTER TAILOR")
        print("Current State:", state)
        print("=" * 48)

        print("1. Configure applicant profile")
        print("2. Select a job posting")
        print("3. Analyze job qualifications")
        print("4. Generate tailored documents")
        print("5. Review documents")
        print("6. Request revisions")
        print("7. Approve documents")
        print("8. Export approved documents")
        print("9. View export history")
        print("10. Exit")

        choice = ask("What would you like to do?")

        if choice == "1":
            configure_profile()
        elif choice == "2":
            select_job()
        elif choice == "3":
            analyze_match()
        elif choice == "4":
            generate_documents()
        elif choice == "5":
            display_documents()
        elif choice == "6":
            revise_documents()
        elif choice == "7":
            approve_documents()
        elif choice == "8":
            export_documents()
        elif choice == "9":
            view_history()
        elif choice == "10":
            set_state("SESSION_ENDED")
            bot("Session ended. Goodbye!")
            break
        else:
            bot("Invalid selection. Choose a number from 1 to 10.")


if __name__ == "__main__":
    main()
