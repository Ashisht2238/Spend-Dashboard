import { formatMoney } from "./format";
import { useApiData } from "./useApiData";
import "./AnomalyTable.css";

function AnomalyTable({ filters }) {
  const { data, error } = useApiData("/api/anomalies", filters);

  let body;
  if (error) {
    body = <p className="table-message">Could not load the unusual orders.</p>;
  } else if (data === null) {
    body = <p className="table-message">Loading...</p>;
  } else if (data.count === 0) {
    body = <p className="table-message">No unusual orders detected.</p>;
  } else {
    body = (
      <>
        <p className="table-caption">
          {data.count === 1 ? "1 order looks" : `${data.count} orders look`}{" "}
          unusual for their category.
        </p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>PO Number</th>
                <th>Date</th>
                <th>Vendor</th>
                <th>Category</th>
                <th>Item</th>
                <th className="num">Quantity</th>
                <th className="num">Unit Price</th>
                <th className="num">Total Amount</th>
              </tr>
            </thead>
            <tbody>
              {data.orders.map((order) => (
                <tr key={order.po_number}>
                  <td>{order.po_number}</td>
                  <td>{order.po_date}</td>
                  <td>{order.vendor}</td>
                  <td>{order.category}</td>
                  <td>{order.item}</td>
                  <td className="num">{order.quantity.toLocaleString("en-IN")}</td>
                  <td className="num">{formatMoney(order.unit_price)}</td>
                  <td className="num">{formatMoney(order.total_amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>
    );
  }

  return (
    <section className="table-card">
      <h2>Unusual Orders</h2>
      {body}
    </section>
  );
}

export default AnomalyTable;