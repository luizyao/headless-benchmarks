import re
from decimal import ROUND_UP, Decimal
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

console = Console()


class CustomDecimal(Decimal):
    @classmethod
    def __get_validators__(cls):
        yield cls.validator

    @classmethod
    def validator(cls, v: float):
        if not isinstance(v, float):
            raise TypeError("float required.")
        return cls.from_float(v).quantize(Decimal(".001"), rounding=ROUND_UP)


class AggregateResults(BaseModel):
    #: 平均值
    mean: CustomDecimal

    #: 标准差
    sd: CustomDecimal

    #: 相对标准差
    rsd: CustomDecimal

    #: P95
    p95: CustomDecimal


def aggregate_results(results: List[float]) -> AggregateResults:
    """
    返回指定列表中数据的平均值、标准差、相对标准偏差和P95。
    :param results:
    :return:
    """
    arr = np.array(results)
    mean = arr.mean()
    sd = arr.std()
    rsd = sd / mean
    p95 = sorted(results, reverse=True)[50]
    return AggregateResults(mean=mean, sd=sd, rsd=rsd, p95=p95)


def aggregate_results_table(caption: str, pattern: str):
    aggregate_results_table = Table(
        caption=caption, expand=True, header_style="bold magenta"
    )
    aggregate_results_table.add_column("无头模式", justify="center")

    internal_table = Table(expand=True, show_edge=False)
    internal_table.add_column(justify="center")

    aggregate_results_list = []
    for p in sorted(Path("results").glob(f"*{pattern}.txt")):
        name = re.search(r"([a-z0-9A-Z\-]+){}".format(pattern), p.stem).group(1).upper()
        internal_table.add_column(name, justify="center")

        with p.open() as f:
            results: List[float] = list(map(float, f.readlines()))
        a_results = aggregate_results(results)
        aggregate_results_list.append(
            [a_results.mean, a_results.sd, a_results.rsd, a_results.p95]
        )

    aggregate_results_array = np.array(aggregate_results_list).T
    measurements = ["平均值", "标准差", "标准偏差", "P95"]
    for key, values in zip(measurements, aggregate_results_array):
        internal_table.add_row(key, *map(str, values))

    aggregate_results_table.add_row(internal_table)

    console.log(aggregate_results_table)


def add_plot(pattern: str, title: str):
    fig, ax = plt.subplots()
    for p in sorted(Path("results").glob(f"*{pattern}.txt")):
        name = re.search(r"([a-z0-9A-Z\-]+){}".format(pattern), p.stem).group(1).upper()
        with p.open() as f:
            results: List[float] = list(map(float, f.readlines()))
        ax.plot(range(1, 1001), results, label=name)

    ax.set_xlabel("Count")
    ax.set_ylabel("Execution Time(sec)")
    ax.set_title(title)
    ax.legend()


if __name__ == "__main__":
    console.log("汇总测试结果", style="bold green", justify="center")

    aggregate_results_table(caption="表-1：登录 pihole 的测试结果", pattern="-login")

    aggregate_results_table(caption="表-2：管理 pihole 的测试结果", pattern="-manage")

    add_plot(pattern="-login", title="login pihole: playwright vs playwright-python")

    add_plot(pattern="-manage", title="manage pihole: playwright vs playwright-python")

    plt.show()
