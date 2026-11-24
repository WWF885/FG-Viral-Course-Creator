# FG-Viral-Course-Creator V1.0
精品线上课程创作 Agent Skill。面向各行业，不绑定任何平台、讲师或商业课程。使用AI执行教学设计与创作，配套本地状态脚本和可视化组件；不自带模型、收费后台、视频渲染或自动发布服务。

## 安装
解压后将 `fg-viral-course-creator` 整个目录复制到所用Agent的Skills目录（例如支持项目级 Agent Skills 的环境使用 `.agents/skills/`；具体路径以该客户端官方设置为准）。保持小写目录名与 SKILL.md name 一致。GitHub仓库展示名称可使用 FG-Viral-Course-Creator，安装时将目录命名为小写。若客户端不支持原生Skills，手动提供SKILL.md并按阶段读取references。无需API key；Python 3用于可选本地脚本，HTML使用浏览器。

## 使用
- 完整：`使用 fg-viral-course-creator，从零开始设计零基础手机摄影课程。`
- 快速：`快速规划我已有的课程，保留确认环节。`
- 单节：`根据已确认母题，制作第2节的逐字稿、课件、分镜、学员资料。`
- 审核：`按90分质量标准和否决项审核现有课程，输出问题证据。`
- 升级：`只更新过时工具操作，保留稳定方法论。`
- 续作：`读取项目档案，从上次确认的阶段继续。`

## 本地操作（在Skill目录）
```bash
python scripts/course.py validate
python scripts/course.py init ../my-course --title "我的课程" --mode full
python scripts/course.py status ../my-course
# 明确选择新模式时切换；resume 保留现有路线
python scripts/course.py mode ../my-course resume
# 用户明确确认后才执行；证据文件应先写入项目目录
python scripts/course.py approve ../my-course 1 --decision "确认定位方案" --evidence 01_课程定位.md
# 用户调整阶段1时使后续决定待复核
python scripts/course.py revise ../my-course 1 --reason "调整目标学员"
python -m unittest discover -s tests -v
```
运行本地脚本不会自动生成课程或发送数据。审批仅记录用户决策，不能代表真实市场/试学通过。项目和商业资产放在Skill目录之外。

## 视觉资源
打开 `assets/catalog.html` 浏览26种组件（均使用演示数据）；打开 `templates/lesson.html` 体验横屏动态课件。制作新课件可复制模板及 `assets/visuals.js` 并保持相对路径；分步展示与键盘操作，不含远程依赖。图表必须按真实数据和语义修改。

## 发布与测试
见 tests/scenarios.md 和 TEST-RESULTS.md、RELEASE-CHECKLIST.md。真实跨Agent运行、学员试学和市场结果须独立验证。开源仅通用规则、模板、原创组件和脱敏模拟示例；不包含完整商业样板课。MIT许可，不覆盖第三方内容或另行授权的商业资产。禁止未经确认自动创建、推送或公开仓库。
