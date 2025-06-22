class ArtistaView:
    def __init__(self):
        pass
    
    def mostrar_artista(self, artista):
        if artista:
            print(f"Nome: {artista.nome}")
            print(f"Idade: {artista.idade}")
            print(f"Nacionalidade: {artista.nacionalidade}")
            print(f"Filmes: {', '.join(artista.filmes_participados)}")
        else:
            print("Artista não encontrado.")
    
    def listar_artistas(self, artistas):
        if not artistas:
            print("Nenhum artista cadastrado.")
            return
        
        print("\n=== ARTISTAS CADASTRADOS ===")
        for i, artista in enumerate(artistas, 1):
            print(f"{i}. {artista.nome} - {artista.nacionalidade}")
    
    def solicitar_dados_artista(self):
        print("\n--- CADASTRAR ARTISTA ---")
        nome = input("Nome: ")
        try:
            idade = int(input("Idade: "))
        except ValueError:
            print("Idade deve ser um número.")
            return None
        
        filmes = input("Filmes participados (separados por vírgula): ").split(',')
        filmes = [f.strip() for f in filmes]
        nacionalidade = input("Nacionalidade: ")
        
        return nome, idade, filmes, nacionalidade