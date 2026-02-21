document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:5000/reviews")
    .then(res => res.json())
    .then(data => {
      const tableBody = document.getElementById("reviewsTableBody");
      tableBody.innerHTML = "";

      data.forEach((review, index) => {
        const timestamp = review["timestamp"] || "";
        const bullyMessage = review["bully_message"] || "";
        const reviewMsg = review["review"] || "";
        const sentiment = review["sentiment"] || "";
        const score = review["sentiment_score"] || "";

        // Sentiment color class
        let sentimentClass = "";
        if (sentiment.toLowerCase() === "positive") sentimentClass = "positive";
        else if (sentiment.toLowerCase() === "negative") sentimentClass = "negative";
        else sentimentClass = "neutral";

        const row = `
          <tr>
            <td>${index + 1}</td>
            <td>${bullyMessage}</td>
            <td>${reviewMsg}</td>
            <td class="${sentimentClass}">${sentiment}</td>
            <td>${score}</td>
            <td>${timestamp}</td>
          </tr>
        `;
        tableBody.innerHTML += row;
      });
    })
    .catch(err => console.error("❌ Error fetching reviews:", err));
});
