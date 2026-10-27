# Template: rascunho de layout → esqueleto do app

Preencha cada bloco e envie à ferramenta de IA.

## Contexto

Sou aluno da disciplina de Análise e Visualização de Dados (Cesar School, 2026.2) construindo um aplicativo em Streamlit a partir da EDA feita na Aula 11 sobre o dataset **Indian Flight Delay** (`data/clean/dataset.csv`, 150.000 linhas). O app é dividido em duas abas (`st.tabs`):
- **Dashboard 1:** análise de correlação (Spearman) e distribuição das 12 variáveis quantitativas (`Scheduled_Departure_Hour`, `Scheduled_Departure_Minute`, `Temperature_C`, `Humidity_pct`, `Wind_Speed_kmh`, `Visibility_km`, `Rainfall_mm`, `Cloud_Cover_pct`, `Origin_Congestion_Index`, `Previous_Flight_Delay_Minutes`, `Turnaround_Risk_Index`, `Departure_Delay`), distinguindo pela coluna `status_voo` (`No Horário` vs `Atrasado`).
- **Dashboard 2:** painel de KPIs operacionais e análise de atrasos por Companhia Aérea (`Airline`), Condição Climática (`Weather`) e faixa de congestão no aeroporto de origem (`Origin_Congestion_Index`).

## Entrada

Rascunhos anexados em `entregas/rascunho-dashboard1.png` e `entregas/rascunho-dashboard2.jpg`.
- **Layout do Dashboard 1:** sidebar à esquerda com `st.multiselect` das variáveis quantitativas, `st.toggle` para colorir por `status_voo` e `st.slider` de intervalo para cada variável ativa; área principal dividida em 2 colunas (`Correlação` à esquerda com heatmap de Spearman e `Distribuição` à direita com histogramas).
- **Layout do Dashboard 2:** filtros de operação (Companhia Aérea, Condição Climática e Horário de Pico), linha superior com 4 cartões `st.metric` (Taxa de Atrasos, Atraso Médio na Partida, Atraso Herdado do Voo Anterior e % sob Congestão Crítica) e linha inferior com 2 gráficos de barras interativos em Altair.

## Restrições

- Utilizar `streamlit` e `altair` (`st.altair_chart`).
- Carregar os dados exclusivamente via `src/data_loader.py` usando `@st.cache_data`.
- Como o CSV tem 150.000 linhas, agregar os dados com `pandas` antes de passar ao `alt.Chart` para não estourar o limite de 5.000 linhas do Altair.
- Tratar os cenários de borda no Dashboard 1 (0 variáveis, 1 variável e 2+ variáveis selecionadas).

## Formato de saída

Código estruturado do `app.py` separado em abas (`st.tabs`), mantendo comentários curtos em cada bloco para facilitar ajustes manuais nas métricas e nos gráficos.
