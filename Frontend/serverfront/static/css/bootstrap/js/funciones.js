document.getElementById('get_file').onclick = function (){
    document.getElementById('my_file').click();
}

function cargarXML(event){
    archivo = event.target.files[0];
    var fr = new FileReader()

    fr.onload = function (event){
        var contenido_xml = event.target.result
        console.log(contenido_xml)
        area_entrada = document.getElementById('area_entrada')
        area_entrada.value = contenido_xml
   }
    fr.readAsText(archivo)
}