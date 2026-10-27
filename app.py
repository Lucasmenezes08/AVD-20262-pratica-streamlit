import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Análise de Atrasos de Voos na Índia — Dashboard",
    layout="wide",
)

st.title("Avaliação de Correlação e Distribuição — Indian Flight Delay Dataset")

df = load_data()

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


@st.cache_data
def calcular_histograma_agregado(dados: pd.DataFrame, coluna: str, por_classe: bool, bins: int = 20) -> pd.DataFrame:
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


with st.sidebar:
    st.header("Filtros")

    variaveis = st.multiselect(
        "Variáveis Quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
        format_func=lambda v: f"{ROTULOS_CURTOS.get(v, v)} ({v})",
        help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
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

df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

st.caption(
    f"{len(df_filtrado):,} de {len(df):,} voos dentro dos intervalos escolhidos.".replace(",", ".")
)

col_correlacao, col_distribuicao = st.columns([1.1, 1.2], gap="large")

COR_NO_HORARIO = "#e9d4d0"
COR_ATRASADO = "#2d223a"
COR_PADRAO = "#c84b31"
CORES_CLASSE = alt.Scale(domain=["No Horário", "Atrasado"], range=[COR_NO_HORARIO, COR_ATRASADO])

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
            x=alt.X("label_x:N", title=None, sort=ordem_x, axis=alt.Axis(labelAngle=-35, labelFontSize=11)),
            y=alt.Y("label_y:N", title=None, sort=ordem_y, axis=alt.Axis(labelFontSize=11)),
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
            color=alt.condition("abs(datum.correlacao) > 0.5", alt.value("white"), alt.value("black")),
        )
        st.altair_chart((heatmap + valores).properties(height=470), width="stretch")

with col_distribuicao:
    st.subheader("Distribuição")

    if not variaveis:
        st.warning("Selecione pelo menos 1 variável para ver a distribuição.")
    elif df_filtrado.empty:
        st.warning("Nenhum voo dentro dos intervalos escolhidos.")
    else:
        var_hist = st.selectbox(
            "Variável para inspecionar a distribuição",
            options=variaveis,
            index=len(variaveis) - 1,
            format_func=lambda v: f"{ROTULOS_CURTOS.get(v, v)} ({v})",
        )
        df_bins = calcular_histograma_agregado(df_filtrado, var_hist, separar_por_classe, bins=25)
        rotulo_var = f"{ROTULOS_CURTOS.get(var_hist, var_hist)} ({var_hist})"

        hist = (
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
            hist = hist.encode(
                color=alt.Color("status_voo:N", title="Status do Voo", scale=CORES_CLASSE),
                tooltip=[
                    alt.Tooltip("status_voo:N", title="Status"),
                    alt.Tooltip("bin_ini:Q", title="De", format=".1f"),
                    alt.Tooltip("bin_fim:Q", title="Até", format=".1f"),
                    alt.Tooltip("contagem:Q", title="Voos", format=","),
                ],
            )
        else:
            hist = hist.mark_bar(color=COR_PADRAO).encode(
                tooltip=[
                    alt.Tooltip("bin_ini:Q", title="De", format=".1f"),
                    alt.Tooltip("bin_fim:Q", title="Até", format=".1f"),
                    alt.Tooltip("contagem:Q", title="Voos", format=","),
                ]
            )
        st.altair_chart(hist, width="stretch")
