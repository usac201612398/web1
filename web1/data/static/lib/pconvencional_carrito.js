(function($){
  $(function(){
      var trClone = $('#myTable tr:eq(1)').clone();
      trClone.find('td:eq(2)').remove();
      trClone.appendTo('#tabla2 tbody');
      var trClone2 = $('#myTable2 tr:eq(1)').clone();
      trClone2.find('td:eq(2)').remove();
      trClone2.appendTo('#tabla2 tbody');
  });

  $('.envio').on('click', function() {
    var data = $(this).closest("tr").find('input[type="number"]').val();
    
    if (data=="") {
      alert("Debe especificar primero la cantidad");
    } 
    else{
      var hermano=$(this).parent();
      localStorage.setItem('test1', hermano.siblings("td:eq(0)").text());
      localStorage.setItem('test2', hermano.siblings("td:eq(1)").text());
      localStorage.setItem('test3', hermano.siblings("td:eq(3)").text());
      localStorage.setItem('test4', data);
      this.parentNode.parentNode.style.backgroundColor="#f1f1f1";
      alert("Listo, ahora debe marcar el centro de costo.")
      
    }                                                
  });

  $('.envio2').on('click', function() {
    itemCod = localStorage.getItem("test1");
    if (itemCod=="") {
      alert("Alerta: Primero seleccione el item.")
    }
    else {
      var hermano1=$(this).parent();
      localStorage.setItem('test5', hermano1.siblings("td:eq(0)").text());
      localStorage.setItem('test6', hermano1.siblings("td:eq(1)").text());
      this.parentNode.parentNode.style.backgroundColor="#f1f1f1";
      alert("Listo, ahora debe confirmar el pedido.")
    }
                                                                       
  });

  $('.confirmar').on('click', function() {

    let itemCod = localStorage.getItem("test1");
    let cantidad = localStorage.getItem("test4");
    let centroCod = localStorage.getItem("test5");

    if (itemCod=="" || centroCod=="") { 

      alert("No especificó item ni centro de costo.")

    } else { 
      if (itemCod!="" && cantidad=="") { 

        alert("Cuidado: Primero se especifica cantidad y luego se marca el item.") 

      }else{ 
        var filas = []
        filas.push(itemCod)
        filas.push(cantidad)
        filas.push(centroCod)
        console.log(filas)
        
        $.ajax({
          type: "POST",
          dataType: "json",
          data: {'array': JSON.stringify(filas)},
          url: "/app1/iniciar/pedido/convencional"  // Colocar aqui la url, esta se genera con Django
      }).then(
        function(response){
            array_sus = response.pedido;
            localStorage.setItem('temporal1',array_sus[0]);
            localStorage.setItem('temporal2',array_sus[1]);
            localStorage.setItem('temporal3',array_sus[2]);
            localStorage.setItem('temporal4',array_sus[3]);
            localStorage.setItem('temporal5',array_sus[4]);
            localStorage.setItem('temporal6',array_sus[5]);
            alert("Se agregó pedido al carrito, ahora debe agregarlo al panel.");
            location.reload();
        }
        
    )

        localStorage.setItem('test1', "");
        localStorage.setItem('test2', ""); 
        localStorage.setItem('test3', ""); 
        localStorage.setItem('test4', "");  
        localStorage.setItem('test5', ""); 
        localStorage.setItem('test6', ""); 

      } 
      
    }
    
  });
  
})(jQuery)

var a = document.querySelectorAll("input");

for(var b in a){
  var c = a[b];
if(typeof c=="object"){
  c.onclick = function (){
     console.log(this.id);
  }
}
}

function myFunction() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function myFunction2() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput2");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function myFunction3() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput3");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable2");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function myFunction4() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput4");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable2");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

