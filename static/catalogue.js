async function loadProduits() {
  const res = await fetch("/api/produits");
  const data = await res.json();
  const container = document.getElementById("productGrid");
  container.innerHTML = "";
  data.forEach(p => {
    const div = document.createElement("div");
    div.className = "product";
    div.setAttribute("data-type", p.type.toLowerCase());
    div.setAttribute("data-name", p.name.toLowerCase());

    div.innerHTML = `
      <img src="${p.image}" alt="${p.name}">
      <h3>${p.name}</h3>
      <p>${p.description}</p>
      <button>Ajouter au panier</button>
    `;
    container.appendChild(div);
  });
}

function filterProducts() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const type = document.getElementById("typeFilter").value;
  const products = document.querySelectorAll(".product");

  products.forEach(product => {
    const name = product.getAttribute("data-name").toLowerCase();
    const productType = product.getAttribute("data-type");
    const matchesSearch = name.includes(input);
    const matchesType = type === "all" || productType === type;
    product.style.display = matchesSearch && matchesType ? "block" : "none";
  });
}

window.onload = loadProduits;
