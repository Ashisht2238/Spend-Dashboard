export function formatRupees(amount) {
  return "₹ " + amount.toLocaleString("en-IN", { maximumFractionDigits: 0 });
}

export function formatMoney(amount) {
  return (
    "₹ " +
    amount.toLocaleString("en-IN", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  );
}

export function formatLakhs(amount) {
  return `₹${(amount / 100000).toFixed(1)}L`;
}

export function formatMonth(yearMonth) {
  const [year, month] = yearMonth.split("-").map(Number);
  return new Date(year, month - 1, 1).toLocaleString("en-IN", {
    month: "long",
    year: "numeric",
  });
}