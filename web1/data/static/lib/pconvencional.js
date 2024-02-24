
(function($){
  $(function(){
      var trClone = $('#myTable tr:eq(1)').clone();
      trClone.find('td:eq(2)').remove();
      trClone.appendTo('#tabla2 tbody');
      var trClone2 = $('#myTable2 tr:eq(1)').clone();
      trClone2.find('td:eq(2)').remove();
      trClone2.appendTo('#tabla2 tbody');
      var trClone3 = $('#tabla2 tr:eq(1)').clone();
      trClone3.find('td:eq(2)').remove();
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
      $(this).closest("tr").find('input[type="number"]').val('');
      alert("Listo, ahora debe marcar el centro de costo.")
      
      
    }
//    $("#tabla2").append("<tr>\
//                        <td>"+hermano.siblings("td:eq(0)").text()+"</td>\
//                        <td>"+hermano.siblings("td:eq(1)").text()+"</td>\
//                        <td>"+data+"</td>\
//                        <td>"+hermano.siblings("td:eq(2)").text()+"</td>\
//                                        </tr>")                                                      
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
      alert("Listo, ahora debe agregar el pedido al carrito.")
    }
    
//    $("#tabla2").append("\
//                        <td>"+hermano.siblings("td:eq(0)").text()+"</td>\
//                        <td>"+hermano.siblings("td:eq(1)").text()+"</td>\
//                                        </tr>")                                                                                       
  });

  $('.completar').on('click', function() {

    let itemCod = localStorage.getItem("test1");
    let itemName = localStorage.getItem("test2");
    let cantidad = localStorage.getItem("test4");
    let dimensiones = localStorage.getItem("test3");
    let centroCod = localStorage.getItem("test5");
    let centroName = localStorage.getItem("test6");

    if (itemCod=="" || centroCod=="") { 

      alert("Listo, ahora debe especificar item y centro de costo.")

    } else { 
      if (itemCod!="" && cantidad=="") { 

        alert("Cuidado: Primero se especifica cantidad y luego se marca el item.") 

      }else{ 
        $("#tabla2").append("<tr>\
                        <td>"+itemCod+"</td>\
                        <td>"+itemName+"</td>\
                        <td>"+cantidad+"</td>\
                        <td>"+dimensiones+"</td>\
                        <td>"+centroCod+"</td>\
                        <td>"+centroName+"</td>\
                        <td><button onclick='eliminar(this)'>x</button></td>\
                                        </tr>")   

        localStorage.setItem('test1', "");
        localStorage.setItem('test2', ""); 
        localStorage.setItem('test3', ""); 
        localStorage.setItem('test4', "");  
        localStorage.setItem('test5', ""); 
        localStorage.setItem('test6', ""); 
      } 
      
    }
    
  });
  $('.envio3').on('click', function() {
    var resume_table = document.getElementById("tabla2");
    var datos = []
    for (var i = 0, row; row = resume_table.rows[i]; i++) {
      //alert(cell[i].innerText);
      filas = []
      for (var j = 0, col; col = row.cells[j]; j++) {
        //alert(col[j].innerText);
        filas.push(col.innerText);
      }
      if (i==0) {
        filas.push("Rubro");
        filas.push("Fecha");
        filas.push("Origen");
      } 
      else {
        var select = document.getElementById("Rub"), //El <select>
          value = select.value, //El valor seleccionado
          text = select.options[select.selectedIndex].innerText;
        filas.push(text);
        var fecha = document.getElementById('date').value;
        var origen = document.getElementById('id').value;
        
        filas.push(fecha);
        filas.push(origen);
        
      }
      datos.push(filas);
    }
    console.log(datos)

    $.ajax({
            type: "POST",
            dataType: "json",
            data: {'array': JSON.stringify(datos)},
            url: "/app1/iniciar/pedido/"  // Colocar aqui la url, esta se genera con Django
    });
  });

})(jQuery)

function eliminar(Id) {

  let row = Id.parentNode.parentNode;
  let table = document.getElementById("tabla2"); 
  table.deleteRow(row.rowIndex);

};

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

function myFunction5() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput5");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[4];
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

function myFunction6() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput6");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[5];
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

