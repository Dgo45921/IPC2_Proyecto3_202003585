document.getElementById('get_file').onclick = function (){
    document.getElementById('my_file').click();
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
 var ctxbar = document.getElementById("grafica")
    let imgcanvas = ctxbar.toDataURL("image/png", 1.0);


    var doc = new jsPDF('landscape')
    doc.text("REPORTE CLASIFICACION POR FECHA", 90, 20)
    doc.addImage(imgcanvas, 'JPEG', 20, 25, 250, 180)

    doc.save("Reporte_fecha")

}

function genera_pdf_entrada_salida(){
    var input = document.getElementById('input').value
    var output = document.getElementById('area_salida').value
    var doc = new jsPDF('p', 'mm', [700, 8000]);
    doc.text("TEXTO ENTRADA", 80, 10)
    doc.setFontSize(10);
    doc.text(input,0,20)
    doc.setFontSize(1);

    doc.addPage();
    doc.setFontSize(10);
    doc.text("TEXTO SALIDA", 80, 10)
    doc.setFontSize(10);
    doc.text(output,0,30)
    doc.setFontSize(1);
    doc.save("Reporte_entrada_salida")
}


function genera_pdf_entrada_salida_prueba(){
    var input = document.getElementById('input').value
    var output = document.getElementById('area_salida').value
    var doc = new jsPDF('p', 'mm', [700, 1000]);
    doc.text("TEXTO ENTRADA", 80, 10)
    doc.setFontSize(10);
    doc.text(input,0,20)
    doc.setFontSize(1);

    doc.addPage();
    doc.setFontSize(10);
    doc.text("TEXTO SALIDA", 80, 10)
    doc.setFontSize(10);
    doc.text(output,0,30)
    doc.setFontSize(1);
    doc.save("Reporte_entrada_salida")
}

function abrir_pdf(){
    window.open("https://drive.google.com/file/d/1sx95lW6Fx49RByT55N7ByBET7LeXcUjc/view?usp=sharing")
}