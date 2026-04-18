import sys

class Tracker:
    def __init__(self) -> None:
        self.state = {
            "target": "[Idle]",
            "platform": "[NONE]",
            "queue": "[0/0]",
            "speed": "[0.0 B/s]",
            "active_size": "[0.0 B]",
            "session_payload": 0.0,
            "success": 0,
            "fail": 0,
            "retry": "",
            "cooldown": "[00:00]"
        }

    def reset_queue(self, total: int, platform: str) -> None:
        self.state["queue"] = f"[0/{total}]"
        self.state["platform"] = f"[{platform}]"
        self.state["success"] = 0
        self.state["fail"] = 0

    def update(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if k in self.state:
                self.state[k] = v
        self.render()

    def add_payload(self, mb: float) -> None:
        self.state["session_payload"] += mb

    def increment_success(self, current_idx: int, total: int) -> None:
        self.state["success"] += 1
        self.state["queue"] = f"[{current_idx}/{total}]"
        self.render()

    def increment_fail(self, current_idx: int, total: int) -> None:
        self.state["fail"] += 1
        self.state["queue"] = f"[{current_idx}/{total}]"
        self.render()

    def render(self) -> None:
        payload_gb = self.state["session_payload"] / 1024
        output = (
            f"\rTarget: {self.state['target']:<40} | "
            f"Plat: {self.state['platform']:<10} | "
            f"Q: {self.state['queue']:<10} | "
            f"Spd: {self.state['speed']:<12} | "
            f"Size: {self.state['active_size']:<10} | "
            f"Sess: [{payload_gb:.2f} GB] | "
            f"Succ: [✓ {self.state['success']}] | "
            f"Fail: [✗ {self.state['fail']}] | "
            f"{self.state['retry']} "
            f"CD: {self.state['cooldown']}"
        )
        sys.stdout.write(output[:sys.getterminalsize().columns - 1].ljust(sys.getterminalsize().columns - 1))
        sys.stdout.flush()