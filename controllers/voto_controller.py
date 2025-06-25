from models.voto import Voto
class VotoController:
    
    def __init__(self, categoria_controller):
        self.__votos = []
        self.__categoria_controller = categoria_controller
    
    def registrar_voto(self, membro, nome_categoria, indicado):
        if not membro.pode_votar():
            return False
        
        categoria = self.__categoria_controller.buscar_categoria(nome_categoria)
        if not categoria:
            return False
        
        if indicado not in categoria.indicados:
            return False
        
        if any(v.membro == membro and v.categoria == categoria for v in self.__votos):
            return False
        
        voto = Voto(membro, categoria, indicado)
        self.__votos.append(voto)
        categoria.registrar_voto(indicado, membro)
        return True
    
    def listar_votos(self):
        return self.__votos
    
    def contar_votos_categoria(self, categoria):
        votos_categoria = [v for v in self.__votos if v.categoria == categoria]
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