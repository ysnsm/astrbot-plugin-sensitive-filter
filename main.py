"""sensitive_filter: 输出敏感信息过滤插件
在 AstrBot 回复发送前，将公网IP/端口/密码/token/key/手机号等敏感信息自动打码。
内网IP（192.168.*、10.*、172.16-31.*、127.*、169.254.*）与公网域名放行。
"""
import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain
from astrbot.api import logger

# key 形态：sk-xxx（DeepSeek/OpenAI）、gh[opu]_xxx（GitHub）、
# 32/40/64 位 hex（frp token、MD5/SHA 型密钥，如 037d71...）
_TOKEN_RE = re.compile(
    r'\bsk-[A-Za-z0-9]{10,}\b'
    r'|\bgh[opu]_[A-Za-z0-9]{10,}\b'
    r'|\b[0-9a-fA-F]{32}\b'
    r'|\b[0-9a-fA-F]{40}\b'
    r'|\b[0-9a-fA-F]{64}\b'
)
# 键值对：password/key/token/密码/口令 等 + 分隔符 + 值
# 分隔符含 全角/半角冒号、空格、反引号、引号（兼容 markdown 代码包裹）
_KV_RE = re.compile(
    r'((?:api[_-]?key|access[_-]?key|secret|token|password|passwd|pwd|'
    r'密码|口令|密钥|key)[=:：\s`\'"\u2018\u2019\u201c\u201d]*)([A-Za-z0-9_\-./@]{6,})',
    re.I,
)
# 大陆手机号：11 位、1[3-9] 开头（只留第 1 位，其余全隐藏，防暴力枚举）
_PHONE_RE = re.compile(r'(?<!\d)1[3-9]\d{9}(?!\d)')
# IPv4（含可选 :端口）
_IP_PORT_RE = re.compile(
    r'(?<!\d)((?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d))(?!\d)(?::(\d{1,5}))?'
)


@register("sensitive_filter", "toolman", "输出敏感信息过滤（自动打码）", "1.0.0")
class SensitiveFilter(Star):
    def __init__(self, context: Context, config=None):
        super().__init__(context)
        self.config = config or {}
        logger.info("[sensitive_filter] 已加载：回复输出前自动打码敏感信息")

    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent, result=None):
        """发送前钩子：遍历消息链中的纯文本，打码敏感信息
        兼容两种调用方式：旧版只传 event；新版传 (event, result)。
        """
        result = result if result is not None else event.get_result()
        if not result or not getattr(result, "chain", None):
            return
        for comp in list(result.chain):
            if isinstance(comp, Plain) and comp.text:
                comp.text = self._sanitize(comp.text)
        # 思考内容打码：AstrBot 在 on_agent_done 时把 reasoning 存进
        # event extra(_llm_reasoning_content)，result_decorate 阶段（本钩子之后）
        # 才把它注入消息链。这里提前打码，思考内容同样被拦截。
        reasoning = event.get_extra("_llm_reasoning_content")
        if reasoning:
            event.set_extra("_llm_reasoning_content", self._sanitize(str(reasoning)))

    def _sanitize(self, text: str) -> str:
        text = _TOKEN_RE.sub('***', text)
        text = _KV_RE.sub(lambda m: m.group(1) + '***', text)
        text = _PHONE_RE.sub('1**********', text)
        text = _IP_PORT_RE.sub(self._mask_ip, text)
        return text

    @staticmethod
    def _mask_ip(m: re.Match) -> str:
        ip = m.group(1)
        if SensitiveFilter._is_private(ip):
            return m.group(0)  # 内网放行
        return '***.***.***.***'  # 公网打码（含端口）

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
        if 224 <= a <= 239 or a >= 240:  # 组播/保留
            return True
        return False
