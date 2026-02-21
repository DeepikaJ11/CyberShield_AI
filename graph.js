document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:5000/reviews")
    .then(res => res.json())
    .then(data => {
      let positiveCount = 0, negativeCount = 0, neutralCount = 0;
      let timestamps = [], sentimentScores = [];

      data.forEach(review => {
        const sentiment = review["sentiment"]?.toLowerCase() || "";
        if (sentiment === "positive") positiveCount++;
        else if (sentiment === "negative") negativeCount++;
        else neutralCount++;

        timestamps.push(review["timestamp"]);
        sentimentScores.push(review["sentiment_score"]);
      });

      // ---------- Pie/Doughnut Chart ----------
      const ctx1 = document.getElementById("sentimentChart").getContext("2d");
      new Chart(ctx1, {
        type: "doughnut",
        data: {
          labels: ["Positive", "Negative", "Neutral"],
          datasets: [{
            data: [positiveCount, negativeCount, neutralCount],
            backgroundColor: [
              "rgba(34, 197, 94, 0.8)",   // Green
              "rgba(239, 68, 68, 0.8)",   // Red
              "rgba(250, 204, 21, 0.8)"   // Yellow
            ],
            borderColor: [
              "rgba(34, 197, 94, 1)",
              "rgba(239, 68, 68, 1)",
              "rgba(250, 204, 21, 1)"
            ],
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "bottom" }
          }
        }
      });

      // ---------- Line Chart ----------
      const ctx2 = document.getElementById("timelineChart").getContext("2d");
      new Chart(ctx2, {
        type: "line",
        data: {
          labels: timestamps,
          datasets: [{
            label: "Sentiment Score over Time",
            data: sentimentScores,
            borderColor: "rgba(59, 130, 246, 1)",   // Blue
            backgroundColor: "rgba(59, 130, 246, 0.3)",
            fill: true,
            tension: 0.4,
            pointRadius: 5,
            pointBackgroundColor: "#1d4ed8"
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: true, max: 1 }
          }
        }
      });
    })
    .catch(err => console.error("❌ Error fetching reviews:", err));
});
