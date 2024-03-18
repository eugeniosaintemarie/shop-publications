import requests
from bs4 import BeautifulSoup
import datetime
import pytz

color_reset = "\033[0m"
color_rojo = "\033[91m"
color_naranja = "\033[38;5;208m"
color_azul = "\033[94m"
color_celeste = "\033[96m"
color_amarillo = "\033[93m"
color_verde = "\033[92m"


def simular_publicacion_ficticia():
    nombre_publicacion = "Producto Ficticio"

    precio_actual = 100000
    precio_anterior = 200000

    return nombre_publicacion, precio_actual, precio_anterior


def obtener_nombre_y_precio(link):
    response = requests.get(link)

    if response.status_code != 200:
        print(color_rojo + f"No se pudo acceder al link {link}" + color_reset)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    class_id_nombre = "ui-pdp-title"
    nombre_element = soup.find(class_=class_id_nombre)

    precio_container = soup.find("div", class_="ui-pdp-price__second-line")
    if precio_container:
        class_id_precio = "andes-money-amount__fraction"
        precio_element = precio_container.find("span", class_=class_id_precio)
    else:
        precio_element = None

    if precio_element:
        precio_actual = precio_element.get_text().strip()
        nombre_publicacion = (
            nombre_element.get_text().strip()
            if nombre_element
            else color_rojo
            + f"Nombre de publicacion no encontrado {link}"
            + color_reset
        )
        return nombre_publicacion, precio_actual
    else:
        print(
            color_rojo
            + f"Precio de publicacion no encontrado {nombre_publicacion}"
            + color_reset
        )
        return None


def generar_html(resultados, enlaces):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Publicaciones-Precios</title>
        <link rel="icon" type="image/svg+xml" href="https://http2.mlstatic.com/frontend-assets/ml-web-navigation/ui-navigation/5.21.22/mercadolibre/favicon.svg">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Roboto', Arial, sans-serif; }
            .item { margin-bottom: 20px; }
            .nombre { font-weight: bold; color: black; text-decoration: none; }
            .precio { color: green; }
            .precio_anterior { color: red; }
            .actualizacion { font-size: 0.75em;}
            .actualizacion-small { font-size: 0.75em;}
        </style>
    </head>
    <body>
    """

    for index, resultado in enumerate(resultados, start=1):
        nombre_publicacion, precio_nuevo, precio_anterior = resultado
        nombre_publicacion = (
            (nombre_publicacion[:50] + "...")
            if len(nombre_publicacion) > 50
            else nombre_publicacion
        )
        nombre_publicacion_link = f'<a href="{enlaces[index-1]}" target="_blank" class="nombre">{nombre_publicacion}</a>'
        if precio_anterior:
            html_content += f"""
            <div class="item">
                <div class="nombre">{nombre_publicacion_link}</div>
                <div class="precio">Precio actual: ${precio_nuevo}</div>
                <div class="precio_anterior">Precio anterior: ${precio_anterior}</div>
            </div>
            """
        else:
            html_content += f"""
            <div class="item">
                <div class="nombre">{nombre_publicacion_link}</div>
                <div class="precio">Precio actual: ${precio_nuevo}</div>
            </div>
            """

    actualizacion = datetime.datetime.now(
        pytz.timezone("America/Argentina/Buenos_Aires")
    ).strftime("%Y/%m/%d %H:%M")
    html_content += f"""
    <div class="actualizacion-small">
        <br/><br/><br/>{actualizacion}
    </div>
    </body>
    </html>
    """

    return html_content


def main():
    mostrar_publicacion_ficticia = True

    if mostrar_publicacion_ficticia:
        publicacion_ficticia = simular_publicacion_ficticia()
    else:
        publicacion_ficticia = None

    with open("links.txt", "r") as file:
        enlaces = [line.strip() for line in file]

    precios_guardados = {}
    resultados = []

    if publicacion_ficticia:
        nombre_publicacion, precio_actual, precio_anterior = publicacion_ficticia
        enlace_ficticio = "https://google.com"
        resultados.append(
            (nombre_publicacion, precio_actual, precio_anterior, enlace_ficticio)
        )

    for enlace in enlaces:
        resultado_obtencion = obtener_nombre_y_precio(enlace)
        if resultado_obtencion:
            nombre_publicacion, precio_nuevo = resultado_obtencion
            nombre_publicacion = nombre_publicacion[:32] + "..."
            if enlace not in precios_guardados:
                precios_guardados[enlace] = {
                    "precio_actual": precio_nuevo,
                    "precio_anterior": None,
                }
                resultados.append((nombre_publicacion, precio_nuevo, None, enlace))
            elif precio_nuevo != precios_guardados[enlace]["precio_actual"]:
                precios_guardados[enlace]["precio_anterior"] = precios_guardados[
                    enlace
                ]["precio_actual"]
                precios_guardados[enlace]["precio_actual"] = precio_nuevo
                resultados.append(
                    (
                        nombre_publicacion,
                        precio_nuevo,
                        precios_guardados[enlace]["precio_anterior"],
                        enlace,
                    )
                )

    html_content = generar_html(resultados, enlaces)
    with open("index.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)


if __name__ == "__main__":
    main()
