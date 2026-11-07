import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { formatLakhs, formatMonth, formatRupees } from "./format";
import { useApiData } from "./useApiData";
import "./SpendCharts.css";

const TOOLTIP_STYLE = {
  contentStyle: {
    background: "#1f2937",
    border: "1px solid #374151",
    borderRadius: 8,
  },
  labelStyle: { color: "#f9fafb" },
  itemStyle: { color: "#f9fafb" },
};

const CATEGORY_COLORS = {
  Facilities: "#f59e0b",
  "IT Hardware": "#7c3aed",
  Logistics: "#38bdf8",
  Marketing: "#ec4899",
  "Office Supplies": "#22c55e",
  Software: "#14b8a6",
};
const FALLBACK_COLOR = "#9ca3af";

function ChartCard({ title, data, error, className = "", children }) {
  let body = children;
  if (error) {
    body = <p className="chart-message">{error}</p>;
  } else if (data === null) {
    body = <p className="chart-message">Loading...</p>;
  } else if (data.length === 0) {
    body = <p className="chart-message">No data for these filters.</p>;
  }

  return (
    <section className={`chart-card ${className}`}>
      <h2>{title}</h2>
      {body}
    </section>
  );
}

function VendorChart({ filters }) {
  const { data, error } = useApiData("/api/spend/vendor", filters);
  return (
    <ChartCard title="Vendor-wise Spending" data={data} error={error}>
      <ResponsiveContainer width="100%" height={460}>
        <BarChart
          data={data}
          layout="vertical" 
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" tickFormatter={formatLakhs}  />
          <YAxis type="category" dataKey="vendor" width={130}  tick={{ fontSize: 14 }}/>
          <Tooltip
            {...TOOLTIP_STYLE}
            cursor={{ fill: "rgba(128, 128, 128, 0.15)" }}
            formatter={(value) => formatRupees(value)}
          />
          <Bar dataKey="total_spend" name="Spend" fill="#7c3aed" />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function CategoryChart({ filters }) {
  const { data, error } = useApiData("/api/spend/category", filters);
  return (
    <ChartCard title="Category-wise Spending" data={data} error={error}>
      <ResponsiveContainer width="100%" height={460}>
        <BarChart data={data}  >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="category" interval={0} tick={{ fontSize: 12 }}  angle={-15} />
          <YAxis tickFormatter={formatLakhs} />
          <Tooltip
            {...TOOLTIP_STYLE}
            cursor={{ fill: "rgba(128, 128, 128, 0.15)" }}
            formatter={(value) => formatRupees(value)}
          />
          <Bar dataKey="total_spend" name="Spend" fill="#38bdf8" />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function MonthlyChart({ filters }) {
  const { data, error } = useApiData("/api/spend/monthly", filters);
  return (
    <ChartCard title="Monthly Spending Trend" data={data} error={error}>
      <ResponsiveContainer width="100%" height={460}>
        <LineChart data={data}  >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" tick={{ fontSize: 12 }} interval={3} angle={-10 } />
          <YAxis tickFormatter={formatLakhs} />
          <Tooltip
            {...TOOLTIP_STYLE}
            formatter={(value) => formatRupees(value)}
          />
          <Line
            type="monotone"
            dataKey="total_spend"
            name="Spend"
            stroke="#22c55e"
            strokeWidth={2}
            dot={{ r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function CategoryPie({ filters }) {
  const { data, error } = useApiData("/api/spend/category", filters);
  const rows = data ?? [];
  return (
    <ChartCard title="Category Spending Distribution" data={data} error={error}>
      <ResponsiveContainer width="100%" height={380}>
        <PieChart>
          <Pie
            data={rows}
            dataKey="total_spend"
            nameKey="category"
            startAngle={90}
            endAngle={-270}
            outerRadius="70%"
            label={({ percent }) => `${(percent * 100).toFixed(1)}%`}
          >
            {rows.map((row) => (
              <Cell
                key={row.category}
                fill={CATEGORY_COLORS[row.category] ?? FALLBACK_COLOR}
              />
            ))}
          </Pie>
          <Tooltip
            {...TOOLTIP_STYLE}
            formatter={(value) => formatRupees(value)}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function ForecastChart({ filters }) {
  const { data, error } = useApiData("/api/forecast", filters);
  const rows = data ? data.forecast : null;
  const message = error || (data && data.message) || "";
  const monthLabel = data && data.next_month ? formatMonth(data.next_month) : "";

  return (
    <ChartCard
      title="Forecast: Next Month's Spend"
      data={rows}
      error={message}
      className="wide"
    >
      <p className="chart-caption">
        Predicted spend for <strong>{monthLabel}</strong>
      </p>
      <ResponsiveContainer width="100%" height={380} >
        <BarChart data={rows}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="category" interval={0} tick={{ fontSize: 12 }} />
          <YAxis tickFormatter={formatLakhs} />
          <Tooltip
            {...TOOLTIP_STYLE}
            cursor={{ fill: "rgba(128, 128, 128, 0.15)" }}
            formatter={(value) => formatRupees(value)}
          />
          <Bar dataKey="forecast_spend" name="Predicted spend" fill="#f59e0b" />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function SpendCharts({ filters }) {
  return (
    <div className="chart-grid">
      <VendorChart filters={filters} />
      <CategoryChart filters={filters} />
      <MonthlyChart filters={filters} />
      <CategoryPie filters={filters} />
      <ForecastChart filters={filters} />
    </div>
  );
}

export default SpendCharts;