
    class Excel{
        constructor(content){
            this.content = content
        }

        header(){
            return this.content[0]
        }

        rows(){
            return new RowCollection(this.content.slice(1, this.content.length)) 
        }

    }

    class RowCollection{

        constructor(rows){
            this.rows = rows
        }

        first(){
            return new Row(this.rows[0])
        }

        get(index){
            return new Row(this.rows[index])
        }

        count(){
            return this.rows.length
        }

    }

    class Row{
        constructor(row){
            this.row = row
        }

        getItemCod(){
            return this.row[0]
        }

        getCantidad(){
            return this.row[1]
        }

        getCCostoCod(){
            return this.row[2]
        }
    }

    class TablePrint{

        static print(tableId, excel){
            const table = document.getElementById(tableId)
            
            for (let index=0; index < excel.rows().count(); index++){
                const row = excel.rows().get(index);
                table.querySelector("tbody").innerHTML += `
                <tr>
                    <td>${row.getItemCod()}</td>
                    <td>${row.getCantidad()}</td>
                    <td>${row.getCCostoCod()}</td>
                </tr>`
            }
        }

        static print2(excel){

            
            var datos = []
//            var encabezado =[]
//            var select = document.getElementById("Rub"), //El <select>
//                value = select.value, //El valor seleccionado
//                text = select.options[select.selectedIndex].innerText;
            var bn = document.getElementById('excel-file').id
//            var origen = document.getElementById('id').value
//            encabezado.push(excel.header()[0])
//            encabezado.push(excel.header()[1])
//            encabezado.push(excel.header()[2])
//            encabezado.push('Rubro')
//            encabezado.push('Fecha')
//            encabezado.push('Origen')
//            datos.push(encabezado)
            for (let index=0; index < excel.rows().count(); index++){
                var filas = []
                const row = excel.rows().get(index)
                const getItem = row.getItemCod()
                const getCantidad= row.getCantidad()
                const getCCostoCod= row.getCCostoCod()
                filas.push(bn)
                filas.push(getItem)
                filas.push(getCantidad)
                filas.push(getCCostoCod)
//                filas.push(text)
//                filas.push(fecha)
//                filas.push(origen)
                datos.push(filas)

            }

            return datos
        }
    }

    var input = document.getElementById('excel-file')
    
    input.addEventListener('change', async function() {
        const content = await readXlsxFile(input.files[0])
        const excel = new Excel(content)
        $.ajax({
            type: "POST",
            dataType: "json",
            data: {'array': JSON.stringify( TablePrint.print2(excel))},
            url: "/app1/iniciar/pedido/masivo"  // Colocar aqui la url, esta se genera con Django
        }).then(
            function(response){
                array_sus = response.pedido;
                
                //localStorage.setItem('json_res', array_sus);
                const table = document.getElementById("tabla2")
                for (let index=0; index < array_sus.length; index++){
                    const row = array_sus[index];
                    table.querySelector("tbody").innerHTML += `
                    <tr>
                        <td>${row[0]}</td>
                        <td>${row[1]}</td>
                        <td>${row[2]}</td>
                        <td>${row[3]}</td>
                        <td>${row[4]}</td>
                        <td>${row[5]}</td>
                    </tr>`
                }
            }
        )
//        TablePrint.print('tabla2',excel) 

            $('.fin').on('click', function() {
                var grabar = []
                var select = document.getElementById("Rub"), //El <select>
                    value = select.value, //El valor seleccionado
                    text = select.options[select.selectedIndex].innerText;
                var bn_ = document.getElementById('enviar').id
                var origen = document.getElementById('id').value
                var fecha = document.getElementById('date').value
                
                //let array_sus = localStorage.getItem("json_res");
//            encabezado.push(excel.header()[0])
//            encabezado.push(excel.header()[1])
//            encabezado.push(excel.header()[2])
//            encabezado.push('Rubro')
//            encabezado.push('Fecha')
//            encabezado.push('Origen')
//            datos.push(encabezado)
                for (let index=0; index < array_sus.length; index++){
                    var filas = []
                    const row = array_sus[index];
                    filas.push(bn_)
                    filas.push(row[0])
                    filas.push(row[2])
                    filas.push(row[4])
                    filas.push(text)
                    filas.push(origen)
                    filas.push(fecha)
                    grabar.push(filas)
                }
                //localStorage.setItem('json_res', "");
                $.ajax({
                    type: "POST",
                    dataType: "json",
                    data: {'array': JSON.stringify(grabar)},
                    url: "/app1/iniciar/pedido/masivo"  // Colocar aqui la url, esta se genera con Django
                })

                alert("Se ha enviado la requisición");

        });
        
        
    });
    

    
    

    
    
    
