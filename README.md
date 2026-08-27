# 敏感信息过滤器 (sensitive_filter)

![](https://camo.githubusercontent.com/686bd6ac0ff62606ebb22b3ebdc7250dd2ad3859f75545e4353d89a5a178f8cc/68747470733a2f2f636f756e742e6765746c6f6c692e636f6d2f406e616761746f7175696e33333f6e616d653d6e616761746f7175696e3333267468656d653d72756c6533342670616464696e673d37266f66667365743d3026616c69676e3d746f70267363616c653d3126706978656c617465643d31266461726b6d6f64653d6175746f)

🌐 [文言](README.md) | [中文](README.zh-CN.md) | [English](README.en.md)

在 AstrBot 回复发送前，按配置自动打码敏感信息。所有检测类别均可通过 WebUI 插件配置独立开关。

## 功能（v1.1.0）
- **手机号**：开关 + 打码方式（partial 保留前3后4 / full 全替）。
- **身份证号**：检测（含 18 位校验位校验，校验位不合法不打码）。
- **密码**：总开关 + 形态开关（纯数字 / 纯字母 / 间隔交替 / 字母数字混排）+ 弱密码词表。
- **替换词** `replace_text`：命中时统一替换为自定义文本（默认 `***`）。
- **自定义屏蔽列表**：单独补充前面规则没防到的词/密码（开关 + 词表）。
- **内置附加**：公网 IP / 端口、`sk-xxx`、`gh[opu]_xxx`、32/64 位 hex、键值对 `token=`/`password:`（兼容反引号/引号包裹）恒启用；内网 IP 与公网域名放行。

## 配置
WebUI → 插件 → `sensitive_filter` → 配置：
- `replace_text`：替换词。
- `phone.enabled` / `phone.mask_mode`：手机号开关与打码方式（partial=保留前3后4，full=整段）。
- `idcard.enabled`：身份证检测（含校验位校验）。
- `password.*`：密码各形态开关。
- `custom_blocklist.enabled` / `.words`：自定义屏蔽列表（换行/逗号/顿号/分号分隔）。

> 注意：`pure_alpha` 默认关闭（避免误伤正常英文单词）；`mixed_other` 会连带命中 `room2026` 这类英文词+数字。

**[规则与用法详见 RULES.md](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/RULES.md)**

## 安装
1. AstrBot 管理面板 → 插件 → 安装 → 填此仓库地址。
2. 启之即用，无需配置。

## 更新记录
- [v1.1.0](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.1.0.md)：配置化，拆分手机号/身份证/密码开关，新增替换词与屏蔽列表；身份证含校验位。
- [v1.0.2](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.2.md)：修 `_KV_RE` 误报之患。
- [v1.0.1](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.1.md)：修漏网之鱼，增 hex 打码之规。
- [v1.0.0](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.0.md)：初版。

## 许可
AGPL-3.0

---

~~（注：此仓库乃 AI 所造，非人力也）~~
