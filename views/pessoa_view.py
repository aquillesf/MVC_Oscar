class PessoaView:
    def __init__(self):
        pass
    
    def mostrar_pessoa(self, pessoa):
        if pessoa:
            print(f"Nome: {pessoa.nome}")
            print(f"Idade: {pessoa.idade}")
        else:
            print("Pessoa não encontrada.")
    
    def listar_pessoas(self, pessoas):
        if not pessoas:
            print("Nenhuma pessoa cadastrada.")
            return
        
        print("\n=== PESSOAS CADASTRADAS ===")
        for i, pessoa in enumerate(pessoas, 1):
            print(f"{i}. {pessoa.nome} ({pessoa.idade} anos)")
    
    def solicitar_dados_pessoa(self):
        print("\n--- CADASTRAR PESSOA ---")
        nome = input("Nome: ")
        try:
            idade = int(input("Idade: "))
            return nome, idade
        except ValueError:
            print("Idade deve ser um número.")
            return None 