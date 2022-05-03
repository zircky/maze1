class Stats():
    """отслеживание статистики"""

    def __init__(self):
        """инициализирует статистику"""
        self.reset_stats()

    def reset_stats(self):
        """статистика, изменяющаяся во время игры"""

        self.gun_left = 2