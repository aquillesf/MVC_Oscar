class IndicacaoView:
    def mostrar_indicacao(self, indicacao):
        if indicacao:
            indicado_nome = indicacao.indicado if isinstance(indicacao.indicado, str) else indicacao.indicado.nome
            print(f"Categoria: {indicacao.categoria.nome}")
            print(f"Indicado: {indicado_nome}")
        else:
            print("Indicação não encontrada.")
    
    def listar_indicacoes(self, indicacoes):
        if not indicacoes:
            print("Nenhuma indicação cadastrada.")
            return
        
        print("\n=== INDICAÇÕES CADASTRADAS ===")
        for i, indicacao in enumerate(indicacoes, 1):
            indicado_nome = indicacao.indicado if isinstance(indicacao.indicado, str) else indicacao.indicado.nome
            print(f"{i}. {indicado_nome} - {indicacao.categoria.nome}")