from functools import lru_cache
import pandas as pd
import csv
import json
from typing import List, Dict, Tuple


#  Data: 20+ registros

def generate_dataset_recursive(n=22):
    """
    Gera N registros sintéticos (recursivamente).
    Retorna lista de dicts.
    """
    base = [
        {"id": 1, "name": "Alice", "avg_continuous_minutes": 120, "num_meetings": 6, "self_report": 4, "last_pause_minutes": 180},
        {"id": 2, "name": "Bruno", "avg_continuous_minutes": 90, "num_meetings": 4, "self_report": 6, "last_pause_minutes": 60},
        {"id": 3, "name": "Carolina", "avg_continuous_minutes": 210, "num_meetings": 8, "self_report": 3, "last_pause_minutes": 240},
        {"id": 4, "name": "Daniel", "avg_continuous_minutes": 45, "num_meetings": 2, "self_report": 8, "last_pause_minutes": 30},
        {"id": 5, "name": "Eduarda", "avg_continuous_minutes": 150, "num_meetings": 5, "self_report": 5, "last_pause_minutes": 120},
        {"id": 6, "name": "Felipe", "avg_continuous_minutes": 180, "num_meetings": 7, "self_report": 4, "last_pause_minutes": 200},
        {"id": 7, "name": "Gabriela", "avg_continuous_minutes": 60, "num_meetings": 3, "self_report": 7, "last_pause_minutes": 45},
        {"id": 8, "name": "Helena", "avg_continuous_minutes": 240, "num_meetings": 9, "self_report": 2, "last_pause_minutes": 300},
        {"id": 9, "name": "Igor", "avg_continuous_minutes": 30, "num_meetings": 1, "self_report": 9, "last_pause_minutes": 15},
        {"id": 10, "name": "Júlia", "avg_continuous_minutes": 200, "num_meetings": 8, "self_report": 3, "last_pause_minutes": 210},
        {"id": 11, "name": "Kleber", "avg_continuous_minutes": 100, "num_meetings": 4, "self_report": 6, "last_pause_minutes": 80},
        {"id": 12, "name": "Larissa", "avg_continuous_minutes": 130, "num_meetings": 5, "self_report": 5, "last_pause_minutes": 100},
        {"id": 13, "name": "Marcos", "avg_continuous_minutes": 75, "num_meetings": 3, "self_report": 7, "last_pause_minutes": 50},
        {"id": 14, "name": "Natália", "avg_continuous_minutes": 95, "num_meetings": 4, "self_report": 6, "last_pause_minutes": 70},
        {"id": 15, "name": "Otávio", "avg_continuous_minutes": 160, "num_meetings": 6, "self_report": 5, "last_pause_minutes": 150},
        {"id": 16, "name": "Patrícia", "avg_continuous_minutes": 220, "num_meetings": 9, "self_report": 3, "last_pause_minutes": 220},
        {"id": 17, "name": "Quico", "avg_continuous_minutes": 55, "num_meetings": 2, "self_report": 8, "last_pause_minutes": 40},
        {"id": 18, "name": "Rafaela", "avg_continuous_minutes": 140, "num_meetings": 5, "self_report": 5, "last_pause_minutes": 110},
        {"id": 19, "name": "Sérgio", "avg_continuous_minutes": 170, "num_meetings": 6, "self_report": 4, "last_pause_minutes": 160},
        {"id": 20, "name": "Tatiana", "avg_continuous_minutes": 85, "num_meetings": 3, "self_report": 7, "last_pause_minutes": 60},
        {"id": 21, "name": "Ulisses", "avg_continuous_minutes": 125, "num_meetings": 4, "self_report": 6, "last_pause_minutes": 90},
        {"id": 22, "name": "Valéria", "avg_continuous_minutes": 190, "num_meetings": 7, "self_report": 4, "last_pause_minutes": 185},
    ]
    # Se n > len(base), repetimos variantes simples recursivamente
    if n <= len(base):
        return base[:n]
    else:
        extra = []
        def make_extra(i, remaining):
            if remaining == 0:
                return
            idx = (len(base) + i - 1) % len(base)
            template = base[idx].copy()
            template["id"] = len(base) + i
            template["name"] = template["name"] + f"#{i}"
            template["avg_continuous_minutes"] = max(20, template["avg_continuous_minutes"] + (i*7) % 60)
            extra.append(template)
            make_extra(i+1, remaining-1)
        make_extra(1, n-len(base))
        return base + extra


# Intervenções (itens da mochila)

INTERVENTIONS = [
    {"name": "Pausa 5 min + respiração", "time_cost": 5, "benefit": 4},
    {"name": "Alongamento rápido 5 min", "time_cost": 5, "benefit": 3},
    {"name": "Exercício de atenção plena 10 min", "time_cost": 10, "benefit": 6},
    {"name": "Micro-learning (vídeo) 15 min", "time_cost": 15, "benefit": 7},
    {"name": "Check-in emocional guiado 10 min", "time_cost": 10, "benefit": 5},
    {"name": "Pausa sensorial 7 min", "time_cost": 7, "benefit": 4},
    {"name": "Exercício respiratório 3 min", "time_cost": 3, "benefit": 2},
    {"name": "Desconexão digital curta 20 min", "time_cost": 20, "benefit": 9},
    {"name": "Sugestão de falar com RH/psicólogo (1ª triagem) 5 min", "time_cost": 5, "benefit": 3},
]


# Função recursiva para calcular stress_index (com memo)

def compute_stress_indices_recursive(records: List[Dict]):
    """
    Calcula stress_index para cada registro (recursivamente).
    stress_index sintetiza: avg_continuous_minutes, num_meetings, inverse self_report, last_pause_minutes.
    Implementado com recursão e memoização.
    Retorna nova lista de dicts com campo 'stress_index'.
    """

    memo = {}

    def compute_single(idx):
        if idx in memo:
            return memo[idx]
        if idx < 0:
            return None
        rec = records[idx].copy()
        a = rec["avg_continuous_minutes"] / 240.0
        b = rec["num_meetings"] / 10.0
        c = (10 - rec["self_report"]) / 10.0
        d = min(rec["last_pause_minutes"] / 240.0, 1.0)
        stress = round( (0.45*a + 0.25*b + 0.2*c + 0.1*d) * 10, 3)
        rec["stress_index"] = stress
        memo[idx] = rec
        if idx == 0:
            return [rec]
        else:
            rest = compute_single(idx-1)
            return rest + [rec]

    result = compute_single(len(records)-1)
    return result


# Merge sort recursivo para ordenar lista de dicts por stress_index

def merge_sort_records(records: List[Dict], key: str, reverse=False) -> List[Dict]:
    """
    Implementação recursiva de merge sort.
    Retorna nova lista ordenada.
    """
    def merge(left, right):
        merged = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if (left[i][key] > right[j][key]) ^ (not reverse):
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    if len(records) <= 1:
        return records[:]
    mid = len(records) // 2
    left = merge_sort_records(records[:mid], key, reverse)
    right = merge_sort_records(records[mid:], key, reverse)
    return merge(left, right)


# Knapsack (0-1) recursivo com memoização

def knapsack_recursive(items: List[Dict], capacity: int) -> Tuple[int, List[int]]:
    """
    items: lista de dicts com 'time_cost' (peso) e 'benefit' (valor)
    capacity: inteiro (minutos)
    Retorna (valor_maximo, lista_indices_itens)
    Implementação recursiva com lru_cache memoization.
    """

    n = len(items)

    @lru_cache(maxsize=None)
    def dp(i, cap):
        if i == n or cap <= 0:
            return (0, ())
        item = items[i]
        w = item["time_cost"]
        v = item["benefit"]
        val_no, seq_no = dp(i+1, cap)
        if w > cap:
            return (val_no, seq_no)
        val_yes, seq_yes = dp(i+1, cap - w)
        val_yes += v
        if val_yes > val_no:
            return (val_yes, seq_yes + (i,))
        else:
            return (val_no, seq_no)

    best_value, best_seq = dp(0, capacity)
    return best_value, list(best_seq)

# Monta recomendações para cada colaborador (recursivamente)

def recommend_for_all_recursive(records: List[Dict], interventions: List[Dict], time_budget: int):
    """
    Para cada registro, aplica a mochila recursiva para selecionar intervenções que maximizem benefício.
    Implementado com recursão para iterar sobre registros.
    Retorna lista de registros com campo 'recommended' contendo chosen items, total_time, total_benefit.
    """
    res = []
    def helper(idx):
        if idx >= len(records):
            return
        rec = records[idx].copy()
        cap = time_budget
        if rec["stress_index"] >= 7:
            cap = min(time_budget + 10, 60)
        val, seq = knapsack_recursive(interventions, cap)
        chosen = [interventions[i] for i in seq]
        rec["recommended"] = chosen
        rec["recommended_total_time"] = sum(item["time_cost"] for item in chosen)
        rec["recommended_total_benefit"] = sum(item["benefit"] for item in chosen)
        res.append(rec)
        helper(idx+1)
    helper(0)
    return res

# Geração de DataFrame e relatórios (recursivo)
def build_dataframe_recursive(records_with_recs: List[Dict]):
    """
    Converte lista de dicts em DataFrame e cria colunas textuais com recomendações.
    """
    def to_row(i):
        if i >= len(records_with_recs):
            return []
        rec = records_with_recs[i]
        row = {
            "id": rec["id"],
            "name": rec["name"],
            "avg_continuous_minutes": rec["avg_continuous_minutes"],
            "num_meetings": rec["num_meetings"],
            "self_report": rec["self_report"],
            "last_pause_minutes": rec["last_pause_minutes"],
            "stress_index": rec["stress_index"],
            "recommended_total_time": rec["recommended_total_time"],
            "recommended_total_benefit": rec["recommended_total_benefit"],
            "recommended_items": "; ".join([f"{it['name']}({it['time_cost']}m)" for it in rec["recommended"]])
        }
        return [row] + to_row(i+1)
    rows = to_row(0)
    df = pd.DataFrame(rows)
    return df


# Função principal que integra tudo
def run_pipeline(n_records=22, time_budget=30, sort_desc=True, save_csv=True, csv_path="menteneural_report.csv"):
    # 1) gerar dataset
    records = generate_dataset_recursive(n_records)

    # 2) calcular stress indices (recursivo)
    with_stress = compute_stress_indices_recursive(records)

    # 3) ordenar por stress_index (merge sort recursivo)
    sorted_records = merge_sort_records(with_stress, key="stress_index", reverse=sort_desc)

    # 4) aplicar recomendações (knapsack recursivo para cada)
    with_recs = recommend_for_all_recursive(sorted_records, INTERVENTIONS, time_budget)

    # 5) construir dataframe (recursivo)
    df = build_dataframe_recursive(with_recs)

    if save_csv:
        df.to_csv(csv_path, index=False)
    return df

if __name__ == "__main__":
    df = run_pipeline(n_records=22, time_budget=30, csv_path="menteneural_report.csv")
    print("Top 5 colaboradores por stress_index (com recomendações):")
    print(df.head(5).to_string(index=False))
    print("\nRelatório salvo em: menteneural_report.csv")
