# astrbot-plugin-sensitive-filter

![](https://camo.githubusercontent.com/686bd6ac0ff62606ebb22b3ebdc7250dd2ad3859f75545e4353d89a5a178f8cc/68747470733a2f2f636f756e742e6765746c6f6c692e636f6d2f406e616761746f7175696e33333f6e616d653d6e616761746f7175696e3333267468656d653d72756c6533342670616464696e673d37266f66667365743d3026616c69676e3d746f70267363616c653d3126706978656c617465643d31266461726b6d6f64653d6175746f)

🌐 [文言](README.md) | [中文](README.zh-CN.md) | [English](README.en.md)

AstrBot 之插件也。凡回复将出，先察其文，遇敏感者辄打码蔽之（公网 IP、端口、token、key、密码之属）。

## 功能

- 公网 IPv4（或含端口）→ `***.***.***.***`
- `sk-xxx`、`gh[opu]_xxx` 之属 → `***`
- 裸 32 / 40 / 64 位 hex（frp token、MD5/SHA 之密钥）→ `***`
- 键值对 `token=`、`password:`、`密钥` 等（markdown 反引号、引号包裹亦兼容）→ 蔽其值
- 内网 IP（192.168.\*、10.\*、172.16-31.\*、127.\*、169.254.\*）与公网域名 → **放行**

**[规则与用法详见 RULES.md](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/RULES.md)**

## 安装

1. AstrBot 管理面板 → 插件 → 安装 → 填此仓库地址
2. 启之即用，无需配置

## 更新记录

- [v1.0.0](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.0.md)：初版。
- [v1.0.1](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.1.md)：修漏网之鱼，增 hex 打码之规。
- [v1.0.2](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.2.md)：修 `_KV_RE` 误报之患。

## 许可

AGPL-3.0

---

~~（注：此仓库乃 AI 所造，非人力也）~~
