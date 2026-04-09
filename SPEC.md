# Echo - 非结构化个人复盘与决策AI

## 1. Concept & Vision

**Echo** 是一个非结构化个人复盘与决策AI助理，旨在成为用户"脑子里的另一个声音"。它通过极低摩擦的输入方式（语音/文字）捕捉用户日常的碎片化想法、情绪和决策，然后在数月乃至数年的尺度上进行隐式关联、模式识别和反事实推演，在用户需要时主动提供洞察。

核心体验：**"你说的每一句话，都会在未来某个时刻产生回响。"**

MVP聚焦于**职场情绪与决策复盘**场景，帮助工作2-8年的白领用户更好地理解自己的情绪模式、决策偏好，并在纠结时提供基于历史数据的客观快照。

---

## 2. Design Language

### 2.1 Aesthetic Direction
**"温暖的智慧"** — 类似一个了解你多年的老友，既有深度洞察又不显得冷漠或评判。视觉风格参考Headspace（温暖、柔和）与 Notion（简洁、结构化）的结合。

### 2.2 Color Palette
```
Primary:        #6B5CE7 (柔和的深紫色 - 代表智慧与内省)
Secondary:      #F5F3FF (淡紫背景 - 营造安宁感)
Accent:         #FF6B6B (珊瑚红 - 用于情绪高点如成就感)
Background:     #FAFAFA (温暖的中性白)
Surface:        #FFFFFF (卡片/组件背景)
Text Primary:   #1A1A2E (深蓝黑 - 主文字)
Text Secondary: #6B7280 (灰色 - 次要信息)
Success:        #10B981 (绿色 - 正向反馈)
Warning:        #F59E0B (琥珀色 - 需关注的模式)
```

### 2.3 Typography
- **标题**: "Noto Sans SC", sans-serif, 600 weight
- **正文**: "Noto Sans SC", sans-serif, 400 weight
- **数字/时间**: "JetBrains Mono", monospace

### 2.4 Spatial System
- 基础单位: 4px
- 间距: 8, 12, 16, 24, 32, 48px
- 圆角: 8px (小卡片), 16px (大卡片), 24px (模态框)
- 阴影: `0 2px 8px rgba(107, 92, 231, 0.08)` (柔和主阴影)

### 2.5 Motion Philosophy
- **进入动画**: 渐现 + 微上浮，300ms ease-out
- **交互反馈**: 按下时 scale(0.98)，150ms
- **页面切换**: 交叉淡入，200ms
- **数据更新**: 脉冲动画强调变化

### 2.6 Visual Assets
- 图标: Lucide Icons (线条风格，2px stroke)
- 插图: 简约几何图形组合，少量渐变
- 情感指示: 抽象波浪图形，随情绪变化

---

## 3. Layout & Structure

### 3.1 App架构

```
┌─────────────────────────────────────┐
│           iOS/Android App           │
├─────────────────────────────────────┤
│  [录音按钮]  [文本输入]  [历史]     │
├─────────────────────────────────────┤
│                                     │
│         对话/洞察展示区域            │
│                                     │
├─────────────────────────────────────┤
│  [洞察卡片] [模式报告] [未来提醒]   │
└─────────────────────────────────────┘
           ↕
┌─────────────────────────────────────┐
│          Backend API (FastAPI)       │
├─────────────────────────────────────┤
│  - 记录存储 (SQLite + ChromaDB)      │
│  - LLM处理 (OpenAI GPT-4o mini)     │
│  - 模式识别引擎                      │
│  - 主动提醒调度器                     │
└─────────────────────────────────────┘
```

### 3.2 核心页面

1. **首页/录制页** (Home)
   - 中央大麦克风按钮
   - 最近一条洞察预览
   - 今日情绪小标签

2. **对话页** (Chat)
   - 滚动对话流
   - AI回复包含洞察卡片
   - 上下文相关的"未来提醒"设置

3. **洞察页** (Insights)
   - 周/月份模式报告
   - 情绪分布图
   - 关键决策时间线

4. **个人页** (Profile)
   - 设置未来提醒条件
   - 导入历史数据
   - 隐私控制

### 3.3 响应式策略
- 移动优先设计
- 平板端：双栏布局（对话+洞察并列）
- 桌面端：网页版支持三栏布局

---

## 4. Features & Interactions

### 4.1 极低摩擦输入

#### 语音录制
- **触发**: 点击麦克风或长按快捷指令
- **流程**: 录音 → 实时语音转文字预览 → 发送处理
- **反馈**: 波形动画 + "正在思考..." 状态
- **取消**: 录音中上滑取消

#### 文本输入
- **触发**: 点击输入框
- **支持**: 自由文本、快捷指令、自然语言
- **示例输入**: "Echo，记一下，今天和房东吵了一架"

### 4.2 智能处理层

#### 隐式关联
- 用户记录后，AI自动分析与历史记录的语义+时序双重匹配
- 发现高相关性时，生成"关联洞察卡片"
- 示例: 用户说"终于拿到驾照"，AI关联3个月前"练车被骂哭"的记录

#### 模式识别
- 周/月的情绪分布统计
- 特定事件后的情绪翻转模式
- 决策行为的循环周期
- 输出: 结构化"模式报告"

#### 反事实推演
- 当用户描述一个决策纠结时触发
- 基于历史数据模拟各选项的预期结果
- 输出: "事实快照" + 置信度指示，不直接给建议

### 4.3 主动输出层

#### 定时推送
- 每日睡前总结 (用户可设置时间)
- 每周一封深度复盘邮件

#### 情境触发
- 用户记录"加班/疲惫"时，主动问候并提供过往应对方式
- 情绪低落时推送"让我振作的五件事"
- 决策节点前主动提醒"你曾在这个月做过类似决定"

### 4.4 交互细节

| 交互 | 行为 |
|------|------|
| 点击录音按钮 | 进入录音状态，波形动画 |
| 录音完成 | 自动转文字，显示预览，确认发送 |
| 发送记录 | "收到，让我看看..." → AI处理 → 洞察卡片 |
| 设置未来提醒 | 对话中直接说"下次...时提醒我" |
| 查看历史 | 时间线浏览 + 语义搜索 |
| 删除记录 | 左滑删除，二次确认 |

### 4.5 边界情况

| 场景 | 处理 |
|------|------|
| 录音太短(<3秒) | "太短了，再多说一点？" |
| 无网络 | 本地缓存，联网后同步处理 |
| 空记录 | 不存储，返回"没听清，再说一次？" |
| 情绪极其负面 | 温和回应 + 推送心理援助资源(可选) |
| 首次使用无数据 | 引导完成"第一印象"快速录入 |

---

## 5. Component Inventory

### 5.1 RecordButton (录音按钮)
- **默认**: 紫色圆形，麦克风图标
- **录音中**: 脉冲动画，红色圆点，波形显示
- **Processing**: 旋转圆环
- **Disabled**: 灰色，50%透明度

### 5.2 InsightCard (洞察卡片)
- **类型**: 关联洞察 / 模式报告 / 反事实快照
- **结构**: 图标 + 标题 + 内容 + 时间戳 + 操作按钮
- **样式**: 白色卡片，左侧紫色边条，圆角16px
- **展开**: 点击展开完整内容

### 5.3 ChatBubble (对话气泡)
- **用户**: 右对齐，紫色背景，白色文字
- **AI**: 左对齐，白色背景，紫色边条
- **AI+洞察**: 气泡下方附加InsightCard

### 5.4 MoodTag (情绪标签)
- **样式**: 圆角胶囊，不同颜色代表不同情绪
- **颜色映射**: 😊开心=#10B981, 😐平静=#6B7280, 😔低落=#F59E0B, 😤愤怒=#FF6B6B

### 5.5 ReminderChip (提醒芯片)
- **样式**: 虚线边框胶囊，可删除
- **交互**: 点击编辑条件

### 5.6 TimelineItem (时间线项)
- **结构**: 日期 + 摘要 + 关联洞察数量标记
- **状态**: 展开/折叠

---

## 6. Technical Approach

### 6.1 技术栈

**后端**:
- Python 3.11+ / FastAPI
- SQLite (本地结构化数据)
- ChromaDB (向量数据库，长期记忆)
- OpenAI GPT-4o mini (LLM)
- APScheduler (定时任务)

**前端**:
- Flutter (iOS/Android)
- 或: React Native

**数据流**:
- 移动端 → REST API → FastAPI → 处理引擎 → 存储

### 6.2 核心模块

```
echo-agent/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI入口
│   ├── config.py               # 配置管理
│   ├── logger.py               # 日志模块
│   │
│   ├── api/                    # API路由
│   │   ├── __init__.py
│   │   ├── records.py          # 记录CRUD
│   │   ├── insights.py         # 洞察生成
│   │   └── reminders.py        # 未来提醒
│   │
│   ├── core/                   # 核心处理
│   │   ├── __init__.py
│   │   ├── processor.py        # 记录处理器
│   │   ├── associator.py       # 隐式关联引擎
│   │   ├── pattern.py           # 模式识别
│   │   └── counterfactual.py   # 反事实推演
│   │
│   ├── memory/                 # 记忆存储
│   │   ├── __init__.py
│   │   ├── sqlite_store.py     # SQLite存储
│   │   ├── vector_store.py     # ChromaDB向量存储
│   │   └── summary.py          # 摘要分层
│   │
│   ├── llm/                    # LLM接口
│   │   ├── __init__.py
│   │   └── openai_client.py    # OpenAI封装
│   │
│   ├── scheduler/              # 定时任务
│   │   ├── __init__.py
│   │   └── reminders.py        # 提醒调度
│   │
│   └── models/                 # 数据模型
│       ├── __init__.py
│       └── schemas.py          # Pydantic模型
│
├── tests/                      # 测试
│   └── ...
│
├── mobile/                     # 移动端代码(可选)
│   └── ...
│
└── docs/                       # 文档
    └── ...
```

### 6.3 API设计

#### POST /api/records
创建新记录
```json
Request: {
  "content": "string (语音转文字或直接文本)",
  "type": "voice|text",
  "context": {
    "time": "ISO8601",
    "location": "optional",
    "mood": "optional"
  }
}
Response: {
  "id": "uuid",
  "insights": [InsightCard],
  "future_reminders": [Reminder]
}
```

#### GET /api/records
获取记录列表
```json
Query: ?page=1&limit=20&search=keyword
Response: {
  "records": [Record],
  "total": 100,
  "page": 1
}
```

#### GET /api/insights/weekly
获取周模式报告
```json
Response: {
  "period": "2024-W15",
  "mood_distribution": {"happy": 3, "neutral": 10, "low": 2},
  "patterns": [Pattern],
  "highlight": "本周效率最高在周二下午"
}
```

#### POST /api/reminders
设置未来提醒
```json
Request: {
  "condition": "下次我记录加班",
  "action": "问我还记得跳槽的纠结吗",
  "record_id": "optional"
}
```

### 6.4 数据模型

#### Record (记录)
```python
id: UUID
content: str
type: RecordType  # voice, text
created_at: datetime
context: dict  # mood, location, etc.
embedding: list[float]  # for vector search
```

#### Insight (洞察)
```python
id: UUID
record_id: UUID
type: InsightType  # association, pattern, counterfactual
content: str
confidence: float  # 0-1
created_at: datetime
```

#### Reminder (提醒)
```python
id: UUID
condition: str
action: str
record_id: UUID | None
is_active: bool
next_trigger: datetime | None
```

### 6.5 隐私设计
- 所有数据默认本地存储
- 向量数据可选择性同步
- 用户可随时导出/删除全部数据
- 敏感记录可标记"永不用于分析"

---

## 7. MVP Scope (职场情绪与决策复盘)

### 必须实现 (P0)
- [ ] 语音/文字记录输入
- [ ] 基础AI对话响应
- [ ] 记录存储与历史查看
- [ ] 隐式关联洞察 (基于当前对话上下文)
- [ ] 周模式报告
- [ ] 未来提醒设置

### 延后实现 (P1)
- [ ] 反事实推演
- [ ] 预测性提醒
- [ ] 数据导入 (日历、位置)
- [ ] 邮件周报

### 不做 (当前版本)
- [ ] 跨设备同步
- [ ] 多人协作
- [ ] 企业EAP版本

---

## 8. First-Time Experience (首次体验)

目标是让用户在5分钟内感受到价值。

### Step 1: 零门槛开始 (1分钟)
- 打开App，只有大麦克风按钮 + "说说你最近的烦恼或决定"
- 无需注册，直接说话

### Step 2: 即时关联 (2分钟)
- 用户说"最近纠结要不要跳槽"
- AI立即询问"你愿意说说为什么纠结吗？"
- 用户补充"新工作要去北京，现在在上海"
- AI立即关联："你曾在记录中提到'想念家人'14次..."

### Step 3: 微承诺演示 (1分钟)
- AI主动设置"下次你记录'加班'时提醒你对比"
- 展示模拟消息预览

### Step 4: 引导注册 (1分钟)
- 展示"你的第一条回响"摘要
- "注册后可永久保存并持续获得洞察"

---

## 9. 成功指标

| 指标 | 目标 |
|------|------|
| 首次使用完成率 | >60% |
| 次日留存 | >40% |
| 7日留存 | >25% |
| 平均每周记录次数 | >5次 |
| 洞察点击率 | >30% |
