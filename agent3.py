
from datetime import datetime, timedelta

# ==========================================================
# AGENT 3: PERSONAL ASSISTANT
# Human-AI Collaboration - Interactive Prototype
# ==========================================================

# OPTIONAL FUTURE API CONFIGURATION
# Use only your institution-provided API key.
API_KEY = "PASTE_YOUR_INSTITUTION_API_KEY_HERE"

# No external API calls are made.

state = "IDLE"
connected_services = []
interviews = []
activity_history = []

# Simulated interview invitations
invitations = [
    {
        "id": 1,
        "company": "AeroTech",
        "role": "Human Factors Engineering Intern",
        "date": "2026-12-01",
        "time": "10:00",
        "duration": 60,
        "status": "PENDING"
    },
    {
        "id": 2,
        "company": "DesignWorks",
        "role": "UX Research Intern",
        "date": "2026-12-02",
        "time": "14:00",
        "duration": 45,
        "status": "PENDING"
    },
    {
        "id": 3,
        "company": "Research Institute",
        "role": "Human-AI Interaction Research Assistant",
        "date": "2026-12-01",
        "time": "10:30",
        "duration": 60,
        "status": "PENDING"
    }
]


def bot(message):
    print("\nAGENT 3:", message)


def set_state(new_state):
    global state
    state = new_state
    print("\n[SYSTEM STATE:", state + "]")


def ask(question):
    return input("\nYOU: " + question + "\n> ").strip()


def record(action, details):
    activity_history.append({
        "action": action,
        "details": details,
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })


def connect_services():
    set_state("SERVICE_CONFIGURATION")

    bot("Choose a service to simulate connecting.")

    services = [
        "Google Calendar",
        "Gmail",
        "Outlook Calendar",
        "Microsoft Outlook",
        "Apple Calendar",
        "iCloud Mail",
        "LinkedIn"
    ]

    for i, service in enumerate(services, 1):
        status = (
            "Connected (simulated)"
            if service in connected_services
            else "Not connected"
        )
        print(f"{i}. {service} - {status}")

    choice = ask("Enter service number or B to cancel:")

    if choice.upper() == "B":
        set_state("READY")
        return

    if not choice.isdigit():
        bot("Invalid selection.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(services):
        bot("Service not found.")
        return

    selected = services[index]

    if selected not in connected_services:
        connected_services.append(selected)
        bot(f"{selected} connected in simulation mode.")
        record("SIMULATED_CONNECTION", selected)
    else:
        bot(f"{selected} is already simulated as connected.")

    bot("No real account authentication occurred.")
    set_state("READY")


def view_invitations():
    set_state("REVIEWING_INVITATIONS")

    bot("Here are your simulated interview invitations.")

    for invitation in invitations:
        print("\nID:", invitation["id"])
        print("Company:", invitation["company"])
        print("Position:", invitation["role"])
        print("Date:", invitation["date"])
        print("Time:", invitation["time"])
        print("Duration:", invitation["duration"], "minutes")
        print("Status:", invitation["status"])

    set_state("READY")


def get_invitation():
    selection = ask("Enter invitation ID:")

    if not selection.isdigit():
        bot("Invalid ID.")
        return None

    invitation = next(
        (i for i in invitations
         if i["id"] == int(selection)),
        None
    )

    if invitation is None:
        bot("Invitation not found.")

    return invitation


def has_calendar_connection():
    calendar_services = [
        "Google Calendar",
        "Outlook Calendar",
        "Apple Calendar"
    ]

    return any(
        service in connected_services
        for service in calendar_services
    )


def check_conflict(invitation):
    proposed_start = datetime.strptime(
        invitation["date"] + " " + invitation["time"],
        "%Y-%m-%d %H:%M"
    )

    proposed_end = proposed_start + timedelta(
        minutes=invitation["duration"]
    )

    for interview in interviews:
        existing_start = datetime.strptime(
            interview["date"] + " " + interview["time"],
            "%Y-%m-%d %H:%M"
        )

        existing_end = existing_start + timedelta(
            minutes=interview["duration"]
        )

        if (
            proposed_start < existing_end
            and proposed_end > existing_start
        ):
            return interview

    return None


def schedule_interview():
    set_state("SCHEDULING_REQUESTED")

    if not has_calendar_connection():
        bot("Please simulate connecting a calendar first.")
        set_state("READY")
        return

    view_invitations()
    invitation = get_invitation()

    if invitation is None:
        set_state("READY")
        return

    if invitation["status"] == "SCHEDULED":
        bot("This interview is already scheduled.")
        set_state("READY")
        return

    set_state("CHECKING_AVAILABILITY")

    conflict = check_conflict(invitation)

    if conflict:
        set_state("CONFLICT_DETECTED")

        bot("Scheduling conflict detected!")
        print("Conflicts with:", conflict["company"])
        print("Date:", conflict["date"])
        print("Time:", conflict["time"])

        bot("Please resolve the conflict before scheduling.")
        return

    set_state("AWAITING_HUMAN_APPROVAL")

    bot("Proposed interview:")
    print("Company:", invitation["company"])
    print("Date:", invitation["date"])
    print("Time:", invitation["time"])

    confirmation = ask(
        "Type CONFIRM to simulate scheduling, "
        "or CANCEL:"
    )

    if confirmation.upper() != "CONFIRM":
        bot("Scheduling canceled.")
        set_state("READY")
        return

    interviews.append(invitation.copy())
    invitation["status"] = "SCHEDULED"

    record(
        "INTERVIEW_SCHEDULED",
        invitation["company"]
    )

    set_state("INTERVIEW_SCHEDULED")
    bot("Interview added to your simulated calendar.")
    bot("No real calendar event or invitation was created.")


def view_calendar():
    set_state("VIEWING_CALENDAR")

    if not interviews:
        bot("Your simulated calendar is empty.")
    else:
        for interview in sorted(
            interviews,
            key=lambda i: (i["date"], i["time"])
        ):
            print("\nCompany:", interview["company"])
            print("Role:", interview["role"])
            print("Date:", interview["date"])
            print("Time:", interview["time"])
            print("Duration:", interview["duration"], "minutes")

    set_state("READY")


def generate_followup():
    set_state("FOLLOWUP_PREPARATION")

    if not interviews:
        bot("Schedule an interview before creating a follow-up.")
        return

    view_calendar()

    company = ask("Enter the company name:")

    interview = next(
        (i for i in interviews
         if i["company"].lower() == company.lower()),
        None
    )

    if interview is None:
        bot("No scheduled interview found for that company.")
        return

    bot("Choose a follow-up action.")

    print("1. Thank-you email")
    print("2. Interview status inquiry")
    print("3. LinkedIn connection message")

    choice = ask("Choose an option:")

    if choice == "1":
        subject = "Thank You for the Interview"
        message = (
            f"Dear {company} Hiring Team,\n\n"
            f"Thank you for taking the time to discuss "
            f"the {interview['role']} position.\n\n"
            "I appreciated the opportunity to learn "
            "more about the role and your organization.\n\n"
            "I look forward to hearing about the next steps.\n\n"
            "Best regards,\n[Applicant Name]"
        )

    elif choice == "2":
        subject = "Interview Follow-Up"
        message = (
            f"Dear {company} Hiring Team,\n\n"
            f"I am following up regarding the "
            f"{interview['role']} position.\n\n"
            "I remain interested in the opportunity "
            "and would appreciate any updates "
            "regarding the hiring process.\n\n"
            "Best regards,\n[Applicant Name]"
        )

    elif choice == "3":
        subject = "LinkedIn Connection Request"
        message = (
            f"Hello,\n\n"
            f"Thank you for discussing the "
            f"{interview['role']} opportunity at "
            f"{company}.\n\n"
            "I enjoyed our conversation and "
            "would be glad to stay connected."
        )

    else:
        bot("Invalid selection.")
        return

    set_state("MESSAGE_REVIEW")

    print("\n" + "=" * 50)
    print("SUBJECT:", subject)
    print(message)
    print("=" * 50)

    confirmation = ask(
        "Type APPROVE to record simulated sending, "
        "or CANCEL:"
    )

    if confirmation.upper() == "APPROVE":
        set_state("SIMULATING_MESSAGE_SEND")

        record(
            "SIMULATED_FOLLOWUP",
            f"{company}: {subject}"
        )

        set_state("FOLLOWUP_RECORDED")

        bot("Follow-up action recorded successfully.")
        bot("No real email or LinkedIn message was sent.")

    else:
        bot("Follow-up canceled.")
        set_state("READY")


def view_history():
    set_state("VIEWING_HISTORY")

    if not activity_history:
        bot("No activity recorded.")
    else:
        for activity in activity_history:
            print("\nAction:", activity["action"])
            print("Details:", activity["details"])
            print("Time:", activity["timestamp"])

    set_state("READY")


def main():
    bot("Welcome to Agent 3: Personal Assistant.")
    bot("I can help coordinate interviews, identify "
        "calendar conflicts, and prepare follow-up messages.")
    bot("All integrations and external actions are simulated.")

    while True:
        print("\n" + "=" * 48)
        print("AGENT 3 - PERSONAL ASSISTANT")
        print("Current State:", state)
        print("=" * 48)

        print("1. Connect a service (simulation)")
        print("2. View interview invitations")
        print("3. Schedule an interview")
        print("4. View calendar")
        print("5. Prepare post-interview follow-up")
        print("6. View activity history")
        print("7. Exit")

        choice = ask("What would you like to do?")

        if choice == "1":
            connect_services()
        elif choice == "2":
            view_invitations()
        elif choice == "3":
            schedule_interview()
        elif choice == "4":
            view_calendar()
        elif choice == "5":
            generate_followup()
        elif choice == "6":
            view_history()
        elif choice == "7":
            set_state("SESSION_ENDED")
            bot("Goodbye!")
            break
        else:
            bot("Invalid selection. Choose 1 through 7.")


if __name__ == "__main__":
    main()
