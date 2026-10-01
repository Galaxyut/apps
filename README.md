const STORAGE_KEY = "stock_transactions";
const sampleData = [
  {
    id: crypto.randomUUID(),
    date: "2026-10-01",
    item: "A4 paper",
    itemCode: "SKU-001",
    inQty: 100,
    outQty: 0,
    unit: "pack",
    party: "ABC Paper",
    remarks: "Purchase"
  },
  {
    id: crypto.randomUUID(),
    date: "2026-10-02",
    item: "A4 paper",
    itemCode: "SKU-001",
    inQty: 0,
    outQty: 20,
    unit: "pack",
    party: "Office",
    remarks: "Office use"
  },
  {
    id: crypto.randomUUID(),
    date: "2026-10-03",
    item: "Pen",
    itemCode: "SKU-002",
    inQty: 50,
    outQty: 0,
    unit: "pcs",
    party: "Stationery Shop",
    remarks: "Restock"
  },
  {
    id: crypto.randomUUID(),
    date: "2026-10-04",
    item: "Pen",
    itemCode: "SKU-002",
    inQty: 0,
    outQty: 10,
    unit: "pcs",
    party: "Student",
    remarks: "Sale"
  }
];

const form = document.getElementById("stockForm");
const transactionTableBody = document.getElementById("transactionTableBody");
const summaryTableBody = document.getElementById("summaryTableBody");
const totalItems = document.getElementById("totalItems");
const totalIn = document.getElementById("totalIn");
const totalOut = document.getElementById("totalOut");
const resetBtn = document.getElementById("resetBtn");

function getTransactions() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(sampleData));
    return [...sampleData];
  }

  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [...sampleData];
  } catch (error) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(sampleData));
    return [...sampleData];
  }
}

function saveTransactions(transactions) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(transactions));
}

function renderTransactions() {
  const transactions = getTransactions();

  transactionTableBody.innerHTML = "";

  if (transactions.length === 0) {
    transactionTableBody.innerHTML = '<tr><td colspan="9" class="empty-state">No transactions yet.</td></tr>';
    renderSummary();
    return;
  }

  transactions
    .slice()
    .reverse()
    .forEach((record) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${record.date}</td>
        <td>${record.item}</td>
        <td>${record.itemCode}</td>
        <td>${record.inQty}</td>
        <td>${record.outQty}</td>
        <td>${record.unit}</td>
        <td>${record.party || "-"}</td>
        <td>${record.remarks || "-"}</td>
        <td><button type="button" data-id="${record.id}">Delete</button></td>
      `;
      transactionTableBody.appendChild(row);
    });

  renderSummary();
}

function renderSummary() {
  const transactions = getTransactions();

  const summaryMap = new Map();

  transactions.forEach((record) => {
    const key = record.itemCode || record.item;
    const current = summaryMap.get(key) || {
      item: record.item,
      itemCode: record.itemCode,
      unit: record.unit,
      totalIn: 0,
      totalOut: 0
    };

    current.totalIn += Number(record.inQty || 0);
    current.totalOut += Number(record.outQty || 0);
    summaryMap.set(key, current);
  });

  const items = Array.from(summaryMap.values()).sort((a, b) => a.item.localeCompare(b.item));
  summaryTableBody.innerHTML = "";

  if (items.length === 0) {
    summaryTableBody.innerHTML = '<tr><td colspan="6" class="empty-state">No data available.</td></tr>';
    totalItems.textContent = "0";
    totalIn.textContent = "0";
    totalOut.textContent = "0";
    return;
  }

  let grandIn = 0;
  let grandOut = 0;

  items.forEach((item) => {
    grandIn += item.totalIn;
    grandOut += item.totalOut;

    const stock = item.totalIn - item.totalOut;
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.item}</td>
      <td>${item.itemCode}</td>
      <td>${item.unit}</td>
      <td>${item.totalIn}</td>
      <td>${item.totalOut}</td>
      <td class="${stock >= 0 ? "stock-positive" : "stock-negative"}">${stock}</td>
    `;
    summaryTableBody.appendChild(row);
  });

  totalItems.textContent = String(items.length);
  totalIn.textContent = String(grandIn);
  totalOut.textContent = String(grandOut);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const newRecord = {
    id: crypto.randomUUID(),
    date: document.getElementById("date").value,
    item: document.getElementById("item").value.trim(),
    itemCode: document.getElementById("itemCode").value.trim(),
    inQty: Number(document.getElementById("inQty").value || 0),
    outQty: Number(document.getElementById("outQty").value || 0),
    unit: document.getElementById("unit").value.trim() || "pcs",
    party: document.getElementById("party").value.trim(),
    remarks: document.getElementById("remarks").value.trim()
  };

  if (!newRecord.date || !newRecord.item || !newRecord.itemCode) {
    alert("Please enter date, item, and item code.");
    return;
  }

  const transactions = getTransactions();
  transactions.push(newRecord);
  saveTransactions(transactions);
  form.reset();

  document.getElementById("date").valueAsDate = new Date();
  document.getElementById("inQty").value = 0;
  document.getElementById("outQty").value = 0;
  document.getElementById("unit").value = "pcs";

  renderTransactions();
});

transactionTableBody.addEventListener("click", (event) => {
  const target = event.target;
  if (!(target instanceof HTMLButtonElement)) return;

  const { id } = target.dataset;
  if (!id) return;

  const transactions = getTransactions().filter((record) => record.id !== id);
  saveTransactions(transactions);
  renderTransactions();
});

resetBtn.addEventListener("click", () => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(sampleData));
  renderTransactions();
});

document.getElementById("date").valueAsDate = new Date();
renderTransactions();
