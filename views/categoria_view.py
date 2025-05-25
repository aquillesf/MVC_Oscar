class CategoriaView:
    def mostrar_categoria(self, categoria):
        if categoria:
            print(f"Categoria: {categoria.nome}")
            print(f"Indicados: {len(categoria.indicados)}")
            for indicado in categoria.indicados:
                nome = indicado if isinstance(indicado, str) else indicado.nome
                print(f"- {nome}")
        else:
            print("Categoria não encontrada.")
    
    def listar_categorias(self, categorias):
        if not categorias:
            print("Nenhuma categoria cadastrada.")
            return
        
        print("\n=== CATEGORIAS DISPONÍVEIS ===")
        for i, categoria in enumerate(categorias, 1):
            print(f"{i}. {categoria.nome} ({len(categoria.indicados)} indicados)")
    
    def selecionar_categoria(self, categorias):
        self.listar_categorias(categorias)
        try:
            opcao = int(input("Escolha o número da categoria: ")) - 1
            return categorias[opcao]
        except (ValueError, IndexError):
            print("Opção inválida.")
            return None