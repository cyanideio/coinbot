from utils.db.models import YunbiTrans, PoloniexTrans

def getPrice(market, coinPair):
    if market == 'yunbi':
        model = YunbiTrans
    if market == 'poloniex':
        model = PoloniexTrans
    return model.select().where(model.coinType==coinPair).order_by(model.timestamp.desc()).get().price