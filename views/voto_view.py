class VotoView:
    def mostrar_voto(self, voto):
        if voto:
            indicado_nome = voto.indicado if isinstance(voto.indicado, str) else voto.indicado.nome
            print(f"Membro: {voto.membro.nome}")
            print(f"Categoria: {voto.categoria.nome}")
            print(f"Indicado: {indicado_nome}")
        else:
            print("Voto não encontrado.")
    
    def listar_votos(self, votos):
        if not votos:
            print("Nenhum voto registrado.")
            return
        
        print("\n=== VOTOS REGISTRADOS ===")
        for i, voto in enumerate(votos, 1):
            indicado_nome = voto.indicado if isinstance(voto.indicado, str) else voto.indicado.nome
            print(f"{i}. {voto.membro.nome} → {indicado_nome} ({voto.categoria.nome})")
    
    def solicitar_voto(self, categoria):
        print(f"\nIndicados para {categoria.nome}:")
        for i, indicado in enumerate(categoria.indicados, 1):
            if isinstance(indicado, str):
                nome = indicado
            elif hasattr(indicado, "nome"):
                nome = indicado.nome
            elif hasattr(indicado, "titulo"):
                nome = indicado.titulo
            else:
                nome = str(indicado)

            print(f"{i}. {nome}")        
        try:
            opcao = int(input("Escolha o número do indicado: ")) - 1
            return categoria.indicados[opcao]
        except (ValueError, IndexError):
            print("Opção inválida.")
            return None