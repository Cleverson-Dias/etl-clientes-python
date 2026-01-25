# =========================
# IMPORTS
# =========================
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from google import genai


# =========================
# CONFIGURAÇÃO DO AMBIENTE
# =========================
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(" ERRO: A chave GOOGLE_API_KEY não foi encontrada no arquivo .env")

client = genai.Client(api_key=API_KEY)

print(" Chave de API carregada e cliente Gemini configurado!")


# =========================
# DADOS DOS CLIENTES
# =========================
clientes_dados = [
    {"ID": 1, "Nome": "Claudia Machado", "Status": "Ativo", "Score": 740},
    {"ID": 2, "Nome": "Jose Dias", "Status": "Inativo", "Score": 579},
    {"ID": 3, "Nome": "Mariana Silva", "Status": "Ativo", "Score": 925},
    {"ID": 4, "Nome": "Paulo Souza", "Status": "Ativo", "Score": 610},
    {"ID": 5, "Nome": "Renato Gonçalves", "Status": "Ativo", "Score": 530},
    {"ID": 6, "Nome": "Michele Pereira", "Status": "Ativo", "Score": 900},
    {"ID": 7, "Nome": "Marcella Ribeiro", "Status": "Ativo", "Score": 720},
    {"ID": 8, "Nome": "Guilherme Santos", "Status": "Ativo", "Score": 780},
    {"ID": 9, "Nome": "Paula Maia", "Status": "Inativo", "Score": 510},
    {"ID": 10, "Nome": "Joice Mendes", "Status": "Ativo", "Score": 890},
    {"ID": 11, "Nome": "Andreza Lima", "Status": "Ativo", "Score": 920},
]

df_clientes = pd.DataFrame(clientes_dados)

print("\nCLIENTES:")
print(df_clientes)


# =========================
# FILTROS DE NEGÓCIO
# =========================
df_ativos = df_clientes[df_clientes["Status"] == "Ativo"]

df_aprovados = df_ativos[df_ativos["Score"] >= 700]


# =========================
# API EXTERNA (VALIDAÇÃO)
# =========================
def buscar_clientes_via_api():
    url = "https://jsonplaceholder.typicode.com/users"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return [cliente["id"] for cliente in response.json()]
    except requests.RequestException:
        pass
    return []


ids_validos_api = buscar_clientes_via_api()

df_final = df_aprovados[df_aprovados["ID"].isin(ids_validos_api)]

print("\nCLIENTES VALIDADOS PELA API:")
print(df_final)


# =========================
# FUNÇÃO DE MARKETING (IA + FALLBACK)
# =========================
def gerar_marketing(nome, score):
    prompt = (
        f"Crie uma frase curta de marketing para {nome}. "
        f"Ele é cliente VIP com score {score}. "
        "Ofereça upgrade de cartão."
    )

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text.strip()

    except Exception:
        # Fallback automático (mantém o projeto funcional)
        return (
            f"{nome}, como cliente VIP com score {score}, "
            "você tem acesso a um upgrade exclusivo do seu cartão, "
            "com mais limite, benefícios e vantagens personalizadas."
        )


# =========================
# APLICAÇÃO DA CAMPANHA
# =========================
if not df_final.empty:
    df_final = df_final.copy()
    df_final["Campanha_IA"] = df_final.apply(
        lambda x: gerar_marketing(x["Nome"], x["Score"]),
        axis=1
    )

    print("\nCAMPANHA GERADA COM SUCESSO:")
    print(df_final[["Nome", "Campanha_IA"]])
else:
    print("\n Nenhum cliente válido para campanha.")

# =========================
# PARTE 3: LOAD (CARGA)
# =========================
if not df_final.empty:
    print("\nIniciando a carga dos dados (LOAD)...")
    
    # Opção A: Salvar em CSV (padrão para desenvolvedores)
    df_final.to_csv("campanha_marketing.csv", index=False, encoding="utf-8-sig")
    
    # Opção B: Salvar em Excel (padrão para negócios/Marketing)
    df_final.to_excel("campanha_marketing.xlsx", index=False)
    
    print(" Sucesso: Arquivos 'campanha_marketing.csv' e '.xlsx' gerados na pasta do projeto!")
else:
    print("\n Carga cancelada: Não há dados para salvar.")

