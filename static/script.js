document.documentElement.setAttribute("data-theme", "light");

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  document.documentElement.setAttribute("data-theme", current === "dark" ? "light" : "dark");
}

async function runQuery() {
  const query = document.getElementById("queryInput").value;
  const response = await fetch("/execute", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });

  const data = await response.json();
  const outputDiv = document.getElementById("output");

  if (data.status === "success") {
    let table = "<table border='1'><tr>";
    for (const col of data.columns) table += `<th>${col}</th>`;
    table += "</tr>";
    for (const row of data.rows) {
      table += "<tr>";
      for (const cell of row) table += `<td>${cell}</td>`;
      table += "</tr>";
    }
    table += "</table>";
    outputDiv.innerHTML = `<div style="color:green;">Query Executed Successfully</div>${table}`;
    window.lastData = data;
  } else {
    outputDiv.innerHTML = `<div style="color:red;">Error: ${data.message}</div>`;
  }
}

async function getSuggestion() {
  const query = document.getElementById("queryInput").value;
  const loader = document.getElementById("loader");
  loader.classList.remove("hidden");

  const response = await fetch("/suggest", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });

  const data = await response.json();
  document.getElementById("suggestionBox").innerText = "Suggested Query:\n" + data.suggestion;

  loader.classList.add("hidden");
}

async function exportCSV() {
  if (!window.lastData) {
    alert("Run a query first!");
    return;
  }

  const response = await fetch("/export_csv", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      columns: window.lastData.columns,
      rows: window.lastData.rows
    })
  });

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "results.csv";
  document.body.appendChild(a);
  a.click();
  a.remove();
}
