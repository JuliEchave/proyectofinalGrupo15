console.log(location.search); // lee los argumentos pasados a este formulario
var id = location.search.substr(4);
console.log(id);

const { createApp } = Vue;
createApp({
  data() {
    return {
      id: 0,
      modelo: "",
      talle: "",
      stock: 0,
      precio: 0,
      imagen: "",
      url: 'http://127.0.0.1:5000/remera/' + id,
    };
  },
  methods: {
    fetchData(url) {
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.id = data.id;
          this.modelo = data.modelo;
          this.talle = data.talle;
          this.stock = data.stock;
          this.precio = data.precio;
          this.imagen = data.imagen;
        })
        .catch(err => {
          console.error(err);
          this.error = true;
        });
    },
    modificar() {
      let remera = {
        modelo: this.modelo,
        talle: this.talle,
        stock: this.stock,
        precio: this.precio,
        imagen: this.imagen,
      };
      var options = {
        body: JSON.stringify(remera),
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        redirect: 'follow',
      };
      fetch(this.url, options)
        .then(() => {
          alert("Registro modificado");
          window.location.href = "./productos.html";
        })
        .catch(err => {
          console.error(err);
          alert("Error al Modificar");
        });
    },
  },
  created() {
    this.fetchData(this.url);
  },
}).mount('#app');
