# Justificativa das métricas — Dashboard 2

## Métrica 1: Taxa de Atrasos Operacionais (%)
- **Variável:** `status_voo` / `Delay_Target` (indicador binário de atraso na partida, onde `Delay_Target > 0` define voo `"Atrasado"` e `0` define `"No Horário"`).
- **O que mede:** A proporção percentual de voos que partiram fora do horário programado dentro do recorte analisado, acompanhada da variação (`delta` em pontos percentuais) frente à média global da malha (86,6%).
- **Por que foi escolhida:** Resume em um único número imediato a confiabilidade e a pontualidade operacional (*On-Time Performance* invertido), sem exigir que o usuário interprete distribuições completas.
- **Público-alvo:** Gestores de operações aéreas (CCO), coordenadores de malha e autoridades aeroportuárias.
- **Qual decisão pode ser apoiada por essa métrica?** Priorizar auditorias operacionais em companhias aéreas ou faixas horárias cuja taxa de atraso supere a média da malha e renegociar janelas de *slot* em aeroportos críticos.
- **O que comunica ao público-alvo:** Qual é a chance real de um voo sofrer atraso naquele recorte específico e se o cenário selecionado está melhor ou pior do que o padrão geral do sistema aéreo indiano.

## Métrica 2: Atraso Médio na Partida (min)
- **Variável:** `Departure_Delay` (tempo de atraso na decolagem, em minutos).
- **O que mede:** A média aritmética dos minutos de atraso na partida dos voos filtrados (com referência complementar da mediana e comparação `delta` em relação à média geral de 42,7 minutos).
- **Por que foi escolhida:** Enquanto a taxa de atrasos mostra a *frequência* do problema, o atraso médio mede a *severidade* do impacto no tempo de viagem e no planejamento de tripulação e conexões.
- **Público-alvo:** Equipes de planejamento de escala de tripulação, atendimento ao passageiro e analistas de logística aérea.
- **Qual decisão pode ser apoiada por essa métrica?** Dimensionar folgas (*buffers*) entre conexões domésticas e acionar planos de contingência de solo quando o atraso médio ultrapassar patamares críticos (> 45 minutos).
- **O que comunica ao público-alvo:** O tempo médio de espera adicional imposto às operações e aos passageiros no recorte filtrado.

## Métrica 3: Atraso Médio Herdado do Voo Anterior (min)
- **Variável:** `Previous_Flight_Delay_Minutes` (atraso acumulado da etapa imediatamente anterior cumprida pela mesma aeronave, em minutos).
- **O que mede:** A média em minutos do atraso que a aeronave já trazia antes de iniciar o procedimento de *turnaround* (preparação em solo) para o voo atual, além de comparar com o atraso final de partida.
- **Por que foi escolhida:** Na EDA da Aula 11, identificamos correlação positiva relevante ($r = 0{,}50$) entre o atraso do voo anterior, o risco de *turnaround* ($r = 0{,}72$) e o atraso de partida. Essa métrica isola quanto do problema vem do "efeito cascata" na rotação da frota.
- **Público-alvo:** Coordenadores de manutenção de linha, equipes de solo (*ground handling*) e planejadores de rotação de frota.
- **Qual decisão pode ser apoiada por essa métrica?** Alocar aeronaves reserva em *hubs* estratégicos ou ampliar o tempo mínimo de solo (*turnaround time*) em rotas que acumulam atraso em cadeia ao longo do dia.
- **O que comunica ao público-alvo:** O quanto os atrasos atuais são consequência de falhas na absorção de atrasos de etapas anteriores da aeronave.

## Métrica 4: Proporção de Voos sob Congestão Crítica na Origem (%)
- **Variável:** `Origin_Congestion_Index` (índice contínuo de 0 a 100 que mede o nível de congestionamento do aeroporto de origem no momento da partida, discretizado na faixa crítica $\ge 75$).
- **O que mede:** A porcentagem de voos que operaram sob condição de saturação severa de pátio/pista no aeroporto de origem (`Origin_Congestion_Index >= 75`), acompanhada do valor médio do índice no recorte.
- **Por que foi escolhida:** Na EDA, `Origin_Congestion_Index` apresentou a maior correlação direta com o risco de giro e com o atraso na partida ($r = 0{,}60$). A discretização em faixa crítica ($\ge 75$) transforma um índice abstrato em um indicador acionável e fácil de interpretar.
- **Público-alvo:** Operadores de controle de pátio/torre e gerentes de infraestrutura aeroportuária.
- **Qual decisão pode ser apoiada por essa métrica?** Redistribuir decolagens para horários fora de pico (`Peak_Hour = 0`) e limitar a concentração simultânea de pousos e decolagens nos terminais mais saturados.
- **O que comunica ao público-alvo:** A parcela da malha aérea que está operando no limite da capacidade física do aeroporto de origem.
