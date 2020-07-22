import re
import os

from ._base_command_handler import BaseCommandHandler
from ._pipe_holder import PipeHolder


class GetCallGraph(BaseCommandHandler):

    def handle(self, *args):
        try:
            pipe = PipeHolder.get_pipe()
            return_value = pipe.cmd("agCd")
        except ValueError:
            return_value = "Pipe must be opened before graphing."
        return return_value


class GetAllFunctionGraphs(BaseCommandHandler):

    def __init__(self, config):
        super().__init__(config)
        self.reserved_statement_pattern = re.compile(r"(digraph|\s+(graph|node|edge))")

    def _merge_graph(self, all_function_graphs):
        graph_content = []
        header_lines = [
            'digraph code {',
            '       graph [bgcolor=azure fontsize=8 fontname="Courier" splines="ortho"];',
            '       node [fillcolor=gray style=filled shape=box];',
            '       edge [arrowhead="normal"];',
        ]
        for line in all_function_graphs.split("\n"):
            if not self.reserved_statement_pattern.findall(line) and not line.strip().startswith("}") and not line.strip().startswith("digraph"):
                graph_content.append(line)
        return os.linesep.join(header_lines + graph_content + ["}"])

    def handle(self, *args):
        try:
            pipe = PipeHolder.get_pipe()
            all_function_graphs = pipe.cmd("agfd @@ fcn.*")
            # Because radare2 just vomits this all out as one big blob
            return_value = self._merge_graph(all_function_graphs)
        except ValueError:
            return_value = "Pipe must be opened before graphing."
        return return_value