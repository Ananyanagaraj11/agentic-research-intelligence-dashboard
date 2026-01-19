import React, { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import Header from "./components/Header.jsx";
import StatCard from "./components/StatCard.jsx";
import DistributionChart from "./components/DistributionChart.jsx";
import RadarCard from "./components/RadarCard.jsx";
import TrendChart from "./components/TrendChart.jsx";
import AgentPanel from "./components/AgentPanel.jsx";
import DataInsights from "./components/DataInsights.jsx";

const FALLBACK = {
  kpis: { precision: 0.818, recall: 0.888, f1: 0.851, accuracy: 0.842 },
  distribution: [
    { label: "NLP", value: 36 },
    { label: "CV", value: 24 },
    { label: "Robotics", value: 12 },
    { label: "Bioinformatics", value: 18 },
    { label: "Security", value: 10 },
  ],
  radar: [
    { metric: "Precision", value: 0.82 },
    { metric: "Recall", value: 0.89 },
    { metric: "F1", value: 0.85 },
    { metric: "Coverage", value: 0.78 },
    { metric: "Drift", value: 0.18 },
  ],
  trend: [
    { month: "Jan", value: 62 },
    { month: "Feb", value: 68 },
    { month: "Mar", value: 74 },
    { month: "Apr", value: 71 },
    { month: "May", value: 79 },
    { month: "Jun", value: 85 },
  ],
  insights: {
    total_records: 10000,
    unique_labels: 12,
    top_labels: [
      { label: "cs.AI", count: 2100 },
      { label: "cs.LG", count: 1800 },
      { label: "cs.CL", count: 1600 },
    ],
    top_terms_global: ["model", "learning", "neural", "network", "data", "training"],
  },
};

const API = "http://localhost:8000/analytics";

export default function App() {
  const [kpis, setKpis] = useState(FALLBACK.kpis);
  const [distribution, setDistribution] = useState(FALLBACK.distribution);
  const [radar, setRadar] = useState(FALLBACK.radar);
  const [trend, setTrend] = useState(FALLBACK.trend);
  const [insights, setInsights] = useState(FALLBACK.insights);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/kpis`).then((r) => r.json()),
      fetch(`${API}/entity-distribution`).then((r) => r.json()),
      fetch(`${API}/radar-metrics`).then((r) => r.json()),
      fetch(`${API}/trend-series`).then((r) => r.json()),
      fetch(`${API}/insights`).then((r) => r.json()),
    ])
      .then(([k, d, r, t, i]) => {
        setKpis(k);
        setDistribution(d);
        setRadar(r);
        setTrend(t);
        setInsights(i);
      })
      .catch(() => null);
  }, []);

  const scoreCards = useMemo(
    () => [
      {
        title: "Precision",
        value: kpis.precision,
        subtitle: "Model accuracy",
      },
      {
        title: "Recall",
        value: kpis.recall,
        subtitle: "Coverage",
      },
      {
        title: "F1-Score",
        value: kpis.f1,
        subtitle: "Harmonic mean",
      },
      {
        title: "Accuracy",
        value: kpis.accuracy,
        subtitle: "Overall quality",
      },
    ],
    [kpis]
  );

  return (
    <div className="app">
      <Header />
      <motion.div
        className="grid"
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {scoreCards.map((card) => (
          <StatCard key={card.title} {...card} />
        ))}
      </motion.div>

      <div className="content-grid">
        <DistributionChart data={distribution} />
        <RadarCard data={radar} />
        <TrendChart data={trend} />
        <DataInsights insights={insights} />
        <AgentPanel />
      </div>
    </div>
  );
}
