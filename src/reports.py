import datetime as dt
import json
import logging
from collections.abc import Callable
from os import makedirs
from typing import Optional, ParamSpec

import pandas as pd

P = ParamSpec("P")

log_file = "logs/reports.log"
log_ok_str = "was executed without errors"
makedirs("logs", exist_ok=True)
logger = logging.getLogger(__name__)
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler = logging.FileHandler(log_file, mode="w")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def write_report(
    filename: Optional[str] = None,
) -> Callable[[Callable[P, pd.DataFrame]], Callable[P, None]]:
    """декоратор для записи отчетов в json"""

    def decorator(inner: Callable[P, pd.DataFrame]) -> Callable[P, None]:

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:

            report_filename = ""
            inner_name = inner.__name__
            if filename is None:
                date = dt.date.today().strftime("%Y-%m-%d")
                report_filename = f"data/{inner_name}_{date}.json"
            else:
                report_filename = filename
            inner_result = inner(*args, **kwargs)
            json_data = inner_result.to_dict("records")
            try:
                with open(report_filename, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False)
            except Exception as e:
                logger.error(f"decorator write_report was executed with error: {e}, func is {inner_name}")
        return wrapper
    return decorator


@write_report()
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """отчет за 3 месяца"""

    filtered_df = pd.DataFrame()
    date_end = dt.date.today()
    if date is not None:
        try:
            date_end = dt.datetime.strptime(date, "%d.%m.%Y").date()
        except Exception as e:
            logger.warning(f"spending_by_category was executed with error: {e}, date: {date}, used current date.")
    date_start = date_end - dt.timedelta(days=1)
    month_start = (date_start.month + 9) % 12
    date_start = date_start.replace(month=month_start)
    if date_start > date_end:
        year_start = date_end.year - 1
        date_start = date_start.replace(year=year_start)
    try:
        transactions["payment_date"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y").dt.date
    except Exception as e:
        logger.error(f"spending_by_category was executed with error: {e}")
        return filtered_df
    try:
        filtered_df = transactions.loc[
            (transactions["Статус"] == "OK")
            & (transactions["Сумма платежа"] < 0)
            & (transactions["Категория"] == category)
            & (transactions["payment_date"] <= date_end)
            & (transactions["payment_date"] >= date_start)
        ]
    except Exception as e:
        logger.error(f"spending_by_category was executed with error: {e}")
        return filtered_df
    logger.debug(f"spending_by_category {log_ok_str}")
    return filtered_df.drop(columns=["payment_date"])
