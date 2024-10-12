import xml.etree.ElementTree as ET
import os

# Função para ler um arquivo XML, extrair o nome do método, e contar as tags <print>, <empty/>, <loop for condition>, <if>, <else>, <loopFor/>
def processar_xml(xml_file, txt_file):
    try:
        # Parse o XML
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Pegar o nome do método
        nome_metodo = root.attrib.get('name', 'Desconhecido')  # Atributo 'name'

        # Contar quantas tags <print> existem
        print_tags = root.findall('.//print')
        quantidade_prints = len(print_tags)

        # Contar quantas tags <empty/> existem
        empty_tags = root.findall('.//empty')
        quantidade_emptys = len(empty_tags)

        # Contar quantas tags <if>, <else>, e <loopFor/> existem
        if_tags = root.findall('.//if')
        else_tags = root.findall('.//else')
        loopFor_tags = root.findall('.//loopFor')

        # Soma total de condicionais
        quantidade_condicionais = len(if_tags) + len(else_tags) + len(loopFor_tags)

        # Escrever no arquivo de texto
        with open(txt_file, 'a') as file:  # 'a' para adicionar ao arquivo sem sobrescrever
            file.write(f"Método testado: {nome_metodo}\n")
            file.write(f"Quantidade de prints: {quantidade_prints}\n")
            file.write(f"Quantidade de empty: {quantidade_emptys}\n")
            file.write(f"Quantidade de condicionais (if, else, loopFor): {quantidade_condicionais}\n\n")
    except ET.ParseError:
        print(f"Erro ao analisar o arquivo XML: {xml_file}")

# Função para ler vários arquivos XML de uma pasta
def ler_arquivos_xml_da_pasta(pasta, txt_file):
    # Limpar ou criar o arquivo de saída
    with open(txt_file, 'w') as file:
        file.write("Resultados dos testes:\n\n")
    
    # Iterar sobre todos os arquivos XML da pasta
    for filename in os.listdir(pasta):
        if filename.endswith(".xml"):
            caminho_completo = os.path.join(pasta, filename)
            print(f"Lendo arquivo: {caminho_completo}")
            processar_xml(caminho_completo, txt_file)

# Defina o nome da pasta e do arquivo de saída
pasta_xml = r'C:\Users\nacla\Downloads\xmlTestGenerator-1.0\xmlTestGenerator-1.0\output_tests'
arquivo_txt_saida = 'saida.txt'

# Executar a função para processar todos os arquivos XML da pasta
ler_arquivos_xml_da_pasta(pasta_xml, arquivo_txt_saida)

print("Processamento concluído!")
