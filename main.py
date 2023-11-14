import PyPDF2
import re
import requests
from datetime import datetime, timedelta

def _get_value_precio_teorico(list):
    for x in list:
        if(x.__contains__("Precio Teórico")):
            return x
            break

def dividir_cadena_empresa(cadena):
    # Utilizar una expresión regular para dividir la cadena
    matches = re.match(r'([^0-9]+)(.*)', cadena)

    if matches:
        # El primer grupo capturado es el nombre de la empresa
        # El segundo grupo capturado son los demás campos
        return [matches.group(1).strip()] + matches.group(2).split()
    else:
        # Si no se encuentra ningún número, devolver la cadena completa como nombre de la empresa
        return [cadena.strip()]

def obtener_siguiente_dia(fecha_texto):
    # Convertir la fecha de texto a objeto datetime
    fecha = datetime.strptime(fecha_texto, '%d%B%y')

    # Calcular la fecha del día siguiente
    siguiente_dia = fecha + timedelta(days=1)

    # Formatear la fecha del día siguiente como texto
    siguiente_dia_texto = siguiente_dia.strftime('%d%B%y')

    return siguiente_dia_texto

fecha_anterior = "13Enero11"
while True:
    print("La fecha a consultar es: ", fecha_anterior)
    items_finish_list = []
    is_finded = 0
    termino_busqueda = "INDICADORESDEMERCADOACCIONARIO"
    termino_split = "Unitario Alto Bajo % miles de US$ % (veces) financiera"
    pdf_name = fecha_anterior  + ".pdf"
    url_pdf = "http://www.bolsadevaloresguayaquil.com/boletines/alcierre/" + pdf_name

    response = requests.get(url_pdf, verify=False)

    if response.status_code != 200:
        print("No se encontro el archivo!")

    else:
        with open(pdf_name, 'wb') as pdf_file:
            pdf_file.write(response.content)

        reader = PyPDF2.PdfReader(pdf_name)
        print(reader._get_num_pages())

        for x in range(0, reader._get_num_pages()):
            # print("------------------------------------------------------------")
            # print("vamos a la pagina: ", x)
            # print("------------------------------------------------------------")
            if is_finded == 1:
                print("Encontrado!!")
                temp_industria = ""
                resultado_termino_busqueda = page_text.split(termino_split)[1]
                precio_teorico_val = _get_value_precio_teorico(resultado_termino_busqueda.split("\n"))
                split_de_items = resultado_termino_busqueda.split(precio_teorico_val)[0].split("\n")
                for z in split_de_items:
                    item = dividir_cadena_empresa(z)
                    if len(item) == 1:
                        if len(item[0]) == 0:
                            print("Espacio vacio")
                        else:
                            print("Titulo: ", item[0])
                            temp_industria = item[0]
                    else:
                        print("Item: ", item)
                        items_finish_list.append({
                            "emisor": item[0],
                            "valorNominalUnitario": item[1],
                            "precioUltimasSemanasAlto": item[2],
                            "precioUltimasSemanasBajo": item[3],
                            "ultimoPrecio": item[4],
                            "precioUnitarioVeces": item[5],
                            "dPYield": item[6],
                            "valorCapMilesUSD": item[7],
                            "pVL": item[8],
                            "presenciaBursatil": item[9],
                            "indiceRotacion": item[10],
                            "actualizacionDeInfoFinanciera": item[11],
                            "industria": temp_industria,
                            "fecha": pdf_name.split(".")[0]
                        })
                break
            else:
                page = reader._get_page(x)
                page_text = page.extract_text()
                # print(page_text)
                if page_text.replace(" ", "").__contains__(termino_busqueda.replace(" ", "")):
                    is_finded = 1

        print(items_finish_list)

    pdf_name = obtener_siguiente_dia(fecha_anterior)