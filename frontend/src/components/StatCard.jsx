import React from "react";
import { motion } from "framer-motion";

const formatter = new Intl.NumberFormat("en-US", {
  style: "percent",
  maximumFractionDigits: 1,
});

export default function StatCard({ title, value, subtitle }) {
  return (
    <motion.div
      className="card stat-card"
      whileHover={{ y: -6 }}
      transition={{ type: "spring", stiffness: 220, damping: 18 }}
    >
      <div className="stat-title">{title}</div>
      <div className="stat-value">{formatter.format(value)}</div>
      <div className="stat-subtitle">{subtitle}</div>
    </motion.div>
  );
}
