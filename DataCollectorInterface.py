import td_data_collector as dc
class DataCollectorInterface:
    def run_analysis(options, criteria):
        boolean_strats, unordered_times = DataCollectorInterface.create_strategies(criteria)
        time_list = DataCollectorInterface.time_order(unordered_times)
        
        path_in = options[0]
        path_out = options[2]
        opt_sel = options[1]
        
        nDays = int(opt_sel.daysToPull)
        day1 = opt_sel.dayOneDate
        
        print(f'time_list: {time_list}')
        dataFilter = dc.DataFilter(path_in, day1, [time_list for i in range(nDays)])    
        master = dataFilter.generateMaster()
        for strat in strats:
            master.filterFor(strat)
        master.export_csv(path_out)
    
    def create_strategies(criteria_list):
        strategies = []
        times = []
        for crit in criteria_list:
            if crit.type == 0: # regular strategy
                str1 = f'{crit.day1} - {crit.time1}'
                str2 = f'{crit.day2} - {crit.time2}'
                times += [crit.time1, crit.time2]
                if crit.comp == '<':
                    strat_func = lambda data: data[str1] < data[str2]
                    strategies.append(dc.BooleanStrategy(strat_func))
                elif crit.comp == '>':
                    strat_func = lambda data: data[str1] > data[str2]
                    strategies.append(dc.BooleanStrategy(strat_func))
                else: # = sign
                    strat_func = lambda data: data[str1] == data[str2]
                    strategies.append(dc.BooleanStrategy(strat_func))
            elif crit.type == 1: # value strategy
                if crit.comp == '<':
                    strat_func = lambda data: data[crit.input_field] < crit.value
                    strategies.append(dc.BooleanStrategy(strat_func))
                elif crit.comp == '>':
                    strat_func = lambda data: data[crit.input_field] > crit.value
                    strategies.append(dc.BooleanStrategy(strat_func))
                else: # = sign
                    strat_func = lambda data: data[crit.input_field] == crit.value
                    strategies.append(dc.BooleanStrategy(strat_func))
        return strategies, list(set(times))
    
    def time_order(time_set):
        mins_list = list(map(DataCollectorInterface.to_minutes, time_set))
        return sorted(mins_list)
    
    def to_minutes(time_str):
        hrs = time_str.split(':')[0]
        mins = time_str.split(':')[1]
        return int(hrs) * 60 + int(mins)
