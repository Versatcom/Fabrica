import { Section } from "../components/Section";
import { useApi } from "../components/useApi";

type SofaModel = {
  id: number;
  name: string;
  description?: string;
};

type Module = {
  id: number;
  name: string;
  width_cm: number;
  depth_cm: number;
  height_cm: number;
  weight_kg: number;
};

type SalesOrder = {
  id: number;
  status: string;
  total_amount: number;
  currency: string;
};

type StockItem = {
  id: number;
  product_name?: string;
  quantity: number;
  unit: string;
};

type Supplier = {
  id: number;
  name: string;
  contact_name: string;
};

type Customer = {
  id: number;
  name: string;
  contact_name: string;
};

export function App() {
  const models = useApi<SofaModel>("/models");
  const modules = useApi<Module>("/modules");
  const orders = useApi<SalesOrder>("/sales-orders");
  const stock = useApi<StockItem>("/stock-items");
  const suppliers = useApi<Supplier>("/suppliers");
  const customers = useApi<Customer>("/customers");

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>Perobell</h1>
        <div className="nav">
          <a href="#">Dashboard</a>
          <a href="#">Modelos</a>
          <a href="#">Módulos</a>
          <a href="#">Stock</a>
          <a href="#">Pedidos</a>
          <a href="#">Compras</a>
          <a href="#">Clientes</a>
          <a href="#">Proveedores</a>
        </div>
      </aside>
      <main className="main">
        <header>
          <h2>Panel general</h2>
          <p>
            Gestión completa de fabricación, escandallo, stock y pedidos.
          </p>
        </header>

        <div className="card-grid">
          <div className="card">
            <h3>Modelos</h3>
            <p className="badge">{models.data.length}</p>
          </div>
          <div className="card">
            <h3>Módulos</h3>
            <p className="badge">{modules.data.length}</p>
          </div>
          <div className="card">
            <h3>Pedidos</h3>
            <p className="badge">{orders.data.length}</p>
          </div>
          <div className="card">
            <h3>Stock</h3>
            <p className="badge">{stock.data.length}</p>
          </div>
        </div>

        <Section
          title="Pedidos recientes"
          description="Seguimiento en tiempo real de órdenes de venta"
        >
          {orders.loading && <p>Cargando...</p>}
          {orders.error && <p>{orders.error}</p>}
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Estado</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {orders.data.map((order) => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>{order.status}</td>
                  <td>
                    {order.total_amount} {order.currency}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Section>

        <Section title="Módulos en catálogo">
          {modules.loading && <p>Cargando...</p>}
          {modules.error && <p>{modules.error}</p>}
          <table className="table">
            <thead>
              <tr>
                <th>Módulo</th>
                <th>Medidas</th>
                <th>Peso</th>
              </tr>
            </thead>
            <tbody>
              {modules.data.map((module) => (
                <tr key={module.id}>
                  <td>{module.name}</td>
                  <td>
                    {module.width_cm} x {module.depth_cm} x {module.height_cm} cm
                  </td>
                  <td>{module.weight_kg} kg</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Section>

        <Section title="Proveedores y clientes">
          <div className="card-grid">
            <div className="card">
              <h4>Proveedores</h4>
              {suppliers.loading && <p>Cargando...</p>}
              {suppliers.error && <p>{suppliers.error}</p>}
              <ul>
                {suppliers.data.map((supplier) => (
                  <li key={supplier.id}>
                    {supplier.name} · {supplier.contact_name}
                  </li>
                ))}
              </ul>
            </div>
            <div className="card">
              <h4>Clientes</h4>
              {customers.loading && <p>Cargando...</p>}
              {customers.error && <p>{customers.error}</p>}
              <ul>
                {customers.data.map((customer) => (
                  <li key={customer.id}>
                    {customer.name} · {customer.contact_name}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </Section>
      </main>
    </div>
  );
}
