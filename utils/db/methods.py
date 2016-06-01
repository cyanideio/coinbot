#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.db.models import CoinCapBTCTrans, CoinCapAltTrans
import datetime

def GetHighestPrice(market, coin, span):
    """Params: Market, Span, Coin
    Span in seconds
    Highest Price of Coin, at Market in Span(Timespan)
    """
    spanAgo = datetime.datetime.now() - datetime.timedelta(seconds=span)
    if market == 'coincap':
        if coin == 'BTC':
            return (CoinCapBTCTrans
                .select()
                .where(CoinCapBTCTrans.timestamp >= spanAgo)
                .order_by(CoinCapBTCTrans.price.desc())
                .get())
        else:
            return (CoinCapAltTrans
                .select()
                .where((CoinCapAltTrans.timestamp >= spanAgo) & (CoinCapAltTrans.coinType == "%s/usd" % coin))
                .order_by(CoinCapAltTrans.price.desc())
                .get())
