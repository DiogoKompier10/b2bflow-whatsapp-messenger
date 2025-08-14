# b2bflow WhatsApp Messenger

Este projeto consiste em um script Python que automatiza o envio de mensagens personalizadas via WhatsApp. Ele busca dados de contatos em um banco de dados Supabase e utiliza a Z-API para disparar as mensagens.

## Funcionalidades

*   Integração com Supabase: Busca contatos (nome e telefone) de uma tabela no seu projeto Supabase.
*   Envio de Mensagens Personalizadas: Utiliza a Z-API para enviar mensagens de WhatsApp, personalizando o texto com o nome do contato.
*   Configuração Segura: Todas as credenciais de API e banco de dados são gerenciadas através de variáveis de ambiente (`.env`).
*   Logging Detalhado: Fornece logs informativos sobre o processo de busca e envio de mensagens, facilitando o monitoramento e depuração.
*   Controle de Envio: Envia mensagens para até os 3 primeiros contatos encontrados no Supabase, conforme o requisito do desafio.

## Pré-requisitos

Antes de executar o script, certifique-se de ter o seguinte:

*   Python 3.x instalado.
*   pip (gerenciador de pacotes do Python).
*   Uma conta no Supabase com um projeto configurado.
*   Uma conta na Z-API com uma instância configurada e ativa.

## Instalação

Siga os passos abaixo para configurar o ambiente e instalar as dependências:

1.  Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```
    (Se você não está usando Git, apenas baixe os arquivos e navegue até a pasta do projeto.)

2.  Crie um ambiente virtual (recomendado):
    ```bash
    python -m venv venv
    ```

3.  Ative o ambiente virtual:
    *   Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  Instale as dependências:
    ```bash
    pip install python-dotenv supabase-py requests
    ```

## Configuração

Para que o script funcione corretamente, você precisará configurar suas credenciais em um arquivo `.env`.

1.  Crie um arquivo chamado `.env` na raiz do seu projeto (na mesma pasta onde está `main.py`).

2.  Adicione as seguintes variáveis ao arquivo `.env`, substituindo os valores pelos seus dados reais:

    ```dotenv
    # Supabase Credentials
    SUPABASE_URL="https://your-project-id.supabase.co"
    SUPABASE_KEY="your-anon-public-key-from-supabase"

    # Z-API Credentials
    ZAPI_INSTANCE_ID="YOUR_ZAPI_INSTANCE_ID"
    ZAPI_TOKEN="YOUR_ZAPI_INSTANCE_TOKEN"
    ZAPI_CLIENT_TOKEN="YOUR_ZAPI_GLOBAL_CLIENT_TOKEN"
    ```

    *   SUPABASE_URL e SUPABASE_KEY: Encontradas no painel do seu projeto Supabase, em `Settings` > `API`. Use a `anon public` key.
    *   ZAPI_INSTANCE_ID e ZAPI_TOKEN: Encontradas no painel da sua instância na Z-API.
    *   ZAPI_CLIENT_TOKEN: Esta é a chave de autenticação global da sua conta Z-API. Encontrada na sessão de segurança nas configurações da sua conta.

### Configuração do Supabase

Certifique-se de que sua tabela de `contacts` no Supabase tenha pelo menos as colunas `name` e `phone_number` (do tipo `text`).

Importante: Row Level Security (RLS)

O Supabase possui RLS ativado por padrão, o que pode impedir que seu script leia os dados. Você tem duas opções:

1.  Desativar RLS para a tabela `contacts`: (Mais fácil, mas menos seguro para produção). No painel do Supabase, vá em `Table Editor`, selecione sua tabela `contacts` e desative o RLS (o botão de `Row Level Security`).
2.  Criar uma política de leitura: (Recomendado para controle de segurança). No painel do Supabase, vá em `Authentication` > `Policies`. Para sua tabela `contacts`, crie uma nova política que permita `SELECT` para o `anon` role (ou `authenticated` se você for usar autenticação). Para permitir leitura de todas as linhas, a expressão pode ser `true`.

## Como Executar

Com as dependências instaladas e o arquivo `.env` configurado, você pode executar o script:

```bash
python main.py
