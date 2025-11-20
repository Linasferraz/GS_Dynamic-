## Integrantes
Carolina Santana Ferraz RM: 86833
Evelyn Choque RM: 557929
Milena Codinhoto RM: 554682

# MenteNeural – Programação Dinâmica Aplicada ao Bem-Estar no Trabalho

Disciplina: Dynamic Programming
Global Solution: O Futuro do Trabalho

## Resumo

Este projeto apresenta uma solução em Python utilizando recursão, memoização, merge sort recursivo e o algoritmo da mochila (knapsack), aplicada ao tema da Global Solution sobre ferramentas de monitoramento de bem-estar e saúde mental no ambiente corporativo.
A aplicação simula recomendações automáticas de bem-estar para colaboradores com base em um índice de estresse calculado a partir de dados comportamentais.

## Objetivo

* Processar informações de colaboradores (mínimo exigido: 20 registros; utilizados: 22)
* Calcular o nível de estresse de forma recursiva
* Ordenar os colaboradores utilizando merge sort recursivo
* Selecionar intervenções de bem-estar usando o algoritmo da mochila
* Utilizar recursão e memoização em todas as funções principais
* Gerar uma estrutura de saída (DataFrame e CSV)

## Entradas

Os dados de cada colaborador incluem:

* avg_continuous_minutes
* num_meetings
* self_report
* last_pause_minutes

A solução também utiliza uma lista de intervenções, cada uma contendo:

* tempo necessário
* benefício emocional

Além disso, há um limite máximo de tempo disponível por colaborador (ex.: 30 minutos).

## Saídas

* Lista ordenada por nível de estresse
* Recomendações de bem-estar calculadas via programação dinâmica
* DataFrame final contendo todas as informações processadas
* Arquivo gerado automaticamente: menteneural_report.csv

## Explicação das Funções (exigência do professor)

1. **generate_dataset_recursive()**
   Gera recursivamente um conjunto de 22 registros sintéticos de colaboradores.
   Garante o requisito mínimo de 20 dados obrigatórios.

2. **compute_stress_indices_recursive()**
   Calcula o stress_index de forma recursiva.
   Considera tempo contínuo de trabalho, número de reuniões, autoavaliação emocional e tempo desde a última pausa.
   Utiliza memoização para evitar recomputações.

3. **merge_sort_records()**
   Implementa o algoritmo de merge sort de forma recursiva para ordenar os colaboradores pelo nível de estresse.
   Complexidade O(n log n).
   Atende ao requisito do professor: quick sort ou merge sort implementado manualmente com recursão.

4. **knapsack_recursive()**
   Implementação recursiva do problema da mochila 0/1, utilizando memoização com o decorador @lru_cache.
   Seleciona as intervenções de maior benefício que cabem dentro do limite de tempo.

5. **recommend_for_all_recursive()**
   Executa o algoritmo da mochila para cada colaborador de forma recursiva.
   Aplica ajustes no limite de tempo para colaboradores com estresse elevado.
   Retorna as recomendações individuais com tempo e benefício totais.

6. **build_dataframe_recursive()**
   Constrói o DataFrame final recursivamente, incluindo as recomendações selecionadas.

7. **run_pipeline()**
   Função principal que integra todas as etapas: geração dos dados, cálculo do estresse, ordenação, execução do algoritmo da mochila, construção do DataFrame e exportação para CSV.
