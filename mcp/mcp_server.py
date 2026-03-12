# mcp/mcp_server.py

from pymongo import MongoClient
from mcp.schema_reader import SchemaReader
from mcp.query_parser import parse_filter, parse_fields_block
from mcp.prompts.crud_system_prompt import crud_system_prompt
from mcp.prompts.aggregate_system_prompt import aggregate_system_prompt
from mcp.tools.create_tool import create_tool
from mcp.tools.read_tool import read_tool
from mcp.tools.update_tool import update_tool
from mcp.tools.delete_tool import delete_tool
from mcp.tools.aggregate_tool import aggregate_tool
from llm.factory import get_llm_strategy

llm = get_llm_strategy()


class MCPServer:

    def __init__(self, mongo_uri: str, db_name: str):
        self.client        = MongoClient(mongo_uri)
        self.db            = self.client[db_name]
        self.schema_reader = SchemaReader(mongo_uri, db_name)

    def handle(self, user_prompt: str) -> dict:
        schema_desc = self.schema_reader.describe_all()
        operation   = self._detect_operation(user_prompt)

        if operation == "AGGREGATE":
            system = aggregate_system_prompt
        else:
            system = crud_system_prompt

        llm_input = (
            "AVAILABLE SCHEMA:\n"
            + schema_desc
            + "\nUSER REQUEST:\n"
            + user_prompt
            + "\n\nGenerate the operation block."
        )

        raw = llm.chat(system_prompt=system, user_prompt=llm_input)
        print(f"\n[MCPServer] LLM output:\n{raw}\n")

        parsed = self._parse_block(raw)

        op = parsed.get("operation", "").upper()

        if op == "CREATE":    return create_tool(self.db, parsed)
        if op == "READ":      return read_tool(self.db, parsed)
        if op == "UPDATE":    return update_tool(self.db, parsed)
        if op == "DELETE":    return delete_tool(self.db, parsed)
        if op == "AGGREGATE": return aggregate_tool(self.db, parsed)

        return {"error": "Could not detect operation from prompt"}

    def _detect_operation(self, prompt: str) -> str:
        prompt = prompt.lower()
        if any(w in prompt for w in ["count", "total", "average", "group", "sum", "revenue", "analytics"]):
            return "AGGREGATE"
        return "CRUD"

    def _parse_block(self, raw: str) -> dict:
        lines   = [l.strip() for l in raw.strip().splitlines() if l.strip()]
        parsed  = {}
        section = None
        buffer  = []

        for line in lines:
            if line == "END":
                if section == "fields":
                    parsed["fields"] = parse_fields_block(buffer)
                elif section == "update_fields":
                    parsed["update_fields"] = parse_fields_block(buffer)
                elif section == "pipeline":
                    parsed["pipeline_lines"] = buffer
                buffer  = []
                section = None

            elif line.startswith("OPERATION:"):
                parsed["operation"] = line.split(":", 1)[1].strip()

            elif line.startswith("COLLECTION:"):
                parsed["collection"] = line.split(":", 1)[1].strip().lower()

            elif line.startswith("FILTER:"):
                parsed["filter"] = line.split(":", 1)[1].strip()

            elif line.startswith("PROJECTION:"):
                parsed["projection"] = line.split(":", 1)[1].strip()

            elif line.startswith("SORT:"):
                parsed["sort"] = line.split(":", 1)[1].strip()

            elif line.startswith("LIMIT:"):
                parsed["limit"] = line.split(":", 1)[1].strip()

            elif line.startswith("SOFT_DELETE:"):
                parsed["soft_delete"] = line.split(":", 1)[1].strip()

            elif line == "FIELDS:":
                section = "fields"

            elif line == "UPDATE_FIELDS:":
                section = "update_fields"

            elif line == "PIPELINE:":
                section = "pipeline"

            elif section in ("fields", "update_fields", "pipeline"):
                buffer.append(line)

        return parsed