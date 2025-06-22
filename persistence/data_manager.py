# persistence/data_manager.py
import json
import os
from typing import Dict, List, Any
from exceptions.oscar_exceptions import ArquivoException

class DataManager:
    def __init__(self, data_directory="data"):
        self.data_directory = data_directory
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Garante que o diretório de dados existe"""
        try:
            if not os.path.exists(self.data_directory):
                os.makedirs(self.data_directory)
        except Exception as e:
            raise ArquivoException("criar diretório", self.data_directory, e)
    
    def get_file_path(self, filename: str) -> str:
        """Retorna o caminho completo do arquivo"""
        return os.path.join(self.data_directory, f"{filename}.json")
    
    def save_data(self, filename: str, data: Dict[str, Any]):
        """Salva dados em arquivo JSON"""
        try:
            file_path = self.get_file_path(filename)
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            raise ArquivoException("salvar", filename, e)
    
    def load_data(self, filename: str) -> Dict[str, Any]:
        """Carrega dados de arquivo JSON"""
        try:
            file_path = self.get_file_path(filename)
            if not os.path.exists(file_path):
                return {}
            
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            raise ArquivoException("carregar", filename, e)
    
    def delete_data(self, filename: str):
        """Deleta arquivo de dados"""
        try:
            file_path = self.get_file_path(filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            raise ArquivoException("deletar", filename, e)
    
    def list_data_files(self) -> List[str]:
        """Lista todos os arquivos de dados"""
        try:
            if not os.path.exists(self.data_directory):
                return []
            
            files = []
            for filename in os.listdir(self.data_directory):
                if filename.endswith('.json'):
                    files.append(filename[:-5])  # Remove .json extension
            return files
        except Exception as e:
            raise ArquivoException("listar", self.data_directory, e)

class PersistenceManager:
    def __init__(self):
        self.data_manager = DataManager()
    
    def save_membros(self, membros):
        """Salva lista de membros"""
        data = []
        for membro in membros:
            data.append({
                'nome': membro.nome,
                'tipo': membro.tipo,
                'senha': membro._Membro__senha,  # Acesso ao atributo privado
                'votos_realizados': [v for v in membro.votos_realizados]
            })
        self.data_manager.save_data('membros', {'membros': data})
    
    def load_membros(self):
        """Carrega lista de membros"""
        from models.membro import Membro
        data = self.data_manager.load_data('membros')
        membros = []
        
        if 'membros' in data:
            for membro_data in data['membros']:
                try:
                    membro = Membro(
                        membro_data['nome'],
                        membro_data['tipo'],
                        membro_data['senha']
                    )
                    # Restaurar votos realizados se existirem
                    if 'votos_realizados' in membro_data:
                        membro._Membro__votos_realizados = membro_data['votos_realizados']
                    membros.append(membro)
                except Exception as e:
                    print(f"Erro ao carregar membro: {e}")
        
        return membros
    
    def save_filmes(self, filmes):
        """Salva lista de filmes"""
        data = []
        for filme in filmes:
            data.append({
                'titulo': filme.titulo,
                'ano': filme.ano,
                'genero': filme.genero,
                'diretor_nome': filme.diretor.nome if filme.diretor else '',
                'descricao': filme.descricao
            })
        self.data_manager.save_data('filmes', {'filmes': data})
    
    def load_filmes(self, diretor_controller):
        """Carrega lista de filmes"""
        from models.filme import Filme
        data = self.data_manager.load_data('filmes')
        filmes = []
        
        if 'filmes' in data:
            for filme_data in data['filmes']:
                try:
                    diretor = diretor_controller.encontrar_ou_criar_diretor(
                        filme_data.get('diretor_nome', 'Desconhecido')
                    )
                    filme = Filme(
                        filme_data['titulo'],
                        filme_data['ano'],
                        filme_data['genero'],
                        diretor,
                        filme_data.get('descricao', '')
                    )
                    filmes.append(filme)
                except Exception as e:
                    print(f"Erro ao carregar filme: {e}")
        
        return filmes
    
    def save_atores(self, atores):
        """Salva lista de atores"""
        data = []
        for ator in atores:
            data.append({
                'nome': ator.nome,
                'idade': ator.idade,
                'filmes_participados': ator.filmes_participados,
                'tipo_ator': ator.tipo_ator,
                'nacionalidade': ator.nacionalidade
            })
        self.data_manager.save_data('atores', {'atores': data})
    
    def load_atores(self):
        """Carrega lista de atores"""
        from models.ator import Ator
        data = self.data_manager.load_data('atores')
        atores = []
        
        if 'atores' in data:
            for ator_data in data['atores']:
                try:
                    ator = Ator(
                        ator_data['nome'],
                        ator_data['idade'],
                        ator_data['filmes_participados'],
                        ator_data['tipo_ator'],
                        ator_data.get('nacionalidade', 'Desconhecida')
                    )
                    atores.append(ator)
                except Exception as e:
                    print(f"Erro ao carregar ator: {e}")
        
        return atores
    
    def save_diretores(self, diretores):
        """Salva lista de diretores"""
        data = []
        for diretor in diretores:
            data.append({
                'nome': diretor.nome,
                'idade': diretor.idade,
                'filmes_dirigidos': diretor.filmes_dirigidos
            })
        self.data_manager.save_data('diretores', {'diretores': data})
    
    def load_diretores(self):
        """Carrega lista de diretores"""
        from models.diretor import Diretor
        data = self.data_manager.load_data('diretores')
        diretores = []
        
        if 'diretores' in data:
            for diretor_data in data['diretores']:
                try:
                    diretor = Diretor(
                        diretor_data['nome'],
                        diretor_data['idade'],
                        diretor_data['filmes_dirigidos']
                    )
                    diretores.append(diretor)
                except Exception as e:
                    print(f"Erro ao carregar diretor: {e}")
        
        return diretores
    
    def save_categorias(self, categorias):
        """Salva lista de categorias com indicados"""
        data = []
        for categoria in categorias:
            indicados_data = []
            for indicado in categoria.indicados:
                if hasattr(indicado, 'nome'):
                    indicados_data.append({'nome': indicado.nome, 'tipo': 'pessoa'})
                elif hasattr(indicado, 'titulo'):
                    indicados_data.append({'titulo': indicado.titulo, 'tipo': 'filme'})
                else:
                    indicados_data.append({'nome': str(indicado), 'tipo': 'string'})
            
            data.append({
                'nome': categoria.nome,
                'indicados': indicados_data
            })
        self.data_manager.save_data('categorias', {'categorias': data})
    
    def save_votos(self, votos):
        """Salva lista de votos"""
        data = []
        for voto in votos:
            indicado_nome = ''
            if hasattr(voto.indicado, 'nome'):
                indicado_nome = voto.indicado.nome
            elif hasattr(voto.indicado, 'titulo'):
                indicado_nome = voto.indicado.titulo
            else:
                indicado_nome = str(voto.indicado)
            
            data.append({
                'membro_nome': voto.membro.nome,
                'categoria_nome': voto.categoria.nome,
                'indicado_nome': indicado_nome
            })
        self.data_manager.save_data('votos', {'votos': data})
    
    def load_votos(self, membro_controller, categoria_controller):
        """Carrega lista de votos"""
        from models.voto import Voto
        data = self.data_manager.load_data('votos')
        votos = []
        
        if 'votos' in data:
            for voto_data in data['votos']:
                try:
                    membro = membro_controller.buscar_membro(voto_data['membro_nome'])
                    categoria = categoria_controller.buscar_categoria(voto_data['categoria_nome'])
                    
                    if membro and categoria:
                        # Encontrar o indicado na categoria
                        indicado = None
                        for ind in categoria.indicados:
                            if hasattr(ind, 'nome') and ind.nome == voto_data['indicado_nome']:
                                indicado = ind
                                break
                            elif hasattr(ind, 'titulo') and ind.titulo == voto_data['indicado_nome']:
                                indicado = ind
                                break
                            elif str(ind) == voto_data['indicado_nome']:
                                indicado = ind
                                break
                        
                        if indicado:
                            voto = Voto(membro, categoria, indicado)
                            votos.append(voto)
                except Exception as e:
                    print(f"Erro ao carregar voto: {e}")
        
        return votos