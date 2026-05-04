"""Experience extractor — derive learnable memories from conversations."""

from ..memory.store import Memory


class ExperienceExtractor:
    """Extract structured memories from user↔assistant exchanges.

    Uses keyword heuristics (MVP). Upgrade to LLM-based extraction
    when an API key is configured.
    """

    # Error-pattern keywords → importance boost
    ERROR_PATTERNS = ["错误", "不行", "失败", "搞不定", "bug", "error", "fix"]
    SUCCESS_PATTERNS = ["好了", "成功", "搞定", "谢谢", "棒", "完美", "works"]
    INSIGHT_PATTERNS = ["原来", "发现", "学到了", "注意", "关键", "trick", "tip"]

    def extract(
        self,
        user_message: str,
        assistant_response: str,
        session_id: str = "",
    ) -> list[Memory]:
        """Extract memories from a single exchange.

        Returns a list of Memory objects ready to store.
        """
        memories = []
        combined = f"{user_message} {assistant_response}".lower()

        # Detect error experiences
        for kw in self.ERROR_PATTERNS:
            if kw in combined:
                memories.append(
                    Memory(
                        type="error",
                        content=f"遇到问题: {user_message[:120]} → 响应: {assistant_response[:120]}",
                        importance=7.0,
                        session_id=session_id,
                        tags=["error", "correction"],
                    )
                )
                break  # one error memory per exchange

        # Detect insight moments
        for kw in self.INSIGHT_PATTERNS:
            if kw in combined:
                memories.append(
                    Memory(
                        type="insight",
                        content=f"获得洞察: {user_message[:120]} → 响应: {assistant_response[:120]}",
                        importance=6.0,
                        session_id=session_id,
                        tags=["insight", "learning"],
                    )
                )
                break

        # Always store as experience (with lower importance)
        # But skip if content is too trivial
        if len(combined) >= 10:
            importance = 3.0
            # Boost importance for longer exchanges
            if len(combined) > 200:
                importance = 5.0

            memories.append(
                Memory(
                    type="experience",
                    content=f"{user_message[:100]} → {assistant_response[:100]}",
                    importance=importance,
                    session_id=session_id,
                    tags=["interaction"],
                )
            )

        return memories