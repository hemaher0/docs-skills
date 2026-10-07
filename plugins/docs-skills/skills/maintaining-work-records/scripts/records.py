#!/usr/bin/env python3
"""Validate and list repository-local document records without dependencies."""

import argparse
import datetime as dt
import json
import re
import string
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*$")
HEADING = re.compile(r"^# (\d{4}-\d{2}-\d{2})-.+$", re.MULTILINE)
SECTION = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
LINK = re.compile(r"\[[^]]+\]\((<[^>]+>|[^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
COMMON_FIELDS = (
    "schema_version",
    "id",
    "type",
    "lifecycle",
    "created_at",
    "updated_at",
)
WEEKDAYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)
EVENT = re.compile(r"^### (\S+) — ([^—\n]+) — ([^—\n]+)\s*$", re.MULTILINE)
BUNDLED_ROOT = Path(__file__).resolve().parents[1]
BUNDLED_SCHEMA = BUNDLED_ROOT / "references/schema.json"
PROJECT_SCHEMA = Path(".agents/config/docs-skills/schema.json")


def resolve_schema(root, selected=None):
    if selected is not None:
        return Path(selected).resolve()
    project_schema = Path(root) / PROJECT_SCHEMA
    if project_schema.exists() or project_schema.is_symlink():
        return project_schema.resolve()
    return BUNDLED_SCHEMA


def template_path(root, template, schema_path=None):
    if Path(template).is_absolute():
        return None
    for directory in (resolve_schema(root, schema_path).parent, BUNDLED_ROOT):
        candidate = directory / template
        if not candidate.resolve().is_relative_to(directory.resolve()):
            return None
        if candidate.exists() or candidate.is_symlink():
            return candidate.resolve() if candidate.is_file() else None
    return None


def schema(root, schema_path=None):
    registry = json.loads(
        resolve_schema(root, schema_path).read_text(encoding="utf-8")
    )
    if not isinstance(registry, dict):
        raise ValueError("schema must be an object")
    types = registry.get("types")
    if not isinstance(types, dict):
        raise ValueError("types must be an object")
    for name, rule in types.items():
        if not isinstance(rule, dict):
            raise ValueError(f"invalid rule for {name}")
        for field in ("required_sections", "lifecycles", "required_fields"):
            if field in rule and (
                not isinstance(rule[field], list)
                or any(
                    not isinstance(value, str) or not value
                    for value in rule[field]
                )
            ):
                raise ValueError(
                    f"{name}: {field} must be a list of nonempty strings"
                )
        if "work_item_required" in rule and not isinstance(
            rule["work_item_required"], bool
        ):
            raise ValueError(f"{name}: work_item_required must be a boolean")
    return registry


def record_directories(root, registry):
    """Derive managed directories from the registered record path templates."""
    types = registry.get("types")
    if not isinstance(types, dict):
        raise ValueError("types must be an object")
    directories = set()
    for name, rule in types.items():
        pattern = rule.get("path") if isinstance(rule, dict) else None
        if (
            not isinstance(pattern, str)
            or not pattern
            or not pattern.endswith(".md")
        ):
            raise ValueError(
                f"{name}: path must be a relative Markdown path template"
            )
        parts = PurePosixPath(pattern).parts
        if PurePosixPath(pattern).is_absolute() or ".." in parts:
            raise ValueError(
                f"{name}: path must stay inside the canonical repository"
            )
        for _, field, spec, conversion in string.Formatter().parse(pattern):
            if field is not None and (
                field not in ("id", "work_item_id") or spec or conversion
            ):
                raise ValueError(f"{name}: unsupported path field {field!r}")
        prefix = []
        for part in parts[:-1]:
            if "{" in part or "}" in part:
                break
            prefix.append(part)
        directory = (root / Path(*prefix)).resolve()
        if not directory.is_relative_to(root):
            raise ValueError(
                f"{name}: record directory resolves outside the canonical repository"
            )
        directories.add(directory)
    return directories


def paths(root, registry=None, schema_path=None):
    root = Path(root).resolve()
    registry = schema(root, schema_path) if registry is None else registry
    found = set()
    for directory in record_directories(root, registry):
        if directory.exists():
            for path in directory.rglob("*.md"):
                if path.is_relative_to(BUNDLED_ROOT) or path.is_relative_to(
                    root / PROJECT_SCHEMA.parent
                ):
                    continue
                if not path.resolve().is_relative_to(root):
                    raise ValueError(
                        f"record resolves outside the canonical repository: {path}"
                    )
                found.add(path)
    yield from sorted(found)


def calendar(registry):
    zone_name = registry.get("timezone")
    weekday = registry.get("week_start")
    if not isinstance(zone_name, str) or not zone_name:
        raise ValueError("timezone must be an IANA timezone name")
    try:
        zone = ZoneInfo(zone_name)
    except (ValueError, ZoneInfoNotFoundError) as error:
        raise ValueError(f"invalid timezone {zone_name!r}") from error
    if not isinstance(weekday, str) or weekday.lower() not in WEEKDAYS:
        raise ValueError("week_start must be a weekday name")
    return zone, WEEKDAYS.index(weekday.lower())


def read_record(path):
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError("missing JSON-scalar front matter")
    parts = content.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("unclosed front matter")
    data = {}
    for line in parts[1].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator or not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise ValueError("invalid front matter line: " + line)
        if key in data:
            raise ValueError("duplicate metadata key: " + key)
        try:
            data[key] = json.loads(value.strip())
        except json.JSONDecodeError as error:
            raise ValueError(
                "metadata value must be a JSON scalar: " + key
            ) from error
        if isinstance(data[key], (dict, list)):
            raise ValueError("metadata value must be a JSON scalar: " + key)
    return data, parts[2]


def valid_date(value):
    try:
        dt.date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def timestamp(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo and parsed.utcoffset() is not None else None


def validate(root, schema_path=None):
    root = Path(root).resolve()
    selected_schema = resolve_schema(root, schema_path)
    errors = []
    try:
        registry = schema(root, selected_schema)
    except (OSError, ValueError) as error:
        return [f"{selected_schema}: {error}"]
    if not isinstance(registry.get("schema_version"), int):
        errors.append(f"{selected_schema}: invalid schema_version")
    types = registry.get("types", {})
    if not isinstance(types, dict):
        return errors + [f"{selected_schema}: types must be an object"]
    try:
        _, week_start = calendar(registry)
    except ValueError as error:
        errors.append(f"{selected_schema}: {error}")
        week_start = None
    for name, rule in types.items():
        if not isinstance(rule, dict):
            errors.append(f"{selected_schema}: invalid rule for {name}")
            continue
        for field in (
            "path",
            "template",
            "create_when",
            "required_sections",
            "lifecycles",
            "work_item_required",
        ):
            if field not in rule:
                errors.append(f"{selected_schema}: {name} missing {field}")
        template = rule.get("template")
        if isinstance(template, str):
            if template_path(root, template, selected_schema) is None:
                errors.append(
                    f"{selected_schema}: {name} missing template {template}"
                )
        else:
            errors.append(f"{selected_schema}: {name} missing template")
    seen = {}
    records = []
    try:
        record_paths = list(paths(root, registry))
    except ValueError as error:
        return errors + [f"{selected_schema}: {error}"]
    for path in record_paths:
        relative = path.relative_to(root).as_posix()
        try:
            data, body = read_record(path)
        except (OSError, ValueError) as error:
            errors.append(f"{relative}: {error}")
            continue
        records.append((relative, data, body))
        for field in COMMON_FIELDS:
            if field not in data or data[field] in ("", None):
                errors.append(f"{relative}: missing {field}")
        doc_type = data.get("type")
        rule = types.get(doc_type)
        if not isinstance(rule, dict):
            errors.append(f"{relative}: unregistered type {doc_type!r}")
            continue
        document_id = data.get("id")
        if not isinstance(document_id, str) or not DATE_PREFIX.fullmatch(
            document_id
        ):
            errors.append(f"{relative}: id requires YYYY-MM-DD-topic form")
            document_date = None
        else:
            document_date = document_id[:10]
            if not valid_date(document_date):
                errors.append(f"{relative}: invalid date {document_date}")
            if document_id in seen:
                errors.append(
                    f"{relative}: duplicate id {document_id} (first: {seen[document_id]})"
                )
            else:
                seen[document_id] = relative
        if data.get("schema_version") != registry.get("schema_version"):
            errors.append(
                f"{relative}: schema_version does not match manifest"
            )
        if data.get("lifecycle") not in rule.get("lifecycles", []):
            errors.append(
                f"{relative}: invalid lifecycle {data.get('lifecycle')!r}"
            )
        created, updated = timestamp(data.get("created_at")), timestamp(
            data.get("updated_at")
        )
        for field, value in (("created_at", created), ("updated_at", updated)):
            if value is None:
                errors.append(
                    f"{relative}: invalid {field}; use ISO 8601 with UTC offset"
                )
        if created and updated and created > updated:
            errors.append(f"{relative}: updated_at precedes created_at")
        work_item_id = data.get("work_item_id")
        if rule.get("work_item_required") and not work_item_id:
            errors.append(f"{relative}: missing work_item_id")
        if work_item_id is not None and (
            not isinstance(work_item_id, str)
            or not DATE_PREFIX.fullmatch(work_item_id)
        ):
            errors.append(f"{relative}: invalid work_item_id")
        if doc_type == "work-item":
            if "parent_work_item_id" not in data:
                errors.append(
                    f"{relative}: missing parent_work_item_id; use null for a root"
                )
            parent_id = data.get("parent_work_item_id")
            if parent_id is not None and (
                not isinstance(parent_id, str)
                or not DATE_PREFIX.fullmatch(parent_id)
                or not valid_date(parent_id[:10])
            ):
                errors.append(f"{relative}: invalid parent_work_item_id")
        for field in rule.get("required_fields", []):
            if not data.get(field):
                errors.append(f"{relative}: missing {field}")
        if isinstance(document_id, str):
            path_rule = rule.get("path")
            if isinstance(path_rule, str):
                expected = path_rule.format(
                    id=document_id, work_item_id=work_item_id
                )
                if relative != expected:
                    errors.append(f"{relative}: expected path {expected}")
            if doc_type in (
                "decision",
                "design",
                "plan",
                "tdd",
            ) and not document_id.endswith("-" + doc_type):
                errors.append(f"{relative}: id must end in -{doc_type}")
        heading = HEADING.search(body)
        if not heading or heading.group(1) != document_date:
            errors.append(f"{relative}: H1 must begin with the id date")
        present = set(SECTION.findall(body))
        for section in rule.get("required_sections", []):
            if section not in present:
                errors.append(f"{relative}: missing section {section}")
        if doc_type == "work-item" and "Timeline" in present:
            timeline = re.search(
                r"^## Timeline\s*\n(.*?)(?=^## |\Z)",
                body,
                re.MULTILINE | re.DOTALL,
            )
            content = timeline.group(1) if timeline else ""
            headings = re.findall(r"^### .+$", content, re.MULTILINE)
            events = list(EVENT.finditer(content))
            if not events:
                errors.append(f"{relative}: missing timeline event")
            if len(headings) != len(events) or any(
                timestamp(event.group(1)) is None for event in events
            ):
                errors.append(
                    f"{relative}: invalid timeline event; use ISO 8601 time — kind — actor"
                )
            times = [timestamp(event.group(1)) for event in events]
            if all(times) and times != sorted(times):
                errors.append(
                    f"{relative}: timeline events are out of time order"
                )
        for match in LINK.finditer(body):
            target = match.group(1).strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or target.startswith("#"):
                continue
            candidate = (
                root / unquote(parsed.path).lstrip("/")
                if parsed.path.startswith("/")
                else path.parent / unquote(parsed.path)
            ).resolve()
            if not candidate.is_relative_to(root) or not candidate.exists():
                errors.append(f"{relative}: broken link {target}")
        if doc_type == "weekly-report":
            start, end = data.get("period_start"), data.get("period_end")
            if not valid_date(start) or not valid_date(end):
                errors.append(f"{relative}: invalid weekly period")
            else:
                start_date, end_date = dt.date.fromisoformat(
                    start
                ), dt.date.fromisoformat(end)
                if (
                    (
                        week_start is not None
                        and start_date.weekday() != week_start
                    )
                    or end_date - start_date != dt.timedelta(days=7)
                    or document_date != start
                ):
                    errors.append(
                        f"{relative}: weekly period must span seven days from the configured week_start"
                    )
            if timestamp(data.get("as_of")) is None:
                errors.append(f"{relative}: invalid as_of")
    work_items = {
        data.get("id"): (relative, data)
        for relative, data, _ in records
        if data.get("type") == "work-item" and isinstance(data.get("id"), str)
    }
    for relative, data, _ in records:
        parent = data.get("work_item_id")
        if parent and parent not in work_items:
            errors.append(
                f"{relative}: orphan document; missing work-item {parent}"
            )
        if data.get("type") == "work-item":
            parent = data.get("parent_work_item_id")
            if isinstance(parent, str) and parent not in work_items:
                errors.append(f"{relative}: missing parent work-item {parent}")
    for document_id, (relative, _) in work_items.items():
        visited = set()
        current = document_id
        while current in work_items:
            if current in visited:
                errors.append(f"{relative}: work-item parent cycle")
                break
            visited.add(current)
            current = work_items[current][1].get("parent_work_item_id")
    return errors


def list_records(root, schema_path=None):
    root = Path(root).resolve()
    listed = []
    for path in paths(root, schema_path=schema_path):
        try:
            data, _ = read_record(path)
        except (OSError, ValueError):
            continue
        listed.append({"path": path.relative_to(root).as_posix(), **data})
    return sorted(
        listed,
        key=lambda record: (
            str(record.get("created_at", "")),
            str(record.get("id", "")),
        ),
    )


def work_tree(root, work_item_id=None, schema_path=None):
    records = list_records(root, schema_path)
    work_items = [
        record for record in records if record.get("type") == "work-item"
    ]
    nodes = {
        record["id"]: {
            "id": record["id"],
            "path": record["path"],
            "lifecycle": record.get("lifecycle"),
            "records": [],
            "children": [],
        }
        for record in work_items
        if isinstance(record.get("id"), str)
    }
    parents = {
        record["id"]: record.get("parent_work_item_id")
        for record in work_items
        if isinstance(record.get("id"), str)
    }
    for record in records:
        parent = record.get("work_item_id")
        if record.get("type") != "work-item" and parent in nodes:
            nodes[parent]["records"].append(
                {
                    key: record.get(key)
                    for key in ("id", "type", "path", "lifecycle")
                }
            )
    for node in nodes.values():
        node["records"].sort(key=lambda record: str(record["id"]))
    for document_id in nodes:
        visited = set()
        current = document_id
        while current is not None:
            if current in visited:
                raise ValueError(f"work-item parent cycle at {current}")
            visited.add(current)
            if current not in nodes:
                raise ValueError(f"missing parent work-item {current}")
            current = parents[current]
    roots = []
    for document_id, node in nodes.items():
        parent = parents[document_id]
        (nodes[parent]["children"] if parent else roots).append(node)

    def sort_children(node):
        node["children"].sort(key=lambda child: child["id"])
        for child in node["children"]:
            sort_children(child)

    roots.sort(key=lambda node: node["id"])
    for node in roots:
        sort_children(node)
    if work_item_id is not None:
        if work_item_id not in nodes:
            raise ValueError(f"unknown work-item {work_item_id}")
        return nodes[work_item_id]
    return roots


def weekly_events(root, week, schema_path=None):
    root = Path(root).resolve()
    registry = schema(root, schema_path)
    zone, week_start = calendar(registry)
    if not valid_date(week):
        raise ValueError("week must be a YYYY-MM-DD date")
    start_date = dt.date.fromisoformat(week)
    if start_date.weekday() != week_start:
        raise ValueError(f"week must start on {WEEKDAYS[week_start].title()}")
    start = dt.datetime.combine(start_date, dt.time.min, zone)
    end = start + dt.timedelta(days=7)
    events = []
    for path in paths(root, registry):
        try:
            data, body = read_record(path)
        except (OSError, ValueError):
            continue
        if data.get("type") != "work-item":
            continue
        timeline = re.search(
            r"^## Timeline\s*\n(.*?)(?=^## |\Z)",
            body,
            re.MULTILINE | re.DOTALL,
        )
        if not timeline:
            continue
        matches = list(EVENT.finditer(timeline.group(1)))
        for index, match in enumerate(matches):
            event_time = timestamp(match.group(1))
            if (
                event_time is None
                or not start <= event_time.astimezone(start.tzinfo) < end
            ):
                continue
            stop = (
                matches[index + 1].start()
                if index + 1 < len(matches)
                else len(timeline.group(1))
            )
            events.append(
                {
                    "timestamp": match.group(1),
                    "kind": match.group(2).strip(),
                    "actor": match.group(3).strip(),
                    "work_item_id": data.get("id"),
                    "path": path.relative_to(root).as_posix(),
                    "content": timeline.group(1)[match.end() : stop].strip(),
                }
            )
    return sorted(
        events,
        key=lambda event: (
            timestamp(event["timestamp"]),
            str(event["work_item_id"]),
        ),
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=("validate", "list", "tree", "events")
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Canonical record repository (default: current directory)",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        help="Custom schema JSON; otherwise use project config or bundled defaults",
    )
    parser.add_argument(
        "--format", choices=("json", "markdown"), default="json"
    )
    parser.add_argument("--lifecycle")
    parser.add_argument(
        "--week",
        help="Start date for events, YYYY-MM-DD using the manifest's week_start and timezone",
    )
    parser.add_argument(
        "--work-item", help="Root work-item ID for a tree view"
    )
    args = parser.parse_args(argv)
    if args.command == "validate":
        errors = validate(args.root, args.schema)
        for error in errors:
            print(error, file=sys.stderr)
        if errors:
            print(f"Validation failed; {len(errors)} errors")
        else:
            print(
                f"Validated {len(list_records(args.root, args.schema))} records; 0 errors"
            )
        return 1 if errors else 0
    if args.command == "events":
        if not args.week:
            parser.error("events requires --week")
        try:
            events = weekly_events(args.root, args.week, args.schema)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        if args.format == "json":
            print(json.dumps(events, indent=2, ensure_ascii=False))
        else:
            for event in events:
                print(
                    f"### {event['timestamp']} — {event['kind']} — {event['actor']}"
                )
                print(f"Source: {event['path']}\n\n{event['content']}\n")
        return 0
    if args.command == "tree":
        try:
            tree = work_tree(args.root, args.work_item, args.schema)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        if args.format == "json":
            print(json.dumps(tree, indent=2, ensure_ascii=False))
        else:

            def print_node(node, depth=0):
                print(
                    "  " * depth
                    + f"- [{node['id']}]({node['path']}) ({node['lifecycle']})"
                )
                for record in node["records"]:
                    print(
                        "  " * (depth + 1)
                        + f"- [{record['id']}]({record['path']}) ({record['type']}, {record['lifecycle']})"
                    )
                for child in node["children"]:
                    print_node(child, depth + 1)

            for node in tree if isinstance(tree, list) else [tree]:
                print_node(node)
        return 0
    try:
        records = list_records(args.root, args.schema)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if args.lifecycle:
        records = [
            record
            for record in records
            if record.get("lifecycle") == args.lifecycle
        ]
    if args.format == "json":
        print(json.dumps(records, indent=2, ensure_ascii=False))
    else:
        print("| ID | Type | Lifecycle | Updated | Path |")
        print("| --- | --- | --- | --- | --- |")
        for record in records:
            print(
                "| "
                + " | ".join(
                    str(record.get(key, ""))
                    for key in (
                        "id",
                        "type",
                        "lifecycle",
                        "updated_at",
                        "path",
                    )
                )
                + " |"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
