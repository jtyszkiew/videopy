from abc import abstractmethod


class LoggerProvider:

    @abstractmethod
    def print(self, message):
        pass


class Logger:
    enabled = True
    level: int = 1
    provider: LoggerProvider = None

    @staticmethod
    def info(message):
        if not Logger.enabled or Logger.level == 0:
            return

        message = message.replace("<<", "[bold cyan]").replace(">>", "[/bold cyan]")
        Logger.provider.print(f"[bold blue]Info:[/bold blue] {message}")

    @staticmethod
    def warn(message):
        if not Logger.enabled or Logger.level < 2:
            return

        message = message.replace("<<", "[bold cyan]").replace(">>", "[/bold cyan]")
        Logger.provider.print(f"[bold orange]Warn:[/bold orange] {message}")

    @staticmethod
    def error(message):
        if not Logger.enabled:
            return

        message = message.replace("<<", "[bold cyan]").replace(">>", "[/bold cyan]")
        Logger.provider.print(f"[bold red]Error:[/bold red] {message}")

    @staticmethod
    def debug(message):
        if not Logger.enabled or Logger.level < 3:
            return

        message = message.replace("<<", "[bold cyan]").replace(">>", "[/bold cyan]")
        Logger.provider.print(f"[bold green]Debug:[/bold green] {message}")

    @staticmethod
    def trace(message):
        if not Logger.enabled or Logger.level < 4:
            return

        message = message.replace("<<", "[bold cyan]").replace(">>", "[/bold cyan]")
        Logger.provider.print(f"[bold magenta]Trace:[/bold magenta] {message}")

    @staticmethod
    def set_level(level: str):
        if level == "info":
            Logger.level = 1
        elif level == "warn":
            Logger.level = 2
        elif level == "debug":
            Logger.level = 3
        elif level == "trace":
            Logger.level = 4
        else:
            Logger.level = 1
