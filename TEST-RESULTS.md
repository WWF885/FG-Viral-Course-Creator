# V1.0.0 本地测试记录
测试日期：2026-11-24。运行环境：Python 3.13.5、Chromium、Playwright。

|项目|结果|证据|
|---|---|---|
|SKILL.md YAML 元数据、目录名、阶段引用、基础密钥模式检查|通过|`python scripts/course.py validate`，另用 PyYAML 解析 frontmatter|
|状态脚本自动化单元测试|15/15 通过|`python -m unittest discover -s tests -v`；六模式路由、无覆盖、顺序校验、缺失/越界证据、变更复核、模式切换、无发布授权等|
|视觉组件渲染|26/26 通过|`tests/browser_check.py` 断言每种组件产生SVG|
|问答反馈、动态步骤、导航、翻页边界、键盘、全屏|通过|Chromium 实际操作；页面脚本错误0|
|HTML本地文件路径直接打开|未验证|测试环境管理策略禁止 file://；将同一 JS 内联加载至测试页面后进行实际交互验证，相对引用路径静态检查通过|
|跨Agent端到端教学创作|未执行|`tests/scenarios.md` 14个计划用例；不是本地脚本测试结果|
|真实学员试学及商业课程质量|未执行|不适用开源包结构验收，不能宣称完整课程正式发布达标|

可选浏览器复测（需安装 Playwright 与 Chromium，非核心Skill运行依赖）：`CHROMIUM_PATH=/usr/bin/chromium python tests/browser_check.py`。Windows PowerShell 可先设置 `$env:CHROMIUM_PATH='实际Chromium路径'`，再执行脚本；不指定时使用Playwright配置的浏览器。

公开包只含通用规则、原创模板/组件、脱敏模拟示例，未复制完整商业课程。基础密钥模式检查并非全面安全审计。尚未执行 GitHub 创建或推送。
