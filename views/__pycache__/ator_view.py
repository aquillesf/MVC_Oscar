class AtorView:
    def mostrar_ator(self, ator):
        if ator:
            print(f"Nome: {ator.nome}")
            print(f"Idade: {ator.idade}")
            print(f"Nacionalidade: {ator.nacionalidade}")
            print(f"Tipo: {ator.tipo_ator}")
            print(f"Filmes: {', '.join(ator.filmes_participados)}")
        else:
            print("Ator não encontrado.")
    
    def listar_atores(self, atores):
        if not atores:
            print("Nenhum ator cadastrado.")
            return
        
        print("\n=== ATORES CADASTRADOS ===")
        for i, ator in enumerate(atores, 1):
            print(f"{i}. {ator.nome} ({ator.tipo_ator}) - {ator.nacionalidade}")
    
    def solicitar_dados_ator(self):
        print("\n--- CADASTRAR ATOR/ATRIZ ---")
        nome = input("Nome: ")
        try:
            idade = int(input("Idade: "))
        except ValueError:
            print("Idade deve ser um número.")
            return None
        
        filmes = input("Filmes participados (separados por vírgula): ").split(',')
        filmes = [f.strip() for f in filmes]
        nacionalidade = input("Nacionalidade: ")
        
        while True:
            tipo = input("Tipo (protagonista/coadjuvante): ").lower()
            if tipo in {"protagonista", "coadjuvante"}:
                break
            print("Tipo inválido. Digite 'protagonista' ou 'coadjuvante'.")
        
        return nome, idade, filmes, tipo, nacionalidade