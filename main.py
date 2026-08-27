"""sensitive_filter: 输出敏感信息过滤插件
在 AstrBot 回复发送前，将手机号/身份证号/密码等敏感信息自动打码（可配置）。
内置附加规则：公网IP/端口、sk-xxx/GitHub token 等恒启用；内网IP与公网域名放行。
"""
import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain
from astrbot.api import logger

# key 形态：sk-xxx（DeepSeek/OpenAI）、gh[opu]_xxx（GitHub）、32/64 位 hex
_TOKEN_RE = re.compile(
    r'\bsk-[A-Za-z0-9]{10,}\b'
    r'|\bgh[opu]_[A-Za-z0-9]{10,}\b'
    r'|\b[0-9a-fA-F]{32}\b'
    r'|\b[0-9a-fA-F]{64}\b'
)
# 键值对：password/key/token/密码/口令 等 + 分隔符 + 值
_KV_RE = re.compile(
    r'((?:api[_-]?key|access[_-]?key|secret|token|password|passwd|pwd|'
    r'密码|口令|密钥|key)[=:：\s`\'"\u2018\u2019\u201c\u201d]*)(?!/)([A-Za-z0-9_\-./@]{6,})',
    re.I,
)
# 大陆手机号：11 位、1[3-9] 开头
_PHONE_RE = re.compile(r'(?<!\d)(1[3-9]\d)\d{8}(?!\d)')
# 身份证号：18 位，前17数字+末位数字或X，含出生日期合理性（不校验校验码）
_IDCARD_RE = re.compile(
    r'(?<!\d)([1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[0-9Xx])(?!\d)'
)
# 纯数字密码：6-20 位纯数字（排除手机号/身份证格式后一般不会误伤，但会命中普通长数字）
_PURE_DIGIT_RE = re.compile(r'(?<!\d)\d{8,20}(?!\d)')
# 纯字母密码：6-24 位纯字母
_PURE_ALPHA_RE = re.compile(r'(?<![A-Za-z])[A-Za-z]{6,24}(?![A-Za-z])')
# 常见弱密码词（纯字母/数字形态的弱密码，大小写不敏感）
_WEAK_PWD_RE = re.compile(
    r'(?<![A-Za-z0-9])(?:password|passw0rd|p@ssw0rd|qwerty|qazwsx|abc123|letmein|'
    r'welcome|iloveyou|dragon|monkey|111111|000000|123456|12345678|'
    r'1234567890|654321|666666|888888|5201314)(?![A-Za-z0-9])',
    re.I,
)
# 间隔交替密码：字母数字严格交替，如 1q2w3e4r
_MIXED_ALT_RE = re.compile(
    r'(?<![A-Za-z0-9])(?:[A-Za-z][0-9]|[0-9][A-Za-z]){3,12}(?![A-Za-z0-9])'
)
# 字母数字混排(非交替)：如 9178sb12b、admin2026（会连带命中 room2026 类英文词+数字）
_MIXED_OTHER_RE = re.compile(
    r'(?<![A-Za-z0-9])(?=[A-Za-z0-9]{7,24})(?=[A-Za-z]*[0-9])(?=[0-9]*[A-Za-z])'
    r'[A-Za-z0-9]{7,24}(?![A-Za-z0-9])'
)
# IPv4（含可选 :端口）
_IP_PORT_RE = re.compile(
    r'(?<!\d)((?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d))(?!\d)(?::(\d{1,5}))?'
)


# 身份证校验位权重 / 校验码
_ID_W = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
_ID_CHECK = "10X98765432"


# Markdown 代码块（fenced 或 ~）与行内 code
_FENCED_RE = re.compile(r'```.*?```|~~~.*?~~~', re.S)
_INLINE_RE = re.compile(r'`[^`\n]*`')


@register("sensitive_filter", "toolman", "输出敏感信息过滤（自动打码）", "1.1.2")
class SensitiveFilter(Star):
    def __init__(self, context: Context, config=None):
        super().__init__(context)
        self.config = config or {}
        self.replace_text = (self.config.get("replace_text") or "***") or "***"

        phone = self.config.get("phone", {}) or {}
        self.en_phone = phone.get("enabled", True)
        self.phone_full = phone.get("mask_mode", "partial") == "full"

        idcard = self.config.get("idcard", {}) or {}
        self.en_idcard = idcard.get("enabled", True)

        pwd = self.config.get("password", {}) or {}
        self.en_pwd = pwd.get("enabled", True)
        self.en_pure_digit = pwd.get("pure_digit", True)
        self.en_pure_alpha = pwd.get("pure_alpha", False)
        self.en_mixed_alt = pwd.get("mixed_alt", True)
        self.en_mixed_other = pwd.get("mixed_other", True)

        bl = self.config.get("custom_blocklist", {}) or {}
        self.en_blocklist = bl.get("enabled", False)
        self._blocklist_re = self._build_blocklist_re(bl.get("words", ""))
        al = self.config.get("allowlist", {}) or {}
        self.en_allowlist = al.get("enabled", False)
        self._allow_re = self._build_words_re(al.get("words", ""))
        self.skip_codeblock = self.config.get("skip_codeblock", False)
        self.skip_inline_code = self.config.get("skip_inline_code", False)

        logger.info(
            f"[sensitive_filter] 已加载 v1.1.0：手机号={self.en_phone} "
            f"身份证={self.en_idcard} 密码={self.en_pwd} 屏蔽列表={self.en_blocklist}"
        )

    def _protect_codeblocks(self, text: str):
        m = {}
        def repl(mo):
            ph = "\x00C%d\x00" % len(m)
            m[ph] = mo.group(0)
            return ph
        if self.skip_codeblock:
            text = _FENCED_RE.sub(repl, text)
        if self.skip_inline_code:
            text = _INLINE_RE.sub(repl, text)
        return text, m

    @staticmethod
    def _build_words_re(words):
        if isinstance(words, list):
            words = "\n".join(str(x) for x in words)
        parts = re.split(r"[\n,，、;；]+", str(words or ""))
        return [p.strip() for p in parts if p and p.strip()]

    @staticmethod
    def _build_blocklist_re(words):
        """按配置构建自定义屏蔽列表正则；无词返回 None。"""
        if not words:
            return None
        if isinstance(words, list):
            words = "\n".join(str(x) for x in words)
        parts = re.split(r"[\n,，、;；]+", str(words))
        parts = [p.strip() for p in parts if p and p.strip()]
        if not parts:
            return None
        return re.compile("|".join(re.escape(p) for p in parts))

    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent, result=None):
        """发送前钩子：遍历消息链中的纯文本，打码敏感信息。"""
        result = result if result is not None else event.get_result()
        if not result or not getattr(result, "chain", None):
            return
        for comp in list(result.chain):
            if isinstance(comp, Plain) and comp.text:
                comp.text = self._sanitize(comp.text)
        reasoning = event.get_extra("_llm_reasoning_content")
        if reasoning:
            event.set_extra("_llm_reasoning_content", self._sanitize(str(reasoning)))

    def _sanitize(self, text: str) -> str:
        rt = self.replace_text
        code_map = None
        if self.skip_codeblock or self.skip_inline_code:
            text, code_map = self._protect_codeblocks(text)
        ph_map = None
        if self.en_allowlist and self._allow_re:
            ph_map = {}
            for i, w in enumerate(self._allow_re):
                ph = "\x00A%d\x00" % i
                if w in text:
                    text = text.replace(w, ph)
                    ph_map[ph] = w
        # 恒定内置：token/key
        text = _TOKEN_RE.sub(rt, text)
        text = _KV_RE.sub(lambda m: m.group(1) + rt, text)
        # 手机号
        if self.en_phone:
            text = _PHONE_RE.sub(rt if self.phone_full else lambda m: m.group(1) + '********', text)
        # 身份证号
        if self.en_idcard:
            text = _IDCARD_RE.sub(self._mask_id, text)
        # 密码（按形态开关）
        if self.en_pwd:
            if self.en_pure_digit:
                text = _PURE_DIGIT_RE.sub(rt, text)
            if self.en_pure_alpha:
                text = _PURE_ALPHA_RE.sub(rt, text)
            text = _WEAK_PWD_RE.sub(rt, text)
            if self.en_mixed_alt:
                text = _MIXED_ALT_RE.sub(rt, text)
            if self.en_mixed_other:
                text = _MIXED_OTHER_RE.sub(rt, text)
        # 自定义屏蔽列表
        if self.en_blocklist and self._blocklist_re:
            text = self._blocklist_re.sub(rt, text)
        # 公网 IP（内网放行）
        text = _IP_PORT_RE.sub(self._mask_ip, text)
        if ph_map:
            for ph, w in ph_map.items():
                text = text.replace(ph, w)
        if code_map:
            for ph, c in code_map.items():
                text = text.replace(ph, c)
        return text

    def _mask_id(self, m: re.Match) -> str:
        s = m.group(1)
        return m.group(0) if not SensitiveFilter._valid_id(s) else self.replace_text

    @staticmethod
    def _valid_id(s: str) -> bool:
        body = s[:-1]
        last = s[-1].upper()
        if not body.isdigit() or len(body) != 17:
            return False
        t = sum(int(c) * _ID_W[i] for i, c in enumerate(body)) % 11
        return _ID_CHECK[t] == last

    @staticmethod
    def _mask_ip(m: re.Match) -> str:
        ip = m.group(1)
        return m.group(0) if SensitiveFilter._is_private(ip) else '***.***.***.***'

    @staticmethod
    def _is_private(ip: str) -> bool:
        try:
            a, b = (int(x) for x in ip.split('.')[:2])
        except Exception:
            return False
        if a == 10 or (a == 192 and b == 168) or (a == 172 and 16 <= b <= 31):
            return True
        if a == 127 or a == 0 or (a == 169 and b == 254):
            return True
        if 224 <= a <= 239 or a >= 240:
            return True
        return False
