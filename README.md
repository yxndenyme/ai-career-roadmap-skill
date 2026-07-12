# AI职业机会分析与学习路线

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](LICENSE)
[![skills.sh](https://skills.sh/b/yxndenyme/ai-career-roadmap-skill)](https://skills.sh/yxndenyme/ai-career-roadmap-skill)

一个面向不同学历、技术基础和行业背景的中文 Agent Skill。它读取简历或通过问答建立个人画像，研究最新 AI 与泛 AI 产业、公司和职位，评估可迁移能力与现实差距，并生成由使用者自定义周期的学习和求职路线。

English: A Chinese-first agent skill that turns a resume or guided intake into current AI and AI-adjacent career opportunities, realistic role matching, skill-gap analysis, and a personalized learning roadmap.

![AI职业机会分析与学习路线](assets/logo.svg)

## 核心能力

- 读取简历、作品集、职位描述，或在没有简历时进行引导式问答。
- 覆盖大模型、智能体、企业 AI、智能驾驶、物理 AI、机器人、科学智能、AI 治理等赛道。
- 区分已核验当前机会、相邻职位、新兴职位、中长期预测和观察清单。
- 根据可迁移经历、市场证据、资质、技术基础和现实约束进行岗位评分。
- 输出主攻职位、强相邻职位、长期专项和“不建议优先投入”方向。
- 将学习内容拆分为通识、职位专项和行业专项。
- 按4周至6个月以上的自定义周期，生成逐周文档、视频、练习、作品和求职行动。
- 默认保护简历隐私，不编造成就、招聘、薪酬或就业承诺。

## 快速安装

### Skills CLI / Skills.sh

```bash
npx skills add yxndenyme/ai-career-roadmap-skill
```

### Claude Code：GitHub 市场

```text
/plugin marketplace add yxndenyme/ai-career-roadmap-skill
/plugin install ai-career-roadmap-skill@ai-career-roadmap-marketplace
```

### Claude Code：本地测试

```bash
claude --plugin-dir .
claude plugin validate
```

### OpenAI / ChatGPT / Codex

仓库已经包含 `.codex-plugin/plugin.json`。公开商店版本需要先通过 OpenAI 插件审核；开发阶段可将仓库打包为 ZIP，在插件提交门户选择 `Skills only`。

### ClawHub / OpenClaw

公开发布后可使用：

```bash
openclaw skills install generate-ai-career-roadmap
```

### 扣子

在扣子技能商店或扣子编程中选择“创建技能”，上传发布包中的扣子 ZIP，完成部署测试后再申请公开上架。

## 调用示例

```text
使用 generate-ai-career-roadmap 分析我上传的简历，研究中国市场最新的AI与泛AI工作机会，并生成16周、每周8小时的职业发展报告。
```

```text
我没有简历。请先通过提问了解我的工作经历、能力和约束，再推荐现实的AI相邻职位。
```

```text
更新我现有报告中的新行业、新公司、新职位和中文学习资源，不要重写已经完成的学习阶段。
```

## 报告包含什么

1. 个人画像、事实、假设和约束。
2. AI 与泛 AI 产业地图和出现条件。
3. 公司、当前招聘、新兴机会和观察清单。
4. 职位评分、可迁移证据和现实障碍。
5. 通识、职位专项和行业专项能力差距。
6. 自定义周期的逐周学习路线。
7. 作品集、简历定位、投递和反馈闭环。
8. 来源、核验日期、风险和替代路线。

## 隐私与安全

- 上传前建议删除电话、住址、证件号、推荐人和雇主机密。
- Skill 本身不运营独立服务器；实际数据处理由运行平台决定。
- 不会自动替使用者投递职位、发送简历或联系公司。
- 所有时效性职位和政策都应在采取行动前再次核验。

完整说明见 [隐私政策](PRIVACY.md) 和 [使用条款](TERMS.md)。

## 项目结构

```text
.codex-plugin/       OpenAI/Codex 插件清单
.claude-plugin/      Claude Code 插件和市场清单
assets/              公共品牌素材
docs/                GitHub Pages 官网
skills/              通用 Agent Skill
submissions/         各商店审核资料
scripts/             生成和发布前检查工具
```

## 作者

**yxn否定我（Yang）** 专注于把 AI 产业前沿、职位变化和个人既往经验，转化为现实、可验证、可持续调整的职业发展路线。希望帮助不同学历、技术基础和行业背景的人，以证据为基础进入 AI 与泛 AI 领域。

## 许可

项目使用 [MIT-0](LICENSE) 许可证，可免费使用、修改和再发布，无署名要求。

问题、安全或隐私反馈：100995431@qq.com
