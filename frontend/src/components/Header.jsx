import React from "react";
import { motion } from "framer-motion";

export default function Header() {
  return (
    <motion.header
      className="hero"
      initial={{ opacity: 0, y: -12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="hero-badge">Agentic Research Intelligence</div>
      <h1>Paper Trend Analytics Dashboard</h1>
      <p>
        Large-scale ingestion, model training, and automated insights on the
        most active research domains.
      </p>
      <div className="hero-metrics">
        <span>arXiv + OpenAlex</span>
        <span>Multi-class Classifier</span>
        <span>Agentic Insight Engine</span>
      </div>
    </motion.header>
  );
}
