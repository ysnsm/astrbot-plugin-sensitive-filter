# astrbot-plugin-sensitive-filter

🌐 [English](README.en.md) | [中文](README.md) | [文言](README.zh-classical.md)

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
