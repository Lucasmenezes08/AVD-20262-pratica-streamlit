import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Análise de Atrasos de Voos na Índia — Dashboards",
    layout="wide",
)

st.title("Análise Exploratória e Operacional — Indian Flight Delay Dataset")

df = load_data()

# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = [
    "Scheduled_Departure_Hour",
    "Scheduled_Departure_Minute",
    "Temperature_C",
    "Humidity_pct",
    "Wind_Speed_kmh",
    "Visibility_km",
    "Rainfall_mm",
    "Cloud_Cover_pct",
    "Origin_Congestion_Index",
    "Previous_Flight_Delay_Minutes",
    "Turnaround_Risk_Index",
    "Departure_Delay",
]

ROTULOS_CURTOS = {
    "Scheduled_Departure_Hour": "Hora Partida",
    "Scheduled_Departure_Minute": "Min. Partida",
    "Temperature_C": "Temp. (°C)",
    "Humidity_pct": "Umidade (%)",
    "Wind_Speed_kmh": "Vento (km/h)",
    "Visibility_km": "Visib. (km)",
    "Rainfall_mm": "Chuva (mm)",
    "Cloud_Cover_pct": "Nuvens (%)",
    "Origin_Congestion_Index": "Congestão Orig.",
    "Previous_Flight_Delay_Minutes": "Atraso Voo Ant.",
    "Turnaround_Risk_Index": "Risco Turnaround",
    "Departure_Delay": "Atraso Partida",
}

COR_NO_HORARIO = "#e9d4d0"
COR_ATRASADO = "#2d223a"
COR_PADRAO = "#c84b31"
CORES_CLASSE = alt.Scale(domain=["No Horário", "Atrasado"], range=[COR_NO_HORARIO, COR_ATRASADO])


@st.cache_data
def calcular_histograma_agregado(dados: pd.DataFrame, coluna: str, por_classe: bool, bins: int = 24) -> pd.DataFrame:
    """Agrega os intervalos do histograma em pandas para evitar o limite de 5.000 linhas do Altair."""
    serie = dados[coluna].dropna()
    if serie.empty:
        return pd.DataFrame()
    cortes = np.linspace(float(serie.min()), float(serie.max()), bins + 1)
    if cortes[0] == cortes[-1]:
        cortes[-1] = cortes[0] + 1.0
    indices = np.clip(np.digitize(dados[coluna], cortes, right=True) - 1, 0, bins - 1)
    aux = pd.DataFrame({
        "bin_ini": cortes[indices],
        "bin_fim": cortes[indices + 1],
        "status_voo": dados["status_voo"].values,
    })
    cols_grupo = ["bin_ini", "bin_fim", "status_voo"] if por_classe else ["bin_ini", "bin_fim"]
    return aux.groupby(cols_grupo, as_index=False).size().rename(columns={"size": "contagem"})


# Sidebar: filtros globais de variáveis quantitativas e intervalos
with st.sidebar:
    st.header("Filtros — Variáveis Quantitativas")

    variaveis = st.multiselect(
        "Variáveis Quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
        format_func=lambda v: f"{ROTULOS_CURTOS.get(v, v)} ({v})",
        help="Selecione as variáveis quantitativas que deseja analisar no Dashboard 1.",
    )

    separar_por_classe = st.toggle(
        "Distinguir por Classe",
        value=False,
        help="Colore a distribuição pela classe (status_voo: No Horário ou Atrasado).",
    )

    intervalos = {}
    for var in variaveis:
        if pd.api.types.is_integer_dtype(df[var]):
            minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
        else:
            minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1
        intervalos[var] = st.slider(
            f"Intervalo de {ROTULOS_CURTOS.get(var, var)}",
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            key=f"intervalo_{var}",
        )

# Aplica filtros de intervalo da sidebar
df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

st.caption(
    f"{len(df_filtrado):,} de {len(df):,} voos dentro dos intervalos selecionados na barra lateral.".replace(",", ".")
)

# Abas separando Dashboard 1 e Dashboard 2
tab_dash1, tab_dash2 = st.tabs([
    "Dashboard 1 — Correlação e Distribuição",
    "Dashboard 2 — KPIs e Desempenho Operacional",
])

# =========================================================================
# ABA 1: DASHBOARD 1 (Correlação de Spearman + Distribuição em Altair)
# =========================================================================
with tab_dash1:
    col_correlacao, col_distribuicao = st.columns([1.1, 1.2], gap="large")

    with col_correlacao:
        st.subheader("Correlação (Spearman)")

        if len(variaveis) < 2:
            st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
        elif len(df_filtrado) < 30:
            st.warning("Poucos voos nos intervalos escolhidos para calcular a correlação.")
        else:
            corr = (
                df_filtrado[variaveis]
                .corr(method="spearman")
                .rename_axis(index="var_y", columns="var_x")
                .stack()
                .rename("correlacao")
                .reset_index()
            )
            ordem = {var: i for i, var in enumerate(variaveis)}
            corr = corr[corr["var_y"].map(ordem) > corr["var_x"].map(ordem)].copy()
            corr["label_x"] = corr["var_x"].map(ROTULOS_CURTOS)
            corr["label_y"] = corr["var_y"].map(ROTULOS_CURTOS)
            ordem_x = [ROTULOS_CURTOS[v] for v in variaveis[:-1]]
            ordem_y = [ROTULOS_CURTOS[v] for v in variaveis[1:]]

            base = alt.Chart(corr).encode(
                x=alt.X(
                    "label_x:N",
                    title=None,
                    sort=ordem_x,
                    axis=alt.Axis(labelAngle=-35, labelFontSize=11),
                ),
                y=alt.Y(
                    "label_y:N",
                    title=None,
                    sort=ordem_y,
                    axis=alt.Axis(labelFontSize=11),
                ),
            )
            heatmap = base.mark_rect().encode(
                color=alt.Color(
                    "correlacao:Q",
                    title="Spearman (r)",
                    scale=alt.Scale(scheme="redblue", domain=[-1, 1], reverse=True),
                ),
                tooltip=[
                    alt.Tooltip("label_y:N", title="Variável Y"),
                    alt.Tooltip("label_x:N", title="Variável X"),
                    alt.Tooltip("correlacao:Q", title="Correlação (r)", format=".2f"),
                ],
            )
            valores = base.mark_text(fontSize=10 if len(variaveis) > 8 else 13).encode(
                text=alt.Text("correlacao:Q", format=".2f"),
                color=alt.condition(
                    "abs(datum.correlacao) > 0.5", alt.value("white"), alt.value("black")
                ),
            )

            st.altair_chart(
                (heatmap + valores).properties(height=470),
                width="stretch",
                alt="Mapa de calor do triângulo inferior da correlação de Spearman",
            )

    with col_distribuicao:
        st.subheader("Distribuição")

        if not variaveis:
            st.warning("Selecione pelo menos 1 variável para ver a distribuição.")
        elif df_filtrado.empty:
            st.warning("Nenhum voo dentro dos intervalos escolhidos.")
        else:
            var_hist = st.selectbox(
                "Variável para o histograma",
                options=variaveis,
                index=len(variaveis) - 1,
                format_func=lambda v: f"{ROTULOS_CURTOS.get(v, v)} ({v})",
                help="Escolha a variável quantitativa cuja distribuição será exibida.",
            )

            df_bins = calcular_histograma_agregado(
                df_filtrado, var_hist, separar_por_classe, bins=24
            )
            rotulo_var = f"{ROTULOS_CURTOS.get(var_hist, var_hist)} ({var_hist})"

            histograma = (
                alt.Chart(df_bins)
                .mark_bar(opacity=0.85)
                .encode(
                    x=alt.X("bin_ini:Q", bin="binned", title=rotulo_var),
                    x2="bin_fim:Q",
                    y=alt.Y("contagem:Q", title="Quantidade de Voos"),
                )
                .properties(height=400)
            )
            if separar_por_classe:
                histograma = histograma.encode(
                    color=alt.Color(
                        "status_voo:N",
                        title="Status do Voo",
                        scale=CORES_CLASSE,
                    ),
                    tooltip=[
                        alt.Tooltip("status_voo:N", title="Status do Voo"),
                        alt.Tooltip("bin_ini:Q", title="Intervalo inicial", format=".1f"),
                        alt.Tooltip("bin_fim:Q", title="Intervalo final", format=".1f"),
                        alt.Tooltip("contagem:Q", title="Voos", format=","),
                    ],
                )
            else:
                histograma = histograma.mark_bar(color=COR_PADRAO).encode(
                    tooltip=[
                        alt.Tooltip("bin_ini:Q", title="Intervalo inicial", format=".1f"),
                        alt.Tooltip("bin_fim:Q", title="Intervalo final", format=".1f"),
                        alt.Tooltip("contagem:Q", title="Voos", format=","),
                    ]
                )

            st.altair_chart(
                histograma,
                width="stretch",
                alt=f"Histograma da variável {var_hist}",
            )

# =========================================================================
# ABA 2: DASHBOARD 2 (KPIs + Gráficos de Barras Agrupados com Cross-Filter)
# =========================================================================
with tab_dash2:
    st.subheader("Painel de Indicadores Operacionais (KPIs)")

    # Controles dedicados do Dashboard 2
    f_col1, f_col2, f_col3 = st.columns([1.3, 1.3, 1])

    opcoes_cias = sorted(df["Airline"].dropna().unique().tolist())
    opcoes_clima = sorted(df["Weather"].dropna().unique().tolist())

    with f_col1:
        cias_filtro = st.multiselect(
            "Companhia Aérea (Airline)",
            options=opcoes_cias,
            default=opcoes_cias,
            key="d2_cias",
        )
    with f_col2:
        clima_filtro = st.multiselect(
            "Condição Climática (Weather)",
            options=opcoes_clima,
            default=opcoes_clima,
            key="d2_clima",
        )
    with f_col3:
        filtro_pico = st.selectbox(
            "Janela de Operação (Peak_Hour)",
            options=["Todos os horários", "Apenas Horário de Pico", "Fora de Pico"],
            index=0,
            key="d2_pico",
        )

    df_d2 = df_filtrado[
        df_filtrado["Airline"].isin(cias_filtro) & df_filtrado["Weather"].isin(clima_filtro)
    ]
    if filtro_pico == "Apenas Horário de Pico":
        df_d2 = df_d2[df_d2["Peak_Hour"] == 1]
    elif filtro_pico == "Fora de Pico":
        df_d2 = df_d2[df_d2["Peak_Hour"] == 0]

    if df_d2.empty:
        st.warning("Nenhum voo encontrado para os filtros selecionados no Dashboard 2.")
    else:
        # Prepara agregação por Companhia Aérea para o gráfico de barras com seleção cruzada
        resumo_cia = (
            df_d2.groupby("Airline", as_index=False)
            .agg(
                voos=("Flight_Number", "count"),
                atraso_medio=("Departure_Delay", "mean"),
                taxa_atraso=("Delay_Target", lambda s: (s > 0).mean() * 100),
            )
            .sort_values("atraso_medio", ascending=False)
        )

        selecao_cia = alt.selection_point(name="selecao_cia", fields=["Airline"])

        grafico_barras_cia = (
            alt.Chart(resumo_cia)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Airline:N", sort="-y", title="Companhia Aérea", axis=alt.Axis(labelAngle=-25)),
                y=alt.Y("atraso_medio:Q", title="Atraso Médio na Partida (min)"),
                color=alt.condition(
                    selecao_cia,
                    alt.Color(
                        "atraso_medio:Q",
                        title="Atraso (min)",
                        scale=alt.Scale(scheme="orangered"),
                    ),
                    alt.value("#d5d1cd"),
                ),
                opacity=alt.condition(selecao_cia, alt.value(1.0), alt.value(0.45)),
                tooltip=[
                    alt.Tooltip("Airline:N", title="Companhia Aérea"),
                    alt.Tooltip("atraso_medio:Q", title="Atraso Médio (min)", format=".1f"),
                    alt.Tooltip("taxa_atraso:Q", title="Taxa de Atrasos (%)", format=".1f"),
                    alt.Tooltip("voos:Q", title="Total de Voos", format=","),
                ],
            )
            .add_params(selecao_cia)
            .properties(height=360, title="Atraso Médio por Companhia Aérea (clique em uma barra para filtrar)")
        )

        # Container para os KPIs no topo (atualizado pela seleção do gráfico abaixo)
        container_kpis = st.container()

        st.markdown("#### Desempenho por Companhia Aérea e Nível de Congestão na Origem")
        g_col1, g_col2 = st.columns([1.1, 1.1], gap="large")

        with g_col1:
            evento_cia = st.altair_chart(
                grafico_barras_cia,
                key="chart_barras_cia",
                on_select="rerun",
                width="stretch",
            )

        # Verifica se o usuário clicou em alguma companhia aérea no gráfico de barras
        itens_clicados = []
        if evento_cia and hasattr(evento_cia, "selection"):
            itens_clicados = evento_cia.selection.get("selecao_cia", [])
        cias_selecionadas = [item["Airline"] for item in itens_clicados if "Airline" in item]

        df_kpis = df_d2[df_d2["Airline"].isin(cias_selecionadas)] if cias_selecionadas else df_d2

        # Cálculo das referências globais da base (para exibir o delta comparativo)
        taxa_base = (df["status_voo"] == "Atrasado").mean() * 100
        atraso_base = df["Departure_Delay"].mean()
        atraso_ant_base = df["Previous_Flight_Delay_Minutes"].mean()
        critica_base = (df["Origin_Congestion_Index"] >= 75).mean() * 100

        # Cálculo das 4 métricas sobre o subconjunto ativo (df_kpis)
        taxa_atraso = (df_kpis["status_voo"] == "Atrasado").mean() * 100
        atraso_medio = df_kpis["Departure_Delay"].mean()
        atraso_voo_ant = df_kpis["Previous_Flight_Delay_Minutes"].mean()
        prop_congestao_critica = (df_kpis["Origin_Congestion_Index"] >= 75).mean() * 100

        with container_kpis:
            if cias_selecionadas:
                st.info(
                    f"Filtro interativo ativo no gráfico: **{', '.join(cias_selecionadas)}** "
                    f"({len(df_kpis):,} voos). Clique em uma área vazia do gráfico para limpar.".replace(",", ".")
                )

            k1, k2, k3, k4 = st.columns(4, gap="small")
            k1.metric(
                "Taxa de Atrasos Operacionais",
                f"{taxa_atraso:.1f}%",
                delta=f"{taxa_atraso - taxa_base:+.1f} p.p. vs malha",
                delta_color="inverse",
                border=True,
                help="Proporção de voos que partiram com atraso (Delay_Target > 0).",
            )
            k2.metric(
                "Atraso Médio na Partida",
                f"{atraso_medio:.1f} min",
                delta=f"{atraso_medio - atraso_base:+.1f} min vs malha",
                delta_color="inverse",
                border=True,
                help="Tempo médio de atraso na decolagem (Departure_Delay).",
            )
            k3.metric(
                "Atraso Herdado (Voo Anterior)",
                f"{atraso_voo_ant:.1f} min",
                delta=f"{atraso_voo_ant - atraso_ant_base:+.1f} min vs malha",
                delta_color="inverse",
                border=True,
                help="Média de atraso acumulado da etapa anterior da aeronave (Previous_Flight_Delay_Minutes).",
            )
            k4.metric(
                "Voos sob Congestão Crítica (≥75)",
                f"{prop_congestao_critica:.1f}%",
                delta=f"{prop_congestao_critica - critica_base:+.1f} p.p. vs malha",
                delta_color="inverse",
                border=True,
                help="Percentual de voos operando com Origin_Congestion_Index >= 75.",
            )

        with g_col2:
            # Discretização de Origin_Congestion_Index combinada com Condição Climática
            faixas = pd.cut(
                df_kpis["Origin_Congestion_Index"],
                bins=[-1, 50, 75, 101],
                labels=["Baixa (<50)", "Moderada (50–74)", "Crítica (≥75)"],
            )
            resumo_congestao = (
                df_kpis.assign(faixa_congestao=faixas)
                .groupby(["faixa_congestao", "status_voo"], observed=False, as_index=False)
                .agg(
                    voos=("Flight_Number", "count"),
                    atraso_medio=("Departure_Delay", "mean"),
                )
            )

            grafico_congestao = (
                alt.Chart(resumo_congestao)
                .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                .encode(
                    x=alt.X(
                        "faixa_congestao:N",
                        sort=["Baixa (<50)", "Moderada (50–74)", "Crítica (≥75)"],
                        title="Faixa de Congestão no Aeroporto de Origem",
                        axis=alt.Axis(labelAngle=0),
                    ),
                    y=alt.Y("voos:Q", title="Volume de Voos"),
                    color=alt.Color("status_voo:N", title="Status do Voo", scale=CORES_CLASSE),
                    xOffset="status_voo:N",
                    tooltip=[
                        alt.Tooltip("faixa_congestao:N", title="Congestão na Origem"),
                        alt.Tooltip("status_voo:N", title="Status do Voo"),
                        alt.Tooltip("voos:Q", title="Quantidade de Voos", format=","),
                        alt.Tooltip("atraso_medio:Q", title="Atraso Médio (min)", format=".1f"),
                    ],
                )
                .properties(
                    height=360,
                    title="Volume de Voos por Faixa de Congestão na Origem e Status",
                )
            )
            st.altair_chart(grafico_congestao, width="stretch")
