from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
import re


class SchemaExecutor:

    def __init__(self, mongo_uri: str, db_name: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def execute(self, agent2_output: str) -> dict:
        results = {}
        blocks = self._split_blocks(agent2_output)

        print(f"\n[SchemaExecutor] Found {len(blocks)} collections\n")

        for block in blocks:
            parsed = self._parse_block(block)
            if not parsed:
                continue

            name = parsed["collection"]
            indexes = parsed["indexes"]

            # Create collection
            if name not in self.db.list_collection_names():
                self.db.create_collection(name)
                results[name] = {"status": "created", "indexes": []}
            else:
                results[name] = {"status": "already exists", "indexes": []}

            # Apply indexes
            for index in indexes:
                try:
                    self.db[name].create_index(
                        index["keys"],
                        **index["options"]
                    )
                    results[name]["indexes"].append({
                        "keys": str(index["keys"]),
                        "status": "created"
                    })
                    print(f"  [{name}] index created: {index['keys']}")
                except Exception as e:
                    results[name]["indexes"].append({
                        "keys": str(index["keys"]),
                        "status": "failed: " + str(e)
                    })

        return results

    def _split_blocks(self, text: str) -> list:
        # Split on END marker — one block per collection
        raw = re.split(r'\bEND\b', text)
        return [b.strip() for b in raw if "COLLECTION:" in b]

    def _parse_block(self, block: str) -> dict:
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]

        parsed = {
            "collection": None,
            "category": None,
            "read_write": None,
            "fields": [],
            "indexes": []
        }

        section = None

        for line in lines:
            if line.startswith("COLLECTION:"):
                parsed["collection"] = line.split(":", 1)[1].strip().lower()

            elif line.startswith("CATEGORY:"):
                parsed["category"] = line.split(":", 1)[1].strip()

            elif line.startswith("READ_WRITE:"):
                parsed["read_write"] = line.split(":", 1)[1].strip()

            elif line == "FIELDS:":
                section = "fields"

            elif line == "INDEXES:":
                section = "indexes"

            elif section == "fields" and "|" in line:
                parsed["fields"].append(self._parse_field(line))

            elif section == "indexes" and "|" in line:
                index = self._parse_index(line)
                if index:
                    parsed["indexes"].append(index)

        return parsed if parsed["collection"] else None

    def _parse_field(self, line: str) -> dict:
        parts = [p.strip() for p in line.split("|")]
        return {
            "name":        parts[0] if len(parts) > 0 else "",
            "type":        parts[1] if len(parts) > 1 else "String",
            "required":    parts[2] if len(parts) > 2 else "no",
            "default":     parts[3] if len(parts) > 3 else "none",
            "enum_values": parts[4] if len(parts) > 4 else "none",
            "ref":         parts[5] if len(parts) > 5 else "none",
        }

    def _parse_index(self, line: str) -> dict:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 2:
            return None

        keys_raw = parts[0]
        index_type = parts[1]
        keys = []
        options = {}

        for field_part in keys_raw.split(","):
            field_part = field_part.strip()
            if ":" not in field_part:
                continue
            field, direction = field_part.split(":", 1)
            field = field.strip()
            direction = direction.strip()

            if direction == "1":
                keys.append((field, ASCENDING))
            elif direction == "-1":
                keys.append((field, DESCENDING))
            elif direction == "text":
                keys.append((field, TEXT))
            else:
                keys.append((field, ASCENDING))

        if index_type.startswith("ttl:"):
            seconds = int(index_type.split(":")[1])
            options["expireAfterSeconds"] = seconds

        if index_type == "unique":
            options["unique"] = True

        return {"keys": keys, "options": options} if keys else None
