# Declaração de Uso de IA

**Nome:** Lucas Menezes
**Data:** 27/10/2026

## Ferramenta

Gemini / Assistente de IA no editor (com as instruções do `streamlit skills` ativadas localmente).

## Prompt usado

### Aula 21 — Esqueleto do layout e filtros dinâmicos
```text
Tenho o rascunho do Dashboard 1 (entregas/rascunho-dashboard1.png) para o dataset Indian Flight Delay (data/clean/dataset.csv). Preciso montar o esqueleto do app.py lendo os dados de src/data_loader.py com @st.cache_data, colocando na sidebar um multiselect para as variáveis quantitativas (VARS_QUANT), um toggle para separar por status_voo ("No Horário" vs "Atrasado") e um loop que crie um st.slider de intervalo para cada variável selecionada respeitando se a coluna é int ou float.
```

### Aula 22 — Adaptação para Altair (150k linhas) e seleção cruzada no Dashboard 2
```text
Estou migrando os gráficos do meu dashboard para Altair seguindo o exemplo da aula, mas meu dataset tem 150.000 linhas e o Altair retorna MaxRowsError ao criar o histograma direto do DataFrame. Como posso pré-calcular os bins no pandas para passar só a tabela agregada para o alt.Chart? Aproveite e mostre como usar alt.selection_point com on_select="rerun" num gráfico de barras agrupado por Airline na segunda aba (st.tabs) para filtrar os 4 st.metric do Dashboard 2.
```

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:**
  - A estrutura base da sidebar com geração dinâmica de `st.slider` diferenciando tipos inteiros e decimais (`pd.api.types.is_integer_dtype`) e o uso de `@st.cache_data` no `src/data_loader.py`.
  - A estratégia de pré-agregar os intervalos (bins) do histograma e o agrupamento por companhia aérea no `pandas` antes de montar o `alt.Chart`, o que resolveu o limite de 5.000 linhas do Altair e deixou a atualização dos gráficos instantânea mesmo com 150.000 voos.
  - O padrão de `alt.selection_point(name="selecao_cia", fields=["Airline"])` combinado com `on_select="rerun"` para permitir que o clique numa barra do Dashboard 2 filtre os cartões de `st.metric`.

- **Modificado:**
  - **Rótulos e layout do Heatmap (Dashboard 1):** os nomes originais das colunas no CSV (como `Previous_Flight_Delay_Minutes` e `Scheduled_Departure_Minute`) eram muito extensos e espremiam a matriz de correlação na coluna da esquerda. Criei manualmente um dicionário de rótulos curtos (`ROTULOS_CURTOS`) e ajustei os ângulos e tamanhos de fonte no Altair para manter a leitura limpa.
  - **Escolha e cálculo das métricas do Dashboard 2:** ajustei as métricas para refletirem o que realmente encontramos na EDA da Aula 11 — priorizando a Taxa de Atrasos, o Atraso Médio na Partida, o Atraso do Voo Anterior (efeito cascata) e a discretização do `Origin_Congestion_Index >= 75` (congestão crítica), além de configurar `delta_color="inverse"` nos KPIs onde valores maiores indicam piora operacional.
  - **Paleta de cores e tema (`.streamlit/config.toml`):** personalizei as cores dos gráficos (`#2d223a` e `#e9d4d0`, mantendo a mesma identidade visual usada no notebook da EDA, junto com `#c84b31` para destaque no tema do Streamlit).

- **Rejeitado:**
  - Rejeitei a primeira sugestão da IA de passar o `df_filtrado` bruto diretamente para o `alt.Chart(df_filtrado).mark_bar()` ou desabilitar a trava com `alt.data_transformers.disable_max_rows()`, pois serializar 150.000 linhas para o navegador deixava a página pesada e lenta a cada movimento de slider.
  - Rejeitei a sugestão de incluir "Temperatura Média" e "Velocidade do Vento" como KPIs principais no Dashboard 2, porque na nossa EDA da Aula 11 ficou comprovado que variáveis meteorológicas isoladas têm correlação praticamente nula ($|r| \le 0{,}04$) com `Departure_Delay` neste dataset, sendo muito mais relevante destacar congestão de origem e atraso herdado da aeronave.
