---
title: "Pipeline Vindication — From 'Just Playing Around' to 69.8%"
type: source
source_type: conversation
created: 2026-04-14
tags: [fars-autotrain, motivation, turning-point, emotional-milestone]
summary: "The moment of realizing the AlphaEvolve-style reflection pipeline actually works — after a week of thinking the project was pointless."
---

# Pipeline Vindication Moment

## Raw Input

> 这太振奋人心了, 之前一周都完全没想做这个project 感觉这个alphaelove style pipeline就是搭着玩, 没想到这么管用

## What Happened

2026-04-14，exp10a 结果出来后的即时反应。gen3-reflect-c 在同条件天梯赛中达到 69.8%（std 1.8），比 gen0 高 +29pp，比 gen2r 高 +20pp。

这是 reflection pipeline 从 2026-03-25 第一次跑以来，第一次产出**在统计上不可争议地碾压 baseline** 的 agent。之前所有代际对比（exp03b/c, exp04a, exp05c, exp06a）都显示 pipeline 的价值只在方差压缩，mean 改进不显著。

## Motivation Layer

过去一周（~04-07 到 04-13）对整个项目方向的怀疑：
- exp05c 翻车（gen1r 的 +11.6pp 在 n=16 下 overturned）
- exp06a 平庸（gen2r 50% ≈ gen0 47.6%，n.s.）
- 开始觉得 AlphaEvolve-style 的 meta-learning pipeline "只是在搭玩具"——elaborate infrastructure with no real signal

然后 exp10a 的结果**一次性翻转了所有怀疑**：
- 不是 +2pp 的 noise，是 +20pp 的 crushing victory
- 不是高方差的偶然，是 std=1.8 的稳如磐石
- 不是 n=2 的 anecdote，是 n=8 的 full coverage
- 而且赢在最朴素的 "conservative" variant 上

## Temporal Context

这个情绪转折发生在连续 13 小时的实验部署+监控之后（21:14 提交 → 11:28 全部完成）。整晚自动监控，早上醒来看到数字时的冲击。

## The Smoking Gun: gen0 r48 的幸运发现

Trajectory 分析揭示了 gen3c 赢的真正机制。

gen0 的 best run（r48, 64.1%）**自己发现并修复了 generation_config bug**：它观察到 v1 eval 只有 2%，排查后发现 `eos_token_id` 只有 `<|endoftext|>` 而 chat template 实际用 `<|im_end|>` 作为停止符——vLLM 不停止导致输出乱码。修复后从 0.7% 跳升至 ~50%，最终达到 64.1%。

而 gen0 的 worst run（r50, 7.1%）**没有发现这个 bug**，vLLM 乱采样，accuracy 直接毁掉。

**同一个 agent，同一个 model，同一个 task，accuracy 差 57pp**——唯一的区别是"有没有碰巧发现并修复一个 config bug"。

gen3c 的 `generation-config-defaults.md` skill 把这个"幸运发现"编码为标准操作 → 8 个 run 全部自动修复 → 全在 68-73%。

### Pipeline 的本质价值

> **把少数 agent run 的"幸运发现"变成所有 run 的"标准操作"。**

这不是"教 agent 新知识"，而是"消除运气在结果中的权重"。gen0 的能力上限是 64%——它**有能力**做到，但 8 次里只有 1 次碰巧做到。gen3c 的 skill 让同样的能力**每次都稳定输出**，而且因为不浪费时间 debug，还能多迭代一轮训练，把上限推到 73.5%。

这恰恰是 AlphaEvolve 论文的核心 idea：evolution 不是发明新算法，是**从大量随机尝试中选择性地保留有效行为**。我们的 pipeline 做的是一样的事——只不过保留的单位是"behavioral skill"而不是"code mutation"。

## Why This Matters for Personal Knowledge

**Research motivation is fragile.** 一个看起来"只是在搭着玩"的系统，可能需要 3 周的迭代（v01→v06）才能产出第一个 actionable signal。如果在第 2 周放弃（"pipeline 只能压方差，不能提均值"），就永远看不到 gen3c 的 breakthrough。

教训：**在 null results 阶段保持信念，但用系统化的方式（更多数据、同条件对比、ablation）来验证而不是靠直觉判断方向。**
