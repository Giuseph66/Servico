from django.http import JsonResponse, HttpResponseRedirect,FileResponse, Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.templatetags.static import static
from django.shortcuts import render,redirect
from datetime import datetime
from .models import *
import matplotlib.colors as mcolors
import matplotlib.pyplot  as plt
import plotly.express as px
from .pdf import PDF
from .extras import *
import pandas as pd
import threading
import socket
import requests
import calendar
import json
import os


def index(request):
    return render(request, 'auditoria_app/login.html',{"validacao":0})
def cads(request):
    return render(request, 'auditoria_app/cadastro.html',{"validacao":0})
def acessar(request):
    x=request.META.get('HTTP_X_FORWARDED_FOR')
    if x is not None:
        ip=x.split(',')[0]
        print('aq')
    else :
        ip= request.META.get('REMOTE_ADDR')
    print("Ip : " + ip)
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        hostname="Nao cadastrado"
    print(hostname)
    try:
        user_agent = request.META.get('HTTP_USER_AGENT', 'Nao encontrado')
        referer = request.META.get('HTTP_REFERER', 'Direct Access')
        language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'Mudinho')
        session_id = request.COOKIES.get('sessionid', 'limpo')
        host = request.META.get('HTTP_HOST', 'impossivel')
        connection_type = request.META.get('HTTP_CONNECTION', 'limpo')

        print("Agente : " + user_agent)
        print("Referer : " + referer)
        print("Ligua : " + language)
        print("Sessao : " + session_id)
        print("Host : " + host)
        print("Conecao : " + connection_type)
        
        if not Conexao.objects.filter(user_agent=user_agent, ip=ip).exists():
            conexao = Conexao(
                ip=ip,
                hostname=hostname,
                user_agent=user_agent,
                referer=referer,
                language=language,
                session_id=session_id,
                host=host,
                connection_type=connection_type
            )
            conexao.save()
            print("Dados salvos no banco de dados.")
        else:
            print("Conexão já registrada. Nenhum dado novo foi salvo.")
    except:
        pass
    if request.method == 'POST':
        gmail = request.POST.get('username').lower()
        senha = request.POST.get('password')

        if Usuario.objects.filter(gmail=gmail, senha=senha).exists():    
            usuario = Usuario.objects.get(gmail=gmail)
            request.session['usu'] = usuario.id_usuario
            return HttpResponseRedirect('/home/0')
        else:
            return render(request, 'auditoria_app/login.html', {
                "validacao": 1,
                "sms": "Senha incorreta ou usuário não cadastrado!"
            })

def cadastrar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        gmail = request.POST.get('username').lower()
        senha = request.POST.get('password')
        tell = request.POST.get('tel')
        if Usuario.objects.filter(nome=nome).exists() or Usuario.objects.filter(gmail=gmail).exists():
            return render(request, 'auditoria_app/login.html',{"validacao":1,"sms":"Usuario já Esta cadastrado"})
        else:
            novo_usuario = Usuario(nome=nome, gmail=gmail, senha=senha,cell=tell)
            novo_usuario.save()
            return render(request,'auditoria_app/login.html',{"validacao":1,"sms":"Novo usuario cadastrado com sucesso!"})
def conf(request, valida):
    usu = testa_usu(request)
    if not usu:
        return redirect('/')

    return render(request, 'auditoria_app/config.html', {
        "usu":usu,
        "valida":valida,
        'fotinha':fotinha(usu)
    })
def prob(request, valida):
    usu = testa_usu(request)
    if not usu:
        return redirect('/')

    return render(request, 'auditoria_app/problema.html', {
        "usu":usu,
        "valida":valida,
        'fotinha':fotinha(usu)
    })
def home(request, valida):
    usu = testa_usu(request)
    if not usu:
        return redirect('/')

    dados_ficticios=[
    {
        "cpf_cnpj": "061.000.471-95",
        "Nome": "Adhan Lucas Frazão dos Santos",
        "Apelido": "Adhan Lucas",
        "NumeroTelefone": "(99) 99999-9999",
        "DataCadastro": "10/11/2023",
        "Empresa": "Tech Solutions LTDA",
        "Rua": "Rua 02",
        "Bairro": "Jardim Milão",
        "Numero": "224",
        "Cidade": "Sinop",
        "UF": "MT",
        "CEP": "78550-000"
    },
    {
        "cpf_cnpj": "062.123.456-78",
        "Nome": "Mariana Costa Pereira",
        "Apelido": "Mari",
        "NumeroTelefone": "(21) 98888-7777",
        "DataCadastro": "15/10/2023",
        "Empresa": "Costa Comércio",
        "Rua": "Av. Central",
        "Bairro": "Centro",
        "Numero": "105",
        "Cidade": "Cuiabá",
        "UF": "MT",
        "CEP": "78000-000"
    },
    {
        "cpf_cnpj": "078.999.888-77",
        "Nome": "Carlos Eduardo Silva",
        "Apelido": "Cadu",
        "NumeroTelefone": "(11) 97777-6666",
        "DataCadastro": "12/09/2023",
        "Empresa": "Silva & Associados",
        "Rua": "Rua das Palmeiras",
        "Bairro": "Jardins",
        "Numero": "350",
        "Cidade": "São Paulo",
        "UF": "SP",
        "CEP": "01000-000"
    },
    {
        "cpf_cnpj": "123.456.789-10",
        "Nome": "Beatriz Almeida Souza",
        "Apelido": "Bia",
        "NumeroTelefone": "(65) 96666-5555",
        "DataCadastro": "08/08/2023",
        "Empresa": "Almeida Consultoria",
        "Rua": "Rua do Lago",
        "Bairro": "Vila Nova",
        "Numero": "45",
        "Cidade": "Várzea Grande",
        "UF": "MT",
        "CEP": "78130-000"
    },
    {
        "cpf_cnpj": "234.567.890-11",
        "Nome": "João Pedro Oliveira",
        "Apelido": "JP",
        "NumeroTelefone": "(31) 95555-4444",
        "DataCadastro": "01/07/2023",
        "Empresa": "Oliveira Tech",
        "Rua": "Alameda dos Anjos",
        "Bairro": "São Luiz",
        "Numero": "782",
        "Cidade": "Belo Horizonte",
        "UF": "MG",
        "CEP": "30140-000"
    },
    {
        "cpf_cnpj": "345.678.901-22",
        "Nome": "Ana Paula Ferreira",
        "Apelido": "Ana",
        "NumeroTelefone": "(81) 94444-3333",
        "DataCadastro": "20/06/2023",
        "Empresa": "Ferreira & Cia",
        "Rua": "Rua 15 de Novembro",
        "Bairro": "Boa Vista",
        "Numero": "120",
        "Cidade": "Recife",
        "UF": "PE",
        "CEP": "50030-000"
    },
    {
        "cpf_cnpj": "456.789.012-33",
        "Nome": "Felipe Matos Gonçalves",
        "Apelido": "Lipe",
        "NumeroTelefone": "(71) 93333-2222",
        "DataCadastro": "05/05/2023",
        "Empresa": "Matos Engenharia",
        "Rua": "Rua do Comércio",
        "Bairro": "Comércio",
        "Numero": "200",
        "Cidade": "Salvador",
        "UF": "BA",
        "CEP": "40010-000"
    },
    {
        "cpf_cnpj": "567.890.123-44",
        "Nome": "Larissa Gomes Santos",
        "Apelido": "Lari",
        "NumeroTelefone": "(48) 92222-1111",
        "DataCadastro": "28/04/2023",
        "Empresa": "Santos Moda",
        "Rua": "Rua das Flores",
        "Bairro": "Centro",
        "Numero": "600",
        "Cidade": "Florianópolis",
        "UF": "SC",
        "CEP": "88010-000"
    },
    {
        "cpf_cnpj": "678.901.234-55",
        "Nome": "Ricardo Souza Mendes",
        "Apelido": "Rick",
        "NumeroTelefone": "(85) 91111-0000",
        "DataCadastro": "15/03/2023",
        "Empresa": "Mendes Transportes",
        "Rua": "Rua das Acácias",
        "Bairro": "Aldeota",
        "Numero": "150",
        "Cidade": "Fortaleza",
        "UF": "CE",
        "CEP": "60140-000"
    },
    {
        "cpf_cnpj": "789.012.345-66",
        "Nome": "Juliana Marques Lima",
        "Apelido": "Juli",
        "NumeroTelefone": "(62) 90000-9999",
        "DataCadastro": "10/02/2023",
        "Empresa": "Lima Contabilidade",
        "Rua": "Av. Goiás",
        "Bairro": "Setor Central",
        "Numero": "80",
        "Cidade": "Goiânia",
        "UF": "GO",
        "CEP": "74030-000"
    }
]

    request.session['dados_usu'] = dados_ficticios
    return render(request, 'auditoria_app/home.html', {
        "usu":usu,
        "valida":valida,
        'fotinha':fotinha(usu),
        'validacao':0,
        'clientes':dados_ficticios
    })
def home_filtro(request, valida,filtro):
    usu = testa_usu(request)
    if not usu:
        return redirect('/')

    dados_usus = request.session.get('dados_usu', [])
    if filtro:
        dados_filtrados = [item for item in dados_usus if item['cpf_cnpj'] == filtro]
        if not dados_filtrados:
            dados_filtrados = [item for item in dados_usus if item['Empresa'] == filtro]

    return render(request, 'auditoria_app/home.html', {
        "usu":usu,
        "valida":valida,
        'fotinha':fotinha(usu),
        'validacao':0,
        'clientes':dados_filtrados
    })
def info(request, valida,pj):
    usu = testa_usu(request)
    if not usu:
        return redirect('/')

    dados_usus = request.session.get('dados_usu', [])
    if pj:
        dados_filtrados = [item for item in dados_usus if item['cpf_cnpj'] == pj]
    else:
        dados_filtrados=""
    return render(request, 'auditoria_app/home.html', {
        "usu":usu,
        "valida":valida,
        'fotinha':fotinha(usu),
        'validacao':1,
        'clientes':dados_usus,
        'exibi_filter':dados_filtrados[0]
    })
def img(request, valida):
    if request.method == 'POST':
        img = request.FILES.get('arquivos')
        if img:
            caminho_completo = os.path.join('auditoria_app','static', 'imagens')
            fs = FileSystemStorage(location=caminho_completo)
            fs.delete('sos.png')
            fs.save('sos.png', img)
    return HttpResponseRedirect(f'/configuracao/{valida}')
def auditoria_api(request, valida, empresa):
    usu = testa_usu(request)
    if not usu:
        return redirect("/")

    first_day, last_day = get_current_month_dates()
    default_data_inicio = first_day.strftime('%Y-%m-%d')
    default_data_fim = last_day.strftime('%Y-%m-%d')

    data_inicio = request.GET.get('data_inicio', default_data_inicio)
    data_fim = request.GET.get('data_fim', default_data_fim)
    print(default_data_inicio, default_data_fim)
    
    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
    
    print(data_inicio, data_fim)
    dados_auditoria = busca_dados_api("a",0)
    print("recebeu dados")
    dados_auditoria = replace_none(dados_auditoria, default_value="N/A")
    
    dados_filtrados = [
        item for item in dados_auditoria
        if data_inicio <= datetime.strptime(item['data'], "%d-%m-%Y").date() <= data_fim
    ]

    executavel = request.GET.get('executavel', '')
    tabela = request.GET.get('tabela', '')
    campo = request.GET.get('campo', '')
    busca = request.GET.get('busca', '')
    print(f" tentei {executavel,tabela,campo,busca}")
    if executavel:
        dados_filtrados = [item for item in dados_filtrados if item['executavel'] == executavel]
    if tabela:
        dados_filtrados = [item for item in dados_filtrados if item['tabela'] == tabela]
    extra=Extras(dados_filtrados)
    if busca or campo:
        ids=extra.pesquisa_generica(busca,campo)
        dados_filtrados = [item for item in dados_filtrados if item['id'] in ids]
    tabelas = list({dado['tabela'] for dado in dados_auditoria})
    executaveis = list({dado['executavel'] for dado in dados_auditoria})
    campos = extra.detectar_campos()
    return render(request, 'auditoria_app/auditoria.html', {
        'dados_auditoria': dados_filtrados,
        'tabelas': tabelas,
        'executaveis': executaveis,
        'campos': campos,
        'default_data_inicio': default_data_inicio,
        'default_data_fim': default_data_fim,
        'validacao': 0,
        'sms': 'Erro',
        'usu': usu,
        'valida': valida,
        'fotinha': fotinha(usu),
        'executavel_selecionado': executavel,  
        'tabela_selecionada': tabela,
        'campo_selecionada': campo,
        'busca_dados': busca,
    })

    
def contra(request, valida,argumento):
    usu = testa_usu(request)
    if not usu:
        return redirect('/')
    atu_dados = request.session.get('dados_usu', [])
    contra=busca_dados_contra(argumento)
    return render(request, 'auditoria_app/home.html', {
    'clientes': atu_dados,
    'validacao':2,
    "usu":usu,
    "contra":contra,
    "valida":valida,
    'fotinha':fotinha(usu) 
    })
def exibir_graficos(request, valida, fim_data, ini_dada):
    usu = testa_usu(request)
    if not usu:
        return redirect('/')
    atu_dados = request.session.get('atu_dados', [])
    print("Graf")
    if atu_dados:
        resultados = {}
        grafico1_thread = threading.Thread(target=gera_grafico_thread, args=(atu_dados, 'maquina', resultados, 'grafico1'))
        grafico2_thread = threading.Thread(target=gera_grafico_thread, args=(atu_dados, 'executavel', resultados, 'grafico2'))
        grafico3_thread = threading.Thread(target=gera_grafico_thread, args=(atu_dados, 'tabela', resultados, 'grafico3'))
        grafico1_thread.start()
        grafico2_thread.start()
        grafico3_thread.start()
        grafico1_thread.join()
        grafico2_thread.join()
        grafico3_thread.join()
        request.session['graf1'] = resultados.get('grafico1', "")
        request.session['graf2'] = resultados.get('grafico2', "")
        request.session['graf3'] = resultados.get('grafico3', "")
    else:
        request.session['graf1'] = ""
        request.session['graf2'] = ""
        request.session['graf3'] = ""
        
    executavel = request.GET.get('executavel', '')
    tabela = request.GET.get('tabela', '')
    campo = request.GET.get('campo', '')
    tabelas = list({dado['tabela'] for dado in atu_dados})
    executaveis = list({dado['executavel'] for dado in atu_dados})
    campos = Extras(atu_dados).detectar_campos()
    return render(request, 'auditoria_app/auditoria.html', {
        'dados_auditoria': atu_dados,
        'tabelas': tabelas,
        'executaveis': executaveis,
        'campos': campos,
        'default_data_inicio': ini_dada,
        'default_data_fim': fim_data,
        'validacao': 2,
        "usu":usu,
        "valida":valida,
        'fotinha':fotinha(usu),
        'grafico1': request.session['graf1'],
        'grafico2': request.session['graf2'],
        'grafico3': request.session['graf3'],
        'graf_linha': graf_barra(atu_dados),
        'executavel_selecionado': executavel,  
        'tabela_selecionada': tabela,
        'campo_selecionada': campo,
    })

def pre(request):
    usu = testa_usu(request)
    if not usu:
        return redirect('/')
    dados = request.session.get('atu_dados', [])
    df = pd.DataFrame(dados)
    colunas = ['cpfCnpj', 'razaoSocial', 'fantasia', 'empresa', 'data', 'hora', 'usuCodigo', 'operacao', 'tabela', 'log', 'maquina', 'executavel']
    renomear_colunas = {
        'cpfCnpj': 'CNPJ', 'razaoSocial': 'Razao Social', 'fantasia': 'Nome Fantasia', 'empresa': 'Empresa',
        'data': 'Data', 'hora': 'Hora', 'usuCodigo': 'Codigo Usuario', 'operacao': 'Operacao', 'tabela': 'Tabela',
        'log': 'Log', 'maquina': 'Maquina', 'executavel': 'Executavel'
    }
    df = df[colunas].rename(columns=renomear_colunas)
    def format_log(log):
        try:
            log_data = eval(log)
            log_html = '<table class="table table-bordered table-sm" style="text-align: center; background-color: #547dd5; color: white;">'
            log_html += '<tr><th>Campo</th><th>Valor Antigo</th><th>Valor Novo</th></tr>'
            for item in log_data:
                log_html += f"<tr><td>{item['name']}</td><td>{item['old']}</td><td>{item['new']}</td></tr>"
            log_html += '</table>'
            return log_html
        except Exception as e:
            return f"Erro ao processar log: {e}"
    
    df['Log'] = df['Log'].apply(format_log)
    central_style = """
    <style>
        .table th, .table td {
            text-align: center;
            vertical-align: middle;
        }
    </style>
    """ 
    html_table = df.to_html(escape=False, classes="table table-striped table-bordered table-hover", border=0)
    tabela=central_style + html_table
    return render(request, 'auditoria_app/visu_completa.html',{
        'tabela_html':tabela,
        "usu":usu,
        "valida":0,
        'fotinha':fotinha(usu),
    })

def dowload_audi(request,ini_data,fim_data):
    print(ini_data,fim_data)
    ini_data = datetime.strptime(ini_data, "%Y-%m-%d")
    fim_data = datetime.strptime(fim_data, "%Y-%m-%d")
    data_inicio = ini_data.strftime("%d/%m/%Y")
    data_fim = fim_data.strftime("%d/%m/%Y")
    dados = request.session.get('atu_dados', [])
    df_dados = pd.DataFrame(dados)
    pdf = PDF(data_inicio,data_fim) 
    pdf.set_auto_page_break(auto=True, margin=15) 
    pdf.add_page()
    pdf.add_table(df_dados)
    pdf.output("auditoria_app/media/relatorios/relatorio_operacoes_formatado.pdf")
    try:
        file_path = 'auditoria_app/media/relatorios/relatorio_operacoes_formatado.pdf'
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = 'attachment; filename="Relatorio.pdf"'
        return response
    except FileNotFoundError:
        raise Http404("Arquivo não encontrado.")







































def fotinha(user):
    url = f"https://github.com/{user.nome}.png"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return url
    except requests.RequestException:
        pass
    return static('imagens/Usu.png')
def get_current_month_dates():
    today = datetime.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    return first_day, last_day



def gera_grafico_thread(dados, foco, resultado, chave):
    resultado[chave] = gera_grafico(dados, foco)

def gera_grafico(dados,foco):
    df = pd.DataFrame(dados)

    grouped_df = df.groupby(foco).size().reset_index(name='values')
    fig = px.pie(
        grouped_df,
        names=foco,
        values='values' 
    )

    qnt_fatia=len(grouped_df)
    color = plt.cm.Blues([0.5 + i * (0.4 / qnt_fatia) for i in range(qnt_fatia     )]) 
    color = [mcolors.rgb2hex(c) for c in color]
    fig.update_traces(
        hovertemplate='<b>%{label} : %{value}<b>',
        textinfo='percent+label',
        textfont_size=18,
        textposition='inside',
        marker=dict(
            colors=color[:len(grouped_df)],  # Aplica as cores na quantidade de categorias presente
            line=dict(color='#FFFFFF', width=2)  # Borda branca
        )
    )

    fig.update_layout(
        width=350,
        height=340,
        showlegend=True,
        legend=dict(
            font=dict(
                family="Arial",
                size=10,
                color="white"
            ),
            orientation="h",
            xanchor="center",
            x=0.5,
            yanchor="bottom",
            y=-1,                   
            bgcolor='#333333',       
            bordercolor='#000000',
            borderwidth=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)',  
        font=dict(color="white"),     
        margin=dict(l=0, r=0, t=0, b=0)  
    )

    return fig.to_html(full_html=False,config={'displayModeBar': False}) 
def graf_barra(dados):
    df = pd.DataFrame(dados)
    contagem_operacoes = df['operacao'].value_counts().reset_index()
    contagem_operacoes.columns = ['Tipo de Operação', 'Quantidade']

    colors = plt.cm.Blues([0.5 + i * (0.4 / 3) for i in range(3)]) 
    colors = [mcolors.rgb2hex(c) for c in colors]
    fig = px.bar(
        contagem_operacoes, 
        x='Tipo de Operação', 
        y='Quantidade',
        color='Tipo de Operação',
        color_discrete_sequence=colors,
        text='Quantidade',  
    )
    fig.update_traces(
        hovertemplate='<b>%{x} : %{y}</b>', 
        textfont_size=18,
        textposition='inside'
    )
    fig.update_layout(
        xaxis_title="Tipo de Operação",
        yaxis_title="Quantidade",
        width=500,
        height=380,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),    
        bargap=0.4,  
    )
    return fig.to_html(full_html=False, config={'displayModeBar': False})
def testa_usu(request):
    try:       
        usu = Usuario.objects.get(id_usuario=request.session.get('usu', [])) 
        if not usu:
            return None
        return usu 
    except:
        return None
    
def replace_none(data, default_value="N/A"):
    if isinstance(data, list):
        return [replace_none(item, default_value) for item in data]
    elif isinstance(data, dict):
        return {key: (default_value if value is None else value) for key, value in data.items()}
    else:
        return data
    
def autentica_token():
    acesso={
        "UserName": "Administrador",
        "PassWord": "#Norte#sistema#2024!"
    }
    retorno = requests.post('http://api.nortesistema.com.br:5500/gateway/conta/autenticar', json=acesso)
    token = retorno.json().get('jwtToken')
    if retorno.status_code == 200:
        token = retorno.json().get('jwtToken')
        print(f'Token de autenticação: {token}')
        precosse.objects.update_or_create(id=1,defaults={'token': token})
        return token
    else:

        print(f'Falha na autenticação. Status: {retorno.status_code}')
        return f'Erro ao conectar {retorno.status_code}'
def busca_dados_api(empresa,tenta):
    token=precosse.objects.get(id=1)
    autenicacao = {'Authorization': f'Bearer {token.token}'}  
    dados_auditoria=requests.get(f'http://api.nortesistema.com.br:5500/gateway/auditoria/pesquisarazaofantasia/{empresa}', headers=autenicacao)
    if dados_auditoria.status_code == 200:
        try:
            print("Foi")
            return dados_auditoria.json().get('result')
        except ValueError:
            print("Erro ao decodificar JSON: Resposta não é um JSON válido.")
            return None
    else:
        if tenta < 5:
            tenta+=1
            autentica_token()
            print(f"Erro na resposta da API: Status {dados_auditoria.status_code}")
            return busca_dados_api(empresa,tenta)
        else:
            print(f"Erro na resposta da API: Status {dados_auditoria.status_code} tentei : {tenta} vezes")
            listaaa=[]
            return listaaa

def busca_dados_contra(argumento):
    passa=argumento.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    print(passa)
    dados=requests.get(f'http://api.nortesistema.com.br:5500/gateway/contrasenha/{passa}')
    if dados.status_code == 200:
        try:
            dados_json = dados.json()
            print(dados_json)
            return dados_json
        except ValueError:
            print("Resposta não contém JSON válido:")
            print(dados.text)
    else:
        print(f"Erro ao fazer a requisição: {dados.status_code}")
        print(dados)

