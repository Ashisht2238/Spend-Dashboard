import { useEffect, useState } from "react";
import { getJson } from "./api";
import "./App.css";
import FilterBar from "./FilterBar";
import KpiCards from "./KpiCards";
import SpendCharts from "./SpendCharts";
import AnomalyTable from "./AnomalyTable";

const EMPTY_FILTERS = {
  vendor: "",
  category: "",
  department: "",
  status: "",
  start_date: "",
  end_date: "",
};

function App() {
  const [options, setOptions] = useState(null);
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getJson("/api/filters")
      .then(setOptions)
      .catch(() => setError("Could not load the filter options."));
  }, []);

  useEffect(() => {
    let ignore = false;
    getJson("/api/summary", filters)
      .then((data) => {
        if (!ignore) {
          setSummary(data);
          setError("");
        }
      })
      .catch(() => {
        if (!ignore) {
          setError("Could not load the summary.");
        }
      });
    return () => {
      ignore = true;
    };
  }, [filters]);

  
  return (
    <div className="page">
  <header className="app-header">
    <h1>Spend Analytics Dashboard</h1>
    <p>Purchase order spend, unusual orders and forecast</p>
  </header>

      {error && <p className="error-banner">{error}</p>}

      {options && (
        <FilterBar
          options={options}
          filters={filters}
          onChange={setFilters}
          onReset={() => setFilters(EMPTY_FILTERS)}
        />
      )}

      {summary && <KpiCards summary={summary} />}
      <SpendCharts filters={filters} />
      <AnomalyTable filters={filters} />
    </div>
  );
}

export default App;