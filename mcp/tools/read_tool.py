# mcp/tools/read_tool.py

from mcp.query_parser import parse_filter, parse_projection, parse_sort


def read_tool(db, parsed: dict) -> dict:
    collection = parsed["collection"]
    filter_str = parsed.get("filter", "none")
    proj_str   = parsed.get("projection", "all")
    sort_str   = parsed.get("sort", "none")
    limit      = int(parsed.get("limit", 100))

    mongo_filter = parse_filter(filter_str)
    mongo_filter["is_deleted"] = {"$ne": True}

    projection = parse_projection(proj_str)
    sort       = parse_sort(sort_str)

    cursor = db[collection].find(mongo_filter, projection)

    if sort:
        cursor = cursor.sort(sort)

    cursor = cursor.limit(limit)
    data   = list(cursor)

    return {
        "operation":  "READ",
        "collection": collection,
        "filter":     mongo_filter,
        "count":      len(data),
        "data":       data
    }