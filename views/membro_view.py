class MembroView:
    def mostrar_membro(self, membro):
        if membro:
            print(f"Nome: {membro.nome}")
            print(f"Tipo: {membro.tipo}")
            print(f"Pode votar: {'Sim' if membro.pode_votar() else 'Não'}")
            print(f"Pode registrar: {'Sim' if membro.pode_registrar() else 'Não'}")
        else:
            print("Membro não encontrado.")
    
    def listar_membros(self, membros):
        if not membros:
            print("Nenhum membro cadastrado.")
            return
        
        print("\n=== MEMBROS CADASTRADOS ===")
        for i, membro in enumerate(membros, 1):
            print(f"{i}. {membro.nome} ({membro.tipo})")
    
    def solicitar_dados_membro(self):
        print("\n--- CADASTRAR MEMBRO ---")
        nome = input("Nome: ")
        
        while True:
            tipo = input("Tipo (VOTADOR/REGISTRADOR): ").upper()
            if tipo in {"VOTADOR", "REGISTRADOR"}:
                break
            print("Tipo inválido. Digite VOTADOR ou REGISTRADOR.")
        
        return nome, tipo
    
    def solicitar_login(self):
        print("\n--- LOGIN ---")
        nome = input("Nome: ")
        return nome