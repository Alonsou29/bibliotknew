import pdfkit
import jinja2


# Función para generar reportes de prestamos
def generarPrestamo(numpres, cedula, nombre, idlibro, titulo, autor, fechapres, fechadev):

    # Diccionario para cambiar las {{variables}} por sus valores correspondientes
    context = {
        "numpres": numpres, 
        "cedula": cedula, 
        "nombre": nombre, 
        "idlibro": idlibro, 
        "titulo": titulo, 
        "autor": autor, 
        "fechapres": fechapres, 
        "fechadev": fechadev
    }

    # Carga la plantilla HTML
    templateLoader = jinja2.FileSystemLoader("./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("reportes/prestamo.html")

    # Reemplaza las {{variables}} usando el diccionario
    outpuText = template.render(context)

    #Hace que pdfkit detecte wkhtmltopdf
    path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" #reemplaza esto por el directorio que tengas, pero no quites la r al inicio
    config = pdfkit.configuration(wkhtmltopdf=path)

    # Indica el nombre que tendrá el archivo pdf
    outputPDF = "prestamo" + numpres + ".pdf"

    # Crea el pdf a partir del archivo html
    pdfkit.from_string(outpuText, outputPDF, configuration=config)

# Prueba de ejemplo
generarPrestamo("5234523", "123412", "Mariana Duqeu", "12345125", "librrrro", "alonsou", "12/123/12341", "1234/2345/23")
