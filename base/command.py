from base.commands import fetch_recommendations


class CommandRunner:
    def __init__(self, command):
        self._command = command

    def fetch_recommendations(self):
        fetch_recommendations()

    def silent_fetch_recommendations(self):
        fetch_recommendations(silent=True)

    def run(self):
        getattr(self, self._command)()
