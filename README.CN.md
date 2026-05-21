# Housing Realism

Housing Realism 是一个 *Victoria 3* 经济类模组，将住房从“隐含在生活水平中的背景项”改为“可生产、可消费、按州定价的本地商品”。

## 定位与设计边界

- 住房被建模为**持续性居住成本**，而不是一次性资产购买。
- 实现遵循原版循环消费框架（`buy_packages` + `pop_needs`），不引入独立购房资产系统。
- 当前核心结构保持为二元：租赁住房 vs 产权住房。

## 当前实现内容

### 商品（Goods）

- `rented_housing`
  - 本地商品（`local = yes`）
  - 类别：`staple`
  - 面向低至中低财富阶层需求
- `owned_housing`
  - 本地商品（`local = yes`）
  - 类别：`luxury`
  - 面向中高至高财富阶层需求

### 建筑与生产方式分层（Production Methods, PMs）

- `building_hrro_rental_developer`
  - 通过 `tenement` -> `apartment` -> `highrise` 的 PM 进阶提供租赁住房
- `building_hrro_owned_developer`
  - 通过 `rowhouse` -> `suburban_villa` -> `luxury_estate` 的 PM 进阶提供产权住房

### Pop 需求与财富分层

- `popneed_rented_housing` 主要覆盖低财富段，并在高财富段逐步退出。
- `popneed_owned_housing` 从中等财富段开始出现，并在高财富段显著增强。
- `common/buy_packages/00_buy_packages.txt` 已完整覆盖 `wealth_1` 至 `wealth_99`，用于编码这一路径切换。

### 本地价格机制（Local Goods）

两类住房都是本地商品，价格与供需压力按州形成，而非单一全国市场信号。

## 兼容信息

- 模组名：`Housing Realism`
- Mod ID：`com.housing_realism`
- 游戏：`victoria3`
- 支持版本：`1.13.*`
- 多人同步：`false`

以上以 `.metadata/metadata.json` 为准。

## 仓库结构导航

- `common/goods/`
  - 住房商品定义
- `common/pop_needs/`
  - 住房 Pop 需求定义
- `common/buy_packages/`
  - 财富分层需求曲线（`wealth_1` 到 `wealth_99`）
- `common/buildings/`
  - 住房建筑定义
- `common/production_method_groups/`
  - 两条住房链路的 PM 组定义
- `common/production_methods/`
  - 建造与所有权 PM 细节
- `common/modifier_type_definitions/`
  - 住房产出 modifier 定义
- `localization/english/`
  - 英文本地化
- `gui/`
  - 文本图标定义
- `.metadata/`
  - 模组声明与兼容元数据
- `docs/agents/`
  - 设计与协作说明文档

## 协作开发流程（面向开发者）

### 改动前检查

- 先确认目标范围，保持最小改动。
- 按需加载 `docs/agents/` 对应主题文档后再改动游戏数据。
- 检查 key 命名一致性（如 `rented_housing`、`owned_housing`）。

### 改动边界

- Gameplay 数据以 `common/*` 为唯一事实源。
- 不扩展未被请求的系统。
- 不将“未实现特性”写成“已落地能力”。

### 提交与 PR 粒度

- 每个 commit 对应一个明确玩法意图（如商品平衡、PM 调整、buy package 曲线调整）。
- 涉及 key 新增/重命名时，数据与本地化放在同一变更集中。
- PR 描述需明确：
  - 影响文件
  - 玩法意图
  - 兼容性前提

### PR 验收清单

- 文档所述机制均可在源码定位。
- 文档中的 metadata 与 `.metadata/metadata.json` 一致。
- key 命名在 `common/*` 与 localization 中一致。
- 不混入无关重构。

## 当前非目标（Non-goals）

- 尚未落地法律系统联动。
- 尚未落地公司系统扩展。
- 尚未落地专用住房可视化分析面板。

## 术语对照

- **Local Goods（本地商品）**：按州定价的商品（`local = yes`）
- **Ownership Housing（产权住房）**：`owned_housing` 对应的需求/供给链
- **Production Methods / PMs（生产方式）**：建筑的分阶段生产与所有权配置
