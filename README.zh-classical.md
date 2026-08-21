# 敏感信息过滤器（astrbot-plugin-sensitive-filter）

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
