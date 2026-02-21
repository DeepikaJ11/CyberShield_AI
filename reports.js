document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:5000/reports")
    .then(res => res.json())
    .then(data => {
      const tableBody = document.getElementById("reportsTableBody");
      tableBody.innerHTML = "";

      data.forEach((log, index) => {
        const timestamp = log["date"] || "";
        const user = log["user"] || "Unknown";      
        const message = log["message"] || "";         
        const severity = log["severity"] || "";      

        // Severity color class
        let severityClass = "";
        if (severity === "High") severityClass = "high";
        else if (severity === "Medium") severityClass = "medium";
        else severityClass = "low";

        const row = `
          <tr>
            <td>${index + 1}</td>
            <td>${user}</td>
            <td>${message}</td>
            <td class="${severityClass}">${severity}</td>
            <td>${timestamp}</td>
          </tr>
        `;
        tableBody.innerHTML += row;
      });
    })
    .catch(err => console.error("❌ Error fetching reports:", err));
});
