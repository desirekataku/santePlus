const form = document.getElementById("productForm");
const list = document.getElementById("productList");

async function fetchProduits() {
  const res = await fetch("/api/produits");
  const data = await res.json();
  list.innerHTML = "<h2>Produits enregistrés</h2>";
  data.forEach((p) => {
    const div = document.createElement("div");
    div.className = "product-item";
    div.innerHTML = `
      <strong>${p.name}</strong> - <span>${p.type}</span>
      <button onclick="deleteProduit(${p.id})">❌ Supprimer</button>
    `;
    list.appendChild(div);
  });
}

async function deleteProduit(id) {
  await fetch(`/api/produits/${id}`, { method: "DELETE" });
  fetchProduits();
}

form.addEventListener("submit", async function (e) {
  e.preventDefault();
  const produit = {
    name: name.value,
    type: type.value,
    description: description.value,
    image: image.value
  };
  await fetch("/api/produits", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(produit),
  });
  form.reset();
  fetchProduits();
});

fetchProduits();
