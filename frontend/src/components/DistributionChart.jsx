import React from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = ["#8b5cf6", "#22d3ee", "#f97316", "#14b8a6", "#f43f5e"];

export default function DistributionChart({ data }) {
  return (
    <div className="card chart-card">
      <h3>Domain Distribution</h3>
      <div className="chart-body">
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="label" innerRadius={55}>
              {data.map((_, idx) => (
                <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
        <div className="legend">
          {data.map((item, idx) => (
            <div key={item.label} className="legend-item">
              <span
                className="legend-dot"
                style={{ background: COLORS[idx % COLORS.length] }}
              />
              <span>{item.label}</span>
              <strong>{item.value}%</strong>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
