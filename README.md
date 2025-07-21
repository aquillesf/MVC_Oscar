Este é um Projeto feito durante as aulas da matéria de Desenvolvimento de Sistemas Orientados a Objetos da UFSC (Universidade Federal de Santa Catarina).
Neste projeto, criei um sistema do 0 de votações usando Python, Tkinter e Pickle para persistência de dados.
O sistema é feito na arquitetura MVC (Model, View Controller) com camadas de exceção de erros e GUI.

## Como Iniciar:

⚙️ Pré-requisitos
Certifique-se de ter o Python 3.10+ instalado. Você pode verificar com:

```bash
python --version
```

📦 1. Instalar Dependências
Pode ser necessário instalar o Tkinter manualmente:

bash```
sudo apt-get install python3-tk
```
No Windows, geralmente o Tkinter já vem com a instalação padrão do Python.

🚀 2. Rodar o Projeto
Navegue até o diretório onde está as GUI's:

bash```
cd/views
```

e execute:

bash```
python main.py
```

🗂️ Estrutura do Projeto (Exemplo de Organização MVC)

/projeto/
│
├── controllers/
│   └── Os controles de dados da aplicação estão aqui
├── dados/
│   └── Aqui é onde estão guardados os dados da aplicação
├── exceptions/
│   └── Onde estão todas as exceções de erros
├── models/
│   └── Modelos das classes do projeto.
├── persistence/
│   └── Aqui está o tratamento de dados e o "save" enviado para a pasta "dados/".
├── views/
│   └── Interface do Usuário do projeto.
└── README.md

