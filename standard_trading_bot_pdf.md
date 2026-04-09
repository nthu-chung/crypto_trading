# 标准交易 Bot 分层设计方案（Roadmap）

## 来源

- 原始文件：`/Users/hankchung/Downloads/标准交易 Bot 分层设计方案（Roadmap） - Big Data - Confluence.pdf`
- 来源页面：Confluence `Project-Clawbot&Trading`
- 说明：本文为按原文语义整理的 Markdown 版本，尽量保留章节结构、字段约束与设计意图，不保留 Confluence 排版、页脚与侧栏噪音。

## 1. 目标与原则

### 1.1 目标拆分

#### 业务目标

- 降低用户构建和迭代量化交易策略的门槛，支持多样化策略开发和快速验证。
- 丰富 Binance 及相关交易市场生态，鼓励用户通过标准协议进行策略二次封装和自定义创新。
- 支持策略、bot 等产品在市场内安全分享和传播，提升用户活跃度及交易粘性。
- 策略和 bot 可独立管理，支持通过前端 UI 进行进程监控、风控报警，避免僵尸交易进程，提升账户安全和透明度。
- 保证用户自定义策略在标准化协议下获得稳定交易体验，实现合规和风险可控。

#### 技术目标

- 支持多周期、多标的的行情拉取与 K 线对齐。
- 数据层除 K 线与量价衍生信息外，统一接入社交与资讯（Tweet / Post / News 等）及链上钱包追踪等另类数据，并与行情共用一套快照协议供信号层消费。
- 多周期回测时，社交与链上事件必须与当时 K 线决策时点 `as_of` 对齐，仅包含该时点已发生且可按策略规则视为可见的资讯与链上数据，并与监控 / 实盘单次 Run 的切片规则一致，避免前视偏差。
- 技术指标计算标准化，方便扩展与维护。
- 信号处理及扩展机制实现量价信号、指标、交易信号、选币等插件化对接。
- 信号与执行采用统一输入输出协议（JSON Schema / Protobuf），保证线上线下回测一致性。
- 回测与实盘监控共用同一套信号计算内核。
- 回测侧按海量历史 `batch / 向量化` 调用。
- 实盘侧仅对当前时刻数据切片做增量、低延迟调用。
- 热点数值逻辑在协议上优先满足 `Numba (njit)` 加速，避免回测与实盘各写一套公式。
- 回测引擎支持自定义费用、滑点、撮合等，并支持批量仿真。
- 触发和监控采用 HTTP、Cron、消息队列等标准接口，具备可观测性、幂等、可重试。
- 执行层外接主流交易所 API，支持风控、下单、撤单、仓位同步，并便于扩展多券商适配器。
- 各层解耦，支持单元测试、集成测试和回放测试，保障可维护和快速迭代。

注：用户可在平台基础上进行策略编写、信号计算、回测仿真、实盘通知与交叉调用，灵活组合和管理多元交易需求。

### 1.2 设计原则

- 最少分层、最大复用：用 4 个逻辑层覆盖全链路；监控与执行同属「运行与执行层」下的两个标准接口，避免为「调度」单独造一层无法复用的壳。
- 协议优先：每层对外只认标准输入输出（IO 契约）；定制通过插件注册表 + 配置完成，不破坏契约。
- 可组合、可单用：任意一层可被上层调用，也可在脚本 / Notebook 中单独实例化，例如只做拉线 + 指标、只做回测、只做纸面执行。
- 计算一致性优先于手写两份：量价类信号的核心应落在同一可测试内核；回测走 batch、实盘走 step，禁止在监控路径复制一套「简化版」逻辑而不做对齐测试。
- 时点一致（Point-in-Time）：回测中每一步组装的 `DataSnapshot` 与实盘中「当前决策时刻」的快照，须遵守同一套 `as_of` / 多周期 bar 闭合语义；社交、链上不得跨越该时点泄露未来信息。

## 2. 总体架构（四层）

### 四层结构

- 运行与执行层（Runtime & Execution）
  - `Monitor API`
  - `Execution Engine`
- 仿真层（Simulation）
  - 回测
  - 纸面撮合
  - 绩效与归因
- 信号层（Signal）
  - 指标
  - 量价
  - 策略
  - 选币
  - 自定义插件
- 数据层（Data）
  - K 线 / 量价
  - 社交与资讯
  - 钱包与链上
  - 缓存 / 对齐

### 数据流

`Data（组装 DataSnapshot） -> Signal -> (Simulation 或 Runtime) -> Execution`

### 典型运行方式

- 回测：Data 的历史回放适配器（可重放录制的行情 + 社交 / 链上时间轴）+ 同一套 Signal 输出 -> Simulation。
- 监控 Cron：Runtime 的 Monitor 触发一次「多源 Data 刷新 -> Signal 计算 -> （可选）Execution」。

### 阅读顺序

- 先读第 3 章：分层定义（各层职责、标准 IO、定制点）
- 再读第 4 章：跨层公共类型（字段级协议）

## 3. 分层定义（标准 IO + 定制点）

### 3.1 数据层（Data）

#### 职责

- 聚合多类数据源。
- 输出统一 `DataSnapshot`。
- 对上层屏蔽重试、限频、主备切换与部分失败策略。

#### 子域

| 子域 | 内容示例 |
| --- | --- |
| 行情 | 多周期 K 线、成交量、资金费率等，装入 `MarketBundle` |
| 社交与资讯 | Tweet、论坛 Post、新闻、RSS，装入 `SocialFeedBundle` |
| 链上与钱包 | 地址监控、标签命中、充提 / 划转类事件，装入 `OnChainSignalBundle` |

#### 标准输入

- `DataQuery`
- 可只填 `market`
- 可只填 `social`
- 可只填 `onchain`
- 也可任意组合
- `options.partial_ok` 控制单源失败时是否仍返回其它子域

#### 标准输出

- `DataSnapshot`
- 内含 `market`
- 可选 `social`
- 可选 `onchain`
- `meta.source_status`

#### 定制扩展（Adapter 协议）

- `MarketDataAdapter: fetch_market(market_block) -> MarketBundle`
- `SocialDataAdapter: fetch_social(social_block) -> SocialFeedBundle`
- `OnChainDataAdapter: fetch_onchain(onchain_block) -> OnChainSignalBundle`

各 Adapter 独立注册；编排层负责并行请求、超时、降级，并写入 `meta.source_status`。禁止在协议外加平行字段，扩展走各子 Bundle 的 `entities / payload` 约定或新版本 `version`。

#### 与信号层的边界

- 情感打分、文本主题模型、链上复杂归因等重计算可放在信号层插件。
- 数据层以可回放、带来源指纹的原始或轻清洗文档 / 事件为主。

#### 可独立使用

- 只跑社交归档
- 只跑钱包监控
- 只拉 K 线

以上都可通过 `DataQuery` 子块裁剪。

#### 多周期与另类数据的时点对齐（与监控一致）

数据层在回测回放与实盘拉取两条路径上，必须使用相同的对齐策略。文中建议独立 `AlignmentPolicy / SnapshotAssembler`，并将版本号写入 `meta.alignment_policy`。

给定决策锚点 `decision_as_of`，通常对应主交易周期上一根已收盘 K 的约定时间戳，整栈统一使用开盘时刻或收盘时刻之一。给定所需多周期 `Timeframe` 列表后，应产出：

- `MarketBundle` 中每一序列在 `as_of` 当时可见的 bar 前缀
- 社交 `published_at <= decision_as_of`
- 链上 `timestamp <= decision_as_of`
- 若供应商存在索引延迟，可进一步约束 `observable_at <= decision_as_of`

禁止在回测里用「全天社交全量 + 历史 K 线」，却在监控里用「窗口切片」且不经过同一过滤器；两者应表现为同一 `DataQuery + decision_as_of` 语义下的不同调用方式。

### 3.2 信号层（Signal）

#### 职责

- 在 `DataSnapshot` 上计算指标、量价规则、舆情 / 链上融合逻辑、策略与选币打分。
- 输出 `SignalBatch`。
- 所有「算的东西」尽量拆成可组合算子，但对外只暴露统一 `SignalEnvelope`。

#### 标准输入

- `DataSnapshot`
  - 至少包含插件声明所需子域
  - 纯量价策略可仅填 `market`
  - 含社交 / 链上或多周期语义时须带 `meta.decision_as_of`
  - 插件不得用墙钟时间绕过 PIT
- 可选 `SignalContext`
  - 账户风险快照
  - 黑名单
  - 上一 tick 的持仓
  - 用于避免循环依赖，可由 Runtime 注入

#### 标准输出

- `SignalBatch`

#### 内部推荐拆分

| 组件 | 作用 |
| --- | --- |
| `IndicatorRegistry` | 注册 `name -> (BarSeries -> FeatureFrame)` |
| `SignalPlugin` | `(DataSnapshot, FeatureFrame?) -> SignalEnvelope[]`，内部可读 `social / onchain` |
| `Composer` | 多插件顺序 / 并行 / 投票，合并为单一 `SignalBatch` |

#### 定制扩展

- 插件约定：`plugin_id`、`config_schema`、`required_inputs: { market?, social?, onchain? }`、`run(snapshot, config) -> SignalBatch`
- 选币类插件输出 `kind=selection`，`payload.rankings`
- 选币插件可融合 `SocialDocument.entities` 与 `ChainObservation.related_instruments`
- `provenance` 中建议包含子源指纹，例如 `social.meta.fetched_at + query hash`，便于与数据层回放对齐

#### 可独立使用

单元测试可构造最小 `DataSnapshot`（CSV / Parquet / 夹具 JSON），无需真实交易所或 Twitter API。

### 3.2.1 回测与实盘：同一逻辑、双执行形态（Batch / Incremental）与 Numba

#### 目标

监控 / 执行时刻产生的 `SignalBatch`，与在同一 `DataSnapshot` 时间点上由回测引擎算出的信号，在数学上同构。允许仅存在浮点舍入差异，但必须在测试中量化上界。

#### 实现约束（推荐协议）

##### 1. 内核单一来源（Single Kernel）

- 每个策略插件将决策相关数值计算收敛为一层与 IO 无关的内核。
- 输入为 numpy 连续数组 / 结构化状态，例如 `float64` 的 OHLCV 窗口、预聚合的社交 / 链上特征列。
- 输出为定长或规则张量，例如每 bar 一个方向标签、强度、触发位。
- `DataSnapshot -> 数组` 的编码在薄适配层（Python）完成。
- 禁止在回测与实盘各写一套不同的指标公式。

##### 2. 两种调用形态，共用同一内核

| 形态 | 调用方 | 数据形态 | 目标 |
| --- | --- | --- | --- |
| Batch | 仿真层、研究脚本 | 长时间序列对齐后的 `T × F` 特征矩阵，可多标的 panel | 吞吐；可整段 `@njit` 循环或向量化 |
| Incremental（Step） | 监控 Cron、实时触发 | 当前 bar / 当前窗口 + 持久化 `SignalState`（滚动缓冲、指标递推状态） | 延迟最小；每 tick 只处理新增切片 |

- Batch：对时间维分块（chunk）调用内核，控制单次内存占用；块与块之间通过显式状态衔接，状态更新规则与 Step 路径一致。
- Step：从 `SignalState` 读入上一步状态，喂入本步新到达的行情与社交 / 链上增量，调用同一内核的单步入口。可视为 batch 长度为 1 的特例，但建议实现独立 step 入口，避免无谓分配。

##### 3. Numba 加速约定

- 内核函数满足 Numba `njit` 友好：类型稳定、无 Python 对象与动态容器、无回调、分支可预测。
- 不适合 JIT 的部分（NLP、复杂图模型）放在特征工程前置，先产出固定维 `float` 特征，再进入 Numba 区。
- 回测优先对整段或大块 T 维循环 `njit`，发挥 SIMD / 并行（如 `prange`）潜力。
- 实盘单步内核仍可为 `njit`，冷启动后极快；避免在热路径上反复编译，应使用进程级缓存的已编译机器码。

##### 4. 一致性验证（必做）

- 对齐测试：对同一插件、同一配置，在随机种子下取若干时刻 `t`，比较 `batch_kernel(...)[t]` 与 `step_kernel` 从 `t=0` 递推到 `t` 的输出，或从录制的 `SignalState` 单步前进，断言在容差内一致。
- 回归：`provenance` 记录内核版本号、配置哈希、输入数组 hash；CI 对 golden 序列做快照对比。

##### 5. 插件对外接口不变

- 对外仍输出 `SignalBatch / SignalEnvelope`
- `Batch` 与 `Step` 仅为插件内部或 `SignalRuntime` 的运行策略
- 不分裂为两套对外协议

#### 示意（概念 API，非强制命名）

```python
encode(snapshot_window) -> FeatureArrays

@njit
def kernel_batch(features, params, out_signals):
    """沿 T 维就地写 out_signals，供回测。"""
    ...

@njit
def kernel_step(state, feature_row, params) -> (new_state, signal_row):
    """单步，供监控；state 为可序列化的定长向量或若干数组。"""
    ...
```

### 3.3 仿真层（Simulation）

#### 职责

- 历史回放 Data 适配器
- 与线上一致的 Signal 管线
- 生成 `BacktestResult`
- 支持 walk-forward、参数网格
- 调度在工具层，核心引擎保持纯函数式

#### 标准输入

- `BacktestRequest`
- 含 `SignalPipeline` 描述：插件链与配置快照

#### 标准输出

- `BacktestResult`

#### 定制扩展

- `FillModel / FeeSchedule / SlippageModel` 可插拔
- 默认实现满足「开箱即用」

#### 与线上一致性

- Signal 层使用同一内核实现 + 同一配置哈希
- Data 层使用录制 `DataSnapshot`（含行情 / 社交 / 链上时间轴）或同一套 Adapter 与 query 快照

#### 时间轴与监控对齐

- 回测主循环按决策时钟推进，与 `§4.6.1` 一致，逐步对应到各周期 K 线闭合点
- 每一步喂给 Signal 的 `DataSnapshot` 必须带 `meta.decision_as_of`
- 其中社交 / 链上内容与该时点可观测集合一致
- 从而与监控 Cron 在「当前最后一根已收盘主周期 bar」触发时的输入等价
- 允许仅数据源延迟配置不同，但须在 `meta` 中声明

#### 性能

- 回测引擎对信号计算采用按时间分块 batch 调用插件内核，避免「每 bar 一次 Python 大对象构造」
- 大块内由 Numba 或向量化承担热点循环
- 批量预计算特征时仍须按 `decision_as_of` 分桶，或在特征里嵌入 `as-of` 约束，禁止跨桶前视

#### 可独立使用

CI 中只做回归对比 `SignalBatch` 哈希与权益曲线，以及 batch vs step 对齐测试。

### 3.4 运行与执行层（Runtime & Execution）

拆成两个标准接口，共享 `RunContext`，避免再多一层空壳。

### 3.4.1 监控 / 调度（Monitor）

#### 职责

- Cron
- HTTP
- 队列消费者
- 触发一次 Run
- 记录日志、指标、告警

#### 标准输入

- `MonitorTrigger`
  - `trigger_type`
  - `payload`
  - 可选覆盖标的列表
  - 可选指定仅信号不下单

#### 标准输出

- `RunSummary`
  - `run_id`
  - `status`
  - `signal_count`
  - `execution_reports[]?`
  - `errors[]`

#### 定制扩展

- 触发器适配器
- 幂等键可为 `(run_id, intent_id)` 或交易所 `client_order_id` 规则

#### 信号路径

- 每次 Run 仅拉取当前有效数据切片，例如最新闭合 K 线 + 滑动窗口长度 `L`
- 与持久化的 `SignalState` 一并传入插件的 Step / 增量入口
- 不为降低延迟而绕过统一内核
- 延迟优化手段包括：减小窗口、缓存编码结果、Numba 单步 `njit`、IO 与计算并行

#### 与回测对齐

- 本次 Run 组装的 `DataSnapshot` 须显式设置 `meta.decision_as_of`
- 其语义等价于「若此刻做回测仿真，历史走到哪一根主周期已收盘 bar」
- 社交 / 链上过滤规则与 `§3.1 / §4.6.1` 一致
- 保证监控交易等于回测该步的输入契约相同

### 3.4.2 执行（Execution）

#### 职责

- `SignalBatch -> 风控 -> ExecutionIntent -> 交易所 API`
- 轮询成交与仓位
- 不向信号层回调
- 保持单向数据流，避免环路

#### 标准输入

- `SignalBatch`
- 可选 `DataSnapshot` 或仅 `MarketBundle`
- `AccountSnapshot`，由执行层或账户子模块同步

#### 标准输出

- `ExecutionReport[]`

#### 定制扩展

- `BrokerAdapter`
- `RiskRule` 链，例如仓位上限、频控、熔断

#### 可独立使用

- 手工构造 `ExecutionIntent` 做压测或应急单
- Monitor 可不启用，仅 CLI 调 `Signal + Execution`

## 4. 跨层公共类型（协议基础）

以下类型作为版本化契约，建议使用 JSON Schema / Protobuf / 等价物描述 `version` 字段。

### 4.1 标识与时间

| 类型 | 含义 |
| --- | --- |
| `InstrumentId` | 统一标的 ID，例如 `BTCUSDT + 交易所 + 合约类型` |
| `Timeframe` | 周期枚举：`1m / 5m / 1h / 1d` 等 |
| `BarTimestamp` | 对齐后的 K 线开盘时间（UTC，毫秒或秒，全项目一致） |
| `RunId / TraceId` | 单次调度或请求链路追踪 |

### 4.2 `Bar / BarSeries`

- `Bar`：`open, high, low, close, volume, quote_volume?, timestamp, instrument_id, timeframe, confirmed`
- `confirmed` 表示是否已收盘
- `BarSeries`：按时间升序
- 附带 `timezone_policy`、`gap_policy`（前向填充 / 留空 / 丢弃）

### 4.3 `MarketBundle`（行情子快照）

面向信号层的行情与量价子集；仍保持独立类型，便于只跑行情流水线与单测。

#### 输入（概念）

- `instruments: InstrumentId[]`
- `timeframes: Timeframe[]`
- `range: [start, end]` 或 `latest N bars`
- `options: { partial_ok, max_staleness_sec, ... }`

#### 输出

- `bars: Map<(InstrumentId, Timeframe), BarSeries>`
- `meta: { data_source, fetched_at, warnings[] }`

### 4.4 另类数据：`SocialDocument / SocialFeedBundle`

统一描述 Tweet、社区 Post、新闻稿、RSS、站内帖等非行情文本流，实现上可映射到多家供应商。

#### `SocialDocument`（单条）

| 字段 | 说明 |
| --- | --- |
| `doc_id` | 全局唯一，含来源命名空间 |
| `source_type` | `twitter | forum | news | rss | internal_post | other` |
| `published_at` | UTC 时间戳，事件发生时间 |
| `observable_at?` | 可选，进入本系统 / 索引可查时间；PIT 过滤可与 `published_at` 二选一或组合 |
| `author_id? / author_handle?` | 平台内作者标识 |
| `title?` | 新闻 / 长帖标题 |
| `text` | 正文或摘要，清洗策略可配置 |
| `url?` | 原文链接 |
| `language?` | 检测或声明语言 |
| `entities` | 结构化抽取：`instruments[]?、tickers[]?、contracts[]?、chains[]?、urls[]?` |
| `sentiment?` | 可选分数或标签，可由数据层或下游 NLP 插件写入 |
| `raw_ref` | 供应商原始 ID、拉取批次，供合规与回放 |

#### `SocialFeedBundle`

- `items: SocialDocument[]`
- `query: { keywords?, authors?, instruments?, lang?, ... }`
- `meta: { provider, fetched_at, cursor?, rate_limit_hint?, warnings[] }`

文中要求在 `meta` 标明 `items` 时间顺序是升序还是降序。

### 4.5 链上数据：`ChainObservation / OnChainSignalBundle`

钱包追踪、大户标签、交易所充提、聪明钱列表等链上可观测事件的标准化封装；不等同于完整节点索引，侧重「可交易相关」信号原料。

#### `ChainObservation`（单条）

| 字段 | 说明 |
| --- | --- |
| `obs_id` | 唯一 ID |
| `chain` | `eth | bsc | sol | ...` |
| `timestamp` | 链上事件时间（UTC）；PIT 与 `decision_as_of` 比较时以此为主 |
| `confirmed_at?` | 可选，满足最终性 / 确认数后的时间，用于更严格的 PIT |
| `event_type` | `transfer | swap | bridge | stake | cex_deposit | cex_withdraw | label_hit | custom` |
| `addresses` | `from?、to?、wallet_label?`，例如 `known_whale、exchange_hot` |
| `tokens?` | `symbol / contract / amount / amount_usd` |
| `direction?` | `in | out | neutral`，相对 watchlist |
| `confidence` | `0~1` 或枚举，表示解析质量、标签来源可信度 |
| `related_instruments?` | 与 `InstrumentId` 的映射，由标签服务或配置表给出 |
| `raw_ref` | `tx_hash、log_index、供应商事件 ID` |

#### `OnChainSignalBundle`

- `observations: ChainObservation[]`
- `watchlist_ref: { version, wallet_set_id }`
- `meta: { provider, fetched_at, chain_tip?, warnings[] }`

### 4.6 `DataSnapshot`（数据层对外的统一输出）

将行情 + 社交资讯 + 链上组合为一次 Run 的可选多源快照。信号层按插件声明依赖的子集消费；未请求的域可为空或省略。

```text
version: string
market: MarketBundle
social?: SocialFeedBundle
onchain?: OnChainSignalBundle
meta: {
  snapshot_id,
  assembled_at,
  partial_ok: boolean,
  source_status: { market?, social?, onchain? },
  warnings[],
  decision_as_of?: BarTimestamp,
  primary_timeframe?: Timeframe,
  alignment_policy?: string,
}
```

字段说明：

- `partial_ok`：是否允许部分源失败
- `source_status`：`ok | degraded | skipped`
- `decision_as_of`：PIT 锚点；多周期回测步进、含 `social/onchain` 或实盘监控时应必填
- `primary_timeframe`：若为多周期，标记主周期
- `alignment_policy`：对齐策略版本 ID，例如 bar 用开盘 / 收盘、未收盘 bar 是否可见等

### 4.6.1 多源时间与 K 线锚定（回测 ≡ 监控）

#### 目的

在多周期历史回测中，社交资讯与钱包 / 链上事件必须与当时的 K 线时间轴对齐，使每一步 `DataSnapshot` 与监控 / 实盘在对应时刻能获得的数据一致，避免前视与双轨逻辑。

#### 决策时钟（Decision Clock）

- 策略需指定主周期，例如 `1h`
- 并定义 bar 何时算「已知」
- 常见规则：该 bar 收盘后才可交易
- 整栈对 `BarTimestamp` 取开盘时间或收盘时间须统一，并在 `alignment_policy` 中版本化
- `decision_as_of` 表示在该主周期语义下，「上一根已收盘 bar」所对应的唯一 UTC 时间戳
- 回测循环每推进一步，更新一次 `decision_as_of`
- 监控 Run 在触发时也按同一公式计算当前 `decision_as_of`

#### 多周期 K 线

- 对任意辅周期，例如 `15m、4h`
- `MarketBundle` 中只包含在 `decision_as_of` 时刻已收盘的 bar
- 若策略显式允许未收盘 bar，则回测与实盘必须使用相同规则
- 高周期未完成时，不得用未来低周期 bar 拼凑出尚未收盘的高周期 OHLC

#### 社交资讯（`SocialFeedBundle`）

- 仅包含 `published_at <= decision_as_of` 的 `SocialDocument`
- 若业务上存在平台索引延迟，再要求 `observable_at <= decision_as_of`
- `published_at / observable_at` 的组合规则由 `alignment_policy` 定义
- 可按滑动窗口截取，例如过去 24h
- 但窗口上界必须为 `decision_as_of`
- 监控 Run 与回测必须使用同一 `DataQuery.social` 参数化规则

#### 链上 / 钱包（`OnChainSignalBundle`）

- 仅包含 `timestamp <= decision_as_of` 的 `ChainObservation`
- 若供应商对确认数 / 最终性有要求，可改用 `confirmed_at <= decision_as_of`
- 也可采用 `block_time + lag` 规则
- 上述规则都必须写入 `alignment_policy`

#### 实现与验证

- 同一装配器：回测 `HistoricalSnapshotAssembler` 与实盘 `LiveSnapshotAssembler` 共享过滤与截断逻辑，仅数据源（文件 / API）不同
- 测试：固定 `decision_as_of = T`
- 断言 `snapshot.social ∪ snapshot.onchain` 是全量历史在 `T` 的 PIT 子集
- 与监控一次 Run 的快照做 diff 或 hash 回归

#### `DataQuery`（数据层标准输入，与 §3.1 对齐）

- `market?: { instruments, timeframes, range/tail }`
- `social?: { time_range, query... } | null`
- `onchain?: { time_range, watchlist_ref, chains? } | null`
- `options: { partial_ok, max_staleness_sec, ... }`

各子查询相互独立；实现上由 `DataSourceAdapter` 注册表并行拉取，再组装为 `DataSnapshot`。

### 4.7 `FeatureFrame`（信号层中间产物，可选暴露）

- 索引：`BarTimestamp`
- 可与某一主周期对齐
- 列：指标名 -> `float | null`
- 多标的可做为 panel，`instrument_id` 可作为额外索引或列

### 4.8 `SignalEnvelope`（信号层主输出）

统一承载交易意图、选币结果、告警等，用 `kind` 区分。

| 字段 | 说明 |
| --- | --- |
| `version` | 协议版本 |
| `signal_id` | 稳定 ID，通常由策略 / 插件实例 + 逻辑版本组成 |
| `kind` | `trade | selection | alert | noop` |
| `instrument_id?` | 交易类必填 |
| `side?` | `buy / sell / flat` |
| `strength` | 连续值或分档，供风控与仓位缩放 |
| `time_horizon` | 信号有效尺度，与周期、持仓周期对齐 |
| `valid_until?` | 过期时间 |
| `payload` | 扩展桶：自定义参数、子信号列表、选币排名等 |
| `provenance` | 插件名、配置哈希、输入数据指纹，便于回放 |

批量输出：

- `SignalBatch = { signals: SignalEnvelope[], batch_id, created_at }`

### 4.9 `ExecutionIntent`（执行层输入）

由 Runtime 将 `SignalEnvelope(kind=trade)` 映射而来，可一对多或多合一。

| 字段 | 说明 |
| --- | --- |
| `intent_id` | 幂等键组成部分 |
| `instrument_id, side, order_type` | 市价 / 限价 / 条件单等 |
| `quantity / notional` | 二选一或按比例 |
| `price?, time_in_force?` | 可选 |
| `reduce_only?, client_tag?` | 可选 |
| `risk_hints` | 最大滑点、最大仓位占比等，执行层仍需再校验 |

### 4.10 `ExecutionReport`

- `status: submitted / partial / filled / rejected / cancelled`
- `external_ids`
- `fills[]`
- `reason`
- 与 `intent_id / RunId` 关联

### 4.11 `BacktestRequest / BacktestResult`（仿真层）

#### Request

- 时间区间
- 标的列表
- 周期
- `SignalPipeline` 配置
- 费率与滑点模型
- 初始资金
- 复权 / 合约规则
- 数据源为按 tick 重放的 `DataSnapshot` 流
- 可仅含 `market`
- 也可含 `social / onchain` 录制带

#### Result

- 权益曲线
- 成交列表
- 按 `SignalEnvelope.provenance` 的归因
- 风险指标
- 可选导出与线上一致的 `SignalBatch` 日志，便于 diff

## 5. 层间协作与独立调用矩阵

| 调用方 | Data | Signal | Simulation | Monitor | Execution |
| --- | --- | --- | --- | --- | --- |
| Monitor | ✓ | ✓ | ✗ | — | ✓（可选） |
| Simulation 内部 Replay | ✓ | ✓ | — | ✗ | ✗（或模拟成交） |
| 脚本 / 研究 | ✓ | ✓ | 可选 | ✗ | 可选（纸面） |
| Execution only | 可选 | ✗ | ✗ | ✗ | ✓ |

## 6. 落地 Roadmap（建议顺序）

1. 冻结 v1 协议：`DataSnapshot`（含 `MarketBundle` 子协议）、`SignalEnvelope`、`ExecutionIntent` 的 `version` 与必填字段。
2. 数据层：先打通 `MarketDataAdapter`；再增量接入 `SocialDataAdapter`、`OnChainDataAdapter` 各一，验证 `partial_ok` 与 `source_status`。
3. 信号层 + 示例插件：先做纯量价（均线）插件，再做一条融合舆情 / 链上的简单插件；落实 `§3.2.1`，包括 `kernel_batch + kernel_step`（或等价）、batch / step 对齐测试、热点 Numba。
4. 仿真层 + 默认费率 / 滑点，与 Signal 使用同一内核、分块 batch 调用；录制 `SignalState` 便于与实盘对拍；PIT 上要求每步 `DataSnapshot.meta.decision_as_of` 与社交 / 链上过滤有单测。
5. 执行层 + `BrokerAdapter` 模拟盘，Monitor 最小 HTTP 触发。
6. 可观测性：`RunId` 贯通、结构化日志、`provenance` 写入。
7. 高级能力：多账户、子策略并行 `SignalBatch` 合并策略、执行层智能路由。

## 7. 小结

- 用数据层、信号层、仿真层、运行与执行层（监控 + 执行双接口）四类即可覆盖需求。
- 行情、社交资讯、链上钱包追踪统一作为数据层子域，经 `DataSnapshot` 输出。
- 指标、量价、舆情融合、选币统一落在信号层插件协议下。
- 标准 IO 以 `DataSnapshot -> SignalBatch -> ExecutionReport / BacktestResult` 为主线，`MarketBundle` 仍为行情子协议。
- 扩展集中在各 `DataAdapter`、`payload`、插件 `required_inputs`，保证可复用、可单测、可回放、可与线上一致对齐。
- 回测与监控执行必须使用同一数值内核：回测 batch、实盘 step；热点用 Numba，对齐测试为强制项，避免双实现漂移。
- 另类数据与多周期通过 `decision_as_of + §4.6.1` 保证社交 / 链上与当时 K 线可见范围一致，确保回测步与监控 Run 使用同一输入契约。
