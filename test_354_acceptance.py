#!/usr/bin/env python3
"""python-tabulate #354 的验收（可执行断言，不是形容词）。

用法：在 python-tabulate 的 clone 根目录跑
    PYTHONPATH=. python3 test_354_acceptance.py
全部 PASS 退出码 0；有 FAIL 退出码 1。改前应当看见 A 是红的。
"""
import sys

from tabulate import _wrap_text_to_colwidths, tabulate

CELL = "The files were concatenated and archived for posterity."


def cell_width(header, w):
    """渲染出来那一格的内容宽（去掉 fancy_grid 两侧各一个空格）。"""
    t = tabulate([[CELL]], headers=[header], tablefmt="fancy_grid", maxcolwidths=[w])
    lines = [l for l in t.splitlines() if l.startswith("\u2502")]
    cell = lines[1].split("\u2502")[1]
    return len(cell) - 2


def check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + "{}: 实测={} 期望={}".format(name, got, want))
    return ok


def main():
    results = []

    # A：表头 8 字、上限 8 → 内容宽必须是 8。
    #    改前实测 10（单元格宽 12），这就是 #354 的偏差本身。
    results.append(check("A 表头 Header#3 + maxcolwidths=8", cell_width("Header#3", 8), 8))

    # B：表头比上限短时本来就对。用来证明缺陷跟表头长度有关，不是折行。
    results.append(check("B 表头 h1 + maxcolwidths=8", cell_width("h1", 8), 8))

    # C：数据格的折行不许被改动（上限就是上限，最长行必须等于 8）。
    #    它是护栏：谁去“修” TextWrapper，这条就会红。
    wrapped = _wrap_text_to_colwidths([[CELL]], [8])[0][0]
    longest = max(len(line) for line in wrapped.split("\n"))
    results.append(check("C 折行最长行 <= 上限", longest, 8))

    print("---")
    print("结论：{}".format("全部通过" if all(results) else "有 FAIL，别提交补丁"))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
