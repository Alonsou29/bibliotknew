import matplotlib.pyplot as plt
import pdfkit
import jinja2

# Función para generar reportes de estadisticas
def generarReporteEst(ruta, fecha, users, clientes, libros, prestamos, librosPrestados):

    # Diccionario para cambiar las {{variables}} por sus valores correspondientes
    context = {
        "fecha": fecha,
        "users": users,
        "clientes": clientes,
        "libros": libros,
        "prestamos": prestamos,
        "librosPrestados": librosPrestados
    }

    # Carga la plantilla HTML
    templateLoader = jinja2.FileSystemLoader("./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("reportes/estadisticas.html")

    # Reemplaza las {{variables}} usando el diccionario
    outpuText = template.render(context)

    #Hace que pdfkit detecte wkhtmltopdf
    path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" #reemplaza esto por el directorio que tengas, pero no quites la r al inicio
    config = pdfkit.configuration(wkhtmltopdf=path)

    # Indica el nombre que tendrá el archivo pdf
    outputPDF = ruta + "Estadísticas" + fecha + ".pdf"

    options = {'enable-local-file-access': None}

    # Crea el pdf a partir del archivo html
    pdfkit.from_string(outpuText, outputPDF, configuration=config, options=options)


# Crea un png del grafico de barras
def guardarBarras(libro1, numero1, libro2, numero2, libro3, numero3):

    # Datos del grafico
    numLibros = [0, 0, 0]
    titulos = ["", "", ""]

    titulos[0] = libro1
    titulos[1] = libro2
    titulos[2] = libro3

    numLibros[0] = numero1
    numLibros[1] = numero2
    numLibros[2] = numero3

    # Cantidad de posiciones en el gráfico
    positions = range(len(numLibros))

    # Estilo del grafico
    plt.style.use("ggplot")

    # Grafico de barras
    plt.bar(positions, numLibros)

    # Remplaza los labels
    plt.xticks(positions, titulos)

    # Guarda el grafico como un png
    plt.savefig("reportes/barras.png")


# Crea un png del grafico de Dona
def guardarDona(aTiempo, tarde):

    # Datos del grafico
    labels = ["A tiempo", "Tarde"]
    datos = [0, 0]
    datos[0] = aTiempo
    datos[1] = tarde

    # Estilo del grafico
    plt.style.use("ggplot")

    # Grafico de pie (datos, titulos, porcentajes, donde comienza el primer angulo)
    plt.pie(x=datos, labels=labels, autopct="%.2f%%", startangle=90)

    # Mantiene una relacion 1:1 con respecto a la altura y la anchura del grafico
    plt.axis("equal")

    # Pone un circulo blanco para hacer el grafico una dona
    circle = plt.Circle(xy=(0,0), radius=.70, facecolor="white")
    plt.gca().add_artist(circle)

    # Guarda el grafico como un png
    plt.savefig("reportes/dona.png")



# Función para generar reportes de prestamos
def generarReportePres(ruta, numpres, cedula, nombre, idlibro, titulo, autor, fechapres, fechadev):

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

    outpuText = template.render(context)

    #Hace que pdfkit detecte wkhtmltopdf
    path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" #reemplaza esto por el directorio que tengas, pero no quites la r al inicio
    config = pdfkit.configuration(wkhtmltopdf=path)

    # Indica el nombre que tendrá el archivo pdf
    outputPDF = ruta + "Préstamo" + numpres + ".pdf"

    # Crea el pdf a partir del archivo html
    pdfkit.from_string(outpuText, outputPDF, configuration=config)

# Prueba de ejemplo
# generarReportePres("", "5234523", "123412", "Mariana Duqeu", "12345125", "librrrro", "alonsou", "12/123/12341", "1234/2345/23")
generarReporteEst("", "5-12-2020", "2342", "1234", "233", "1231", "12")

# Generamos png nuevos de los graficos
# guardarDona(dona1, dona2)
# guardarBarras("libro 1", 120, "libro 2", 80, "libro 2", 50)
