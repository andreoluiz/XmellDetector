import xml.etree.ElementTree as ET
import os
import re

def processar_xml(xml_file, txt_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        nome_metodo = root.attrib.get('name', 'Desconhecido')

        quantidade_prints = len(root.findall('.//print'))
        quantidade_emptys = len(root.findall('.//empty'))
        quantidade_asserts = len(root.findall('.//assertEquals'))  # Conta os asserts
        quantidade_literal = 0  # Inicializa contagem de literais

        # Checar os literais nos atributos de assertEquals
        for assert_elem in root.findall('.//assertEquals'):
            expected = assert_elem.attrib.get('expected', '')
            actual = assert_elem.attrib.get('actual', '')
            # Conta literais apenas se estiverem nos asserts
            quantidade_literal += count_literals_in_expression(expected) + count_literals_in_expression(actual)

        quantidade_exception = len(root.findall('.//try'))
        quantidade_if = len(root.findall('.//if'))
        quantidade_else = len(root.findall('.//else'))
        quantidade_loopFor = len(root.findall('.//LoopFor'))

        quantidade_condicionais = quantidade_if + quantidade_else + quantidade_loopFor

        with open(txt_file, 'a') as file:
            file.write(f"Método testado: {nome_metodo}\n")
            file.write(f"Quantidade de literais dentro de asserts: {quantidade_literal}\n")
            file.write(f"Quantidade de prints: {quantidade_prints}\n")
            file.write(f"Quantidade de empty: {quantidade_emptys}\n")
            file.write(f"Quantidade de asserts: {quantidade_asserts}\n")  # Adiciona contagem de asserts
            file.write(f"Quantidade de exceptions: {quantidade_exception}\n")
            file.write(f"Quantidade de condicionais (if, else, loopFor): {quantidade_condicionais}\n\n")
    except ET.ParseError as e:
        print(f"Erro ao analisar o arquivo XML: {xml_file}\nErro: {e}")

def count_literals_in_expression(expression):
    """Conta literais numéricos e de string em uma expressão."""
    literals_count = 0
    # Contar literais numéricos
    literals_count += len(re.findall(r'<literalNumber>(\d+)</literalNumber>', expression))
    # Contar literais de string
    literals_count += len(re.findall(r'<literalString>(.*?)</literalString>', expression))
    return literals_count

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
