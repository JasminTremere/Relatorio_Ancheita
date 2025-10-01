import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Configuração da página
st.set_page_config(
    page_title="Dashboard EAD",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard EAD - Análise de Assuntos")
st.markdown("Análise de assuntos extraídos do CSV.")
 
df_ead = pd.read_csv('dados_ead.csv', sep=';')

# Separar coluna 'Ações,%,Total'
df_colunas = df_ead['Ações,%,Total'].str.split('|', expand=True).iloc[:, :3]
df_colunas.columns = ['Nome', 'Telefone', 'Assunto']

# Limpar prefixos
df_colunas['Nome'] = df_colunas['Nome'].str.replace('Nome:', '', regex=False).str.strip()
df_colunas['Telefone'] = df_colunas['Telefone'].str.replace('Telefone:', '', regex=False).str.strip()
df_colunas['Assunto'] = df_colunas['Assunto'].str.replace('Assunto:', '', regex=False).str.strip()

# Criar DataFrame limpo
df_limpo = df_colunas.copy()

 category_patterns = {
    # Categoria Atendimento
    'Atendimento Humano': ['falar com atendente','atendente','consultor','quero falar com alguém','quero falar com uma pessoa'],
    # Categoria Colação de grau/Conclusão de Curso
    'Colação de grau/Conclusão de Curso': ['Conclusão','conclusão','Colação de grau','colação de grau','Terminar','Formatura','Colação','Colacao','colacao','colação','formatura'],
    # Categoria de Ativdades Complementares
    'Atividades Complementares':['Hora','hora','Horas','horas','atividade complementar',' Atividade complementar','Hora complementar','Atividades complementares','atividades complementares'],
    # Categoria De Perguntas sobre o Curso
    'Sobre Curso': ['Meu curso','meu curso','Cursos','data de finalização','ao curso','Durabilidade do curso', 'finalizo o curso?','finalizar curso', 'sobre o curso','do curso',' coordenação do meu curso','Curso'],
    # Categoria De Certificados e Diploma
    'Certificado/Diploma': ['Certificado','certificado', 'diploma','Diploma'],
    # Categoria de Tranferencia
    'Transferência': ['transferir','mudar','Sobre mudar de curso','Transferência'],
    # Categoria Sobre Históricos
    'Histórico': ['Historico','Historico escolar', 'Histórico escolar','Histórico'],
    # Categoria sobre Estágio
    'Estágio': ['estágio', 'estágio remunerado','Estágio','Estagio','Estágio não obrigatorio','Estágio obrigatorio','Estágio não obrigatório','Estágio obrigatório','Carreiras','carreiras','estágio obrigatório','estagio obrigatorio','estágio não obrigatório','estagio não obrigatorio'],
    # Categoria Documento
    'Documentos': ['Documento','documento','Documentos','documentos','Documentações','documentações', 'Documentação','documentação','Comprovante','comprovante','atestado médico','atestado de frequência','cnpj','atestado de matrícula'],
    # Categoria Dados para serem modificados
    'Dados Cadastrais': ['Dados cadastrais','dados pessoais','Mudança','Atualizar','alteração do meu nome','Data de nascimento','data de nascimento','Alteração de nome','Queria atualizar','Atualizar e-mail'],
    # Categoria Dispensas
    'Dispensas': ['eliminar matérias', 'dispensas','Dispensa','dispensa','Dispensas'],
    # Categoria Dúvidas
    'Dúvidas': ['tirar dúvidas', 'dúvidas','dúvida','Dúvida','Dúvidas','duvidas','duvida','Duvida'],
    # Categoria Matrículas
    'Matrícula': ['graduações','Graduação','Estudo','Matrícula', 'Matrículas', 'matricula','matriculas','Matricula','Matriculas','fazer algum curso','Estudar','minha vaga'],
    # Categoria sobre as Carteirinhas
    'Carteirinha': ['passe escolar','emtu escolar','carteira','Carteira', 'Carteirinha', 'carteirinha','Cartão','cartão', 'Bilhete escolar','bilhete escolar','bilhete unico','bilhete único','Bilhete único','carteira de meia passagem','Cartão de meia passagem','Carteira de meia passagem','cartão de meia passagem'],
    # Categoria sobre as Provas e as Notas
    'Avaliação/Notas': ['Média','Media','media','média','notas','Notas','nota','Nota','Notas abaixo da média','médias','Avaliação on-line', 'Pontuação','provas','prova','Prova','Provas','recuperação','Recuperação'],
    # Categoria sobre Aulas e Hórarios
    'Aulas/Horários': ['Aula','Aula inaugural','Aulas','aulas','aula online','férias','Férias','início das aulas','aulas pendentes','começa as aulas'],
    #  Categoria Financeiro/Acordos
    'Financeiro': ['parcelas','Parcelas','parcela','Parcela','cobrança','Cobrança','pendências','Acordo','acordo','Acordos','acordos','quitação','data de vencimento','pagamento','pagamentos','Pagamento','Pagamentos','Boleto','Boletos','boletos','boleto','financeiro','Financeiro','Mensalidade','mensalidade','Contrato','Fatura','fatura','Valores','valores','Consulta de Valores','valores de cursos'],
    # Categoria Contato Geral
    # 'Geral': ['Eu mandei mensagem','ola','Bom dia', 'Boa tarde', 'Boa noite', 'Olá', 'Oi', 'tudo bem', 'Gostaria de saber', 'queria saber', 'preciso de ajuda', 'informação', 'ajuda', 'problema', 'questão', 'situação', 'verificar', 'consultar', 'obrigado', 'grato', 'por favor', 'poderia', 'precisa', 'falar', 'atendimento', 'atendente', 'contestar','Não','Okk','ok', 'Ok'],
    # Categoria Biblioteca
    'Minha Biblioteca': ['Biblioteca','biblioteca'],
    # Categoria dos Polos
    'Polos': ['Polo','polo','Polos','polos'],
    # Categoria Secretária Geral: Prouni
    'Secretária Geral': ['Prouni','prouni','ProUni','Secretaria','secretaria','Secretária','secretária'],
    # Acesso E-mails
    'Acesso Emais': ['e-mail institucional','email institucional','recebemos esse e-mail','email estranho','E-mail','sobre esses e-mails'],
    # Pacote Office para os alunos
    'Pacote Office': ['Microsoft','pacote office','usar o Word','Pacote','Word'],
    # Categoria Disciplinas e Turmas
    'Disciplinas/Turmas': ['Disciplinas','Disciplina','disciplinas','disciplina','Enturmações','Enturmação','enturmação','enturmações','grade curricular','grade','Grade','Grade curricular','Turma','turma','Turmas','turmas'],
    #  Categoria Site
    'Site': ['Site','site'],
    # Categoria Análise
    'Análise': ['Análise','retorno da analise','analises','Retorno análise','Análises','analise'],
    # Categoria Suporte
    'Suporte ao Aluno': ['Suporte e Inf. Gerais','Suporte','suporte'],
    # Categoria Bolsas
    'Bolsa': ['analise da bolsa','bolsa','Bolsa'],
    # Categoria Retorno ao Curso
    'Retorno ao Curso': ['Atualização do meu R A','ativar RA','Atualização do meu RA','Retorno a graduação hibrida','quero saber se posso voltar','Teria como iniciar novamente o curso','Refazer o curso','Recomeçar estudos','Reiniciar o curso do início','retorno ao curso'],
    # Categoria Ouvidoria
    'Ouvidoria': ['Ouvidoria','ouvidoria'],
    # Bagagens
    'Bagagem': ['bagagem','Bagagem','bagagens'],
    # Jornada Acadêmica
    'Jornada acadêmica': ['Jornada acadêmica','jornada acadêmica','jornada academica','Jornada Academica','Jornada academica','Jornada Acadêmica'],
    # Requerimento
    'Requerimento': ['requerimento','Requerimento'],
    # Imagem/Video/Audio
    'img/video': ['{type":"v', '{type":"i','{type":"a'],
    # Categoria Trancar matrícula (Refinado)
    'Trancar matrícula': ['Trancar matrícula', 'Trancar o curso', 'Trancar curso', 'Trancar a faculdade', 'trancar', 'Trancamento','trancamento','Encerrar inscrição','Trancar','parar de estudar','tranquei','cancelament','Trancamento de curso','outra instituição','troca','trocar','Trocar','Troca',' Tranquei','trancamento do curso','encerrar o curso','cancelamento','Cancelar matricula','cancelar','Cancelamento de matrícula'],
    # Categoria DP/ADAP (Refinado)
    'DP/ADAP': ['DP', 'ADAP', 'dp', 'adap', 'dependência', 'dependencia'],
    # Categoria Acesso Ava/Aluno online (Refinado)
    'Acesso Ava/Aluno online': ['não consigo logar','não estou conseguindo logar','logar na minha conta','Aluno online','aluno online','acadêmico','Acadêmico','academico','Academico','ambientação','Meu login','meu acesso','Ambientação Virtual de Aprendizagem','ambientação','Ambientação','acessar','plataforma','Portal','Senha','Acesso','canva','portal do aluno','acesso','Canvas','login na plataforma','senha do AVA','Ava','ava','AVA', 'acessar o ava', 'acesso', 'acessa','RA','senha do curso', 'aplicativo','Aplicativo','App','app','Senha no aplicativo'],
    # Categoria Material/Conteúdo (Refinado)
    'Material/Conteúdo': ['Tarefa','tarefa','Tarefas','tarefas','Prazo','Prazos','prazo','prazos','Atividade','atividades','Atividades','Matérias do curso', 'Matérias', 'materia', 'atividade','Matéria','Envio de trabalho','Exercício','Exercícios','exercício','exercicios','exercicio','exercício','conteúdo','Conteúdo'],
    # Categoria Prática
    'Prática Extensionista': ['prática','Prática','praticas','PRÁTICA EXTENSIONISTA','práticas extensionistas','Pratica','pratica','Prática Extensionista'],
    # Categoria Relatório
    'Relatório': ['Máscara de relatório e liberação da pasta star'],
    }

 # Função para categorizar
def categorize_assunto(assunto):
    if not isinstance(assunto, str):
        return 'Outros'
    assunto_lower = assunto.lower()
    for category, patterns in category_patterns.items():
        for pattern in patterns:
            if pattern.lower() in assunto_lower:
                return category
    return 'Outros'

# Aplicar categorização
df_limpo['Categoria'] = df_limpo['Assunto'].apply(categorize_assunto)

#--------------------------------------------------------------------------------------------------------------------------------

# --- Barra Lateral (Filtros) ---
 
st.sidebar.header("🔍 Filtros")
 
# Filtrar por Categoria
categorias_disponiveis = sorted(df_limpo['Categoria'].unique())
categorias_selecionadas = st.sidebar.multiselect("Categoria", categorias_disponiveis, default=categorias_disponiveis)

# Filtrar por Nome
nomes_disponiveis = sorted(df_limpo['Nome'].unique())
nomes_selecionados = st.sidebar.multiselect("Nome", nomes_disponiveis, default=nomes_disponiveis)

# Aplicar filtros
df_filtrado = df_limpo[
    (df_limpo['Categoria'].isin(categorias_selecionadas)) &
    (df_limpo['Nome'].isin(nomes_selecionados))
]
 
# --- Conteúdo Principal ---
st.title("👾Dashboard de Análise Ancheita!👾")
st.markdown("aaaaaaaaaaaaaaaaaaaaaaaah")
 
st.subheader("Métricas Principais")

col1, col2, col3 = st.columns(3)
col1.metric("Total de registros", df_filtrado.shape[0])
col2.metric("Categorias únicas", df_filtrado['Categoria'].nunique())
col3.metric("Nomes únicos", df_filtrado['Nome'].nunique())

st.markdown("---")

# Gráfico de barras por categoria
grafico_categoria = df_filtrado['Categoria'].value_counts().reset_index()
grafico_categoria.columns = ['Categoria', 'Count']

fig = px.bar(
    grafico_categoria,
    x='Categoria',
    y='Count',
    title='Distribuição de Categorias',
    labels={'Categoria':'Categoria', 'Count':'Quantidade'}
)
st.plotly_chart(fig, use_container_width=True)

# Gráfico de pizza por categoria
fig_pie = px.pie(
    grafico_categoria,
    names='Categoria',
    values='Count',
    title='Proporção por Categoria',
    hole=0.4
)
st.plotly_chart(fig_pie, use_container_width=True)

# Tabela detalhada
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
 

#col_graf1, col_graf2 = st.columns(2)
# 
#with col_graf1:
#    if not df_filtrado.empty:
#        top_cargos = df_filtrado.groupby('Categoria')['Count'].mean().nlargest(10).sort_values(ascending=True).reset_index()
#        grafico_cargos = px.bar(
#            top_cargos,
#            x='Categoria',
#            y='Count',
#            orientation='h',
#            title="Distribuição de Categorias de Assunto",
#            labels={'Categoria': 'Categoria de Assunto', 'Count': 'Número de Ocorrências'}
#        )
#        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
#        st.plotly_chart(grafico_cargos, use_container_width=True)
#    else:
#        st.warning("Nenhum dado para exibir no gráfico.")
# 
#with col_graf2:
#    if not df_filtrado.empty:
#        grafico_hist = px.histogram(
#            df_filtrado,
#            x='usd',
#            nbins=30,
#            title="Distribuição de salários anuais",
#            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
#        )
#        grafico_hist.update_layout(title_x=0.1)
#        st.plotly_chart(grafico_hist, use_container_width=True)
#    else:
#        st.warning("Nenhum dado para exibir no gráfico de distribuição.")
# 
#col_graf3, col_graf4 = st.columns(2)
# 
#with col_graf3:
#    if not df_filtrado.empty:
#        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
#        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
#        grafico_remoto = px.pie(
#            remoto_contagem,
#            names='tipo_trabalho',
#            values='quantidade',
#            title='Proporção dos tipos de trabalho',
#            hole=0.5
#        )
#        grafico_remoto.update_traces(textinfo='percent+label')
#        grafico_remoto.update_layout(title_x=0.1)
#        st.plotly_chart(grafico_remoto, use_container_width=True)
#    else:
#        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")
# 
#with col_graf4:
#    if not df_filtrado.empty:
#        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
#        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
#        grafico_paises = px.choropleth(media_ds_pais,
#            locations='residencia_iso3',
#            color='usd',
#            color_continuous_scale='rdylgn',
#            title='Salário médio de Cientista de Dados por país',
#            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
#        grafico_paises.update_layout(title_x=0.1)
#        st.plotly_chart(grafico_paises, use_container_width=True)
#    else:
#        st.warning("Nenhum dado para exibir no gráfico de países.")
 
# --- Tabela de Dados Detalhados ---
#st.subheader("Dados Detalhados")
#st.dataframe(df_filtrado)
 
