![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

# 📌 Sistema de Fila de Atendimento

Projeto desenvolvido para atendimento ao setor público PAC.


## 📖 Sumário
- [Sobre](#-sobre)
- [Estrutura do Projeto](#estrutura-do-projeto-)
- [Tecnologias](#-tecnologias)  
- [Pré-requisitos](#-pré-requisitos)  
- [Instalação](#-instalação)  
- [Licença](#-licença)  
- [Contribuidores](#contribuidores)



## 📋 Sobre
O projeto consiste em agilizar o atendimento do setor público PAC. Separado em 3 entidades:

#### Painel
O painel apresenta as senhas que estão aguardando serem chamadas, emitidas através da entidade `Totem`.

#### Totem
O totem emite senhas aleatórias, cada senha gerada é impressa pela impressora térmica plugada ao raspberry local. Em caso de sucesso, a informação de que a senha foi gerada é propagada nas outras entidades, apresentada no `Painel` e visualizada na página do `Atendente`.

#### Atendente
O atendente é responsável por gerenciar as senhas geradas através da entidade `Totem`, podendo chamar, cancelar e finalizar o atendimento. Ao escolher uma das opções, a informação é propagada para outros atendentes existentes e a entidade `Painel` para visualização da senha.

## 📁 Estrutura do Projeto
```
PAC_ATENDIMENTO/
├── app/
│   ├── database/
│   ├── models/
│   ├── routes/
├── static/
├── templates/
│   ├── atendente/
│   ├── painel/
│   ├── totem/
├── .gitignore
├── .env.example
├── .htaccess
├── LICENCE
├── passenger_wsgi.py
├── PROD.md
├── README.md
├── requirements.txt
```

## 🛠 Tecnologias
Principais tecnologias utilizadas no projeto:

- [Python](https://www.python.org/)  
- [Flask](https://flask.palletsprojects.com/en/stable/)



## ⚙️ Pré-requisitos
Informe o que o usuário precisa ter instalado antes de rodar o projeto:

- [Git](https://git-scm.com/)  
- [Python 3+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/) 
- [pip](https://pypi.org/project/pip/) 

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
        <img src="https://avatars.githubusercontent.com/u/126031325?v=4" width="100px;" alt="Foto do Arthur"/><br>
        <sub>
          <b>Arthur</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/cairesh" title="Perfil Github">
        <img src="https://avatars.githubusercontent.com/u/211517325?v=4" width="100px;" alt="Foto do Henrique"/><br>
        <sub>
          <b>Henrique</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/MusgoNato" title="Perfil Github">
        <img src="https://avatars.githubusercontent.com/u/131496781?v=4" width="100px;" alt="Foto do Hugo"/><br>
        <sub>
          <b>Hugo Josue Lema Das Neves</b>
        </sub>
      </a>
    </td>
  </tr>
</table>