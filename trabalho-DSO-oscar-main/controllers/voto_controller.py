from models.voto import Voto
from persistence.voto_dao import VotoDAO

class VotoController:
    
    def __init__(self, categoria_controller):
        self.__dao = VotoDAO()
        self.__votos_cache = {} 
        self.__categoria_controller = categoria_controller
        self.__carregar_cache()
    
    def __carregar_cache(self):
        for voto in self.__dao.listar():
            chave = (voto.membro.nome.lower(), voto.categoria.nome.lower())
            self.__votos_cache[chave] = voto
    
    def registrar_voto(self, membro, nome_categoria, indicado):
        if not membro.pode_votar():
            return False
        
        categoria = self.__categoria_controller.buscar_categoria(nome_categoria)
        if not categoria:
            return False
        
        if indicado not in categoria.indicados:
            return False
        
        chave = (membro.nome.lower(), categoria.nome.lower())
        if chave in self.__votos_cache:
            return False
        
        voto = Voto(membro, categoria, indicado)
        self.__dao.adicionar(voto)
        self.__votos_cache[chave] = voto
        categoria.registrar_voto(indicado, membro)
        return True
    
    def listar_votos(self):
        return self.__dao.listar()
    
    def contar_votos_categoria(self, categoria):
        votos_categoria = []
        for (membro_nome, cat_nome), voto in self.__votos_cache.items():
            if cat_nome == categoria.nome.lower():
                votos_categoria.append(voto)
        
        contagem = {}
        for voto in votos_categoria:
            if isinstance(voto.indicado, str):
                indicado_nome = voto.indicado
            elif hasattr(voto.indicado, "nome"):
                indicado_nome = voto.indicado.nome
            elif hasattr(voto.indicado, "titulo"):
                indicado_nome = voto.indicado.titulo
            else:
                indicado_nome = str(voto.indicado)
            contagem[indicado_nome] = contagem.get(indicado_nome, 0) + 1
        return contagem