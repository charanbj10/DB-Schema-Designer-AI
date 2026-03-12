# mcp/tools/aggregate_tool.py

from pymongo import ASCENDING, DESCENDING


def aggregate_tool(db, parsed: dict) -> dict:
    collection = parsed["collection"]
    pipeline   = _build_pipeline(parsed.get("pipeline_lines", []))

    results = list(db[collection].aggregate(pipeline))
    for r in results:
        r.pop("_id", None)

    return {
        "operation":  "AGGREGATE",
        "collection": collection,
        "pipeline":   pipeline,
        "count":      len(results),
        "data":       results
    }


def _build_pipeline(lines: list) -> list:
    pipeline = []
    acc_map  = {
        "sum": "$sum", "avg": "$avg",
        "min": "$min", "max": "$max"
    }

    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        stage = parts[0].upper()

        if stage == "MATCH" and len(parts) > 1 and parts[1].lower() != "none":
            match = {}
            for seg in parts[1].split(","):
                if ":" in seg:
                    k, v = seg.strip().split(":", 1)
                    match[k.strip()] = v.strip()
            pipeline.append({"$match": match})

        elif stage == "GROUP" and len(parts) > 1:
            group_stage = {}
            id_raw = parts[1]
            if ":" in id_raw:
                _, id_field = id_raw.split(":", 1)
                group_stage["_id"] = "$" + id_field.strip()
            else:
                group_stage["_id"] = None

            for acc in parts[2:]:
                acc_parts = acc.split(":")
                if len(acc_parts) == 3:
                    alias, field, op = [x.strip() for x in acc_parts]
                    if op == "count":
                        group_stage[alias] = {"$sum": 1}
                    elif op in acc_map:
                        group_stage[alias] = {acc_map[op]: "$" + field}

            pipeline.append({"$group": group_stage})

        elif stage == "SORT" and len(parts) > 1 and parts[1].lower() != "none":
            sort = {}
            for s in parts[1].split(","):
                if ":" in s:
                    f, d = s.strip().split(":")
                    sort[f.strip()] = int(d.strip())
            pipeline.append({"$sort": sort})

        elif stage == "LIMIT" and len(parts) > 1 and parts[1].lower() != "none":
            pipeline.append({"$limit": int(parts[1])})

        elif stage == "PROJECT" and len(parts) > 1 and parts[1].lower() != "none":
            proj = {"_id": 0}
            for f in parts[1].split(","):
                proj[f.strip()] = 1
            pipeline.append({"$project": proj})

    return pipeline