import websocket
import json
import pprint
import talib
import numpy

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUATITY = 0.50

closes = []
in_position = False


def on_open(ws):
    print('opened connection')


def on_close(ws):
    print('connection closed')


def on_message(ws, message):
    global closes

    print('message recieved')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print('candle closed at {}'.format(close))
        closes.append(float(close))
        print('closes')
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            last_rsi = rsi[-1]
            print("Calculated RSI's so far:")
            print(rsi)
            print('Current RSI:'.format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print('Sell! Sell! Sell! Sell! Sell!')
                    # binance sell logic
                else:
                    print('Cant sell not enough available')

            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print('Cant buy anymore.')
                else:
                    print('Buy! Buy! Buy! Buy! Buy! Buy!')
                    # binance order logic


ws = websocket.WebSocketApp(SOCKET, on_open=on_open,
                            on_close=on_close, on_message=on_message)

ws.run_forever()
