import json
import sys

class BuildManager:
    def build(self, config):
        config = self._configure(config)
        ordered = self._topo_sort(config)
        actions = []
        for node in ordered:
            self._refresh(config, node, actions)
        return actions

    def _refresh(self, config, node, actions):
        assert node in config, f"Unknown node {node}"
        actions.append(config[node]["rule"])

    def _must(self, condition, message):
        if not condition:
            raise ValueError(message)

    def _configure(self, config):
        known = set(config.keys())
        return {n: self._check(n, d, known)
                for n, d in config.items() if not self._is_phony(config[n])}

    def _check(self, name, details, known):
        
        self._check_keys(name, details)
        depends = set(details["depends"])
        self._must(
            depends.issubset(known), f"Unknown depends for {name}"
        )
        result = details.copy()
        result["depends"] = depends
        return result

    def _check_keys(self, name, details):
        self._must("rule" in details, f"Missing rule for {name}")
        self._must(
            "depends" in details, f"Missing depends for {name}"
        )

    def _topo_sort(self, config):
        graph = {n: config[n]["depends"] for n in config}
        result = []
        while graph:
            available = {n for n in graph if not graph[n]}
            self._must(
                available,
                f"Circular graph {list(graph.keys())}",
            )
            result.extend(sorted(available))
            graph = {
                n: graph[n] - available
                for n in graph
                if n not in available
            }
        return result


    def _is_phony(self, node):
        if "phony" not in node:
            return False
        
        if node["phony"] is True:
            return True
        else:
            return False 
        