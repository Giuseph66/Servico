import json
from collections import defaultdict


class Extras():
    def __init__(self, dados_filtrados, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dados=dados_filtrados
    def detectar_reversoes(self):
        historico_alteracoes = defaultdict(list)
        reversoes = []

        for log in self.dados:
            if log and 'log' in log and log['log'] not in (None, "N/A", ""):
                print(log)
                log_data = json.loads(log['log'])
                data_atual = log['data']
                hora_atual = log['hora']
                usuario = log['usuCodigo']
                maquina = log['maquina']
                empresa = log['empresa']
                tabela = log['tabela']
                
                for item in log_data:
                    campo = item['name']
                    old_value = item['old']
                    new_value = item['new']
                    
                    if old_value == new_value:
                        continue
                    
                    chave = (tabela, campo)
                    
                    for alteracao in historico_alteracoes[chave]:
                        if alteracao['new'] == old_value and alteracao['old'] == new_value:
                            reversoes.append({
                                "fantazia":log['razaoSocial'],
                                "tabela": tabela,
                                "campo": campo,
                                "valor_alterado": new_value,
                                "valor_revertido_para": old_value,
                                "primeira_alteracao": {
                                    "data": alteracao['data'],
                                    "hora": alteracao['hora'],
                                    "usuCodigo": alteracao['usuario'],
                                    "maquina": alteracao['maquina'],
                                    "empresa": alteracao['empresa']
                                },
                                "reversao": {
                                    "data": data_atual,
                                    "hora": hora_atual,
                                    "usuCodigo": usuario,
                                    "maquina": maquina,
                                    "empresa": empresa
                                }
                            })
                            break  
                    
                    historico_alteracoes[chave].append({
                        "old": old_value,
                        "new": new_value,
                        "data": data_atual,
                        "hora": hora_atual,
                        "usuario": usuario,
                        "maquina": maquina,
                        "empresa": empresa
                    })
        
        return reversoes
    
    
    def pesquisa_generica(self,valor_busca,campos_busca):
        print(f"values : {valor_busca,campos_busca}")
        resultados = []
        for log in self.dados:
            if log and 'log' in log and log['log'] not in (None, "N/A", ""):
                log_data = json.loads(log.get("log", "[]")) 
                for item in log_data:
                    if valor_busca and campos_busca:
                        if(((valor_busca.lower() in str(item.get("old", "")).lower()) or (valor_busca.lower() in str(item.get("new", "")).lower())) and (campos_busca.lower() in str(item.get("name", "")).lower())) :
                            resultados.append(log["id"])
                            break  
                    elif (valor_busca and not campos_busca): 
                        if(valor_busca.lower() in str(item.get("old", "")).lower() or valor_busca.lower() in str(item.get("new", "")).lower()):
                            resultados.append(log["id"])
                            break
                    else:
                        if (campos_busca.lower() in str(item.get("name", "")).lower()):
                            resultados.append(log["id"])
                            break
        return resultados
    
    def detectar_campos(self):
        campos_geral=[]
        for log in self.dados:
            if log and 'log' in log and log['log'] not in (None, "N/A", ""):
                log_data = json.loads(log.get("log", "[]")) 
                campos = list({dado['name'] for dado in log_data})
                for c in campos:
                    if c not in campos_geral:
                        campos_geral.append(c)
                    
        return sorted(campos_geral)