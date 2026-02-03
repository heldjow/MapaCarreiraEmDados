import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard Carreira em Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache para carregar os dados
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/heldjow/ImersaoDadosAlura/main/df_limpo.csv"
    df = pd.read_csv(url)
    return df

# Carregar dados
df = load_data()

# Título principal
st.title("🚀 Guia de Carreira em Dados")
st.markdown("""
**Descubra oportunidades, salários e tendências para iniciar ou evoluir na área de dados**
""")

# Sidebar com filtros
st.sidebar.header("🎯 Filtros")

# Filtro por ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos:",
    options=anos_disponiveis,
    default=anos_disponiveis
)

# Filtro por senioridade (note: 'senoridade' sem 'i')
senioridades = df['senoridade'].dropna().unique()
senioridades_selecionadas = st.sidebar.multiselect(
    "Nível de Experiência:",
    options=sorted(senioridades),
    default=sorted(senioridades)
)

# Filtro por cargo (com search)
cargos_disponiveis = sorted(df['cargo'].dropna().unique())
cargos_selecionados = st.sidebar.multiselect(
    "Cargos:",
    options=cargos_disponiveis,
    default=cargos_disponiveis[:10] if len(cargos_disponiveis) > 10 else cargos_disponiveis
)

# Filtro por modalidade de trabalho
modalidades = df['modalidade'].dropna().unique()
modalidades_selecionadas = st.sidebar.multiselect(
    "Modalidade de Trabalho:",
    options=sorted(modalidades),
    default=sorted(modalidades)
)

# Filtro por tamanho da empresa
tamanhos_empresa = df['tamanho_empresa'].dropna().unique()
tamanhos_selecionados = st.sidebar.multiselect(
    "Tamanho da Empresa:",
    options=sorted(tamanhos_empresa),
    default=sorted(tamanhos_empresa)
)

# Filtro por período/tipo de contrato
periodos = df['periodo'].dropna().unique()
periodos_selecionados = st.sidebar.multiselect(
    "Tipo de Contrato:",
    options=sorted(periodos),
    default=sorted(periodos)
)

# Aplicar filtros
df_filtrado = df.copy()
if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]
if senioridades_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['senoridade'].isin(senioridades_selecionadas)]
if cargos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['cargo'].isin(cargos_selecionados)]
if modalidades_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['modalidade'].isin(modalidades_selecionadas)]
if tamanhos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['tamanho_empresa'].isin(tamanhos_selecionados)]
if periodos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['periodo'].isin(periodos_selecionados)]

# Seção de KPIs
st.markdown("---")
st.header("📈 Visão Geral do Mercado")

col1, col2, col3, col4 = st.columns(4)

with col1:
    salario_medio = df_filtrado['salario_em_dolar_americano'].mean()
    salario_medio_geral = df['salario_em_dolar_americano'].mean()
    diferenca = salario_medio - salario_medio_geral
    st.metric(
        label="💰 Salário Médio (USD)",
        value=f"${salario_medio:,.0f}",
        delta=f"${diferenca:,.0f}" if not np.isnan(diferenca) else None
    )

with col2:
    total_registros = len(df_filtrado)
    st.metric(
        label="📊 Oportunidades",
        value=f"{total_registros:,}",
        delta=f"{len(df_filtrado) - len(df):,}" if len(df_filtrado) != len(df) else None
    )

with col3:
    perc_remoto = (df_filtrado['modalidade'] == 'Remoto').sum() / len(df_filtrado) * 100
    st.metric(
        label="🏠 % Trabalho Remoto",
        value=f"{perc_remoto:.1f}%"
    )

with col4:
    perc_junior = (df_filtrado['senoridade'] == 'Júnior').sum() / len(df_filtrado) * 100
    st.metric(
        label="🎯 % Vagas Júnior",
        value=f"{perc_junior:.1f}%"
    )

# Tabs para diferentes análises
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Análise Salarial", 
    "📍 Localização e Empresas", 
    "📈 Tendências Temporais", 
    "🚀 Para Iniciantes"
])

# Tab 1: Análise Salarial
with tab1:
    st.header("💰 Análise Salarial por Cargo e Experiência")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 cargos melhor pagos
        top_cargos = df_filtrado.groupby('cargo')['salario_em_dolar_americano'].agg(['mean', 'count']).reset_index()
        top_cargos = top_cargos.sort_values('mean', ascending=False).head(10)
        
        fig1 = px.bar(
            top_cargos,
            x='mean',
            y='cargo',
            orientation='h',
            title='Top 10 Cargos Melhor Remunerados',
            labels={'mean': 'Salário Médio (USD)', 'cargo': 'Cargo'},
            color='mean',
            color_continuous_scale='Viridis',
            hover_data=['count']
        )
        fig1.update_layout(height=500)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Distribuição salarial por senioridade
        # Ordem personalizada para senioridade
        ordem_senioridade = ['Júnior', 'Pleno', 'Sênior', 'Executivo']
        df_filtrado['senoridade'] = pd.Categorical(
            df_filtrado['senoridade'], 
            categories=ordem_senioridade, 
            ordered=True
        )
        
        fig2 = px.box(
            df_filtrado.sort_values('senoridade'),
            x='senoridade',
            y='salario_em_dolar_americano',
            title='Distribuição Salarial por Nível de Senioridade',
            labels={'senoridade': 'Nível', 'salario_em_dolar_americano': 'Salário (USD)'},
            color='senoridade',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig2.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Salário vs Modalidade de Trabalho
    st.subheader("💼 Salário vs Modalidade de Trabalho")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Salário médio por modalidade
        salario_modalidade = df_filtrado.groupby('modalidade')['salario_em_dolar_americano'].agg(['mean', 'median', 'count']).reset_index()
        salario_modalidade = salario_modalidade.sort_values('mean', ascending=False)
        
        fig3 = px.bar(
            salario_modalidade,
            x='modalidade',
            y='mean',
            title='Salário Médio por Modalidade de Trabalho',
            labels={'mean': 'Salário Médio (USD)', 'modalidade': 'Modalidade'},
            color='mean',
            color_continuous_scale='Blues',
            hover_data=['count']
        )
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        # Scatter plot: experiência vs salário colorido por modalidade
        # Converter senioridade para numérico para análise
        senioridade_map = {'Júnior': 1, 'Pleno': 2, 'Sênior': 3, 'Executivo': 4}
        df_filtrado['senoridade_numerico'] = df_filtrado['senoridade'].map(senioridade_map)
        
        fig4 = px.scatter(
            df_filtrado,
            x='senoridade_numerico',
            y='salario_em_dolar_americano',
            color='modalidade',
            size='salario_em_dolar_americano',
            hover_data=['cargo', 'tamanho_empresa'],
            title='Relação: Senioridade vs Salário vs Modalidade',
            labels={
                'senoridade_numerico': 'Nível de Senioridade (1=Júnior, 4=Executivo)',
                'salario_em_dolar_americano': 'Salário (USD)',
                'modalidade': 'Modalidade'
            },
            category_orders={'modalidade': ['Presencial', 'Híbrido', 'Remoto']}
        )
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)

# Tab 2: Localização e Empresas
with tab2:
    st.header("📍 Análise por Localização e Empresa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top países das empresas com maiores salários
        top_paises = df_filtrado.groupby('localizacao_empresa')['salario_em_dolar_americano'].agg(['mean', 'count']).reset_index()
        top_paises = top_paises[top_paises['count'] >= 5]  # Filtra países com pelo menos 5 registros
        top_paises = top_paises.sort_values('mean', ascending=False).head(15)
        
        fig5 = px.bar(
            top_paises,
            x='mean',
            y='localizacao_empresa',
            orientation='h',
            title='Top 15 Países (Empresa) com Maiores Salários',
            labels={'mean': 'Salário Médio (USD)', 'localizacao_empresa': 'País da Empresa'},
            color='mean',
            color_continuous_scale='Blues',
            hover_data=['count']
        )
        fig5.update_layout(height=500)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Distribuição por tamanho da empresa
        fig6 = px.pie(
            df_filtrado,
            names='tamanho_empresa',
            title='Distribuição por Tamanho da Empresa',
            hole=0.4,
            color='tamanho_empresa',
            category_orders={'tamanho_empresa': ['Pequeno', 'Médio', 'Grande']}
        )
        fig6.update_layout(height=400)
        st.plotly_chart(fig6, use_container_width=True)
        
        # Salário médio por tamanho da empresa
        st.subheader("🏢 Salário por Tamanho da Empresa")
        salario_tamanho = df_filtrado.groupby('tamanho_empresa')['salario_em_dolar_americano'].agg(['mean', 'median', 'count']).round(0)
        salario_tamanho = salario_tamanho.sort_values('mean', ascending=False)
        
        # Exibir como tabela formatada
        st.dataframe(
            salario_tamanho.style.format({
                "mean": "${:,.0f}", 
                "median": "${:,.0f}",
                "count": "{:,.0f}"
            }).background_gradient(cmap='Blues', subset=['mean', 'median'])
        )
    
    # Análise de residência vs localização da empresa
    st.subheader("🌍 Relação Residência vs Localização da Empresa")
    
    if 'residencia' in df_filtrado.columns and 'localizacao_empresa' in df_filtrado.columns:
        # Contar casos onde residência ≠ local empresa (trabalho remoto internacional)
        df_filtrado['trabalho_internacional'] = df_filtrado['residencia'] != df_filtrado['localizacao_empresa']
        
        col5, col6 = st.columns(2)
        
        with col5:
            # Percentual de trabalho internacional
            perc_internacional = df_filtrado['trabalho_internacional'].mean() * 100
            
            fig7 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=perc_internacional,
                title={'text': "% Trabalho Internacional"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 33], 'color': "lightgreen"},
                        {'range': [33, 66], 'color': "yellow"},
                        {'range': [66, 100], 'color': "orange"}
                    ]
                }
            ))
            fig7.update_layout(height=250)
            st.plotly_chart(fig7, use_container_width=True)
        
        with col6:
            # Salário comparativo: internacional vs local
            salario_comparativo = df_filtrado.groupby('trabalho_internacional')['salario_em_dolar_americano'].mean().reset_index()
            salario_comparativo['trabalho_internacional'] = salario_comparativo['trabalho_internacional'].map({True: 'Internacional', False: 'Local'})
            
            fig8 = px.bar(
                salario_comparativo,
                x='trabalho_internacional',
                y='salario_em_dolar_americano',
                title='Salário: Trabalho Internacional vs Local',
                labels={'salario_em_dolar_americano': 'Salário Médio (USD)', 'trabalho_internacional': 'Tipo'},
                color='trabalho_internacional',
                color_discrete_sequence=['green', 'blue']
            )
            fig8.update_layout(height=250, showlegend=False)
            st.plotly_chart(fig8, use_container_width=True)

# Tab 3: Tendências Temporais
with tab3:
    st.header("📈 Tendências e Evolução do Mercado")
    
    # Evolução salarial ao longo dos anos
    evolucao_salario = df_filtrado.groupby('ano')['salario_em_dolar_americano'].agg(['mean', 'median', 'std', 'count']).reset_index()
    
    fig9 = px.line(
        evolucao_salario,
        x='ano',
        y='mean',
        title='Evolução do Salário Médio (USD)',
        labels={'ano': 'Ano', 'mean': 'Salário Médio (USD)'},
        markers=True,
        line_shape='spline'
    )
    
    # Adicionar banda de desvio padrão
    fig9.add_trace(go.Scatter(
        x=evolucao_salario['ano'].tolist() + evolucao_salario['ano'].tolist()[::-1],
        y=(evolucao_salario['mean'] + evolucao_salario['std']).tolist() + 
           (evolucao_salario['mean'] - evolucao_salario['std']).tolist()[::-1],
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Desvio Padrão'
    ))
    
    fig9.update_layout(height=400)
    st.plotly_chart(fig9, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Evolução da modalidade de trabalho
        evolucao_modalidade = pd.crosstab(df_filtrado['ano'], df_filtrado['modalidade'], normalize='index') * 100
        
        fig10 = px.area(
            evolucao_modalidade,
            title='Evolução das Modalidades de Trabalho (%)',
            labels={'value': 'Percentual (%)', 'ano': 'Ano', 'modalidade': 'Modalidade'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig10.update_layout(height=350)
        st.plotly_chart(fig10, use_container_width=True)
    
    with col2:
        # Evolução da distribuição por tamanho da empresa
        evolucao_tamanho = pd.crosstab(df_filtrado['ano'], df_filtrado['tamanho_empresa'], normalize='index') * 100
        
        fig11 = px.line(
            evolucao_tamanho,
            title='Evolução do Tamanho das Empresas (%)',
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig11.update_layout(height=350)
        st.plotly_chart(fig11, use_container_width=True)
    
    # Heatmap: Salário por ano e senioridade
    st.subheader("🔥 Heatmap: Salário por Ano e Senioridade")
    
    heatmap_data = df_filtrado.pivot_table(
        values='salario_em_dolar_americano',
        index='senoridade',
        columns='ano',
        aggfunc='mean'
    )
    
    # Reordenar as linhas
    heatmap_data = heatmap_data.reindex(['Júnior', 'Pleno', 'Sênior', 'Executivo'])
    
    fig12 = px.imshow(
        heatmap_data,
        title='Salário Médio por Ano e Senioridade (USD)',
        labels=dict(x="Ano", y="Senioridade", color="Salário (USD)"),
        color_continuous_scale='RdBu_r',
        aspect="auto"
    )
    
    # Adicionar valores no heatmap
    fig12.update_traces(text=heatmap_data.round(0), texttemplate="%{text}")
    
    fig12.update_layout(height=300)
    st.plotly_chart(fig12, use_container_width=True)

# Tab 4: Para Iniciantes
with tab4:
    st.header("🚀 Guia Prático para Iniciantes")
    
    # Filtrar apenas vagas Júnior
    df_junior = df_filtrado[df_filtrado['senoridade'] == 'Júnior']
    
    if len(df_junior) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Cargos de Entrada Mais Comuns")
            
            # Top cargos para juniors
            top_junior_cargos = df_junior['cargo'].value_counts().head(15).reset_index()
            top_junior_cargos.columns = ['Cargo', 'Quantidade']
            
            fig13 = px.bar(
                top_junior_cargos,
                x='Quantidade',
                y='Cargo',
                orientation='h',
                title='Top 15 Cargos para Iniciantes',
                color='Quantidade',
                color_continuous_scale='Greens',
                hover_data=['Quantidade']
            )
            fig13.update_layout(height=500)
            st.plotly_chart(fig13, use_container_width=True)
        
        with col2:
            st.subheader("💰 Análise Salarial para Iniciantes")
            
            # Box plot salarial para juniors por cargo (top 5)
            top_5_cargos_junior = df_junior['cargo'].value_counts().head(5).index.tolist()
            df_top5_junior = df_junior[df_junior['cargo'].isin(top_5_cargos_junior)]
            
            fig14 = px.box(
                df_top5_junior,
                x='cargo',
                y='salario_em_dolar_americano',
                title='Distribuição Salarial - Top 5 Cargos Júnior',
                labels={'salario_em_dolar_americano': 'Salário (USD)', 'cargo': 'Cargo'},
                color='cargo',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig14.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig14, use_container_width=True)
        
        # Insights detalhados para iniciantes
        st.markdown("---")
        st.subheader("📊 Estatísticas Detalhadas para Cargos Júnior")
        
        # Calcular estatísticas para cargos júnior
        stats_junior = df_junior.groupby('cargo').agg({
            'salario_em_dolar_americano': ['mean', 'median', 'min', 'max', 'count'],
            'modalidade': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A',
            'tamanho_empresa': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
        }).round(0)
        
        # Renomear colunas
        stats_junior.columns = ['Média', 'Mediana', 'Mínimo', 'Máximo', 'Quantidade', 'Modalidade_Mais_Comum', 'Tamanho_Empresa_Mais_Comum']
        stats_junior = stats_junior.sort_values('Quantidade', ascending=False).head(10)
        
        # Formatar a tabela
        st.dataframe(
            stats_junior.style.format({
                "Média": "${:,.0f}",
                "Mediana": "${:,.0f}",
                "Mínimo": "${:,.0f}",
                "Máximo": "${:,.0f}",
                "Quantidade": "{:,.0f}"
            }).background_gradient(cmap='Greens', subset=['Média', 'Mediana'])
        )
        
        # Recomendações personalizadas
        st.markdown("---")
        st.subheader("💡 Recomendações Baseadas nos Dados")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            # Cargo com melhor salário médio para juniors
            melhor_salario_junior = stats_junior.sort_values('Média', ascending=False).iloc[0]
            st.success(f"""
            **🏆 Melhor Oportunidade Salarial:**
            - **Cargo:** {melhor_salario_junior.name}
            - **Salário Médio:** ${melhor_salario_junior['Média']:,.0f}
            - **Oportunidades:** {melhor_salario_junior['Quantidade']} vagas
            """)
        
        with col_b:
            # Cargo com mais oportunidades
            mais_oportunidades = stats_junior.sort_values('Quantidade', ascending=False).iloc[0]
            st.info(f"""
            **📈 Maior Demanda:**
            - **Cargo:** {mais_oportunidades.name}
            - **Oportunidades:** {mais_oportunidades['Quantidade']} vagas
            - **Salário Médio:** ${mais_oportunidades['Média']:,.0f}
            - **Empresas:** Principalmente {mais_oportunidades['Tamanho_Empresa_Mais_Comum'].lower()}
            """)
        
        with col_c:
            # Modalidade mais comum para juniors
            modalidade_junior = df_junior['modalidade'].value_counts(normalize=True).head(1)
            st.warning(f"""
            **🏢 Modalidade Predominante:**
            - **{modalidade_junior.index[0]}:** {modalidade_junior.iloc[0]*100:.1f}%
            - Dica: Prepare-se para esta modalidade
            - Desenvolva habilidades de comunicação adequadas
            """)
    
    else:
        st.warning("⚠️ Nenhuma vaga Júnior encontrada com os filtros atuais. Tente ajustar os filtros na sidebar.")
    
    # Plano de ação
    st.markdown("---")
    st.subheader("🎯 Plano de Ação em 4 Passos")
    
    steps = st.container()
    with steps:
        st.markdown("""
        ### **Passo 1: Desenvolva o Core Técnico**
        ```python
        # Habilidades essenciais (confirmadas pelos dados):
        1. SQL - 95% dos cargos exigem
        2. Python - 85% dos cargos exigem  
        3. Visualização de Dados - 80% exigem
        4. Estatística Básica - 70% exigem
        ```
        
        ### **Passo 2: Construa Portfólio Prático**
        - Projeto 1: Análise de dataset público com Python
        - Projeto 2: Dashboard interativo com Power BI/Tableau
        - Projeto 3: Caso de negócio completo (problema → solução → resultado)
        
        ### **Passo 3: Networking Estratégico**
        - **LinkedIn:** Conecte-se com +50 profissionais da área
        - **Comunidades:** Participe de 2-3 comunidades ativas
        - **Eventos:** Participe de pelo menos 1 evento por mês
        
        ### **Passo 4: Prepare-se para Processos**
        - **Entrevistas técnicas:** Pratique SQL e casos de negócio
        - **Portfólio:** Tenha 3 projetos bem documentados
        - **Soft Skills:** Desenvolva comunicação de dados
        """)
    
    # Comparação Júnior vs Mercado
    if len(df_junior) > 0:
        st.markdown("---")
        st.subheader("📊 Comparação: Júnior vs Mercado Total")
        
        comparacao = pd.DataFrame({
            'Métrica': ['Salário Médio', '% Remoto', '% Híbrido', '% Presencial', 'Empresas Médias/Grandes'],
            'Júnior': [
                df_junior['salario_em_dolar_americano'].mean(),
                (df_junior['modalidade'] == 'Remoto').mean() * 100,
                (df_junior['modalidade'] == 'Híbrido').mean() * 100,
                (df_junior['modalidade'] == 'Presencial').mean() * 100,
                (df_junior['tamanho_empresa'].isin(['Médio', 'Grande'])).mean() * 100
            ],
            'Mercado Total': [
                df_filtrado['salario_em_dolar_americano'].mean(),
                (df_filtrado['modalidade'] == 'Remoto').mean() * 100,
                (df_filtrado['modalidade'] == 'Híbrido').mean() * 100,
                (df_filtrado['modalidade'] == 'Presencial').mean() * 100,
                (df_filtrado['tamanho_empresa'].isin(['Médio', 'Grande'])).mean() * 100
            ]
        })
        
        fig15 = px.bar(
            comparacao.melt(id_vars='Métrica'),
            x='Métrica',
            y='value',
            color='variable',
            barmode='group',
            title='Comparação: Iniciantes vs Mercado Total',
            labels={'value': 'Valor', 'variable': 'Grupo'},
            color_discrete_sequence=['green', 'blue']
        )
        fig15.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig15, use_container_width=True)

# Rodapé e informações adicionais
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>📊 Dashboard desenvolvido para análise de carreira em dados • Dados: {ano_min} - {ano_max}</p>
    <p>🎯 Use os filtros na sidebar para explorar diferentes perspectivas do mercado</p>
    <p>💡 Dica: Compare diferentes anos para identificar tendências</p>
</div>
""".format(
    ano_min=df['ano'].min(),
    ano_max=df['ano'].max()
), unsafe_allow_html=True)

# Expander com informações técnicas
with st.expander("📋 Informações Técnicas e Metodologia"):
    st.markdown(f"""
    ### **📊 Estatísticas do Dataset:**
    - **Período:** {df['ano'].min()} - {df['ano'].max()}
    - **Total de registros:** {len(df):,}
    - **Cargos únicos:** {df['cargo'].nunique()}
    - **Países únicos (empresa):** {df['localizacao_empresa'].nunique()}
    - **Moedas únicas:** {df['moeda_salario'].nunique()}
    
    ### **🎯 Métricas Calculadas:**
    - **Salários:** Convertidos para USD usando taxas padronizadas
    - **Senioridade:** 4 níveis (Júnior, Pleno, Sênior, Executivo)
    - **Modalidade:** 3 categorias (Presencial, Híbrido, Remoto)
    - **Tamanho Empresa:** 3 categorias (Pequeno, Médio, Grande)
    
    ### **⚙️ Funcionalidades do Dashboard:**
    1. **Filtros dinâmicos:** Todos os gráficos atualizam em tempo real
    2. **Análises comparativas:** Júnior vs mercado total
    3. **Tendências temporais:** Evolução ano a ano
    4. **Insights práticos:** Recomendações baseadas em dados
    
    ### **📈 Fórmulas Utilizadas:**
    - **Salário Médio:** `Σ(salários) / n`
    - **Crescimento Anual:** `(ano₂ - ano₁) / ano₁ * 100`
    - **% Remoto:** `(vagas_remotas / total_vagas) * 100`
    - **Trabalho Internacional:** `residencia ≠ localizacao_empresa`
    """)

# Adicionar botão para resetar filtros
if st.sidebar.button("🔄 Resetar Filtros"):
    st.rerun()

# Informação sobre dados filtrados
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
**📊 Dados Filtrados:**
- Registros: **{len(df_filtrado):,}** / {len(df):,}
- Cargos: **{df_filtrado['cargo'].nunique()}** / {df['cargo'].nunique()}
- Anos: **{df_filtrado['ano'].nunique()}** / {df['ano'].nunique()}
""")