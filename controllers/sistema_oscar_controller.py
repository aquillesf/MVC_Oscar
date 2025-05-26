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
        self.__membro_logado = None
    
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
    
    @property
    def membro_logado(self):
        return self.__membro_logado
    
    def cadastrar_membro(self, nome, tipo, senha):
        try:
            membro = self.__membro_controller.criar_membro(nome, tipo, senha)
            return True, f"Membro {nome} cadastrado com sucesso!"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro inesperado ao cadastrar membro: {str(e)}"

    
    def fazer_login(self, nome, senha):
        membro = self.__membro_controller.autenticar(nome, senha)
        if membro:
            self.__membro_logado = membro
            return True, f"Login realizado com sucesso! Bem-vindo, {nome}."
        return False, "Nome de usuário ou senha incorretos."
    
    def fazer_logout(self):
        if self.__membro_logado:
            nome = self.__membro_logado.nome
            self.__membro_logado = None
            return True, f"Logout realizado com sucesso! Até logo, {nome}."
        return False, "Nenhum usuário está logado."
    
    def alterar_senha(self, senha_atual, nova_senha):
        if not self.__membro_logado:
            return False, "Nenhum usuário está logado."
        
        sucesso = self.__membro_controller.alterar_senha_membro(
            self.__membro_logado.nome, senha_atual, nova_senha
        )
        
        if sucesso:
            return True, "Senha alterada com sucesso!"
        return False, "Senha atual incorreta."
    
    def verificar_autenticacao(self):
        return self.__membro_logado is not None
    
    def obter_permissoes_usuario(self):
        if not self.__membro_logado:
            return {'pode_votar': False, 'pode_registrar': False}
        
        return {
            'pode_votar': self.__membro_logado.pode_votar(),
            'pode_registrar': self.__membro_logado.pode_registrar(),
            'nome': self.__membro_logado.nome,
            'tipo': self.__membro_logado.tipo
        }
    
    def gerar_relatorio_completo(self):
        if not self.verificar_autenticacao():
            return "Acesso negado. Faça login primeiro."
        
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
                    if isinstance(indicado, str):
                        nome = indicado
                    elif hasattr(indicado, 'nome'):
                        nome = indicado.nome
                    elif hasattr(indicado, 'titulo'):
                        nome = indicado.titulo
                    else:
                        nome = "Desconhecido"
                    relatorio.append(f"    - {nome}")
            else:
                relatorio.append("  Nenhum indicado cadastrado")
        
        return "\n".join(relatorio)
    
    def gerar_relatorio_categoria(self, nome_categoria):
        if not self.verificar_autenticacao():
            return "Acesso negado. Faça login primeiro."
        
        categoria = self.__categoria_controller.buscar_categoria(nome_categoria)
        if not categoria:
            return "Categoria não encontrada."
        
        relatorio = []
        relatorio.append(f"=== RELATÓRIO DA CATEGORIA: {categoria.nome} ===\n")
        
        if not categoria.indicados:
            relatorio.append("Nenhum indicado cadastrado para esta categoria.")
            return "\n".join(relatorio)

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
                
                if isinstance(indicado, str):
                    nome_indicado = indicado
                elif hasattr(indicado, 'nome'):
                    nome_indicado = indicado.nome
                elif hasattr(indicado, 'titulo'):
                    nome_indicado = indicado.titulo
                else:
                    nome_indicado = "Desconhecido"

                relatorio.append(f"{i}º lugar: {nome_indicado}")
                relatorio.append(f"  Votos: {votos} ({porcentagem:.1f}%)")
                relatorio.append("")
        else:
            relatorio.append("Nenhum voto registrado ainda.")

        relatorio.append("--- TODOS OS INDICADOS ---")
        for i, indicado in enumerate(categoria.indicados, 1):
            if isinstance(indicado, str):
                nome = indicado
            elif hasattr(indicado, 'nome'):
                nome = indicado.nome
            elif hasattr(indicado, 'titulo'):
                nome = indicado.titulo
            else:
                nome = "Desconhecido"
            votos = contagem.get(nome, 0)
            relatorio.append(f"{i}. {nome} ({votos} votos)")
        
        return "\n".join(relatorio)
    
    def obter_estatisticas_membro(self, membro=None):
        if not self.verificar_autenticacao():
            return None
        
        if membro is None:
            membro = self.__membro_logado
        
        votos_membro = [v for v in self.__voto_controller.listar_votos() if v.membro == membro]
        
        estatisticas = {
            'total_votos': len(votos_membro),
            'categorias_votadas': [v.categoria.nome for v in votos_membro],
            'pode_votar': membro.pode_votar(),
            'pode_registrar': membro.pode_registrar()
        }
        
        return estatisticas
    
    def verificar_elegibilidade_voto(self, categoria):
        if not self.verificar_autenticacao():
            return False, "Usuário não está logado."
        
        membro = self.__membro_logado
        
        if not membro.pode_votar():
            return False, "Membro não tem permissão para votar."
        
        if not categoria.indicados:
            return False, "Categoria não possui indicados."

        votos_categoria = [v for v in self.__voto_controller.listar_votos() 
                          if v.membro == membro and v.categoria == categoria]
        
        if votos_categoria:
            return False, "Você já votou nesta categoria."
        
        return True, "Você pode votar nesta categoria."
    
    def obter_vencedores(self):
        if not self.verificar_autenticacao():
            return "Acesso negado. Faça login primeiro."
        
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
        """Reseta a votação (apenas para administradores)"""
        if not self.verificar_autenticacao():
            return False, "Acesso negado. Faça login primeiro."
        self.__voto_controller = VotoController(self.__categoria_controller)
        
        for categoria in self.__categoria_controller.listar_categorias():
            categoria._Categoria__votos = {}
        
        return True, "Votação resetada com sucesso."
    
    def validar_sistema(self):
        """Valida o sistema"""
        if not self.verificar_autenticacao():
            return ["Acesso negado. Faça login primeiro."]
        
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