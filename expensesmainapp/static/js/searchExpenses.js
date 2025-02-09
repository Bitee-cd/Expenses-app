const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
var buttons = document.querySelectorAll('.show-document-button');

console.log('this is right')
tableOutput.style.display = "none";

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;
  tbody.innerHTML = "";

  if (searchValue.trim().length > 0) {
    fetch("/search-expenses", {
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
          data.forEach((expense) => {
            tbody.innerHTML += `<tr>
        <td>${expense.amount}</td>
        <td>${expense.category}</td>
        <td>${expense.description}</td>
        <td>${expense.date}</td>
        <td><a href="expense-edit/${expense.id}" class="btn btn-secondary">Edit</a></td>
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

buttons.forEach(function(button) {
    button.addEventListener('click', function() {
    console.log("you are working")
        var documentUrl = this.getAttribute('data-url');
        var documentDisplay = document.getElementById('document-display');

        // Create an <iframe> element
        var iframe = document.createElement('iframe');
        iframe.src = documentUrl;
        iframe.width = '800';
        iframe.height = '600';

        // Clear any previous content in the documentDisplay div
        documentDisplay.innerHTML = '';

        // Append the <iframe> to the documentDisplay div
        documentDisplay.appendChild(iframe);
    });
});