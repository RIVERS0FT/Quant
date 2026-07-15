#!/usr/bin/env python3
from pathlib import Path
import re

STAGES = [
    "stage-06-cross-sectional-model-rolling-training",
    "stage-07-portfolio-optimization-risk-model",
    "stage-08-paper-and-small-capital-trading",
    "stage-09-agent-quant-research-system",
    "stage-10-automated-experiment-audit-elimination",
    "stage-11-multi-strategy-platform-capacity",
    "stage-12-personal-quant-platform",
]
ROOT = Path(__file__).resolve().parents[1] / "stages"


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def write(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_stage(stage: Path):
    stage_text = (stage / "README.md").read_text(encoding="utf-8")
    weeks_text = (stage / "weeks" / "README.md").read_text(encoding="utf-8")
    title = clean(re.search(r"^#\s*(.+)$", stage_text, re.M).group(1))
    period_m = re.search(r"\*\*时间：(.+?)\*\*", stage_text)
    goal_m = re.search(r"^目标：(.+)$", stage_text, re.M)
    result_m = re.search(r"阶段成果：(.+)$", stage_text, re.M)
    period = clean(period_m.group(1)) if period_m else ""
    goal = clean(goal_m.group(1)) if goal_m else f"系统掌握{title}所需的研究、工程、验证与治理能力。"
    project = clean(result_m.group(1)) if result_m else f"完成{title}阶段项目。"
    weeks = []
    for line in weeks_text.splitlines():
        match = re.match(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|", line)
        if match:
            weeks.append((int(match.group(1)), clean(match.group(2))))
    if len(weeks) != 13:
        raise RuntimeError(f"{stage.name}: expected 13 weeks, got {len(weeks)}")
    return title, period, goal, project, weeks


def build_stage(stage: Path) -> None:
    title, period, goal, project, weeks = parse_stage(stage)
    write(stage / "README.md", [
        f"# {title}", "", f"**时间：{period}**", "", "## 阶段目标", "", goal, "",
        "本阶段采用“概念与边界 → 数据与接口 → 基准实现 → 扩展实现 → 系统集成 → 测试审查 → 周项目”的固定节奏，保证学习内容最终沉淀为可复现成果。", "",
        "## 学习导航", "", "[进入 13 周学习计划](weeks/README.md)", "", "## 阶段项目", "", project, "",
        "## 阶段完成标准", "", "- 13 周均具有独立周目录、周目标、7 天学习路径和验收清单。",
        "- 核心模块具备清晰输入输出、配置、日志、测试和复现说明。", "- 数据、代码、参数、模型、策略或系统版本可以追踪。",
        "- 结果同时记录效果、风险、成本、稳定性、失败案例和适用边界。", "- 完成阶段项目、总结报告和下一阶段计划。",
    ])

    index = [f"# {title}：13 周学习计划", "", "| 周次 | 主题 | 周成果 |", "|---:|---|---|"]
    for number, topic in weeks:
        outcome = f"完成“{topic}”的可运行模块、测试与学习报告"
        index.append(f"| {number} | [{topic}](week-{number:02d}/) | {outcome} |")
    index += ["", "## 每周执行节奏", "", "1. 第 1 天理解概念、目标、适用条件和失败边界。", "2. 第 2 天整理数据、接口、时间语义、权限或约束。",
              "3. 第 3—4 天完成基准与扩展实现。", "4. 第 5 天接入既有研究、回测、交易或平台系统。", "5. 第 6 天进行测试、稳健性、风险或故障审查。",
              "6. 第 7 天完成周项目、复盘、文档和 Git 提交。", "", "## 统一原则", "", "- 先实现简单、透明、可验证的基准，再增加复杂度。",
              "- 所有数据、配置、代码、模型、策略和运行结果均可追踪。", "- 所有自动流程都具有限制、告警、停止条件和人工接管路径。",
              "- 评价同时覆盖效果、风险、成本、稳定性和维护复杂度。"]
    write(stage / "weeks" / "README.md", index)

    for number, topic in weeks:
        week = stage / "weeks" / f"week-{number:02d}"
        outcome = f"完成“{topic}”的可运行模块、测试与学习报告"
        write(week / "README.md", [
            f"# 第 {number} 周：{topic}", "", "## 本周目标", "",
            f"理解{topic}的核心概念、适用条件、工程接口、验证方法与主要风险，并将其接入个人量化研究平台。", "",
            "## 核心成果", "", outcome + "。", "", "## 每日安排", "", "[查看 7 天学习路径](days/README.md)", "", "## 完成标准", "",
            "- 能脱离代码解释核心概念、假设和不适用场景。", "- 输入、输出、数据时点、配置、版本和约束均有记录。",
            "- 至少覆盖正常、边界和失败案例，并完成自动测试或抽样核验。", "- 形成可复现的代码、配置、图表、报告或运行手册。",
        ])
        rows = [
            (1, "概念与边界", f"学习{topic}的定义、目标、术语、假设、适用条件与失败方式", "概念笔记与问题清单"),
            (2, "数据与接口", f"整理{topic}所需数据、输入输出、时间语义、权限和配置", "字段字典与接口契约"),
            (3, "基准实现", f"以最简单透明的方法实现{topic}的可运行基准，并构造小样本", "基准代码与样例"),
            (4, "扩展实现", "加入现实约束、异常处理、配置化、性能或自动化能力", "扩展模块"),
            (5, "系统集成", f"将{topic}接入已有数据、研究、回测、交易、Agent 或平台流程并对账", "端到端集成样例"),
            (6, "测试与审查", "执行单元、集成、稳健性、风险或故障测试，记录失败案例和限制", "测试与审查报告"),
            (7, "周项目与复盘", "整理代码、配置、日志、图表、文档和复现步骤，完成本周交付", outcome),
        ]
        days = [f"# 第 {number} 周每日学习路径：{topic}", "", "| 天 | 主题 | 学习与实践 | 当天输出 |", "|---:|---|---|---|"]
        days += [f"| {d} | {name} | {task} | {output} |" for d, name, task, output in rows]
        days += ["", "## 本周检查清单", "", "- [ ] 核心概念、适用边界和失败方式能够清楚说明。", "- [ ] 输入、输出、时间、权限、配置和版本均已记录。",
                 "- [ ] 正常、边界和失败案例至少各验证一次。", "- [ ] 核心结果可通过测试、对账、日志或抽样检查复核。",
                 "- [ ] 本周成果已提交 Git，并记录技术债与后续计划。", "", "## 学习记录", "", "- 本周最重要的新认识：",
                 "- 最容易出现的研究或系统偏差：", "- 尚未解决的问题：", "- 已提交的代码、配置或报告："]
        write(week / "days" / "README.md", days)


def main() -> None:
    for stage_name in STAGES:
        build_stage(ROOT / stage_name)


if __name__ == "__main__":
    main()
