import td_data_collector as dc
from DecrypterModule import get_key_and_token
api_key, oauth_token = get_key_and_token()
# print(api_key)
# print(oauth_token)
dc.init_auth_data(api_key, oauth_token)

class DataCollectorInterface:
    def run_analysis(options, criteria, en_ex):

        boolean_strats, unordered_times = DataCollectorInterface.create_strategies(criteria)

        if DataCollectorInterface.validate_ee(en_ex):
            day_in = int(en_ex[0])
            time_in = en_ex[1]
            day_out = int(en_ex[2])
            time_out = en_ex[3]

            unordered_times += [time_in, time_out]

            def entry_exit_test(data):
                p1 = data[f'{day_in} - {time_in}']
                p2 = data[f'{day_out} - {time_out}']
                perc_incr = 100 * (p2 - p1) / p1
                return round(perc_incr, 2)

        time_list = DataCollectorInterface.time_order(unordered_times)
        
        path_in = options[0]
        path_out = options[2]
        opt_sel = options[1]
        
        nDays = int(opt_sel.daysToPull)
        day1 = opt_sel.dayOneDate
        
        print(f'time_list: {time_list}')
        dataFilter = dc.DataFilter(path_in, day1, [time_list for i in range(nDays)])    
        if not time_list == []:
            master = dataFilter.generateMaster()
        else:
            master = dataFilter
        for strat in boolean_strats:
            # master.show()
            master.filterFor(strat)

        if DataCollectorInterface.validate_ee(en_ex):
            total_success_rate = master.func_test("Percentage Win", entry_exit_test)

        master.export_csv(path_out)

        if DataCollectorInterface.validate_ee(en_ex):
            return total_success_rate
        else:
            return None

    def validate_ee(en_ex):
        for x in en_ex:
            if x == "":
                return False
        return True
    
    def create_strategies(criteria_list):
        strategies = []
        times = []
        for crit in criteria_list:
            if crit.type == 0: # regular strategy
                str1 = f'{crit.day1} - {crit.time1}'
                str2 = f'{crit.day2} - {crit.time2}'
                times += [crit.time1, crit.time2]
                if crit.by_perc == None:
                    if crit.comp == '<':
                        strat_func = lambda data, str1=str1, str2=str2: data[str1] < data[str2]
                        strategies.append(dc.BooleanStrategy(strat_func))
                    elif crit.comp == '>':
                        strat_func = lambda data, str1=str1, str2=str2: data[str1] > data[str2]
                        strategies.append(dc.BooleanStrategy(strat_func))
                    else: # = sign
                        strat_func = lambda data, str1=str1, str2=str2: data[str1] == data[str2]
                        strategies.append(dc.BooleanStrategy(strat_func))
                else:
                    if crit.comp == '<':
                        strat_func = lambda data, str1=str1, str2=str2: data[str1] < data[str2] * (1 - crit.by_perc / 100)
                        strategies.append(dc.BooleanStrategy(strat_func))
                    elif crit.comp == '>':
                        strat_func = lambda data, str1=str1, str2=str2: data[str1] > data[str2] * (1 + crit.by_perc / 100)
                        strategies.append(dc.BooleanStrategy(strat_func))
                    else: # = sign
                        strat_func = lambda data, str1=str1, str2=str2: data[str1] == data[str2]
                        strategies.append(dc.BooleanStrategy(strat_func))

            elif crit.type == 1: # value strategy
                if crit.comp == '<':
                    def strat_func(data, crit=crit):
                        try:
                            return int(data[crit.input_field]) < int(crit.value)
                        except:
                            return False
                    strategies.append(dc.BooleanStrategy(strat_func))
                elif crit.comp == '>':
                    def strat_func(data, crit=crit):
                        try:
                            return int(data[crit.input_field]) > int(crit.value)
                        except:
                            return False
                    strategies.append(dc.BooleanStrategy(strat_func))
                else: # = sign
                    def strat_func(data, crit=crit):
                        try:
                            return data[crit.input_field] == crit.value
                        except:
                            return False
                    strategies.append(dc.BooleanStrategy(strat_func))
        return strategies, list(set(times))
    
    def time_order(t_list):
        time_set = list(set(t_list))
        mins_list = list(map(DataCollectorInterface.to_minutes, time_set))
        return [t for _, t in sorted(zip(mins_list, time_set))]
    
    def to_minutes(time_str):
        hrs = time_str.split(':')[0]
        mins = time_str.split(':')[1]
        return int(hrs) * 60 + int(mins)
