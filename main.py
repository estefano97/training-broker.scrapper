import PyPDF2
termino_busqueda = "INDICADORES DE MERCADO ACCIONARIO"
termino_split = "Unitario Alto Bajo % miles de US$ % (veces) financiera"
url_pdf = "EneroScrap.pdf" pdf_item = open(url_pdf, "rb")

reader = PyPDF2.PdfReader(pdf_item)
is_finded = 0
print(reader._get_num_pages())
for x in range(0, reader._get_num_pages()):
    print("------------------------------------------------------------")
    print("vamos a la pagina: ", x)
    print("------------------------------------------------------------")
    
    if is_finded == 1:
        print("Finalizado!!")
        break
    else:
        page = reader._get_page(x)
        page_text = page.extract_text()
        if page_text.__contains__(termino_busqueda):
            print(page_text.split(termino_split))

if(is_finded == 0): print("No se encontro ni mergas!")