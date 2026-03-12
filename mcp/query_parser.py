# mcp/query_parser.py

from pymongo import ASCENDING, DESCENDING


def parse_filter(filter_str: str) -> dict:
    if not filter_str or filter_str.strip().lower() == "none":
        return {}

    operator_map = {
        "gt": "$gt", "lt": "$lt",
        "gte": "$gte", "lte": "$lte",
        "ne": "$ne", "in": "$in"
    }

    mongo_filter = {}

    for part in filter_str.split(","):
        part = part.strip()
        segments = part.split(":")

        if len(segments) == 2:
            field, value = segments
            mongo_filter[field.strip()] = cast(value.strip())

        elif len(segments) == 3:
            field, operator, value = segments
            field    = field.strip()
            operator = operator.strip()
            value    = value.strip()

            if operator == "in":
                mongo_filter[field] = {
                    "$in": [cast(v) for v in value.split(";")]
                }
            elif operator in operator_map:
                mongo_filter[field] = {
                    operator_map[operator]: cast(value)
                }

    return mongo_filter


def parse_projection(projection_str: str) -> dict:
    if not projection_str or projection_str.strip().lower() == "all":
        return {"_id": 0}
    fields = {"_id": 0}
    for f in projection_str.split(","):
        fields[f.strip()] = 1
    return fields


def parse_sort(sort_str: str) -> list:
    if not sort_str or sort_str.strip().lower() == "none":
        return None
    result = []
    for part in sort_str.split(","):
        if ":" in part:
            field, direction = part.strip().split(":")
            result.append((
                field.strip(),
                ASCENDING if direction.strip() == "1" else DESCENDING
            ))
    return result or None


def parse_fields_block(lines: list) -> dict:
    fields = {}
    for line in lines:
        if ":" in line:
            key, val = line.split(":", 1)
            fields[key.strip()] = cast(val.strip())
    return fields


def cast(value: str):
    if value.lower() == "true":  return True
    if value.lower() == "false": return False
    try: return int(value)
    except ValueError: pass
    try: return float(value)
    except ValueError: pass
    return value