# Instruções

## Criação do aplicativo python no cPanel

## Versão do python
Somente coloque uma versão que você vai usar, de acordo com a versão que você usou no desenvolvimento local, se não for nenhuma das disponíveis, coloque a que se aproxima mais.

## Raiz do aplicativo
Coloque `public_html/nomesubdominio`, caso contrário ele vai criar 2 pastas, uma dentro de public que aponta para seu projeto em si e outra com o nome que você deu na raiz do aplicativo.

*Obs: Somente coloque isso se caso você quer criar um subdomínio dentro de um domínio principal*
- Ex: `https:dominio_principal.com.br/meu-site`, o `meu-site` seria seu site rodando a partir dali, como um subdomínio do domínio principal

## Arquivo de inicialização
Esse arquivo é a entrada da aplicação, é ele quem vai extrair o objeto da aplicação, ou seja, comumente pra configurar ele somente é necessário importar o objeto da aplicação, esse objeto está no arquivo que você inicializa as rotas com as `blueprints`, etc. Coloque o nome de `passenger_wsgi.py`, assim fica mais fácil configurar depois, pois o próprio cPanel cria esse arquivo pra você.

*Obs: Lembre-se que se voce deseja importar um arquivo, trate ele como um pacote, você deve criar na pasta onde esse arquivo está um `__init__.py` vazio, é ele quem determina que os arquivos daquela pasta são pacotes pra serem importados, dessa forma você consegue importar variáveis de dentro do arquivo para outros arquivos via `from teste import var1, var2`*

```bash
# Se sua aplicação está em um determinado diretório, importe ele junto da aplicação que contém o objeto
from app import application
```

O `application` é variável, ele varia de acordo com o que você coloca lá na criação do aplicativo python. Então se você colocou que o *Application Entry point* é `application`, você deve colocar na variável que recebe o objeto da sua aplicação `application` também. 

Ex:

- arquivo `app.py`
    ```bash
    # Primeiro voce faz a instanciacao do objeto da sua aplicação Flask na variavel app
    app = Flask(__name__)

    # Depois voce define o nome da variavel que vai receber o objeto da sua aplicação Flask. Evite fazer direto, ou seja application = Flask(__name__). Você pode querer fazer alguma coisa, como conexao com o banco antes do servidor chegar nessa aplicação, então é melhor evitar fazer de forma direta.
    application = app
    ```
- Lá no `passenger_wsgi.py`
    ```bash
    from app import application

    ```
*Atenção: O app.py está dentro da pasta `/app`, por isso a importação no `passenger_wsgi.py` é `from app`, ele importa a variavel que contém o objeto da aplicação em si*

## Permissões
Em host compartilhado, todas as pastas devem estar com permissão 0755 e o arquivo `.htaccess` também, demais arquivos devem estar com permissão 0644.

## .htaccess
Esse arquivo define como o servidor lê e executa alguns arquivos, depois de ter colocado as permissões de forma correta, você deve definir que todas as rotas dentro de um subdomínio começam a partir da sua `URI`, se você criou `/pac` como subdomínio, a partir dele devem vir as outras rotas. 

- Caso essa especificação dentro do arquivo não exista, coloque ela, trocando o nome pelo subdomínio que você criou
    ```bash
    # Define de onde vai iniciar seu site
    PassengerBaseURI "/pac"
    ```

## Pastas públicas
As pastas `/templates` `/static` devem estar publicas, ou seja, na raiz do subdomínio para que sejam carregadas corretamente.

## Variáveis de ambiente
Em desenvolvimento local você utiliza o `load_dotenv` para carregar as variáveis de ambiente dentro do arquivo `.env`. No servidor você não precisa fazer isso, declare todas as variáveis e seus valores na criação da aplicação python e exclua o arquivo `.env`. Após isso só precisa extrair essas variáveis com `getenv` do pacote `os`.

## Ambiente virtual
Quando você tentar instalar via python com pip no terminal os seus pacotes, não é necessário dar downgrade nas versões das bibliotecas que você utiliza. Lembre-se de não enviar o seu ambiente virtual, pois vai entrar em conflito com o caminho do seu computador.

Depois de criar a aplicação em python, vai aparecer um código com essa mensagem:
`Enter to the virtual environment. To enter to virtual environment, run the command`. Copie o código e vá no terminal do servidor, cole o código e já instale as dependências necessárias com:
```bash
pip install -r requirements.txt
```
Após isso você deve criar um ambiente virtual, pra isso rode o comando abaixo:
```bash
# Cria ambiente virtual
python3 -m ven ven

# Depois voce entra dentro
source venv/bin/activate

```

Dentro do ambiente virtual você novamente instala as dependências do arquivo `requirements.txt`

## Roteamento
Rotas são um problema, principalmente em subdomínios. Na aplicação python, no registro das rotas, defina o prefixo que elas terão, pois a partir disso o FLask e o servidor saberão de onde começar a servir essas rotas.
Ex:
```bash
app = Flask(__name__)

# Entrada da usa aplicação, o '/' inicial do seu subdominio
app.register_blueprint(welcome)

# Aqui você registra um prefixo pra rota, assim o servidor e o Flask sabem que depois da sua rota principal, que no caso é a '/', vem este prefixo '/login'.

# Dentro do arquivo de login, caso voce tenha outras rotas, voce define qualquer tipo de URI para a rota (login.route("/")), pois o prefixo vai continuar, seguindo a URI do seu subdomínio.
app.register_blueprint(login, url_prefix='/login')
```

## Log de erros
#### Log de erro da aplicação
Caso você tenha alguns erros ao tentar acessar alguma rota e retorne uma mensagem contendo `issue` alguma coisa. Vá ao log de erro que você definiu na criação da aplicação do python, já vai estar o caminho pra voce encontrar, é ele quem vai dizer se sua aplicação inicializou de forma correta
#### Log de erro do servidor
Se você tiver algum erro mais profundo que o log da aplicação não está cobrindo ou está vazio, vá ao log de erro do servidor, fica localizado na aba ferramentas dentro do cPanel.