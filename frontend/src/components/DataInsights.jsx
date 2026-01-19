import React from "react";

export default function DataInsights({ insights }) {
  return (
    <div className="card insights-card">
      <h3>Dataset Meaning</h3>
      <p className="insights-subtitle">
        What the large corpus is about, extracted from titles and abstracts.
      </p>
      <div className="insights-stats">
        <div>
          <span>Total records</span>
          <strong>{insights.total_records.toLocaleString()}</strong>
        </div>
        <div>
          <span>Unique labels</span>
          <strong>{insights.unique_labels}</strong>
        </div>
      </div>
      <div className="insights-section">
        <span>Top domains</span>
        <div className="insights-list">
          {insights.top_labels.map((item) => (
            <div key={item.label} className="insight-pill">
              <span>{item.label}</span>
              <strong>{item.count}</strong>
            </div>
          ))}
        </div>
      </div>
      <div className="insights-section">
        <span>Global concepts</span>
        <div className="insights-list">
          {insights.top_terms_global.map((term) => (
            <div key={term} className="insight-pill">
              {term}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
