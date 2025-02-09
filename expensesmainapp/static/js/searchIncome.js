const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");

tableOutput.style.display = "none";

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;
  tbody.innerHTML = "";

  if (searchValue.trim().length > 0) {
    fetch("/ income/search-income", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        appTable.style.display = "none";
        paginationContainer.style.display = "none";
        tableOutput.style.display = "block";
        if (data.length <= 0) {
          tableOutput.innerHTML = "No results found";
        } else {
          data.forEach((income) => {
            tbody.innerHTML += `<tr>
        <td>${income.amount}</td>
        <td>${income.source}</td>
        <td>${income.description}</td>
        <td>${income.date}</td>
        <td><a href="income-edit/${income.id}" class="btn btn-secondary">Edit</a></td>
      </tr>`;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
