
// ======================================================
// JOB APPLICANT - HUMAN-AI COLLABORATION SYSTEM
// Interactive frontend prototype
// ======================================================

// No API key or external service is required.
// All agent actions below are simulations.

const $ = (id) => document.getElementById(id);

const jobs = [
  {
    title: "Human Factors Engineering Intern",
    company: "AeroTech",
    skills: ["python", "usability", "research"],
    focus: "usability testing and human-centered design",
    questions: [
      {
        text: "How would you evaluate interface usability?",
        keywords: ["users", "testing", "tasks", "feedback"]
      },
      {
        text: "Describe a time you improved a design.",
        keywords: ["situation", "action", "result", "feedback"]
      }
    ]
  },
  {
    title: "UX Research Intern",
    company: "DesignWorks",
    skills: ["research", "interviews", "usability"],
    focus: "user interviews and interface evaluation",
    questions: [
      {
        text: "How would you conduct a user interview?",
        keywords: ["questions", "participants", "listening"]
      },
      {
        text: "Describe a challenging research project.",
        keywords: ["situation", "action", "result"]
      }
    ]
  },
  {
    title: "Software Engineering Intern",
    company: "CodeLabs",
    skills: ["python", "javascript", "git"],
    focus: "software development and testing",
    questions: [
      {
        text: "How do you debug a software problem?",
        keywords: ["reproduce", "test", "debug", "solution"]
      },
      {
        text: "Describe a collaborative coding project.",
        keywords: ["team", "communication", "result"]
      }
    ]
  },
  {
    title: "Human-AI Interaction Research Assistant",
    company: "Research Institute",
    skills: ["python", "research", "human-ai"],
    focus: "human-AI collaboration research",
    questions: [
      {
        text: "How would you evaluate trust in an AI system?",
        keywords: ["trust", "users", "evaluation", "feedback"]
      },
      {
        text: "Describe learning an unfamiliar technology.",
        keywords: ["situation", "action", "learning", "result"]
      }
    ]
  }
];

const invitations = [
  {
    id: 1, job: 0, date: "2026-12-01",
    time: "10:00", duration: 60
  },
  {
    id: 2, job: 1, date: "2026-12-02",
    time: "14:00", duration: 45
  },
  {
    id: 3, job: 3, date: "2026-12-01",
    time: "10:30", duration: 60
  }
];

const app = {
  applications: [],
  calendarConnected: false,
  scheduled: [],
  documentsApproved: false,
  resume: "",
  letter: "",
  followup: "",
  questionIndex: 0,
  practiceJob: null,
  practiceScores: [],
  feedback: []
};

// ------------------------------------------------------
// SHARED UTILITIES
// ------------------------------------------------------

function status(id, message) {
  $(id).textContent = message;
}

function createElement(tag, text, className = "") {
  const element = document.createElement(tag);
  element.textContent = text;
  if (className) element.className = className;
  return element;
}

function addButton(parent, label, action, primary = false) {
  const button = createElement("button", label);
  button.type = "button";
  if (primary) button.className = "primary-button";
  button.addEventListener("click", action);
  parent.appendChild(button);
  return button;
}

function validEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
}

function validateEmail(inputId, errorId) {
  const input = $(inputId);
  const valid = validEmail(input.value);

  input.setAttribute("aria-invalid", String(!valid));
  $(errorId).textContent = valid
    ? ""
    : "Enter a valid email address, such as name@example.com.";

  return valid;
}

function validateRequired(ids) {
  let firstInvalid = null;

  ids.forEach((id) => {
    const field = $(id);
    const invalid = !field.value.trim();

    field.setAttribute("aria-invalid", String(invalid));

    if (invalid && !firstInvalid) firstInvalid = field;
  });

  if (firstInvalid) firstInvalid.focus();
  return !firstInvalid;
}

function confirmAction(message, callback) {
  $("dialog-message").textContent = message;

  const dialog = $("confirm-dialog");
  dialog.showModal();

  $("dialog-confirm").onclick = () => {
    dialog.close();
    callback();
  };

  $("dialog-cancel").onclick = () => dialog.close();
}

// ------------------------------------------------------
// NAVIGATION
// ------------------------------------------------------

function showTab(tabId) {
  document.querySelectorAll(".tab").forEach((tab) => {
    const active = tab.id === tabId;
    tab.hidden = !active;
    tab.classList.toggle("active", active);
  });

  document.querySelectorAll(".nav-button").forEach((button) => {
    const active = button.dataset.tab === tabId;
    button.classList.toggle("active", active);

    if (active) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });

  const heading = $(tabId).querySelector("h2");
  if (heading) {
    heading.setAttribute("tabindex", "-1");
    heading.focus({ preventScroll: true });
  }
}

document.querySelectorAll(".nav-button").forEach((button) => {
  button.addEventListener("click", () => {
    showTab(button.dataset.tab);
  });
});

document.querySelectorAll(".open-agent").forEach((button) => {
  button.addEventListener("click", () => {
    showTab(button.dataset.target);
  });
});

// ------------------------------------------------------
// DARK / LIGHT MODE
// ------------------------------------------------------

const themeButton = $("theme-toggle");

function updateTheme(dark) {
  document.body.classList.toggle("dark-mode", dark);
  themeButton.textContent = dark ? "Light Mode" : "Dark Mode";
  themeButton.setAttribute(
    "aria-label",
    dark ? "Switch to light mode" : "Switch to dark mode"
  );
}

try {
  updateTheme(localStorage.getItem("theme") === "dark");
} catch {
  updateTheme(false);
}

themeButton.addEventListener("click", () => {
  const dark = !document.body.classList.contains("dark-mode");
  updateTheme(dark);

  try {
    localStorage.setItem("theme", dark ? "dark" : "light");
  } catch {
    // Continue without persistent storage.
  }
});

// ------------------------------------------------------
// AGENT 1: JOB SEARCH
// ------------------------------------------------------

function renderApplicationHistory() {
  const container = $("application-history");
  container.replaceChildren();

  if (!app.applications.length) {
    container.textContent = "No simulated applications yet.";
    return;
  }

  app.applications.forEach((record) => {
    container.appendChild(createElement(
      "p",
      `${record.title} at ${record.company} — Simulated submission`
    ));
  });
}

$("job-form").addEventListener("submit", (event) => {
  event.preventDefault();

  const skillsValid = validateRequired(["skills"]);
  const emailValid = validateEmail("job-email", "job-email-error");

  if (!skillsValid || !emailValid) {
    status("job-status", "Error: Correct the highlighted fields.");
    return;
  }

  status("job-status", "SEARCHING: Evaluating simulated job listings.");

  const userSkills = $("skills").value.toLowerCase()
    .split(",").map((skill) => skill.trim()).filter(Boolean);

  const threshold = Number($("threshold").value);
  const results = $("job-results");
  results.replaceChildren();

  let count = 0;

  jobs.forEach((job, index) => {
    const matched = job.skills.filter(
      (skill) => userSkills.includes(skill)
    );

    const score = Math.round(
      matched.length / job.skills.length * 100
    );

    if (score < threshold) return;
    count++;

    const card = createElement("article", "", "card");

    card.appendChild(createElement("h3", job.title));
    card.appendChild(createElement("p", job.company));
    card.appendChild(createElement(
      "p", `Skill match: ${score}%`
    ));
    card.appendChild(createElement(
      "p", `Matched: ${matched.join(", ") || "None"}`
    ));
    card.appendChild(createElement(
      "p",
      `Not demonstrated: ${
        job.skills.filter(s => !matched.includes(s)).join(", ")
        || "None"
      }`
    ));

    addButton(card, "Review and Apply", () => {
      status("job-status", "AWAITING_HUMAN_APPROVAL");

      confirmAction(
        `Simulate an application to ${job.company} for ` +
        `${job.title}? No real application will be sent.`,
        () => {
          if (app.applications.some(a => a.index === index)) {
            status("job-status", "Application already recorded.");
            return;
          }

          app.applications.push({
            index, title: job.title, company: job.company
          });

          status(
            "job-status",
            "APPLICATION_RECORDED: Simulated submission complete."
          );

          renderApplicationHistory();
        }
      );
    }, true);

    results.appendChild(card);
  });

  status(
    "job-status",
    count
      ? `RESULTS_AVAILABLE: ${count} matching jobs found.`
      : "NO_RESULTS: Lower the threshold or update your skills."
  );
});

$("job-email").addEventListener("input", () => {
  if ($("job-email").value) {
    validateEmail("job-email", "job-email-error");
  }
});

renderApplicationHistory();

// ------------------------------------------------------
// AGENT 2: RESUME AND COVER LETTER TAILOR
// ------------------------------------------------------

$("resume-form").addEventListener("submit", (event) => {
  event.preventDefault();

  if (!validateRequired([
    "applicant-name", "education", "resume-skills", "experience"
  ])) {
    status("resume-status", "Error: Complete required fields.");
    return;
  }

  status("resume-status", "GENERATING_DRAFTS");

  const job = jobs[Number($("target-job").value)];
  const name = $("applicant-name").value.trim();
  const education = $("education").value.trim();
  const skills = $("resume-skills").value.trim();
  const experience = $("experience").value.trim();
  const achievements = $("achievements").value.trim();

  const skillList = skills.split(",").map(s => s.trim());
  const matched = job.skills.filter(s =>
    skillList.some(u => u.toLowerCase() === s)
  );

  app.resume =
`RESUME - TAILORED DRAFT

${name}

TARGET POSITION
${job.title} | ${job.company}

EDUCATION
${education}

SKILLS
${skills}

EXPERIENCE
${experience}

ACHIEVEMENTS
${achievements || "Not provided"}

MATCHED JOB SKILLS
${matched.join(", ") || "None identified"}`;

  app.letter =
`Dear ${job.company} Hiring Team,

I am interested in the ${job.title} position.

My educational background is ${education}.

My relevant experience includes:
${experience}

My listed skills include ${skills}.

I am interested in the role's focus on ${job.focus}.

Thank you for considering my application.

Sincerely,
${name}`;

  $("resume-text").textContent = app.resume;
  $("letter-text").textContent = app.letter;

  $("resume-output").hidden = false;
  $("download-documents").disabled = true;
  app.documentsApproved = false;

  status(
    "resume-status",
    "AWAITING_HUMAN_REVIEW: Verify all content before approval."
  );
});

$("approve-documents").addEventListener("click", () => {
  confirmAction(
    "Have you reviewed both documents and verified that " +
    "all information is accurate?",
    () => {
      app.documentsApproved = true;
      $("download-documents").disabled = false;
      status("resume-status", "APPROVED: Documents ready for export.");
    }
  );
});

function downloadText(filename, content) {
  const blob = new Blob([content], {
    type: "text/plain;charset=utf-8"
  });

  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();

  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

$("download-documents").addEventListener("click", () => {
  if (!app.documentsApproved) return;

  downloadText("tailored_resume.txt", app.resume);
  downloadText("tailored_cover_letter.txt", app.letter);

  status("resume-status", "EXPORTED: Download initiated.");
});

// ------------------------------------------------------
// AGENT 3: PERSONAL ASSISTANT
// ------------------------------------------------------

$("connect-calendar").addEventListener("click", () => {
  app.calendarConnected = true;

  status(
    "calendar-status",
    "CONNECTED_SIMULATION: " +
    $("calendar-service").value +
    ". No real account was accessed."
  );
});

function minutes(date, time) {
  return new Date(`${date}T${time}:00`).getTime();
}

function hasConflict(invitation) {
  const start = minutes(invitation.date, invitation.time);
  const end = start + invitation.duration * 60000;

  return app.scheduled.some((existing) => {
    const otherStart = minutes(existing.date, existing.time);
    const otherEnd = otherStart + existing.duration * 60000;

    return start < otherEnd && end > otherStart;
  });
}

function renderInvitations() {
  const container = $("invitation-list");
  container.replaceChildren();

  invitations.forEach((invitation) => {
    const job = jobs[invitation.job];
    const card = createElement("article", "", "card");

    card.appendChild(createElement("h3", job.company));
    card.appendChild(createElement("p", job.title));
    card.appendChild(createElement(
      "p", `${invitation.date} at ${invitation.time}`
    ));

    const alreadyScheduled = app.scheduled.some(
      i => i.id === invitation.id
    );

    const button = addButton(
      card,
      alreadyScheduled ? "Scheduled" : "Schedule Interview",
      () => {
        if (!app.calendarConnected) {
          status(
            "calendar-status",
            "ACTION_REQUIRED: Connect a simulated calendar first."
          );
          return;
        }

        if (hasConflict(invitation)) {
          status(
            "calendar-status",
            "CONFLICT_DETECTED: This interview overlaps " +
            "with an existing simulated appointment."
          );
          return;
        }

        status("calendar-status", "AWAITING_HUMAN_APPROVAL");

        confirmAction(
          `Schedule ${job.company} on ${invitation.date} ` +
          `at ${invitation.time}?`,
          () => {
            app.scheduled.push(invitation);
            renderInvitations();
            renderScheduled();

            status(
              "calendar-status",
              "INTERVIEW_SCHEDULED: Simulated calendar updated."
            );
          }
        );
      },
      true
    );

    button.disabled = alreadyScheduled;
    container.appendChild(card);
  });
}

function renderScheduled() {
  const container = $("scheduled-list");
  const select = $("followup-company");

  container.replaceChildren();
  select.replaceChildren();

  if (!app.scheduled.length) {
    container.textContent = "No interviews scheduled.";
    select.appendChild(
      new Option("No scheduled interviews", "")
    );
    return;
  }

  app.scheduled.forEach((invitation) => {
    const job = jobs[invitation.job];

    container.appendChild(createElement(
      "p",
      `${job.company} — ${invitation.date}, ${invitation.time}`
    ));

    select.appendChild(
      new Option(`${job.company}: ${job.title}`, invitation.id)
    );
  });
}

$("generate-followup").addEventListener("click", () => {
  const invitation = app.scheduled.find(
    i => i.id === Number($("followup-company").value)
  );

  if (!invitation) {
    status("calendar-status", "Schedule an interview first.");
    return;
  }

  const job = jobs[invitation.job];
  const type = $("followup-type").value;

  if (type === "thanks") {
    app.followup =
`Dear ${job.company} Hiring Team,

Thank you for discussing the ${job.title} position.
I appreciated learning more about the opportunity.

Best regards,
[Applicant Name]`;
  } else if (type === "status") {
    app.followup =
`Dear ${job.company} Hiring Team,

I am following up regarding the ${job.title} position.
I remain interested and would appreciate any updates.

Best regards,
[Applicant Name]`;
  } else {
    app.followup =
`Hello,

Thank you for discussing the ${job.title} opportunity
at ${job.company}. I would be glad to stay connected.`;
  }

  $("followup-text").textContent = app.followup;
  $("followup-preview").hidden = false;

  status("calendar-status", "MESSAGE_REVIEW: Approval required.");
});

$("approve-followup").addEventListener("click", () => {
  if (!app.followup) return;

  confirmAction(
    "Approve this simulated message? " +
    "No real email or connection request will be sent.",
    () => {
      status(
        "calendar-status",
        "FOLLOWUP_RECORDED: Simulated message approved."
      );
      $("followup-preview").hidden = true;
      app.followup = "";
    }
  );
});

renderInvitations();
renderScheduled();

// ------------------------------------------------------
// AGENT 4: INTERVIEW COACH
// ------------------------------------------------------

function showQuestion() {
  const questions = app.practiceJob.questions;
  const question = questions[app.questionIndex];

  $("question-progress").textContent =
    `Question ${app.questionIndex + 1} of ${questions.length}`;

  $("interview-question").textContent = question.text;
  $("interview-answer").value = "";
  $("interview-answer").removeAttribute("aria-invalid");
  $("answer-error").textContent = "";
  $("coaching-feedback").replaceChildren();

  $("submit-answer").disabled = false;
  $("next-question").hidden = true;
}

$("start-practice").addEventListener("click", () => {
  app.practiceJob = jobs[Number($("coach-job").value)];
  app.questionIndex = 0;
  app.practiceScores = [];

  $("practice-area").hidden = false;
  showQuestion();

  status("coach-status", "PRACTICE_SESSION: In progress.");
});

$("submit-answer").addEventListener("click", () => {
  const answer = $("interview-answer").value.trim();

  if (!answer) {
    $("interview-answer").setAttribute("aria-invalid", "true");
    $("answer-error").textContent =
      "Enter a response before requesting feedback.";
    return;
  }

  const question = app.practiceJob.questions[app.questionIndex];
  const lowerAnswer = answer.toLowerCase();

  const matched = question.keywords.filter(
    keyword => lowerAnswer.includes(keyword)
  );

  const score = Math.round(
    matched.length / question.keywords.length * 100
  );

  app.practiceScores.push(score);

  const missing = question.keywords.filter(
    keyword => !matched.includes(keyword)
  );

  const feedback = $("coaching-feedback");
  feedback.replaceChildren();

  feedback.appendChild(createElement(
    "h4", "Coaching Feedback"
  ));
  feedback.appendChild(createElement(
    "p", `Keyword coverage: ${score}%`
  ));
  feedback.appendChild(createElement(
    "p", `Recognized concepts: ${matched.join(", ") || "None"}`
  ));
  feedback.appendChild(createElement(
    "p", `Consider discussing: ${missing.join(", ") || "None"}`
  ));
  feedback.appendChild(createElement(
    "p",
    "This is a keyword-based estimate, not a validated " +
    "measure of interview quality."
  ));

  $("submit-answer").disabled = true;
  $("next-question").hidden = false;

  const last = app.questionIndex ===
    app.practiceJob.questions.length - 1;

  $("next-question").textContent =
    last ? "Finish Practice" : "Next Question";

  status("coach-status", "FEEDBACK_AVAILABLE");
});

$("next-question").addEventListener("click", () => {
  app.questionIndex++;

  if (app.questionIndex < app.practiceJob.questions.length) {
    showQuestion();
    status("coach-status", "PRACTICE_SESSION: In progress.");
    return;
  }

  const average = Math.round(
    app.practiceScores.reduce((a, b) => a + b, 0) /
    app.practiceScores.length
  );

  $("practice-area").hidden = true;

  status(
    "coach-status",
    `SESSION_COMPLETE: Average keyword coverage ${average}%.`
  );
});

// ------------------------------------------------------
// CUSTOMER SERVICE / FEEDBACK
// ------------------------------------------------------

$("feedback-form").addEventListener("submit", (event) => {
  event.preventDefault();

  const requiredValid = validateRequired([
    "feedback-name", "feedback-message"
  ]);

  const emailValid = validateEmail(
    "feedback-email", "feedback-email-error"
  );

  const message = $("feedback-message").value.trim();

  if (!requiredValid || !emailValid || message.length < 10) {
    if (message.length < 10) {
      $("feedback-message").setAttribute("aria-invalid", "true");
    }

    status(
      "feedback-status",
      "Error: Complete all fields and enter at least " +
      "10 characters in your message."
    );
    return;
  }

  confirmAction(
    "Record this feedback locally in the current session? " +
    "It will not be sent to a customer service team.",
    () => {
      app.feedback.push({
        name: $("feedback-name").value.trim(),
        email: $("feedback-email").value.trim(),
        category: $("feedback-category").value,
        message
      });

      $("feedback-form").reset();

      ["feedback-name", "feedback-email", "feedback-message"]
        .forEach(id => $(id).removeAttribute("aria-invalid"));

      $("feedback-email-error").textContent = "";

      status(
        "feedback-status",
        "FEEDBACK_RECORDED: Thank you. " +
        "Your feedback was saved for this session only."
      );
    }
  );
});

$("feedback-email").addEventListener("input", () => {
  if ($("feedback-email").value) {
    validateEmail("feedback-email", "feedback-email-error");
  }
});
