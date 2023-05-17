import td_data_collector as dc


def run_entry_exit_test(trading_day, start_time='9:30', end_time='10:00', tp=0.03, sl=0.05):
    """
    This function simulates running a full 'entry exit' test which in-
    cludes a take profit and stop loss order.
    E.g: tp = 0.03, sl = 0.05 means a 3% take profit and a 5% stop loss.
    Note: this is not a destructive method to the candles.
    """
    start_index = trading_day.candles.index(trading_day.getCandleAfterTime(start_time)) - 1
    end_index = trading_day.candles.index(trading_day.getCandleAfterTime(end_time)) - 1
    ep = trading_day.candles[start_index].price
    print(ep)
    for candle in trading_day.candles[start_index:end_index]:
        if candle.did_price_occur(ep*(1+tp)):
            return 1, candle
        elif candle.did_price_occur(ep*(1-sl)):
            return 2, candle
    return 0, candle

if __name__ == '__main__':
    trd = dc.TradingDay.createTradingDay('AAPL', '5/17/2023')
    token, candle = run_entry_exit_test(trd, '10:00', '11:30', 0.01, 0.01)
    print('doing test')
    print(token)
    print(candle.price)
    print(candle.human_time)

