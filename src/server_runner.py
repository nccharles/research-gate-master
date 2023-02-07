__author__ = "Sylivie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

from src.server.research_gate_server import ResearchGateServer
import sys

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        port = sys.argv[1]
    else:
        port = 5050
    server: ResearchGateServer = ResearchGateServer(port=port)
    server.start()
