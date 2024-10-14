import xml.etree.ElementTree as ET
import os

def processar_xml(xml_file, txt_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        nome_metodo = root.attrib.get('name', 'Desconhecido')

        quantidade_prints = len(root.findall('.//print'))
        quantidade_emptys = len(root.findall('.//empty'))
        quantidade_literal = len(root.findall('.//literal'))
        quantidade_exception = len(root.findall('.//try'))
        quantidade_if = len(root.findall('.//if'))
        quantidade_else = len(root.findall('.//else'))
        quantidade_loopFor = len(root.findall('.//LoopFor'))

        quantidade_condicionais = quantidade_if + quantidade_else + quantidade_loopFor

        with open(txt_file, 'a') as file:
            file.write(f"Método testado: {nome_metodo}\n")
            file.write(f"Quantidade de literais: {quantidade_literal}\n")
            file.write(f"Quantidade de prints: {quantidade_prints}\n")
            file.write(f"Quantidade de empty: {quantidade_emptys}\n")
            file.write(f"Quantidade de exceptions: {quantidade_exception}\n")
            file.write(f"Quantidade de condicionais (if, else, loopFor): {quantidade_condicionais}\n\n")
    except ET.ParseError as e:
        print(f"Erro ao analisar o arquivo XML: {xml_file}\nErro: {e}")

def ler_arquivos_xml_da_pasta(pasta, txt_file):
    with open(txt_file, 'w') as file:
        file.write("Resultados dos testes:\n\n")
    
    for filename in os.listdir(pasta):
        if filename.endswith(".xml"):
            caminho_completo = os.path.join(pasta, filename)
            print(f"Lendo arquivo: {caminho_completo}")
            processar_xml(caminho_completo, txt_file)

pasta_xml = r'C:\Users\nacla\OneDrive\desktop\André\xmlTestGenerator\saida'
arquivo_txt_saida = 'saida.txt'

ler_arquivos_xml_da_pasta(pasta_xml, arquivo_txt_saida)

print("Processamento concluído!")
