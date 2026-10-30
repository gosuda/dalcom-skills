# Show the available tasks.
default:
    @just --list

# Regenerate every generated file: skill manifests, plugin manifests, registries, skill index, and the doctrine cascade.
render:
    node scripts/render-skill-manifests.mjs
    node scripts/sync-knowledge-copies.mjs
    node scripts/render-plugin-surfaces.mjs
    node scripts/render-skill-index.mjs
    python3 scripts/sync-baseline.py || [ $? -eq 1 ]

# Mirror every skill into the outline repository as a flat Devin skill tree.
sync-outline:
    node scripts/sync-outline-skills.mjs

# Run every gate over the whole tree.
check:
    prek run --all-files

# Validate every skill against the Agent Skills specification with the GitHub CLI.
validate-skills:
    gh skill publish --dry-run

# Everything a change must pass before it is committed.
verify: check validate-skills

sync-carriers:
    python3 scripts/sync-carriers.py

sync-carriers-check:
    python3 scripts/sync-carriers.py --check
