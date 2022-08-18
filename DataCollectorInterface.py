import time
import td_data_collector as dc
import os

global GLOBAL_ACCT_INFO
GLOBAL_ACCT_INFO = None

with open('td_auth.txt', 'r') as f:
    acct_num, refresh_token = [l.strip('\n') for l in f.readlines()]
    acct_info = dc.init_auth_data(acct_num, refresh_token)
    if not acct_info == None:
        # global GLOBAL_ACCT_INFO
        GLOBAL_ACCT_INFO = acct_info
        

class DataCollectorInterface:
    def create_batch_market_order(symbols, amts, tp_perc=None, sl_perc=None):
        sender = dc.OrderSender.create_order_sender()
        return sender.create_batch_market_order(symbols, amts, tp_perc, sl_perc)

    def get_order_status(order_id):
        sender = dc.OrderSender.create_order_sender()
        sender.get_order_status(order_id)

    def cancel_order(order_id):
        sender = dc.OrderSender.create_order_sender()
        sender.cancel_order(order_id)

    def create_batch_closes(order_ids):
        sender = dc.OrderSender.create_order_sender()
        sender.create_batch_closes(order_ids)

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
        
        nDays = DataCollectorInterface.get_n_days(criteria, en_ex)
        print(nDays)
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

        def finisher():
            os.startfile(path_out)
            return list(master.currentState['Symbol'])

        if DataCollectorInterface.validate_ee(en_ex):
            return total_success_rate, finisher
        else:
            return None, finisher

    def validate_ee(en_ex):
        for x in en_ex:
            if x == "":
                return False
        return True

    def get_n_days(crit_list, en_ex):
        all_days = []
        for crit in crit_list:
            if crit.type == 0:
                all_days += [int(crit.day1), int(crit.day2)]
        if DataCollectorInterface.validate_ee(en_ex):
            all_days += [int(en_ex[0]), int(en_ex[2])]
        return max(all_days)
    
    def create_strategies(criteria_list):
        strategies = []
        times = []
        for crit in criteria_list:
            if type(crit) == list: # or clause
                or_clause_list, or_clause_times = DataCollectorInterface.create_strategies(crit)
                def strat_func(data, or_clause_list=or_clause_list):
                    for b_strat in or_clause_list:
                        if b_strat.apply(data):
                            return True
                    return False
                strategies.append(dc.BooleanStrategy(strat_func))
                times += or_clause_times
            else:
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
                            strat_func = lambda data, str1=str1, str2=str2, crit=crit: data[str1] < data[str2] * (1 - crit.by_perc / 100)
                            strategies.append(dc.BooleanStrategy(strat_func))
                        elif crit.comp == '>':
                            strat_func = lambda data, str1=str1, str2=str2, crit=crit: data[str1] > data[str2] * (1 + crit.by_perc / 100)
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
