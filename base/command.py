from base.commands import fetch_recommendations


class CommandRunner:
    def __init__(self, command):
        self._command = getattr(self, command)

    def fetch_recommendations(self):
        fetch_recommendations()

    def silent_fetch_recommendations(self):
        fetch_recommendations(silent=True)

    def run(self):
        self._command()
