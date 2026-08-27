# astrbot-plugin-sensitive-filter

![](https://camo.githubusercontent.com/686bd6ac0ff62606ebb22b3ebdc7250dd2ad3859f75545e4353d89a5a178f8cc/68747470733a2f2f636f756e742e6765746c6f6c692e636f6d2f406e616761746f7175696e33333f6e616d653d6e616761746f7175696e3333267468656d653d72756c6533342670616464696e673d37266f66667365743d3026616c69676e3d746f70267363616c653d3126706978656c617465643d31266461726b6d6f64653d6175746f)

🌐 [文言](README.md) | [中文](README.zh-CN.md) | [English](README.en.md)

AstrBot 之插件也。凡回复将出，先察其文，遇敏感者辄打码蔽之。

## 功能（v1.1.1）

- 手机号 → 打码（partial 留前3后4，full 全蔽）。
- 身份证 → 含校验位，校验不合者不蔽。
- 密码 → 总开关 + 形态（纯数字、纯字母、间隔交替、字母数字混排）+ 弱密码词表。
- 替换词 `replace_text` → 命中悉以所填之词蔽之（默 `***`）。
- 自定义屏蔽列表 `custom_blocklist` → 单独补前规未防之词。
- 白名单 `allowlist` → 填此者虽中规亦不蔽。
- 代码块 -> `skip_codeblock`（```/~~~ 块）或 `skip_inline_code`（行内 `code`）开启者，其中不蔽。
- 内置附加：公网 IPv4（或含端口）→ `***.***.***.***`；`sk-xxx`、`gh[opu]_xxx` 之属 → `***`；裸 32/64 位 hex → `***`；键值对 `token=`、`password:`、`密钥` 等（反引号、引号包裹亦兼容）→ 蔽其值。
- 内网 IP（192.168.\*、10.\*、172.16-31.\*、127.\*、169.254.\*）与公网域名 → **放行**。

**[规则与用法详见 RULES.md](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/RULES.md)**

## 安装

1. AstrBot 管理面板 → 插件 → 安装 → 填此仓库地址
2. 启之即用，无需配置

## 更新记录

- [v1.1.2](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.1.2.md)：可跳过代码块/行内代码不屏蔽（`skip_codeblock`、`skip_inline_code`）。
- [v1.1.1](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.1.1.md)：增白名单，纯数字阈值敛至 8 位以上，减 6 位纯数字误伤。
- [v1.1.0](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.1.0.md)：配置化，拆分手机号/身份证/密码开关，增替换词与屏蔽列表，身份证含校验位。
- [v1.0.2](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.2.md)：修 `_KV_RE` 误报之患。
- [v1.0.1](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.1.md)：修漏网之鱼，增 hex 打码之规。
- [v1.0.0](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.0.md)：初版。

## 许可

AGPL-3.0

---

~~（注：此仓库乃 AI 所造，非人力也）~~
