const API_BASE = "/api/expenses";

document.getElementById("today-date").textContent = new Date().toLocaleDateString("en-US", {
  weekday: "long",
  year: "numeric",
  month: "long",
  day: "numeric",
});

document.getElementById("expense-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const amount = parseFloat(document.getElementById("amount").value);
  const category = document.getElementById("category").value.trim();
  const description = document.getElementById("description").value.trim();

  if (!amount || !category) return;

  await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount, category, description }),
  });

  document.getElementById("amount").value = "";
  document.getElementById("category").value = "";
  document.getElementById("description").value = "";

  loadExpenses();
});

async function loadExpenses() {
  const res = await fetch(API_BASE);
  const expenses = await res.json();
  const list = document.getElementById("expenses-list");
  list.innerHTML = "";

  if (expenses.length === 0) {
    list.innerHTML = "<p class='loading'>No expenses yet.</p>";
    return;
  }

  expenses.forEach((item) => {
    const li = document.createElement("li");
    li.className = "expense-item";

    const desc = document.createElement("span");
    desc.className = "expense-desc";
    desc.textContent = item.description || item.category;

    const cat = document.createElement("span");
    cat.className = "expense-category";
    cat.textContent = item.category;

    const amt = document.createElement("span");
    amt.className = "expense-amount";
    amt.textContent = `$${item.amount.toFixed(2)}`;

    const time = document.createElement("span");
    time.className = "expense-time";
    time.textContent = new Date(item.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    const delBtn = document.createElement("span");
    delBtn.className = "delete-btn material-icons";
    delBtn.textContent = "close";
    delBtn.onclick = () => deleteExpense(item.id);

    li.appendChild(desc);
    li.appendChild(cat);
    li.appendChild(amt);
    li.appendChild(time);
    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

async function deleteExpense(id) {
  await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
  loadExpenses();
  loadSummary();
}

async function loadSummary() {
  const res = await fetch(`${API_BASE}/summary`);
  const summary = await res.json();
  const container = document.getElementById("summary");

  if (summary.count === 0) {
    container.innerHTML = "<p class='loading'>No expenses today.</p>";
    return;
  }

  let html = "";
  html += `<div class="summary-item"><span class="label">Total Spent</span><span class="value">$${summary.total.toFixed(2)}</span></div>`;
  html += `<div class="summary-item"><span class="label">Entries</span><span class="value">${summary.count}</span></div>`;

  for (const [cat, val] of Object.entries(summary.by_category)) {
    html += `<div class="summary-item"><span class="label">${cat}</span><span class="value">$${val.toFixed(2)}</span></div>`;
  }

  container.innerHTML = html;
}

loadExpenses();
loadSummary();
