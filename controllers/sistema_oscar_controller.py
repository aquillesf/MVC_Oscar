# controllers/sistema_oscar_controller.py
from controllers.pessoa_controller import PessoaController
from controllers.artista_controller import ArtistaController
from controllers.diretor_controller import DiretorController
from controllers.ator_controller import AtorController
from controllers.filme_controller import FilmeController
from controllers.categoria_controller import CategoriaController
from controllers.membro_controller import MembroController
from controllers.voto_controller import VotoController
from controllers.indicacao_controller import IndicacaoController
class SistemaOscarController:
    def __init__(self):
        self.__pessoa_controller = PessoaController()
        self.__artista_controller = ArtistaController()
        self.__diretor_controller = DiretorController()
        self.__ator_controller = AtorController()
        self.__filme_controller = FilmeController(self.__diretor_controller)
        self.__categoria_controller = CategoriaController()
        self.__membro_controller = MembroController()
        self.__voto_controller = VotoController(self.__categoria_controller)
        self.__indicacao_controller = IndicacaoController(self.__categoria_controller)
    
    @property
    def pessoa_controller(self):
        return self.__pessoa_controller
    
    @property
    def artista_controller(self):
        return self.__artista_controller
    
    @property
    def diretor_controller(self):
        return self.__diretor_controller
    
    @property
    def ator_controller(self):
        return self.__ator_controller
    
    @property
    def filme_controller(self):
        return self.__filme_controller
    
    @property
    def categoria_controller(self):
        return self.__categoria_controller
    
    @property
    def membro_controller(self):
        return self.__membro_controller
    
    @property
    def voto_controller(self):
        return self.__voto_controller
    
    @property
    def indicacao_controller(self):
        return self.__indicacao_controller
    
    def gerar_relatorio_completo(self):
        """Gera um relatório completo do sistema"""
        relatorio = []
        relatorio.append("=== RELATÓRIO COMPLETO DO SISTEMA OSCAR ===\n")
        
        relatorio.append("--- ESTATÍSTICAS GERAIS ---")
        relatorio.append(f"Total de membros: {len(self.__membro_controller.listar_membros())}")
        relatorio.append(f"Total de filmes: {len(self.__filme_controller.listar_filmes())}")
        relatorio.append(f"Total de atores: {len(self.__ator_controller.listar_atores())}")
        relatorio.append(f"Total de diretores: {len(self.__diretor_controller.listar_diretores())}")
        relatorio.append(f"Total de categorias: {len(self.__categoria_controller.listar_categorias())}")
        relatorio.append(f"Total de indicações: {len(self.__indicacao_controller.listar_indicacoes())}")
        relatorio.append(f"Total de votos: {len(self.__voto_controller.listar_votos())}")
        relatorio.append("")
        
        relatorio.append("--- RESULTADOS POR CATEGORIA ---")
        for categoria in self.__categoria_controller.listar_categorias():
            relatorio.append(f"\n{categoria.nome}:")
            if categoria.indicados:
                contagem = self.__voto_controller.contar_votos_categoria(categoria)
                if contagem:
                    resultados = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
                    for i, (indicado, votos) in enumerate(resultados, 1):
                        relatorio.append(f"  {i}º lugar: {indicado} ({votos} votos)")
                else:
                    relatorio.append("  Nenhum voto registrado ainda")
                
                relatorio.append("  Indicados:")
                for indicado in categoria.indicados:
                    nome = indicado if isinstance(indicado, str) else indicado.nome
                    relatorio.append(f"    - {nome}")
            else:
                relatorio.append("  Nenhum indicado cadastrado")
        
        return "\n".join(relatorio)
    
    def gerar_relatorio_categoria(self, nome_categoria):
        """Gera relatório específico de uma categoria"""
        categoria = self.__categoria_controller.buscar_categoria(nome_categoria)
        if not categoria:
            return "Categoria não encontrada."
        
        relatorio = []
        relatorio.append(f"=== RELATÓRIO DA CATEGORIA: {categoria.nome} ===\n")
        
        if not categoria.indicados:
            relatorio.append("Nenhum indicado cadastrado para esta categoria.")
            return "\n".join(relatorio)
        
        # Contagem de votos
        contagem = self.__voto_controller.contar_votos_categoria(categoria)
        total_votos = sum(contagem.values())
        
        relatorio.append(f"Total de votos: {total_votos}")
        relatorio.append(f"Total de indicados: {len(categoria.indicados)}")
        relatorio.append("")
        
        if contagem:
            relatorio.append("--- RESULTADOS ---")
            resultados = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
            
            for i, (indicado, votos) in enumerate(resultados, 1):
                porcentagem = (votos / total_votos * 100) if total_votos > 0 else 0
                relatorio.append(f"{i}º lugar: {indicado}")
                relatorio.append(f"  Votos: {votos} ({porcentagem:.1f}%)")
                relatorio.append("")
        else:
            relatorio.append("Nenhum voto registrado ainda.")
        
        # Lista todos os indicados
        relatorio.append("--- TODOS OS INDICADOS ---")
        for i, indicado in enumerate(categoria.indicados, 1):
            nome = indicado if isinstance(indicado, str) else indicado.nome
            votos = contagem.get(nome, 0)
            relatorio.append(f"{i}. {nome} ({votos} votos)")
        
        return "\n".join(relatorio)
    
    def obter_estatisticas_membro(self, membro):
        """Retorna estatísticas de um membro específico"""
        votos_membro = [v for v in self.__voto_controller.listar_votos() if v.membro == membro]
        
        estatiscas = {
            'total_votos': len(votos_membro),
            'categorias_votadas': [v.categoria.nome for v in votos_membro],
            'pode_votar': membro.pode_votar(),
            'pode_registrar': membro.pode_registrar()
        }
        
        return estatiscas
    
    def verificar_elegibilidade_voto(self, membro, categoria):
        """Verifica se um membro pode votar em uma categoria específica"""
        if not membro.pode_votar():
            return False, "Membro não tem permissão para votar."
        
        if not categoria.indicados:
            return False, "Categoria não possui indicados."

        votos_categoria = [v for v in self.__voto_controller.listar_votos() 
                          if v.membro == membro and v.categoria == categoria]
        
        if votos_categoria:
            return False, "Membro já votou nesta categoria."
        
        return True, "Membro pode votar nesta categoria."
    
    def obter_vencedores(self):
        """Retorna os vencedores de cada categoria (quem tem mais votos)"""
        vencedores = {}
        
        for categoria in self.__categoria_controller.listar_categorias():
            if categoria.indicados:
                contagem = self.__voto_controller.contar_votos_categoria(categoria)
                if contagem:
                    vencedor = max(contagem.items(), key=lambda x: x[1])
                    vencedores[categoria.nome] = {
                        'indicado': vencedor[0],
                        'votos': vencedor[1]
                    }
        
        return vencedores
    
    def resetar_votacao(self):
        self.__voto_controller = VotoController(self.__categoria_controller)

        for categoria in self.__categoria_controller.listar_categorias():
            categoria._Categoria__votos = {}  
    
    def validar_sistema(self):
        problemas = []

        if not self.__membro_controller.listar_membros():
            problemas.append("Nenhum membro cadastrado no sistema.")
        votadores = self.__membro_controller.listar_por_tipo('VOTADOR')
        if not votadores:
            problemas.append("Nenhum membro votador cadastrado.")

        categorias_vazias = []
        for categoria in self.__categoria_controller.listar_categorias():
            if not categoria.indicados:
                categorias_vazias.append(categoria.nome)
        
        if categorias_vazias:
            problemas.append(f"Categorias sem indicados: {', '.join(categorias_vazias)}")
        
        return problemas if problemas else ["Sistema validado com sucesso!"]