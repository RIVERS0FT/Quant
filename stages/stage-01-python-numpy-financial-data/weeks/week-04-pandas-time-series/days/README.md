# 第 4 周每日学习路径

## 本周主题

pandas 基础与金融时间序列。

## 每日安排

| 天 | 主题 | 学习与实践 | 当天输出 | 状态 |
|---:|---|---|---|---|
| 1 | Series 与 DataFrame 基础 | 索引、列名、数据类型、形状和基础信息 | 股票日线 DataFrame | [已保存](day-01-series-and-dataframe-basics.md) |
| 2 | 数据读取、保存与字段类型 | CSV、Parquet、日期、股票代码和数值类型 | 标准类型行情文件 | [已保存](day-02-data-io-and-dtypes.md) |
| 3 | 日期索引与金融时间序列 | `DatetimeIndex`、排序、日期范围筛选 | 标准日期索引行情 | [已保存](day-03-datetime-index.md) |
| 4 | 筛选、排序与列操作 | `loc`、`iloc`、多条件筛选、新字段和重命名 | 行情筛选脚本 | [已保存](day-04-filter-sort-columns.md) |
| 5 | 长表与宽表 | `pivot`、`pivot_table`、`melt`、`stack`、`unstack` | 收盘价宽表 | [已保存](day-05-long-wide-format.md) |
| 6 | 标准行情表设计 | 字段规范、主键、缺失值、重复值和标准化函数 | 行情清洗模块 | [已保存](day-06-standard-market-schema.md) |
| 7 | 阶段项目与复习 | 清洗、排序、长宽表转换、保存与验证 | 标准行情表项目 | [已保存](day-07-project-and-review.md) |

## 推荐标准字段

```text
trade_date
stock_code
open
high
low
close
volume
amount
adj_factor
source
```

## 学习顺序

```text
认识 pandas 数据结构
    ↓
读取文件并修正类型
    ↓
建立日期索引和排序规则
    ↓
掌握筛选、排序和列操作
    ↓
完成长表与宽表转换
    ↓
建立标准行情字段规范
    ↓
完成标准行情表阶段项目
```

## 每日学习要求

每天按照以下结构推进：

1. 阅读核心概念；
2. 运行并修改示例代码；
3. 完成当日练习；
4. 保存代码和结果；
5. 回答自检问题；
6. 将完成状态更新为“已完成”。

## 检查清单

- [ ] 日期字段为日期类型；
- [ ] 股票代码使用字符串并保留前导零；
- [ ] OHLCV 字段为数值类型；
- [ ] 数据按股票代码和交易日期排序；
- [ ] `(trade_date, stock_code)` 主键无重复；
- [ ] 长表与宽表转换前后数据一致；
- [ ] CSV 与 Parquet 重新读取后类型符合预期；
- [ ] 原始数据与处理后数据分开保存。
