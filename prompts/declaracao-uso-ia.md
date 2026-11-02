# Declaração de Uso de Inteligência Artificial Generativa

**Atividade Streamlit AVD – 2026.2** — Dashboards com Streamlit (Aulas 21 a 23)

> A versão oficial diagramada no layout da disciplina encontra-se em [`prompts/DECLARACAO_IA.pdf`](DECLARACAO_IA.pdf) (e [`prompts/DECLARACAO_IA.docx`](DECLARACAO_IA.docx)).

## 1. Identificação

| Campo | Informação |
| :--- | :--- |
| **Turma** | ☑ 5A &nbsp;&nbsp; ☐ 5B |
| **Nome Completo** | Lucas Menezes Santana |
| **E-mail** | lms4@cesar.school |
| **Repositório (link)** | https://github.com/Lucasmenezes08/AVD-20262-pratica-streamlit |
| **App Publicado (Streamlit Cloud)** | https://avd-20262-pratica-app-t2e2gvybxtzoatkk68bmxv.streamlit.app |
| **Data de entrega** | 02/11/2026 |

## 3. Declaração geral

- [ ] **Não utilizei** nenhuma ferramenta de IA generativa em nenhuma etapa do projeto.
- [x] **Utilizei** IA generativa, somente nas situações permitidas, e registrei todos os usos nas Seções 4 a 6 (links das conversas ou blocos de registro).

## 4. Ferramentas utilizadas

| Ferramenta | Versão / plano | Em que parte da atividade |
| :--- | :--- | :--- |
| **Streamlit Skills (`streamlit skills`)** | Skill oficial do Streamlit | Padrões da biblioteca, esqueleto inicial do `app.py` (Aula 21) e cache (`@st.cache_data`). |
| **Gemini** | Gemini 2.5 Pro | Esqueleto do `app.py`, sintaxe de gráficos no Altair (Dashboards 1 e 2), debug do `MaxRowsError` e revisão da documentação/deploy (Aula 23). |
| **ChatGPT** | GPT-4o (OpenAI) | Consulta de contraste de cores para o `.streamlit/config.toml` e revisão gramatical de textos. |

## 5. Registro de usos (Opção B — bloco a bloco)

### Uso nº 1
- **Data:** 22/10/2026
- **Ferramenta:** Gemini + Streamlit Skills (`streamlit skills`)
- **Parte da atividade:** `app.py` (esqueleto inicial) e `src/data_loader.py`
- **Finalidade:** Usar a Skill oficial do Streamlit e gerar o esqueleto do `app.py` a partir do rascunho de layout usando o Template de Prompt (Aula 21).
- **O que foi pedido:** Enviei o rascunho `entregas/rascunho-dashboard1.png` junto com o template `prompts/layout-skeleton-prompt.md` pedindo a estrutura base com leitura via `@st.cache_data`, `multiselect` para variáveis quantitativas, `toggle` de classe e sliders dinâmicos.
- **O que foi aproveitado e o que foi modificado:** Aproveitei o esqueleto de colunas, o cache e a criação automática dos sliders diferenciando `int` e `float`. Modifiquei a exibição dos nomes criando o dicionário `ROTULOS_CURTOS` para evitar truncamento na barra lateral.
- **Como verifiquei que estava correto:** Executei `streamlit run app.py` localmente e testei cada slider e seletor conferindo a contagem de voos filtrados.
- **Link ou anexo:** Prompt documentado em `prompts/layout-skeleton-prompt.md` e trecho marcado com `# [IA]` no código.

### Uso nº 2
- **Data:** 27/10/2026
- **Ferramenta:** Gemini
- **Parte da atividade:** `app.py` — Dashboard 1 (Correlação e Distribuição em Altair)
- **Finalidade:** Apoio com a sintaxe de biblioteca de visualização (Altair) e depuração de erro (`MaxRowsError` com 150.000 linhas).
- **O que foi pedido:** Pedi apoio para escrever a sintaxe do mapa de calor triangular no Altair e para corrigir o erro `MaxRowsError` ao plotar o histograma com as 150.000 linhas do dataset.
- **O que foi aproveitado e o que foi modificado:** Aproveitei a ideia de pré-calcular os intervalos (`bins`) no `pandas` antes de passar ao `alt.Chart` e a sobreposição `mark_rect + mark_text`. Rejeitei desabilitar o limite de 5.000 linhas do Altair para não travar o navegador e ajustei as cores para o padrão da minha EDA (`#2d223a` e `#e9d4d0`).
- **Como verifiquei que estava correto:** Comparei os coeficientes de Spearman e o formato do histograma no dashboard com os gráficos originais do notebook `notebooks/eda.ipynb` e testei com 0, 1 e 2+ variáveis.
- **Link ou anexo:** Registrado bloco a bloco nesta seção e demarcado em `app.py` (`# [IA] Gemini`).

### Uso nº 3
- **Data:** 27/10/2026
- **Ferramenta:** Gemini + Streamlit Skills (`streamlit skills`)
- **Parte da atividade:** `app.py` — Dashboard 2 (Seleção cruzada no Altair e cartões `st.metric`)
- **Finalidade:** Apoio com a sintaxe de visualização interativa no Altair (seleção cruzada) e dúvidas sobre parâmetros do Streamlit (`st.tabs` e `st.metric`).
- **O que foi pedido:** Consultei como configurar `alt.selection_point` junto com `on_select="rerun"` no gráfico de barras por companhia aérea para filtrar dinamicamente os cartões de `st.metric` na segunda aba.
- **O que foi aproveitado e o que foi modificado:** Aproveitei a leitura da seleção via `evento_cia.selection` e o uso de `delta_color="inverse"`. Modifiquei os cálculos para aplicar as 4 métricas operacionais que defini a partir da EDA, rejeitando sugestões genéricas de KPIs climáticos.
- **Como verifiquei que estava correto:** Cliquei em cada barra de companhia aérea no app e validei os valores exibidos nos 4 KPIs contra o cálculo direto no `pandas`.
- **Link ou anexo:** Registrado bloco a bloco nesta seção e demarcado em `app.py` (`# [IA] Gemini`).

### Uso nº 4
- **Data:** 27/10/2026
- **Ferramenta:** ChatGPT
- **Parte da atividade:** `.streamlit/config.toml` e `entregas/justificativa-metricas.md`
- **Finalidade:** Apoio na criação de identidade visual (`.streamlit/config.toml`) e revisão ortográfica/gramatical de textos escritos por mim.
- **O que foi pedido:** Consultei sugestões de cores de fundo e destaque com bom contraste para acompanhar a paleta da minha EDA no `config.toml` e pedi revisão gramatical do texto que escrevi em `entregas/justificativa-metricas.md`.
- **O que foi aproveitado e o que foi modificado:** Aproveitei a combinação de fundo claro (`#f4f1ea`) com destaque terracota (`#c84b31`) no `config.toml` e correções pontuais de pontuação, mantendo inalteradas minhas escolhas e justificativas das métricas.
- **Como verifiquei que estava correto:** Verifiquei a legibilidade dos componentes localmente e no link publicado no Streamlit Community Cloud.
- **Link ou anexo:** Registrado bloco a bloco nesta seção e demarcado em `.streamlit/config.toml` (`# [IA] ChatGPT`).

### Uso nº 5
- **Data:** 02/11/2026
- **Ferramenta:** Gemini
- **Parte da atividade:** `README.md`, comentários `# [IA]` no código e atualização da documentação em `prompts/`
- **Finalidade:** Revisar a ortografia e clareza do README e de textos escritos por mim, além de apoio para padronizar as marcações `# [IA]` e o checklist de deploy (Aula 23).
- **O que foi pedido:** Pedi apoio para conferir o checklist de entrega da Aula 23, padronizar os comentários `# [IA] <ferramenta> – <finalidade>` no código conforme o novo documento da atividade e revisar a atualização do `README.md` com o link publicado no Streamlit Community Cloud.
- **O que foi aproveitado e o que foi modificado:** Aproveitei a revisão de formatação da documentação e a padronização dos comentários `# [IA]` nos trechos correspondentes de `app.py`, `src/data_loader.py` e `.streamlit/config.toml`, mantendo a descrição fiel às etapas que realizei.
- **Como verifiquei que estava correto:** Testei a abertura do link público em janela anônima, rodei os testes locais da aplicação e conferi os arquivos versionados no GitHub.
- **Link ou anexo:** Registrado bloco a bloco nesta seção e refletido nos commits finais de documentação do repositório.

## 6. Trechos de código feitos com apoio de IA

| Arquivo / parte | Teve apoio de IA? | Tipo de apoio |
| :--- | :--- | :--- |
| `app.py` (esqueleto) | ☑ Sim &nbsp; ☐ Não | Esqueleto inicial via Template de Prompt + Streamlit Skills (sidebar e colunas) |
| Dashboard 1 (correlação + distribuição) | ☑ Sim &nbsp; ☐ Não | Sintaxe do Altair (heatmap triangular) e pré-agregação de bins para evitar `MaxRowsError` |
| Dashboard 2 (KPIs) | ☑ Sim &nbsp; ☐ Não | Sintaxe de seleção cruzada (`alt.selection_point` + `on_select="rerun"`) e parâmetros do `st.metric` |
| Deploy / configuração | ☑ Sim &nbsp; ☐ Não | Consulta de contraste de cores para o tema customizado em `.streamlit/config.toml` |
| `src/data_loader.py` | ☑ Sim &nbsp; ☐ Não | Função de leitura do CSV tratado com decorador `@st.cache_data` via Streamlit Skills |

## 7. Reflexão individual

Utilizei as ferramentas de IA como apoio técnico para agilizar a estruturação de layout, consultar a sintaxe do Altair e depurar erros de execução. O Gemini (com o `streamlit skills` ativo) auxiliou na geração do esqueleto inicial do `app.py` a partir do rascunho da Aula 21 e na sintaxe de seleção cruzada (`on_select="rerun"`) do Dashboard 2, enquanto o ChatGPT foi consultado para validar o contraste das cores do tema (`.streamlit/config.toml`) e revisar a gramática da documentação. Durante a implementação do Dashboard 1, rejeitei a sugestão inicial da IA de desabilitar a trava de 5.000 linhas do Altair para plotar as 150.000 linhas brutas, preferindo pré-calcular os intervalos do histograma no `pandas` para garantir fluidez. No planejamento do Dashboard 2, também descartei sugestões genéricas de usar médias de temperatura e velocidade do vento como KPIs principais. Garanti que os indicadores refletissem minha própria escolha baseando-me diretamente nos resultados da minha EDA da Aula 11, onde verifiquei que variáveis meteorológicas isoladas possuem correlação quase nula ($|r| \le 0{,}04$) com o atraso de partida, enquanto a congestão na origem ($r = 0{,}60$) e o atraso do voo anterior ($r = 0{,}50$) explicam o efeito cascata real da malha. Com isso, selecionei e validei os cálculos no `pandas` antes de integrá-los ao dashboard.
