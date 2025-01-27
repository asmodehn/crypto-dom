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
    COUNT
)



# ============================================================
# SPREAD
# ============================================================


# doc: https://www.kraken.com/features/api#get-recent-spread-data 

URL = "https://api.kraken.com/0/public/Spread"
METHOD = "GET"

# ------------------------------
# Request
# ------------------------------

class _SpreadReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/Spread

    Fields:
    -------
        pair : str 
            Asset pair to get spread data for
        since : int 
            Timestamp in seconds
            Return trade data since given id (optional)
    """

    pair: str
    # timestamp in seconds
    since: typing.Optional[TIMESTAMP_S]

    @pydantic.validator('since')
    def check_year_from_timestamp(cls, v):
        if v == 0 or v is None:
            return v

        y = date.fromtimestamp(v).year
        if not y > 2009 and y < 2050:
            err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
            raise ValueError(err_msg)
        return v


# ------------------------------
# Response
# ------------------------------


def generate_model(pair: str) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model"


    class _BaseSpreadResp(pydantic.BaseModel):

        # timestamp received from kraken in s
        last: TIMESTAMP_S

        @pydantic.validator('last')
        def check_year_from_timestamp(cls, v, values):
            # convert from ns to s

            y = date.fromtimestamp(v).year
            if not y > 2009 and y < 2050:
                err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
                raise ValueError(err_msg)
            return v

    _Spread = typing.Tuple[Decimal, Decimal, Decimal]

    kwargs = {
        pair: (typing.Tuple[_Spread, ...], ...),
        "__base__": _BaseSpreadResp
    }

    model = pydantic.create_model(
        '_SpreadResp',
        **kwargs    #type: ignore
    )

    return model



class _SpreadResp:
    """Response Model for endpoint https://api.kraken.com/0/public/Spread

    Fields:
    -------
        `pair_name` : str
            Array of array entries (time, bid, ask)
        last: int
            Timestamp in seconds
            Id to be used as since when polling for new spread dat
    """

    def __new__(_cls, pair: str):
        model = generate_model(pair)
        return model
