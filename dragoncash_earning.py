def round_half_away_from_zero(x):
    import math
    if x >= 0:
        decimal = x - math.floor(x)
        if decimal < 0.5: return math.floor(x)
        return math.ceil(x)
    else:
        decimal = x - math.ceil(x)
        if decimal > -0.5: return math.ceil(x)
        return math.floor(x)


def build_decimal_earning_table(earn_gold: int, elder: bool):
    import decimal
    earning_table = []
    for level in range(1,21 + elder):
        earning_rate = 6000*(decimal.Decimal('.4')+decimal.Decimal('.6')*decimal.Decimal(level))/earn_gold
        earning_table.append(earning_rate)
    
    return earning_table


def build_earning_table(earn_gold: int, elder: bool, round_function):
    import numpy as np
    
    earning_table = []
    for level in range(1,21 + elder):
        earning_rate = 6000/((earn_gold * np.float32(1.6666666))/np.float32((level+0.6666666)))
        earning_table.append(round_function(earning_rate))
        
    return earning_table


def build_used_earn_golds_to_reported_earning_tables(earningRates, quils_earning_data, create_used_earn_golds_to_reported_earning_tables_file):
    # Note, if an elder and non-elder dragon share an earn gold, only the elder (length 21) earning table is in the returned data set
    
    import json
    wikis_dragoncash_dragons = set([dragon_name for dragon_name, earning_data in earningRates.items() if earning_data['Currency'] == 'DragonCash'])
    quils_dragoncash_dragons = set([dragon_name for dragon_name, earning_data in quils_earning_data.items() if 'Earn Gold' in earning_data.keys()])
    
    shared_dragoncash_dragons = wikis_dragoncash_dragons & quils_dragoncash_dragons
    
    earn_gold_and_earning_tuple = set()
    
    for dragon_name in shared_dragoncash_dragons:
        earn_gold_and_earning_tuple.add((quils_earning_data[dragon_name]['Earn Gold'], tuple(earningRates[dragon_name]['Rates'])))
    
    used_earn_golds_to_reported_earning_tables = {}
    
    for earn_gold, earning_tuple in earn_gold_and_earning_tuple:
        if earn_gold in used_earn_golds_to_reported_earning_tables and len(earning_tuple) == 20: continue
        used_earn_golds_to_reported_earning_tables[earn_gold] = list(earning_tuple)
    
    if create_used_earn_golds_to_reported_earning_tables_file:
        with open('all-realistic-unique-earn-golds-and-earning-tables.json', 'w+') as file:
            json.dump(used_earn_golds_to_reported_earning_tables, file, indent=4, separators=(',', ': '), sort_keys=True)   
    
    return used_earn_golds_to_reported_earning_tables


def find_all_realistic_earn_golds_and_earning_tables(create_all_realistic_unique_earn_golds_and_earning_tables_file: bool):
    import json
    
    large_unique_earn_golds_and_earning_tuples = set()
    
    earn_gold = 1
    while earn_gold <= 6000: # Doesn't find tables with earning rates less than 1 DC/min at level 1.
        earning_tuple = tuple(build_earning_table(earn_gold, True, round_half_away_from_zero))
        large_unique_earn_golds_and_earning_tuples.add((earn_gold, earning_tuple))
        earn_gold += 1
    
    unique_earn_golds_and_earning_tuples = large_unique_earn_golds_and_earning_tuples.copy()
    for earn_gold, earning_tuple in large_unique_earn_golds_and_earning_tuples: unique_earn_golds_and_earning_tuples.add((earn_gold, earning_tuple[:20]))
    
    unique_earning_tables = []
    
    for earn_gold, earning_tuple in unique_earn_golds_and_earning_tuples:
        if max(earning_tuple) < 6000: unique_earning_tables.append([earn_gold, list(earning_tuple)])
        
    unique_earning_tables.sort()
    
    if create_all_realistic_unique_earn_golds_and_earning_tables_file:
        with open('all-realistic-unique-earn-golds-and-earning-tables.json', 'w+') as file:
            json.dump(unique_earning_tables, file)
    
    return unique_earning_tables


def find_all_potential_problem_earn_golds_and_elder_onlies(realistic: bool, create_problem_earn_golds_and_elder_onlies_file: bool):
    # "elder only" refers to an earning table that is only an issue if it is an elder earning table (21 elements long)
    import decimal
    import json
    
    potential_problem_earn_golds_and_elder_onlies = []
    
    earn_gold = 1
    while True:
        earning_table = build_decimal_earning_table(earn_gold, True)
        
        if max(earning_table) < .5 or (realistic and earn_gold > 6000): break
        
        ends_in_point_5_earning_table = [earning_rate-int(earning_rate) == decimal.Decimal('.5') for earning_rate in earning_table]
        
        if True in ends_in_point_5_earning_table:
            elder_only =  ends_in_point_5_earning_table == ([False]*20)+[True]
            potential_problem_earn_golds_and_elder_onlies.append([earn_gold, elder_only])
        
        earn_gold += 1
    
    potential_problem_earn_golds_and_elder_onlies.sort()
    
    if create_problem_earn_golds_and_elder_onlies_file:
        with open(f'all-{'realistic-'*realistic}potential-problem-earn-golds-and-elder-onlies.json', 'w+') as file:
            json.dump(potential_problem_earn_golds_and_elder_onlies, file)
            
    return potential_problem_earn_golds_and_elder_onlies


def find_all_problem_earning_tables(earningRates, quils_earning_data, potential_problem_earn_golds_and_elder_onlies, create_all_problem_earning_tables_file: bool):
    import json
    
    used_earn_golds_and_elders_to_dragon_names = {}
    for dragon_name, earning_data in quils_earning_data.items():
        if 'Earn Gold' in earning_data.keys():
            earn_gold_and_elder = (earning_data['Earn Gold'], earning_data['Is Elder'])
            if earn_gold_and_elder not in used_earn_golds_and_elders_to_dragon_names.keys(): used_earn_golds_and_elders_to_dragon_names[earn_gold_and_elder] = []
            used_earn_golds_and_elders_to_dragon_names[earn_gold_and_elder].append(dragon_name)
    
    used_earn_golds_and_elders = [[earn_gold, elder] for earn_gold, elder in used_earn_golds_and_elders_to_dragon_names.keys()]
    
    problem_earn_golds_and_elders = []
    
    for potential_problem_earn_gold, elder_only in potential_problem_earn_golds_and_elder_onlies:
        if elder_only:
            if [potential_problem_earn_gold, True] in used_earn_golds_and_elders: problem_earn_golds_and_elders.append([potential_problem_earn_gold, True])
        else:
            if [potential_problem_earn_gold, True] in used_earn_golds_and_elders: problem_earn_golds_and_elders.append([potential_problem_earn_gold, True])
            if [potential_problem_earn_gold, False] in used_earn_golds_and_elders: problem_earn_golds_and_elders.append([potential_problem_earn_gold, False])
    
    all_problem_earning_tables = {}
    
    for earn_gold, elder in problem_earn_golds_and_elders:
        dragon_names = used_earn_golds_and_elders_to_dragon_names[(earn_gold, elder)]
        
        for dragon_name in dragon_names:
            try:
                reported_earning_table = earningRates[dragon_name]['Rates']
                break
            except KeyError: pass
        
        if earn_gold not in all_problem_earning_tables.keys():
            all_problem_earning_tables[earn_gold] = []
        all_problem_earning_tables[earn_gold].append({'elder': elder, 'dragon-names': dragon_names, 'reported-earning-table': reported_earning_table})
    
    if create_all_problem_earning_tables_file:
        with open('all-problem-earning-tables.json', 'w+') as file:
            json.dump(all_problem_earning_tables, file, indent=4, separators=(',', ': '), sort_keys=True)
    
    return all_problem_earning_tables