import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.kraken.definitions import (
    TIMEFRAMES,
    TIMESTAMP_S,
    COUNT,
    ORDERID,
    ORDERSTATUS,
    ORDERTYPE,
    ORDERSIDE,
    FLAGS
)



# ============================================================
# QUERY LEDGERS
# ============================================================


# doc: https://www.kraken.com/features/api#query-ledgers

URL = "https://api.kraken.com/0/public/QueryLedgers"
METHOD = "POST"


# ------------------------------
# Sample Response (ccxt)
# ------------------------------


# { error: [],
#   result: {'LPUAIB-TS774-UKHP7X': {  refid: "A2B4HBV-L4MDIE-JU4N3N",
#                                         time:  1520103488.314,
#                                         type: "withdrawal",
#                                       aclass: "currency",
#                                        asset: "XETH",
#                                       amount: "-0.2805800000",
#                                          fee: "0.0050000000",
#                                      balance: "0.0000051000"           }}}


# ------------------------------
# Request
# ------------------------------

class _QueryLedgersReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/QueryLedgers

    Fields:
    -------
        id : List[str]
            Comma delimited list of ledger ids to query info about (20 maximum)
        nonce : int
            Always increasing unsigned 64 bit integer
    """

    id: typing.List[str]
    nonce: pydantic.PositiveInt


# ------------------------------
# Response
# ------------------------------


def generate_model(keys: typing.List[ORDERID]) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model"


    class _Ledger(pydantic.BaseModel):

        refid: typing.Optional[str]
        time: TIMESTAMP_S
        type: str
        aclass: str
        asset: str
        amount: Decimal
        fee: Decimal
        balance: Decimal

    # we do not know the keys in advance, only the type of their value
    kwargs = {
        **{k: (_Ledger, ...) for k in keys},
        "__base__": pydantic.BaseModel
    }

    model = pydantic.create_model(
        '_QueryLedgersResp',
        **kwargs    #type: ignore
    )

    return model


class _QueryLedgersResp(pydantic.BaseModel):
    """Response Model for endpoint https://api.kraken.com/0/public/QueryLedgers

    Fields:
    -------
        `Ledger d` : leger info
            mapping of ledger id to their info
                ledger id : str
                ledger info : dict
    
    Note:
    -----
        Ledger Info dict type:
            refid: str
                Reference id
            time : float
                Unix timestamp of ledger in seconds
            type : str
                Type of ledger entry
            aclass : str
                Asset class
            asset : str
                Asset
            amount : Decimal
                Transaction amount
            fee : Decimal
                Transaction fee
            balance : Decimal
                Resulting balance
   """


    def __call__(self, **kwargs):
        model = generate_model(list(kwargs.keys()))
        print("\nFields", model.__fields__, "\n")
        return model(**kwargs)