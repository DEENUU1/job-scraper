from typing import Optional, List


def check_title(title: str, keywords: List[Optional[str]]) -> bool:
    if not keywords:
        return False

    keywords_lower = [keyword.lower() for keyword in keywords]
    title = title.lower()

    for keyword in keywords_lower:
        if keyword in title:
            return True
    return False
