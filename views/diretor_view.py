class DiretorView:
    def __init__(self):
        pass
    
    def mostrar_diretor(self, diretor):
        if diretor:
            print(f"Nome: {diretor.nome}")
            print(f"Idade: {diretor.idade}")
            print(f"Filmes dirigidos: {', '.join(diretor.filmes_dirigidos)}")
        else:
            print("Diretor não encontrado.")
    
    def listar_diretores(self, diretores):
        if not diretores:
            print("Nenhum diretor cadastrado.")
            return
        
        print("\n=== DIRETORES CADASTRADOS ===")
        for i, diretor in enumerate(diretores, 1):
            filmes_count = len(diretor.filmes_dirigidos)
            print(f"{i}. {diretor.nome} ({filmes_count} filmes)")
    
    def solicitar_dados_diretor(self):
        print("\n--- CADASTRAR DIRETOR ---")
        nome = input("Nome: ")
        try:
            idade = int(input("Idade: "))
        except ValueError:
            print("Idade deve ser um número.")
            return None
        
        filmes = input("Filmes dirigidos (separados por vírgula): ").split(',')
        filmes = [f.strip() for f in filmes if f.strip()]
        
        return nome, idade, filmes