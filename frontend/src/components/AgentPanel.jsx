import React, { useState } from "react";
import { motion } from "framer-motion";

const INSIGHTS = [
  "Data QA flagged 1.8% noisy abstracts for review.",
  "Emerging growth: Bioinformatics +18% in the last 30 days.",
  "Precision improved after rebalancing minority classes.",
  "Suggested action: fine-tune with SciBERT embeddings.",
];

const API = "http://localhost:8000/analytics";

export default function AgentPanel() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleReport = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API}/weekly-report`);
      const data = await res.json();
      setReport(data);
    } catch (err) {
      setError("Failed to generate report. Check the API.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      className="card agent-card"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2, duration: 0.5 }}
    >
      <h3>Agentic Insight Engine</h3>
      <p className="agent-subtitle">
        Autonomous analysis, trend detection, and narrative reporting.
      </p>
      <div className="agent-list">
        {(report?.highlights || INSIGHTS).map((text) => (
          <div key={text} className="agent-item">
            <span className="agent-dot" />
            <span>{text}</span>
          </div>
        ))}
      </div>
      {report?.title && <div className="agent-report">{report.title}</div>}
      {error && <div className="agent-error">{error}</div>}
      <button className="agent-btn" onClick={handleReport} disabled={loading}>
        {loading ? "Generating..." : "Generate Weekly Report"}
      </button>
    </motion.div>
  );
}
