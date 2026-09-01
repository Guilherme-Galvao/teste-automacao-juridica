import csv
import json
import urllib.request
import urllib.error

# Lista com 10 CNPJs reais e de teste (inclui CNPJs válidos, um inapto/inexistente e formato inválido)
LISTA_CNPJS = [
    "00000000000191",  # Banco do Brasil (Válido)
    "33000167000101",  # Petrobras (Válido)
    "60701190000104",  # Itaú Unibanco (Válido)
    "07526557000100",  # Ambev (Válido)
    "00360305000104",  # Caixa Econômica Federal (Válido)
    "33592510000154",  # Vale S.A. (Válido)
    "11111111111111",  # CNPJ Inexistente / Inválido na Receita
    "12345",           # Formato Inválido (menos dígitos)
    "02558157000162",  # Telefonica Brasil (Válido)
    "47960950000121"   # Magazine Luiza - (Válido)
]
NOME_ARQUIVO_SAIDA = "relatorio_due_diligence_cnpjs.csv"


def consultar_cnpj_brasil_api(cnpj_raw: str) -> dict:
    """
    Consulta dados cadastrais de empresas na Receita Federal via BrasilAPI.
    Aplica tratamento de erros para inconsistências de rede e CNPJs inválidos.
    """
    # Sanitize: Remove pontos, traços e barras
    cnpj_limpo = "".join(filter(str.isdigit, str(cnpj_raw)))

    # Validação de estrutura básica do CNPJ (deve ter 14 dígitos)
    if len(cnpj_limpo) != 14:
        return {
            "cnpj_informado": cnpj_raw,
            "razao_social": "N/A",
            "nome_fantasia": "N/A",
            "situacao_cadastral": "N/A",
            "uf": "N/A",
            "status_consulta": "ERRO: Formato de CNPJ inválido (deve conter 14 dígitos)"
        }

    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # Timeout para evitar bloqueios da aplicação
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                dados = json.loads(response.read().decode('utf-8'))
                
                return {
                    "cnpj_informado": cnpj_raw,
                    "razao_social": dados.get("razao_social", "N/A"),
                    "nome_fantasia": dados.get("nome_fantasia") or "NÃO INFORMADO",
                    "situacao_cadastral": dados.get("descricao_situacao_cadastral", "N/A"),
                    "uf": dados.get("uf", "N/A"),
                    "status_consulta": "SUCESSO"
                }

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {
                "cnpj_informado": cnpj_raw,
                "razao_social": "N/A",
                "nome_fantasia": "N/A",
                "situacao_cadastral": "N/A",
                "uf": "N/A",
                "status_consulta": "ERRO: CNPJ não encontrado na base da Receita Federal"
            }
        return {
            "cnpj_informado": cnpj_raw,
            "razao_social": "N/A",
            "nome_fantasia": "N/A",
            "situacao_cadastral": "N/A",
            "uf": "N/A",
            "status_consulta": f"ERRO HTTP: Código {e.code}"
        }
    except Exception as e:
        return {
            "cnpj_informado": cnpj_raw,
            "razao_social": "N/A",
            "nome_fantasia": "N/A",
            "situacao_cadastral": "N/A",
            "uf": "N/A",
            "status_consulta": f"ERRO DE CONEXÃO/SISTEMA: {str(e)}"
        }


def executar_automacao():
    resultados = []
    print("Iniciando auditoria cadastral de CNPJs...")

    for cnpj in LISTA_CNPJS:
        print(f"Consultando CNPJ: {cnpj}...")
        res = consultar_cnpj_brasil_api(cnpj)
        resultados.append(res)

    headers = [
        "cnpj_informado",
        "razao_social",
        "nome_fantasia",
        "situacao_cadastral",
        "uf",
        "status_consulta"
    ]

    with open(NOME_ARQUIVO_SAIDA, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=";")
        writer.writeheader()
        writer.writerows(resultados)

    print(f"\nRelatório de Due Diligence gerado com sucesso: {NOME_ARQUIVO_SAIDA}")


if __name__ == "__main__":
    executar_automacao()