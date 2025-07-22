

class Report:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def generate(self) -> str:
        return f"Report Title: {self.title}\nContent:\n{self.content}"