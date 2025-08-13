import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client
import requests

# 1. Configuração de Logs
# Níveis de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 2. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# 3. Credenciais Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 4. Credenciais Z-API
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
# Nova variável de ambiente para o Client-Token da Z-API
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

# Verifica se todas as variáveis de ambiente estão configuradas
# Adicionamos ZAPI_CLIENT_TOKEN à verificação
if not all([SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE_ID, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN]):
    logging.error("Erro: Algumas variáveis de ambiente (SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE_ID, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN) não estão configuradas no arquivo .env")
    exit(1) # Sai do programa se as credenciais não estiverem configuradas

# Inicializa o cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_contacts_from_supabase():
    """
    Busca contatos na tabela 'contacts' do Supabase.
    Retorna uma lista de dicionários com 'name' e 'phone_number'.
    """
    logging.info("Buscando contatos no Supabase...")
    try:
        # Substitua 'contacts' pelo nome da sua tabela no Supabase
        response = supabase.from_('contacts').select('name, phone_number').execute()
        contacts = response.data
        if contacts:
            logging.info(f"Encontrados {len(contacts)} contatos.")
        else:
            logging.warning("Nenhum contato encontrado no Supabase.")
        return contacts
    except Exception as e:
        logging.error(f"Erro ao buscar contatos no Supabase: {e}")
        return []

def send_whatsapp_message(phone_number: str, contact_name: str):
    """
    Envia uma mensagem personalizada via Z-API para o número especificado.
    """
    message = f"Olá {contact_name}, tudo bem com você?"
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN # Adicionando o Client-Token no cabeçalho
    }
    
    payload = {
        "phone": phone_number,
        "message": message
    }
    
    logging.info(f"Tentando enviar mensagem para {phone_number} (Contato: {contact_name})...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Levanta um erro para status de erro HTTP
        
        response_data = response.json()
        if response_data.get("id"): # Verifica se a API retornou um ID de mensagem
            logging.info(f"Mensagem enviada com sucesso para {phone_number}. ID: {response_data.get('id')}")
        else:
            logging.warning(f"Mensagem para {phone_number} enviada, mas sem ID de confirmação claro: {response_data}")

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"Erro HTTP ao enviar para {phone_number}: {http_err} - Resposta: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Erro de conexão ao enviar para {phone_number}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Tempo esgotado ao enviar para {phone_number}: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Erro na requisição ao enviar para {phone_number}: {req_err}")
    except Exception as e:
        logging.error(f"Erro inesperado ao enviar mensagem para {phone_number}: {e}")

def main():
    """
    Função principal que orquestra a busca de contatos e o envio de mensagens.
    """
    contacts = get_contacts_from_supabase()

    if not contacts:
        logging.info("Nenhum contato para processar. Encerrando.")
        return

    # Limita o envio para no máximo 3 contatos, conforme a regra do desafio
    # Se você tiver mais de 3, ele pegará os 3 primeiros da lista
    contacts_to_send = contacts[:3] 
    
    logging.info(f"Iniciando envio de mensagens para {len(contacts_to_send)} contato(s)...")
    for contact in contacts_to_send:
        name = contact.get('name')
        phone = contact.get('phone_number')
        
        if name and phone:
            send_whatsapp_message(phone, name)
        else:
            logging.warning(f"Contato com dados incompletos encontrado e ignorado: {contact}")
            
    logging.info("Processo de envio de mensagens concluído.")

if __name__ == "__main__":
    main()