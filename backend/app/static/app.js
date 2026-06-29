const state = {
  user: null,
  sessionId: null,
  currentQuestion: null,
};

async function fetchJSON(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Request failed");
  }
  return response.json();
}

function renderPills(items = []) {
  return items.map((item) => `<span class="pill">${item}</span>`).join("");
}

function formatList(items, emptyText, renderer) {
  if (!items || !items.length) {
    return `<p>${emptyText}</p>`;
  }
  return items.map((item) => `<div class="list-block">${renderer(item)}</div>`).join("");
}

function persistUser(user) {
  state.user = user;
  localStorage.setItem("ai-career-lab-user", JSON.stringify(user));
}

function loadStoredUser() {
  const raw = localStorage.getItem("ai-career-lab-user");
  if (!raw) {
    return;
  }
  try {
    state.user = JSON.parse(raw);
    document.getElementById("auth-result").textContent =
      `Signed in as ${state.user.name} (${state.user.email})`;
  } catch {
    localStorage.removeItem("ai-career-lab-user");
  }
}

async function loadHealth() {
  const data = await fetchJSON("/api/health");
  document.getElementById("health-status").textContent = `${data.status} | ${data.mode} mode`;
}

async function loadJobDescription() {
  const data = await fetchJSON("/api/job-description");
  document.getElementById("job-title").textContent = data.title;
  document.getElementById("job-description").textContent = data.description;
}

async function loadDashboard() {
  if (!state.user) {
    return;
  }
  const data = await fetchJSON(`/api/dashboard/${state.user.user_id}`);
  document.getElementById("dashboard-summary").textContent =
    `${data.user.name} has ${data.sessions.length} saved sessions, ${data.feedback.length} feedback items, and ${data.resume_matches.length} resume scores.`;

  document.getElementById("dashboard-sessions").innerHTML = formatList(
    data.sessions,
    "No sessions yet.",
    (item) =>
      `<strong>${item.target_role}</strong><br>${item.candidate_name} | ${item.experience_level}<br>${renderPills(
        item.focus_areas
      )}<br>Questions asked: ${item.question_count}`
  );

  document.getElementById("dashboard-feedback").innerHTML = formatList(
    data.feedback,
    "No feedback history yet.",
    (item) =>
      `<strong>${item.score}/100</strong><br>${item.question}<br><span>${item.answer.slice(0, 120)}...</span>`
  );

  document.getElementById("dashboard-resumes").innerHTML = formatList(
    data.resume_matches,
    "No resume scores yet.",
    (item) =>
      `<strong>${item.match_score}/100 match</strong><br>${renderPills(item.matched_skills)}${renderPills(
        item.missing_skills.map((skill) => `Need: ${skill}`)
      )}`
  );
}

async function authenticate(mode) {
  const form = document.getElementById("auth-form");
  const formData = new FormData(form);
  const payload = {
    name: formData.get("name"),
    email: formData.get("email"),
    password: formData.get("password"),
  };
  const endpoint = mode === "register" ? "/api/auth/register" : "/api/auth/login";
  const result = await fetchJSON(endpoint, {
    method: "POST",
    body: JSON.stringify(payload),
  });
  persistUser(result);
  document.getElementById("auth-result").textContent = `Signed in as ${result.name} (${result.email})`;
  await loadDashboard();
}

document.getElementById("auth-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await authenticate("login");
  } catch (error) {
    document.getElementById("auth-result").textContent = error.message;
  }
});

document.getElementById("register-button").addEventListener("click", async () => {
  try {
    await authenticate("register");
  } catch (error) {
    document.getElementById("auth-result").textContent = error.message;
  }
});

document.getElementById("session-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.user) {
    document.getElementById("session-result").textContent = "Log in first to create and save a session.";
    return;
  }

  const formData = new FormData(event.currentTarget);
  const payload = {
    user_id: state.user.user_id,
    candidate_name: formData.get("candidate_name"),
    target_role: formData.get("target_role"),
    experience_level: formData.get("experience_level"),
    focus_areas: String(formData.get("focus_areas"))
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean),
  };

  try {
    const result = await fetchJSON("/api/interview/session", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.sessionId = result.session_id;
    document.getElementById("session-result").textContent = result.welcome_message;
    await loadDashboard();
  } catch (error) {
    document.getElementById("session-result").textContent = error.message;
  }
});

document.getElementById("question-button").addEventListener("click", async () => {
  if (!state.sessionId) {
    document.getElementById("question-text").textContent = "Create a session first.";
    return;
  }

  try {
    const result = await fetchJSON("/api/interview/question", {
      method: "POST",
      body: JSON.stringify({
        session_id: state.sessionId,
        include_follow_up: true,
      }),
    });
    state.currentQuestion = result.question;
    document.getElementById("question-text").textContent = result.question;
    document.getElementById("question-meta").textContent = `${result.category} | ${result.why_it_matters}`;
    await loadDashboard();
  } catch (error) {
    document.getElementById("question-text").textContent = error.message;
  }
});

document.getElementById("feedback-button").addEventListener("click", async () => {
  if (!state.sessionId || !state.currentQuestion) {
    document.getElementById("feedback-result").textContent =
      "Start a session and generate a question first.";
    return;
  }

  const answer = document.getElementById("answer-input").value.trim();
  if (!answer) {
    document.getElementById("feedback-result").textContent = "Add an answer first.";
    return;
  }

  try {
    const result = await fetchJSON("/api/interview/feedback", {
      method: "POST",
      body: JSON.stringify({
        session_id: state.sessionId,
        question: state.currentQuestion,
        answer,
      }),
    });

    document.getElementById("feedback-result").innerHTML = `
      <p><strong>Score:</strong> ${result.score}/100</p>
      <p><strong>Strengths</strong><br>${renderPills(result.strengths)}</p>
      <p><strong>Improvements</strong><br>${renderPills(result.improvements)}</p>
      <p><strong>Better answer direction:</strong> ${result.sample_better_answer}</p>
    `;
    await loadDashboard();
  } catch (error) {
    document.getElementById("feedback-result").textContent = error.message;
  }
});

document.getElementById("resume-button").addEventListener("click", async () => {
  const resumeText = document.getElementById("resume-input").value.trim();
  if (!resumeText) {
    document.getElementById("resume-result").textContent = "Paste resume text first.";
    return;
  }

  try {
    const result = await fetchJSON("/api/resume/match", {
      method: "POST",
      body: JSON.stringify({
        user_id: state.user?.user_id || null,
        resume_text: resumeText,
      }),
    });

    document.getElementById("resume-result").innerHTML = `
      <p><strong>Match score:</strong> ${result.match_score}/100</p>
      <p><strong>Matched skills</strong><br>${renderPills(result.matched_skills)}</p>
      <p><strong>Missing skills</strong><br>${renderPills(result.missing_skills)}</p>
      <p><strong>Recommendations</strong><br>${renderPills(result.recommendations)}</p>
    `;
    await loadDashboard();
  } catch (error) {
    document.getElementById("resume-result").textContent = error.message;
  }
});

loadStoredUser();
loadHealth().catch(() => {
  document.getElementById("health-status").textContent = "backend unavailable";
});
loadJobDescription().catch(() => {
  document.getElementById("job-title").textContent = "Unable to load";
});
loadDashboard().catch(() => {});
