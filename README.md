<div>
    <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
</div>

# 📌 ATENDIMENTO PAC

Projeto desenvolvido para atendimento no setor público PAC.


## 📖 Sumário
- [Sobre](#-sobre)
- [Estrutura do Projeto](#estrutura-do-projeto-)
- [Tecnologias](#-tecnologias)  
- [Pré-requisitos](#-pré-requisitos)  
- [Instalação](#-instalação)  
- [Licença](#-licença)  
- [Contribuidores](#contribuidores)



## 📋 Sobre
O projeto consiste em agilizar o atendimento do setor público PAC, gerando senhas aleatórias para cada guichê, organizando o atendimento ao cliente. 



## 📁 Estrutura do Projeto
```
PAC_ATENDIMENTO/
├── src/
│   ├── client/
│   ├── server/
├── .gitignore
├── .env.example
├── requirements.txt
└── README.md
```

## 🛠 Tecnologias
Principais tecnologias utilizadas no projeto:

- [Python](https://www.python.org/)  



## ⚙️ Pré-requisitos
Informe o que o usuário precisa ter instalado antes de rodar o projeto:

- [Git](https://git-scm.com/)  
- [Python 3+](https://www.python.org/) 
- [pip](https://pypi.org/project/pip/) 



## Passo a passo 🕹️
Para desenvolvedores:
```bash
# Verifique em qual branch está
git status

# Caso esteja em uma branch diferente, troque para a correta
git checkout nome_da_sua_branch

# Atualize o seu repositório local caso esteja diferente do repositório em nuvem (Github).
# Obs: git pull é comum usar se alguém mexeu na sua branch e subiu essas alterações no repositório em nuvem (Github). Logo, se ninguém alterou nada, não é necessário o comando e você continua seu trabalho de onde parou em sua branch.
git pull

# Commite a alteração do seu código
# Obs: O tipo do commit 1 e 2 é um padrão, esse mesmo padrão você pode encontrar no site https://dev.to/renatoadorno/padroes-de-commits-commit-patterns-41co. Cada commit deve ser claro, se caso você alterou muita coisa no código e não consegue deixar de forma concisa, utilize o commit do tipo 2.

# Commit somente título da mensagem
1 - git commit -m ":sparkles: feat: Funcionalidade gerar senha adicionada"

# Commit título e corpo da mensagem 
2 - git commit -m ":sparkles: feat: Funcionalidade gerar senha adicionada" -m "Refeito estilização totem; Adicionado funcionalidade gerenciar atendente; Configuração de arquivos de estilização"

# ATENÇÃO (git push)
# Somente use o comando caso já finalizou algo. Ex: botão de chamar senha, estilizar cabeçalho, funcionalidade de criar usuario, etc.
git push


```

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/MusgoNato/PAC_ATENDIMENTO.git

# Entre na pasta do projeto
cd PAC_ATENDIMENTO

# Crie um ambiente virtual em python
python -m venv venv

# Ative o ambiente virtual
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

## 📃 Licença
Distribuído sob licença `MIT`. Veja o arquivo `LICENCE` para mais detalhes

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
  <td align="center">
      <a href="https://github.com/Redeziim" title="Perfil Github">
        <img src="https://avatars.githubusercontent.com/u/126031325?v=4" width="100px;" alt="Foto do Augusto"/><br>
        <sub>
          <b>Arthur</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/augutso1" title="Perfil Github">
        <img src="https://avatars.githubusercontent.com/u/97047246?v=4" width="100px;" alt="Foto do Augusto"/><br>
        <sub>
          <b>Augusto do Rêgo Franke</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/cairesh" title="Perfil Github">
        <img src="https://avatars.githubusercontent.com/u/211517325?v=4" width="100px;" alt="Foto do Augusto"/><br>
        <sub>
          <b>Henrique</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/MusgoNato" title="Perfil Github">
        <img src="https://avatars.githubusercontent.com/u/131496781?v=4" width="100px;" alt="Foto do Hugo"/><br>
        <sub>
          <b>Hugo Josué Lema Das Neves</b>
        </sub>
      </a>
    </td>
  </tr>
</table>