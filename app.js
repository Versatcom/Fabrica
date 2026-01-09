const models = [
  { id: "MX-100", name: "Silla MX-100" },
  { id: "LX-210", name: "Mesa LX-210" },
  { id: "QT-55", name: "Sofá QT-55" },
  { id: "VN-32", name: "Banco VN-32" },
];

let stock = [
  { modelId: "MX-100", onHand: 120, reserved: 24 },
  { modelId: "LX-210", onHand: 75, reserved: 12 },
  { modelId: "QT-55", onHand: 42, reserved: 8 },
  { modelId: "VN-32", onHand: 210, reserved: 30 },
];

let production = [
  {
    id: "PR-084",
    modelId: "MX-100",
    stage: "Corte y ensamblaje",
    units: 45,
    startDate: "2026-01-05",
    eta: "2026-01-16",
  },
  {
    id: "PR-091",
    modelId: "LX-210",
    stage: "Barnizado",
    units: 30,
    startDate: "2026-01-08",
    eta: "2026-01-20",
  },
  {
    id: "PR-093",
    modelId: "QT-55",
    stage: "Tapizado",
    units: 18,
    startDate: "2026-01-10",
    eta: "2026-01-18",
  },
  {
    id: "PR-094",
    modelId: "VN-32",
    stage: "Inspección final",
    units: 60,
    startDate: "2026-01-11",
    eta: "2026-01-15",
  },
];

let orders = [
  {
    id: "PD-311",
    client: "Casa Urbana",
    modelId: "MX-100",
    quantity: 30,
    date: "2026-01-09",
    status: "En producción",
    costs: { materials: 5400, labor: 2100, time: 900 },
  },
  {
    id: "PD-312",
    client: "Interior Lab",
    modelId: "LX-210",
    quantity: 20,
    date: "2026-01-10",
    status: "Pendiente",
    costs: { materials: 4800, labor: 1900, time: 750 },
  },
  {
    id: "PD-313",
    client: "Grupo Nexo",
    modelId: "QT-55",
    quantity: 14,
    date: "2026-01-11",
    status: "En producción",
    costs: { materials: 6200, labor: 2600, time: 1100 },
  },
  {
    id: "PD-314",
    client: "Arq. Nova",
    modelId: "VN-32",
    quantity: 45,
    date: "2026-01-12",
    status: "Listo para envío",
    costs: { materials: 4300, labor: 1600, time: 640 },
  },
  {
    id: "PD-315",
    client: "Casa Urbana",
    modelId: "LX-210",
    quantity: 12,
    date: "2026-01-13",
    status: "Pendiente",
    costs: { materials: 3100, labor: 1200, time: 420 },
  },
];

const filterStart = document.getElementById("filter-start");
const filterEnd = document.getElementById("filter-end");
const filterClient = document.getElementById("filter-client");
const filterModel = document.getElementById("filter-model");
const resetFilters = document.getElementById("reset-filters");

const metricStock = document.getElementById("metric-stock");
const metricProduction = document.getElementById("metric-production");
const metricOrders = document.getElementById("metric-orders");
const productionTable = document.getElementById("production-table");
const ordersTable = document.getElementById("orders-table");
const costTable = document.getElementById("cost-table");
const lastUpdated = document.getElementById("last-updated");

const totalMaterials = document.getElementById("total-materials");
const totalLabor = document.getElementById("total-labor");
const totalTime = document.getElementById("total-time");
const totalOverall = document.getElementById("total-overall");

const currencyFormatter = new Intl.NumberFormat("es-ES", {
  style: "currency",
  currency: "EUR",
  maximumFractionDigits: 0,
});

const dateFormatter = new Intl.DateTimeFormat("es-ES", {
  year: "numeric",
  month: "short",
  day: "2-digit",
});

const getModelName = (modelId) => models.find((model) => model.id === modelId)?.name ?? modelId;

const getFilters = () => ({
  start: filterStart.value ? new Date(`${filterStart.value}T00:00:00`) : null,
  end: filterEnd.value ? new Date(`${filterEnd.value}T23:59:59`) : null,
  client: filterClient.value,
  modelId: filterModel.value,
});

const isDateWithin = (dateString, { start, end }) => {
  const date = new Date(`${dateString}T12:00:00`);
  if (start && date < start) {
    return false;
  }
  if (end && date > end) {
    return false;
  }
  return true;
};

const applyFilters = () => {
  const filters = getFilters();

  const filteredOrders = orders.filter((order) => {
    if (filters.client !== "all" && order.client !== filters.client) {
      return false;
    }
    if (filters.modelId !== "all" && order.modelId !== filters.modelId) {
      return false;
    }
    return isDateWithin(order.date, filters);
  });

  const filteredProduction = production.filter((item) => {
    if (filters.modelId !== "all" && item.modelId !== filters.modelId) {
      return false;
    }
    return isDateWithin(item.startDate, filters);
  });

  const filteredStock = filters.modelId === "all"
    ? stock
    : stock.filter((item) => item.modelId === filters.modelId);

  return { filteredOrders, filteredProduction, filteredStock };
};

const updateMetrics = ({ filteredOrders, filteredProduction, filteredStock }) => {
  const stockTotal = filteredStock.reduce((sum, item) => sum + item.onHand - item.reserved, 0);
  const productionTotal = filteredProduction.reduce((sum, item) => sum + item.units, 0);
  const ordersTotal = filteredOrders.filter((order) => order.status !== "Entregado").length;

  metricStock.textContent = `${stockTotal}`;
  metricProduction.textContent = `${productionTotal}`;
  metricOrders.textContent = `${ordersTotal}`;
};

const updateProductionTable = (filteredProduction) => {
  productionTable.innerHTML = "";

  if (!filteredProduction.length) {
    productionTable.innerHTML =
      '<tr><td colspan="6" class="empty">No hay órdenes de producción con estos filtros.</td></tr>';
    return;
  }

  filteredProduction.forEach((item) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.id}</td>
      <td>${getModelName(item.modelId)}</td>
      <td>${item.stage}</td>
      <td>${item.units}</td>
      <td>${dateFormatter.format(new Date(`${item.startDate}T00:00:00`))}</td>
      <td>${dateFormatter.format(new Date(`${item.eta}T00:00:00`))}</td>
    `;
    productionTable.appendChild(row);
  });
};

const updateOrdersTable = (filteredOrders) => {
  ordersTable.innerHTML = "";

  if (!filteredOrders.length) {
    ordersTable.innerHTML =
      '<tr><td colspan="6" class="empty">No hay pedidos para los filtros seleccionados.</td></tr>';
    return;
  }

  filteredOrders.forEach((order) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${order.id}</td>
      <td>${order.client}</td>
      <td>${getModelName(order.modelId)}</td>
      <td>${order.quantity}</td>
      <td>${dateFormatter.format(new Date(`${order.date}T00:00:00`))}</td>
      <td>${order.status}</td>
    `;
    ordersTable.appendChild(row);
  });
};

const updateCostReport = (filteredOrders) => {
  const totalsByModel = models.map((model) => {
    const modelOrders = filteredOrders.filter((order) => order.modelId === model.id);
    const totals = modelOrders.reduce(
      (acc, order) => {
        acc.materials += order.costs.materials;
        acc.labor += order.costs.labor;
        acc.time += order.costs.time;
        return acc;
      },
      { materials: 0, labor: 0, time: 0 }
    );

    return {
      modelId: model.id,
      modelName: model.name,
      ...totals,
      total: totals.materials + totals.labor + totals.time,
    };
  });

  costTable.innerHTML = "";

  totalsByModel.forEach((item) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.modelName}</td>
      <td>${currencyFormatter.format(item.materials)}</td>
      <td>${currencyFormatter.format(item.labor)}</td>
      <td>${currencyFormatter.format(item.time)}</td>
      <td>${currencyFormatter.format(item.total)}</td>
    `;
    costTable.appendChild(row);
  });

  const totals = totalsByModel.reduce(
    (acc, item) => {
      acc.materials += item.materials;
      acc.labor += item.labor;
      acc.time += item.time;
      acc.total += item.total;
      return acc;
    },
    { materials: 0, labor: 0, time: 0, total: 0 }
  );

  totalMaterials.textContent = currencyFormatter.format(totals.materials);
  totalLabor.textContent = currencyFormatter.format(totals.labor);
  totalTime.textContent = currencyFormatter.format(totals.time);
  totalOverall.textContent = currencyFormatter.format(totals.total);
};

const updateTimestamp = () => {
  const now = new Date();
  lastUpdated.textContent = now.toLocaleTimeString("es-ES", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
};

const refreshDashboard = () => {
  const filteredData = applyFilters();
  updateMetrics(filteredData);
  updateProductionTable(filteredData.filteredProduction);
  updateOrdersTable(filteredData.filteredOrders);
  updateCostReport(filteredData.filteredOrders);
  updateTimestamp();
};

const seedFilters = () => {
  const clients = Array.from(new Set(orders.map((order) => order.client))).sort();

  filterClient.innerHTML = '<option value="all">Todos</option>';
  clients.forEach((client) => {
    const option = document.createElement("option");
    option.value = client;
    option.textContent = client;
    filterClient.appendChild(option);
  });

  filterModel.innerHTML = '<option value="all">Todos</option>';
  models.forEach((model) => {
    const option = document.createElement("option");
    option.value = model.id;
    option.textContent = model.name;
    filterModel.appendChild(option);
  });
};

const randomDelta = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

const simulateRealtimeUpdates = () => {
  production = production.map((item) => {
    if (Math.random() > 0.65) {
      const stages = ["Corte y ensamblaje", "Barnizado", "Tapizado", "Inspección final"];
      const nextStage = stages[(stages.indexOf(item.stage) + 1) % stages.length];
      return { ...item, stage: nextStage };
    }
    return item;
  });

  stock = stock.map((item) => {
    const adjustment = randomDelta(-8, 6);
    const onHand = Math.max(item.onHand + adjustment, 0);
    return { ...item, onHand };
  });

  orders = orders.map((order) => {
    if (order.status === "Pendiente" && Math.random() > 0.7) {
      return { ...order, status: "En producción" };
    }
    if (order.status === "En producción" && Math.random() > 0.8) {
      return { ...order, status: "Listo para envío" };
    }
    return order;
  });

  refreshDashboard();
};

filterStart.addEventListener("change", refreshDashboard);
filterEnd.addEventListener("change", refreshDashboard);
filterClient.addEventListener("change", refreshDashboard);
filterModel.addEventListener("change", refreshDashboard);

resetFilters.addEventListener("click", () => {
  filterStart.value = "";
  filterEnd.value = "";
  filterClient.value = "all";
  filterModel.value = "all";
  refreshDashboard();
});

seedFilters();
refreshDashboard();

setInterval(simulateRealtimeUpdates, 6000);
