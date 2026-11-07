import "./KpiCards.css";
import { formatRupees } from "./format";

function KpiCard({ label, value }) {
  return (
    <div className="kpi-card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
    </div>
  );
}

function KpiCards({ summary }) {
  return (
    <section className="kpi-grid">
      <KpiCard label="Total Spend" value={formatRupees(summary.total_spend)} />
      <KpiCard
        label="Total Orders"
        value={summary.total_orders.toLocaleString("en-IN")}
      />
      <KpiCard label="Total Vendors" value={summary.total_vendors} />
      <KpiCard label="Flagged Orders" value={summary.flagged_orders} />
    </section>
  );
}

export default KpiCards;