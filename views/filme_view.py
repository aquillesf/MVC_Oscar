class FilmeView:
    def mostrar_filme(self, filme):
        if filme:
            print(f"Título: {filme.titulo}")
            print(f"Ano: {filme.ano}")
            print(f"Gênero: {filme.genero}")
            print(f"Diretor: {filme.diretor.nome}")
            if filme.descricao:
                print(f"Descrição: {filme.descricao}")
        else:
            print("Filme não encontrado.")
    
    def listar_filmes(self, filmes):
        if not filmes:
            print("Nenhum filme cadastrado.")
            return
        
        print("\n=== FILMES CADASTRADOS ===")
        for i, filme in enumerate(filmes, 1):
            print(f"{i}. {filme.titulo} ({filme.ano}) - {filme.diretor.nome}")
    
    def solicitar_dados_filme(self):
        print("\n--- CADASTRAR FILME ---")
        titulo = input("Título: ")
        ano = input("Ano: ")
        genero = input("Gênero: ")
        diretor = input("Diretor: ")
        descricao = input("Descrição (opcional): ")
        
        return titulo, ano, genero, diretor, descricao