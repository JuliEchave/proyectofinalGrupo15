const { createApp } = Vue
  createApp({
    data() {
      return {
        Remeras:[],
        url:'http://127.0.0.1:5000/remera', 
        error:false,
        cargando:true,
        /*atributos para el guardar los valores del formulario */
        id:0,
        modelo:"",
        talle:"",
        stock:0,
        precio:0, 
        imagen:"",
        
    }  
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.remera= data;
                    this.cargando=false
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },
        eliminar(remera) {
            const url = this.url+'/' + remera;
            var options = {
                method: 'DELETE',
            }
            fetch(url, options)
                .then(res => res.text()) // or res.json() text
                .then(res => {
                    location.reload();
                })
        },
        grabar(){
            let remera = {
                modelo:this.modelo,
                talle:this.talle,   
                stock: this.stock, 
                precio: this.precio,
                imagen:this.imagen
            }
            var options = {
                body:JSON.stringify(remera),
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            }
            fetch(this.url, options)
                .then(function () {
                    alert("Registro grabado")
                    window.location.href = "./productos.html";  
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Grabar")
                })      
        }
    },
    created() {
        this.fetchData(this.url)
    },
  }).mount('#app')