function connectDB() {
    let data = {
        host: document.getElementById("host").value,
        port: document.getElementById("port").value,
        dbname: document.getElementById("dbname").value,
        user: document.getElementById("user").value,
        password: document.getElementById("password").value
    };

    fetch("/connect_db", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => {
          alert(data.status === "success" ? "Connected successfully!" : `Error: ${data.message}`);
      });
}

function startGeneration() {
    fetch("/start_generation", { method: "POST" })
        .then(response => response.json())
        .then(() => alert("Data generation started!"));
}

function stopGeneration() {
    fetch("/stop_generation", { method: "POST" })
        .then(response => response.json())
        .then(() => alert("Data generation stopped!"));
}

function fetchData() {
    fetch("/fetch_data")
        .then(response => response.json())
        .then(data => {
            let display = "<h3>Customers</h3>";
            data.customers.forEach(c => display += `<p><strong>${c[1]}</strong> - ${c[2]} - ${c[3]}</p>`);

            display += "<h3>Transactions</h3>";
            data.transactions.forEach(t => display += `<p>Customer ID: ${t[1]} - Amount: <strong>$${t[2]}</strong></p>`);

            display += "<h3>Orders</h3>";
            data.orders.forEach(o => display += `<p>Customer ID: ${o[1]} - Product: <strong>${o[2]}</strong> - Quantity: ${o[3]}</p>`);

            document.getElementById("data-display").innerHTML = display;
        });
}
