import random
import time

def human_delay(min_s: float = 0.8, max_s: float = 2.5) -> None:
    time.sleep(random.uniform(min_s, max_s))

def heavy_delay() -> None:
    time.sleep(random.uniform(3.0, 12.0))

def typing_delay(text: str) -> None:
    """
    Simula digitação humana
    """
    for _ in text:
        time.sleep(random.uniform(0.03, 0.12))