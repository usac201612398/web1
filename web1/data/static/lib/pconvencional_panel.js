
(function($){

  $(function(){
      var trClone3 = $('#tabla2 tr:eq(1)').clone();
      trClone3.find('td:eq(2)').remove();
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

    $.ajax({
            type: "POST",
            dataType: "json",
            data: {'array': JSON.stringify(datos)},
            url: "/app1/iniciar/pedido/"  // Colocar aqui la url, esta se genera con Django
    });
  });
  
  $('.add').on('click', function() {
    
    const table = document.getElementById("tabla2")
    if (localStorage.getItem("temporal1")==""){alert("Debe seleccionar primero un item.")}
    else {
    table.querySelector("tbody").innerHTML += `
    <tr>
        <td>${localStorage.getItem("temporal1")}</td>
        <td>${localStorage.getItem("temporal4")}</td>
        <td>${localStorage.getItem("temporal2")}</td>
        <td>${localStorage.getItem("temporal5")}</td>
        <td>${localStorage.getItem("temporal3")}</td>
        <td>${localStorage.getItem("temporal6")}</td>
        <td><button onclick='eliminar(this)'>x</button></td>
    </tr>`

    localStorage.setItem('temporal1', "");
    localStorage.setItem('temporal2', "");
    localStorage.setItem('temporal3', "");
    localStorage.setItem('temporal4', "");
    localStorage.setItem('temporal5', "");
    localStorage.setItem('temporal6', "");

  }
  });

})(jQuery)

function eliminar(Id) {

  let row = Id.parentNode.parentNode;
  let table = document.getElementById("tabla2"); 
  table.deleteRow(row.rowIndex);

};