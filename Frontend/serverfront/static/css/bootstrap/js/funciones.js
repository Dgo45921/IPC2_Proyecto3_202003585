document.getElementById('get_file').onclick = function (){
    document.getElementById('my_file').click();
}
// para generar el pdf del rango de fechas
document.getElementById('reporte_rango').onclick = function (){
    document.getElementById('boton_rango').click();
}


function cargarXML(event){
    archivo = event.target.files[0];
    var fr = new FileReader()

    fr.onload = function (event){
        var contenido_xml = event.target.result
        console.log(contenido_xml)
        area_entrada = document.getElementById('input')
        area_entrada.value = contenido_xml
   }
    fr.readAsText(archivo)
}

function genera_pdf_rango_fechas(){
 var ctxbar = document.getElementById("grafica")
    let imgcanvas = ctxbar.toDataURL("image/png", 1.0);


    var doc = new jsPDF('landscape')
    doc.text("REPORTE RANGO FECHAS", 120, 20)
    doc.addImage(imgcanvas, 'JPEG', 20, 25, 250, 180)

    doc.save("Reporte_rango_fechas")

}

function genera_pdf_fecha(){
    console.log("hola")
 var ctxbar = document.getElementById("grafica")
    let imgcanvas = ctxbar.toDataURL("image/png", 1.0);


    var doc = new jsPDF('landscape')
    doc.text("REPORTE CLASIFICACION POR FECHA", 120, 20)
    doc.addImage(imgcanvas, 'JPEG', 20, 25, 250, 180)

    doc.save("Reporte_fecha")

}