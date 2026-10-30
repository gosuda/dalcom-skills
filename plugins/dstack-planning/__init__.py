from pathlib import Path

SKILLS = Path(__file__).resolve().parent / "skills"


def _scalar(raw):
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
    return value


def _frontmatter(text):
    lines = text.lstrip("\ufeff").split("\n")
    if not lines or lines[0].rstrip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.rstrip() == "---":
            return fields
        key, separator, value = line.partition(":")
        if separator and key and key == key.strip() and key.replace("-", "_").isidentifier():
            fields[key] = _scalar(value)
    return {}


def register(ctx):
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        fields = _frontmatter(skill_md.read_text(encoding="utf-8"))
        ctx.register_skill(skill_md.parent.name, skill_md, fields.get("description", ""), fields)
