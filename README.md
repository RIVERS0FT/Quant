# 个人量化研究学习路线

> 目标：用 36 个月完成从 Python 与金融数据基础，到 A 股研究、因子模型、机器学习、组合管理、模拟实盘、Agent 研究系统和个人量化平台的完整能力建设。

## 仓库结构

```text
Quant/
├── README.md                         # 36 个月总学习大纲
└── stages/
    ├── stage-01-python-numpy-financial-data/
    │   ├── README.md                 # 阶段目标与周计划
    │   └── weeks/
    │       ├── week-01-python-environment-basics/
    │       │   ├── README.md         # 本周目标、知识点与成果
    │       │   └── days/             # 按天学习路径
    │       └── ...
    ├── stage-02-a-share-data-backtesting/
    └── ...
```

## 36 个月阶段路线

| 阶段 | 时间 | 主题 | 阶段目录 |
|---|---:|---|---|
| 01 | 第 1—3 个月 | Python、NumPy 与金融数据基础 | [进入阶段](stages/stage-01-python-numpy-financial-data/) |
| 02 | 第 4—6 个月 | A 股数据处理与日频回测系统 | [进入阶段](stages/stage-02-a-share-data-backtesting/) |
| 03 | 第 7—9 个月 | 统计检验与因子研究 | [进入阶段](stages/stage-03-statistical-testing-factor-research/) |
| 04 | 第 10—12 个月 | 多因子组合与完整研究项目 | [进入阶段](stages/stage-04-multifactor-portfolio-project/) |
| 05 | 第 13—15 个月 | 机器学习量化基础 | [进入阶段](stages/stage-05-machine-learning-quant-basics/) |
| 06 | 第 16—18 个月 | 截面选股模型与滚动训练 | [进入阶段](stages/stage-06-cross-sectional-model-rolling-training/) |
| 07 | 第 19—21 个月 | 组合优化与风险模型 | [进入阶段](stages/stage-07-portfolio-optimization-risk-model/) |
| 08 | 第 22—24 个月 | 模拟交易与小资金实盘验证 | [进入阶段](stages/stage-08-paper-and-small-capital-trading/) |
| 09 | 第 25—27 个月 | Agent 量化研究系统 | [进入阶段](stages/stage-09-agent-quant-research-system/) |
| 10 | 第 28—30 个月 | 自动实验、审计与策略淘汰机制 | [进入阶段](stages/stage-10-automated-experiment-audit-elimination/) |
| 11 | 第 31—33 个月 | 多策略平台与容量管理 | [进入阶段](stages/stage-11-multi-strategy-platform-capacity/) |
| 12 | 第 34—36 个月 | 个人量化研究平台定型 | [进入阶段](stages/stage-12-personal-quant-platform/) |

## 第 1—3 个月周学习路线

| 周次 | 主题 | 核心内容 | 周成果 |
|---:|---|---|---|
| 第 1 周 | Python 开发环境与基础语法 | Python 环境、虚拟环境、变量、数据类型、条件判断、循环、函数、异常处理、文件路径、Git 基础 | 创建个人量化研究仓库，编写并运行第一个收益率函数 |
| 第 2 周 | NumPy 与单资产收益率 | 数组、索引、切片、数据类型、向量化、简单收益率、对数收益率、累计净值、NaN 与无穷值 | 完成收益率计算模块及单元测试 |
| 第 3 周 | NumPy 二维数组与多资产计算 | 二维矩阵、axis、广播、布尔筛选、多股票价格矩阵、多资产收益率、均值与波动率 | 完成多股票收益率和波动率计算程序 |
| 第 4 周 | pandas 基础与金融时间序列 | Series、DataFrame、日期索引、筛选、排序、CSV 与 Parquet、长表与宽表 | 将原始日线数据整理为标准行情表 |
| 第 5 周 | pandas 分组与滚动计算 | groupby、shift、rolling、rank、merge、多股票分组计算、未来收益标签 | 计算 5 日、20 日收益、均线、波动率和截面排名 |
| 第 6 周 | SQL、DuckDB 与数据存储 | SQL 查询、筛选、聚合、连接、窗口函数、DuckDB、Parquet 分区、查询效率 | 建立本地行情数据库并完成基础查询脚本 |
| 第 7 周 | 描述统计与收益分布 | 均值、中位数、方差、标准差、分位数、偏度、峰度、相关系数、异常值 | 完成多股票收益分布分析报告 |
| 第 8 周 | 概率、抽样与假设检验 | 样本与总体、标准误、置信区间、t 检验、p 值、第一类错误、多重检验 | 完成一次简单事件研究 |
| 第 9 周 | 策略绩效指标 | 年化收益、年化波动率、夏普比率、最大回撤、Calmar、胜率、盈亏比、超额收益 | 编写统一绩效评价模块 |
| 第 10 周 | A 股价格、复权与公司行为 | 原始价格、前复权、后复权、复权因子、分红、送股、拆股、价格收益与总收益 | 比较同一股票不同复权方式下的收益差异 |
| 第 11 周 | A 股股票池与交易规则 | 幸存者偏差、历史成分股、新股、退市、ST、停牌、涨跌停、T+1、整手交易 | 建立股票可交易状态字段 |
| 第 12 周 | 数据质量与阶段项目 | 重复数据、缺失值、异常价格、时间错位、字段校验、数据版本、自动测试 | 完成 A 股日线数据质量报告和阶段总结 |

## 学习执行规则

1. 每周以一个可验证成果结束，不只停留在阅读和记忆。
2. 每天学习文件按“目标、概念、实践、输出、检查清单”组织。
3. 代码、数据、报告分目录保存，保证研究过程可复现。
4. 所有收益计算明确价格口径、复权方式、手续费和时间对齐规则。
5. 每周最后一天完成复盘、测试和 Git 提交。

## 推荐学习节奏

- 工作日：概念学习 30—45 分钟，实践 45—90 分钟。
- 周末：综合练习、项目迭代、错题整理和阶段复盘。
- 遇到公式时使用标准 Markdown 数学语法：行内 `$R_t$`，独立公式使用 `$$...$$`。

## 当前阶段

从 [阶段 01：Python、NumPy 与金融数据基础](stages/stage-01-python-numpy-financial-data/) 开始。