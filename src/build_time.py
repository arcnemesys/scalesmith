from build_manager import BuildManager

class BuildTime(BuildManager):
    def _check_keys(self, name, details):
        super()._check_keys(name, details)
        self._must("time" in details, f"No time for {name}")

    def _refresh(self, config, node, actions):
        assert node in config, f"Unknown node {node}"
        if self._needs_update(config, node):
            actions.append(config[node]["rule"])

    def _needs_update(self, config, node):
        return any(
            config[node]["time"] < config[d]["time"]
            for d in config[node]["depends"]
        )
