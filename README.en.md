# astrbot-plugin-sensitive-filter

🌐 [文言](README.md) | [中文](README.zh-CN.md) | [English](README.en.md)

An AstrBot plugin that automatically masks sensitive information (public IP / port / token / key / password) before replies are sent.

## Features

- Public IPv4 (with optional port) → `***.***.***.***`
- Keys like `sk-xxx`, `gh[opu]_xxx` → `***`
- Bare 32 / 40 / 64-char hex strings (frp tokens, MD5/SHA-style keys) → `***`
- Key-value pairs `token=` / `password:` / `密钥` etc. (markdown backtick/quote wrapping supported) → value masked
- Private IPs (192.168.\*, 10.\*, 172.16-31.\*, 127.\*, 169.254.\*) and public domains → **passed through**

**[Click here for the full rules and usage](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/RULES.md)**

## Installation

1. AstrBot Dashboard → Plugins → Install → enter this repository URL
2. Enable the plugin — no extra configuration required

## Changelog

- [v1.0.0](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.0.md): Initial release.
- [v1.0.1](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.1.md): Bug fixes + new masking rules.
- [v1.0.2](https://github.com/ysnsm/astrbot-plugin-sensitive-filter/blob/main/update/v1.0.2.md): Fixed `_KV_RE` false positives.

## License

AGPL-3.0

---

~~(Note: This repository was made by an AI.)~~
