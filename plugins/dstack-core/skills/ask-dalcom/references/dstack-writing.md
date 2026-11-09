# DStack Writing

DStack workflows for documentation, editorial prose, and copy. Install it with `claude plugin install dstack-writing@dstack` in Claude Code or `codex plugin add dstack-writing@dstack` in Codex; Claude Code invokes its skills as `/dstack-writing:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- A README or a project's public face: `/skill:good-readme`, then dstack-marketing `/skill:developer-discovery-surfaces` and `/skill:developer-docs-led-growth`, then core `/skill:unslop` before the pull request.
- Documentation: `/skill:docs-writing` for Diataxis types, `/skill:good-readme`, `/skill:docs-update` (user only) when docs drifted from code, `/skill:rewrite-clean-v0` for a document that reads as sediment, `/skill:reorder` for a drifted listing. Product copy: `/skill:copywriting`.
- Plain language by language: English `/skill:humanizer-plain-english` or `/skill:humanizer-simple-english-asd-ste100`, Korean `/skill:humanizer-korean-plain` or `/skill:humanizer-korean-ste`, French `/skill:humaniseur-fr`. The author runs core `/skill:unslop` first, then a humanizer.
- Finding the words at all: `/skill:articulate` (user only). Rhythm: `/skill:rhythmic-taste` (user only). Collaborative documents: `/skill:proof`.
