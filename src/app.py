import json
import sys
from build_manager import BuildManager


def main():
    with open(sys.argv[1], "r") as reader:
        config = json.load(reader)
    
    manager = BuildManager()
    build_actions = manager.build(config)

    for action in build_actions:
        print(action)
    

if __name__ == "main":
    main()