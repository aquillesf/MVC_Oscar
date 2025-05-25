from models.sistemaoscar import SistemaOscar

class OscarConsoleUI:
    def __init__(self):
        self.sistema = SistemaOscar()
        self.membro_logado = None
    
    def mostrar_menu_principal(self):
        while True:
            print("\n=== SISTEMA DO OSCAR ===")
            print("1. Cadastrar-se")
            print("2. Login")
            print("3. Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                self.cadastrar_membro()
            elif opcao == "2":
                self.login()
            elif opcao == "3":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")
    
    def cadastrar_membro(self):
        print("\n--- CADASTRO DE MEMBRO ---")
        nome = input("Nome: ")
        
        while True:
            tipo = input("Tipo (VOTADOR/REGISTRADOR): ").upper()
            if tipo in {"VOTADOR", "REGISTRADOR"}:
                break
            print("Tipo inválido. Digite VOTADOR ou REGISTRADOR.")
        
        if self.sistema.cadastrar_membro(nome, tipo):
            print("Cadastro realizado com sucesso!")
        else:
            print("Erro ao cadastrar membro.")
    
    def login(self):
        print("\n--- LOGIN ---")
        nome = input("Nome: ")
        
        membro = self.sistema.login(nome)
        if membro:
            self.membro_logado = membro
            print(f"Bem-vindo, {membro.nome} ({membro.tipo})!")
            self.mostrar_menu_logado()
        else:
            print("Membro não encontrado.")
    
    def mostrar_menu_logado(self):
        while self.membro_logado:
            print("\n=== MENU PRINCIPAL ===")
            
            if self.membro_logado.pode_registrar():
                print("1. Adicionar Filme")
                print("2. Adicionar Ator/Atriz")
                print("3. Adicionar Indicação")
            
            if self.membro_logado.pode_votar():
                print("4. Votar em uma categoria")
            
            print("5. Gerar relatório")
            print("6. Logout")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1" and self.membro_logado.pode_registrar():
                self.adicionar_filme()
            elif opcao == "2" and self.membro_logado.pode_registrar():
                self.adicionar_ator()
            elif opcao == "3" and self.membro_logado.pode_registrar():
                self.adicionar_indicacao()
            elif opcao == "4" and self.membro_logado.pode_votar():
                self.votar_categoria()
            elif opcao == "5":
                self.gerar_relatorio()
            elif opcao == "6":
                self.membro_logado = None
                print("Logout realizado com sucesso.")
            else:
                print("Opção inválida ou não permitida para seu tipo de usuário.")
    
    def adicionar_filme(self):
        print("\n--- ADICIONAR FILME ---")
        titulo = input("Título: ")
        ano = input("Ano: ")
        genero = input("Gênero: ")
        diretor = input("Diretor: ")
        
        filme = self.sistema.adicionar_filme(titulo, ano, genero, diretor)
        print(f"Filme '{filme.titulo}' adicionado com sucesso!")
    
    def adicionar_ator(self):
        print("\n--- ADICIONAR ATOR/ATRIZ ---")
        nome = input("Nome: ")
        filmes = input("Filmes participados (separados por vírgula): ").split(',')
        filmes = [f.strip() for f in filmes]
        nacionalidade = input("Nacionalidade: ")
        
        while True:
            tipo = input("Tipo (protagonista/coadjuvante): ").lower()
            if tipo in {"protagonista", "coadjuvante"}:
                break
            print("Tipo inválido. Digite 'protagonista' ou 'coadjuvante'.")
        
        ator = self.sistema.adicionar_ator(nome, filmes, tipo, nacionalidade)
        print(f"Ator/Atriz '{ator.nome}' adicionado com sucesso!")
    
    def adicionar_indicacao(self):
        print("\n--- ADICIONAR INDICAÇÃO ---")
    
        print("\nCategorias disponíveis:")
        for i, cat in enumerate(self.sistema.categorias, 1):
            print(f"{i}. {cat.nome}")
        
        try:
            opcao = int(input("Escolha o número da categoria: ")) - 1
            categoria = self.sistema.categorias[opcao]
        except (ValueError, IndexError):
            print("Opção inválida.")
            return
        

        if "Filme" in categoria.nome:
            print("\nFilmes disponíveis:")
            for i, filme in enumerate(self.sistema.filmes, 1):
                print(f"{i}. {filme.titulo} ({filme.ano})")
            
            try:
                opcao = int(input("Escolha o número do filme: ")) - 1
                indicado = self.sistema.filmes[opcao].titulo
            except (ValueError, IndexError):
                print("Opção inválida.")
                return
        
        elif "Diretor" in categoria.nome:
            print("\nDiretores disponíveis:")
            for i, diretor in enumerate(self.sistema.diretores, 1):
                print(f"{i}. {diretor.nome}")
            
            try:
                opcao = int(input("Escolha o número do diretor: ")) - 1
                indicado = self.sistema.diretores[opcao].nome
            except (ValueError, IndexError):
                print("Opção inválida.")
                return
        
        else:  
            print("\nAtores/Atrizes disponíveis:")
            for i, ator in enumerate(self.sistema.atores, 1):
                print(f"{i}. {ator.nome} ({ator.tipo_ator})")
            
            try:
                opcao = int(input("Escolha o número do ator/atriz: ")) - 1
                indicado = self.sistema.atores[opcao].nome
            except (ValueError, IndexError):
                print("Opção inválida.")
                return
        
        if self.sistema.adicionar_indicacao(categoria.nome, indicado):
            print(f"Indicação adicionada com sucesso na categoria {categoria.nome}!")
        else:
            print("Erro ao adicionar indicação.")
    
    def votar_categoria(self):
        print("\n--- VOTAR EM CATEGORIA ---")
        
        print("\nCategorias disponíveis:")
        categorias_com_indicados = [
            cat for cat in self.sistema.categorias 
            if cat.indicados
        ]
        
        if not categorias_com_indicados:
            print("Nenhuma categoria com indicados disponível para votação.")
            return
        
        for i, cat in enumerate(categorias_com_indicados, 1):
            print(f"{i}. {cat.nome}")
        
        try:
            opcao = int(input("Escolha o número da categoria: ")) - 1
            categoria = categorias_com_indicados[opcao]
        except (ValueError, IndexError):
            print("Opção inválida.")
            return
        
        print(f"\nIndicados para {categoria.nome}:")
        for i, indicado in enumerate(categoria.indicados, 1):
            if isinstance(indicado, str):
                print(f"{i}. {indicado}")
            else:
                print(f"{i}. {indicado.nome}")
        
        try:
            opcao = int(input("Escolha o número do indicado: ")) - 1
            indicado = categoria.indicados[opcao]
        except (ValueError, IndexError):
            print("Opção inválida.")
            return
        
        if self.sistema.registrar_voto(self.membro_logado, categoria.nome, indicado):
            print("Voto registrado com sucesso!")
        else:
            print("Erro ao registrar voto. Você já votou nesta categoria?")
    
    def gerar_relatorio(self):
        relatorio = self.sistema.gerar_relatorio()
        print("\n" + relatorio)
        input("Pressione Enter para continuar...")
