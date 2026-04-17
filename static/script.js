async function loadAlerts() {
    const res = await fetch('/alerts');
    const data = await res.json();

    let table = document.querySelector("#alertsTable tbody");
    table.innerHTML = "";

    if (data.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="5">No security issues detected</td>
            </tr>
        `;
        return;
    }

    data.forEach(alert => {
        let severityClass = alert.severity.toLowerCase();

        let row = `
            <tr>
                <td>${alert.type}</td>
                <td>${alert.doc}</td>
                <td>
                    <span class="badge ${severityClass}">
                        ${alert.severity}
                    </span>
                </td>
                <td>${alert.details || "-"}</td>
                <td>
                    <button class="fix-btn" onclick="remediate('${alert.id}')">
                        Resolve
                    </button>
                    
                    ${alert.row_id ? `
                    <button class="delete-btn" onclick="deleteRow('${alert.id}', '${alert.table_id}', '${alert.row_id}')">
                        Delete
                    </button>
                    ` : ''}
                </td>
            </tr>
        `;

        table.innerHTML += row;
    });
}

async function remediate(id) {
    await fetch(`/fix/${id}`);
    alert("Issue resolved");
    loadAlerts();
}

async function deleteRow(docId, tableId, rowId) {
    if (!confirm("Are you sure you want to delete this sensitive data?")) return;

    await fetch(`/delete/${docId}/${tableId}/${rowId}`);
    alert("🗑️ Data deleted successfully");

    loadAlerts();
}

setInterval(loadAlerts, 4000);
loadAlerts();