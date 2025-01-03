from quils_data import get_quils_earning_data, get_quils_data
from dragoncash_earning import round_half_away_from_zero, build_used_earn_golds_to_reported_earning_tables, find_all_problem_earning_tables, find_all_potential_problem_earn_golds_and_elder_onlies
from fandom_wikis_data import get_fandom_wikis_earning_data

import numpy as np


def num_build_earning_table(earn_gold, elder, round_function, num1, num2):
    earning_table = []
    for level in range(1,21 + elder):
        earning_rate = 6000/((earn_gold * num1)/(level+num2))
        # earning_rate = 6000/(earn_gold / (0.6*level + 0.4))
        earning_table.append(round_function(earning_rate))
        
    return earning_table


def analytics(used_earn_golds_to_reported_earning_tables, all_problem_earning_tables, round_function, num1, num2):
    non_problem_tables_correct = 0
    total_non_problem_tables = 0
    non_problem_earning_rates_correct = 0
    total_non_problem_earning_rates = 0
    problem_tables_correct = 0
    total_problem_tables = 0
    problem_earning_rates_correct = 0
    total_problem_earning_rates = 0
    
    problem_earn_golds = all_problem_earning_tables.keys()
    
    for earn_gold, reported_earning_table in used_earn_golds_to_reported_earning_tables.items():
        earning_table_length = len(reported_earning_table)
        built_earning_table = num_build_earning_table(earn_gold, earning_table_length-20, round_function, num1, num2)
        
        if earn_gold in problem_earn_golds:
            if built_earning_table == reported_earning_table:
                problem_tables_correct += 1
                problem_earning_rates_correct += earning_table_length
            else:
                for reported_earning_rate, built_earning_rate in zip(reported_earning_table, built_earning_table):
                    if reported_earning_rate == built_earning_rate: problem_earning_rates_correct += 1
            total_problem_tables += 1
            total_problem_earning_rates += earning_table_length
        else:
            if built_earning_table == reported_earning_table:
                non_problem_tables_correct += 1
                non_problem_earning_rates_correct += earning_table_length
            else:
                for reported_earning_rate, built_earning_rate in zip(reported_earning_table, built_earning_table):
                    if reported_earning_rate == built_earning_rate: non_problem_earning_rates_correct += 1
            total_non_problem_tables += 1
            total_non_problem_earning_rates += earning_table_length
    
    total_tables_correct = non_problem_tables_correct + problem_tables_correct
    total_tables = total_non_problem_tables + total_problem_tables
    total_earning_rates_correct = non_problem_earning_rates_correct + problem_earning_rates_correct
    total_earning_rates = total_non_problem_earning_rates + total_problem_earning_rates
    
    results = {
        'num1': num1,
        'num2': num2,
        'non-problem-tables-correct': non_problem_tables_correct,
        'total-non-problem-tables': total_non_problem_tables,
        'non-problem-earning-rates-correct': non_problem_earning_rates_correct,
        'total-non-problem-earning-rates': total_non_problem_earning_rates,
        'problem-tables-correct': problem_tables_correct,
        'total-problem-tables': total_problem_tables,
        'problem-earning-rates-correct': problem_earning_rates_correct,
        'total-problem-earning-rates': total_problem_earning_rates,
        'total-tables-correct': total_tables_correct,
        'total-tables': total_tables,
        'total-earning-rates-correct': total_earning_rates_correct,
        'total-earning-rates': total_earning_rates,
    }
    
    return results


def try_num1_and_num2_values(used_earn_golds_to_reported_earning_tables, all_problem_earning_tables):
    all_analytics = []
    num1 = 1.6666666666666 # 1.6666666666666
    while num1 <= 1.6666666666666666: # 1.6666666666666666
        num2 = 0.6666666666666 # 0.6666666666666
        while num2 <= 0.6666666666666666: # 0.6666666666666666
            all_analytics.append(analytics(used_earn_golds_to_reported_earning_tables, all_problem_earning_tables, round_half_away_from_zero, num1, num2))
            num2 = np.nextafter(num2, 9)
        num1 = np.nextafter(num1, 9)
    return all_analytics

def nextafter_n_times(number, towards, n_times):
    for _ in range(n_times):
        number = np.nextafter(number, towards)
    return number

def try_num1_and_num2_values2(used_earn_golds_to_reported_earning_tables, all_problem_earning_tables):
    all_analytics = []
    
    sixes = list(set([(float('.'+'6'*i)) for i in range(1,21)]))
    
    num1s = []
    num2s = []
    
    for six in sixes:
        num = nextafter_n_times(six, 0, 8)
        for _ in range(16):
            num1s.append(num+1)
            num2s.append(num)
            num = np.nextafter(num, 9)
    
    for num1 in num1s:
        for num2 in num2s:
            all_analytics.append(analytics(used_earn_golds_to_reported_earning_tables, all_problem_earning_tables, round_half_away_from_zero, num1, num2))
        
    return all_analytics

def try_num1_and_num2_values3(used_earn_golds_to_reported_earning_tables, all_problem_earning_tables):
    all_analytics = []
    
    sixes = list(set([np.float32(float('.'+'6'*i)) for i in range(1,21)]))
    
    for six in sixes:
        num1s = []
        num2s = []
        
        num = nextafter_n_times(six, 0, 50)

        for _ in range(100):
            num1s.append(num+1)
            num2s.append(num)
            num = np.nextafter(num, 9)
    
        for num1 in num1s:
            for num2 in num2s:
                all_analytics.append(analytics(used_earn_golds_to_reported_earning_tables, all_problem_earning_tables, round_half_away_from_zero, num1, num2))
        
    return all_analytics

def main():
    earningRates = get_fandom_wikis_earning_data(False, False)['earningRates']
    quils_earning_data = get_quils_earning_data(get_quils_data(True, False), False)
    
    used_earn_golds_to_reported_earning_tables = build_used_earn_golds_to_reported_earning_tables(earningRates, quils_earning_data, False)
    
    all_potential_problem_earn_golds_and_elder_onlies = find_all_potential_problem_earn_golds_and_elder_onlies(False, False)
    all_problem_earning_tables = find_all_problem_earning_tables(earningRates, quils_earning_data, all_potential_problem_earn_golds_and_elder_onlies, False)
        
    # all_analytics = try_num1_and_num2_values(used_earn_golds_to_reported_earning_tables, all_problem_earning_tables)
    # all_analytics = try_num1_and_num2_values2(used_earn_golds_to_reported_earning_tables, all_problem_earning_tables)
    all_analytics = try_num1_and_num2_values3(used_earn_golds_to_reported_earning_tables, all_problem_earning_tables)
    
    
    max_non_problem_tables_correct = 0
    max_non_problem_earning_rates_correct = 0
    max_problem_tables_correct = 0
    max_problem_earning_rates_correct = 0
    max_total_tables_correct = 0
    max_total_earning_rates_correct = 0
    
    for analytics in all_analytics:
        non_problem_tables_correct = analytics['non-problem-tables-correct']
        non_problem_earning_rates_correct = analytics['non-problem-earning-rates-correct']
        problem_tables_correct = analytics['problem-tables-correct']
        problem_earning_rates_correct = analytics['problem-earning-rates-correct']
        total_tables_correct = analytics['total-tables-correct']
        total_earning_rates_correct = analytics['total-earning-rates-correct']

        if non_problem_tables_correct > max_non_problem_tables_correct: max_non_problem_tables_correct = non_problem_tables_correct
        if non_problem_earning_rates_correct > max_non_problem_earning_rates_correct: max_non_problem_earning_rates_correct = non_problem_earning_rates_correct
        if problem_tables_correct > max_problem_tables_correct: max_problem_tables_correct = problem_tables_correct
        if problem_earning_rates_correct > max_problem_earning_rates_correct: max_problem_earning_rates_correct = problem_earning_rates_correct
        if total_tables_correct > max_total_tables_correct: max_total_tables_correct = total_tables_correct
        if total_earning_rates_correct > max_total_earning_rates_correct: max_total_earning_rates_correct = total_earning_rates_correct
        
        if total_tables_correct >= 189 and total_earning_rates_correct >= 3883:
            print(analytics['num1'], analytics['num2'])
        
    print(max_non_problem_tables_correct)
    print(max_non_problem_earning_rates_correct)
    print(max_problem_tables_correct)
    print(max_problem_earning_rates_correct)
    print(max_total_tables_correct)
    print(max_total_earning_rates_correct)
    
if __name__ == '__main__':
    main()