# astrbot-plugin-sensitive-filter

![](https://camo.githubusercontent.com/686bd6ac0ff62606ebb22b3ebdc7250dd2ad3859f75545e4353d89a5a178f8cc/68747470733a2f2f636f756e742e6765746c6f6c692e636f6d2f406e616761746f7175696e33333f6e616d653d6e616761746f7175696e3333267468656d653d72756c6533342670616464696e673d37266f66667365743d3026616c69676e3d746f70267363616c653d3126706978656c617465643d31266461726b6d6f64653d6175746f)

🌐 [文言](README.md)  [中文](README.zh-CN.md)  [English](README.en.md)

AstrBot 插件：在回复发送前自动对敏感信息打码（公网 IP / 端口 / token / key / 密码）。

## 功能

- 公网 IPv4（含端口）→ `***.***.***.***`
- `sk-xxx`、`gh[opu]_xxx` 形态 key → `***`
- 裸 32 / 40 / 64 位 hex（frp token、MD5/SHA 型密钥）→ `***`
- 键值对 `token=` / `password:` / `密钥` 等（兼容 markdown 反引号/引号包裹）→ 值打码
- 内网 IP（192.168.\*、10.\*、172.16-31.\*、127.\*、169.254.\*）与公网域名 → **放行**

**[点击这里查看规则列表与用法](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/RULES.md)**

## 安装

1. AstrBot 管理面板 → 插件 → 安装 → 填入本仓库地址
2. 启用插件即可，无需额外配置

## 更新记录

- [v1.0.0](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.0.md)：初始版本。
- [v1.0.1](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.1.md)：修复问题+新增打码规则
- [v1.0.2](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.2.md)：修复`_KV_RE`误报

---

~~（注：这个仓库是AI做的）~~
