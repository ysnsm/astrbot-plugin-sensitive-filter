# 敏感信息过滤器 (sensitive_filter)

在 AstrBot 回复发送前，自动打码敏感信息。所有检测类别均可通过 WebUI 插件配置独立开关。

## 功能
- 三类敏感信息：**手机号**、**身份证号**（含校验位校验）、**密码**
- 密码再分形态开关：纯数字 / 纯字母 / 间隔交替 / 字母数字混排 + 弱密码词表
- **替换词**：命中时统一替换为自定义文本（默认 `***`）
- **自定义屏蔽列表**：单独补充前面的规则没防到的词/密码
- 内置附加规则：公网 IP / 端口、sk-xxx/GitHub token 等（恒启用，内网IP放行）

## 配置
在 WebUI → 插件 → `sensitive_filter` → 配置 中设置：
- `replace_text`：替换词
- `phone.enabled` / `phone.mask_mode`：手机号开关与打码方式（partial=保留前3后4，full=整段）
- `idcard.enabled`：身份证检测（含校验位校验）
- `password.*`：密码各形态开关
- `custom_blocklist.enabled` / `.words`：自定义屏蔽列表（换行/逗号/顿号/分号分隔）

> 注意：`pure_alpha` 默认关闭（避免误伤正常英文单词）；`mixed_other` 会连带命中 `room2026` 这类英文词+数字。

## 安装
将插件目录放入 `data/plugins/`，在 WebUI 插件管理重载或重启 AstrBot 生效。
