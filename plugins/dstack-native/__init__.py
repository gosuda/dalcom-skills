import json
from pathlib import Path


def _scalar(raw):
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return json.loads(value)
    return value


def _description(skill_md):
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    for line in text[4:end].splitlines():
        key, separator, raw = line.partition(":")
        if separator and key == "description":
            return _scalar(raw)
    return ""


def register(ctx):
    skills = Path(__file__).parent / "skills"
    for child in sorted(skills.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.is_file():
            ctx.register_skill(child.name, skill_md, _description(skill_md))
