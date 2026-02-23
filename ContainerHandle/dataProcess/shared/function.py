
from typing import TYPE_CHECKING, TypeVar

from pandas import date_range

if TYPE_CHECKING:
    from pandas import DataFrame

OutputType = TypeVar('OutputType', 'DataFrame', dict[str, 'DataFrame'])

# return dataframe with standard date range
def standard_dataframe_index(df: 'DataFrame', freq='h') -> 'DataFrame':
    start = df.index.min().replace(minute=0, second=0, microsecond=0)
    end = df.index.max().replace(minute=0, second=0, microsecond=0)

    std_idx = date_range(start=start, end=end, freq=freq)

    return df.reindex(std_idx)

def standard_output(output: OutputType) -> OutputType:

    if isinstance(output, dict):
        for key in output:
            output[key] = standard_dataframe_index(output[key])
    else:
        output = standard_dataframe_index(output)

    return output

