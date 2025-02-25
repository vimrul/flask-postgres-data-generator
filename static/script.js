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
      .then(data => alert(data.status === "success" ? "Connected successfully!" : `Error: ${data.message}`));
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

// Fetch data every 2 seconds
function fetchData() {
    fetch("/fetch_data")
        .then(response => response.json())
        .then(data => {
            let customerHTML = "";
            data.customers.forEach(c => {
                customerHTML += `<tr><td>${c[1]}</td><td>${c[2]}</td><td>${c[3]}</td></tr>`;
            });

            let transactionHTML = "";
            data.transactions.forEach(t => {
                transactionHTML += `<tr><td>${t[0]}</td><td>${t[1]}</td><td>$${t[2]}</td></tr>`;
            });

            let orderHTML = "";
            data.orders.forEach(o => {
                orderHTML += `<tr><td>${o[0]}</td><td>${o[1]}</td><td>${o[2]}</td><td>${o[3]}</td></tr>`;
            });

            document.getElementById("customer-data").innerHTML = customerHTML;
            document.getElementById("transaction-data").innerHTML = transactionHTML;
            document.getElementById("order-data").innerHTML = orderHTML;
        });
}

// Auto-refresh data
setInterval(fetchData, 2000);
