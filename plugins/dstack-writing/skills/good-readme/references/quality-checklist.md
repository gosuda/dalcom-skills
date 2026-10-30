# Quality checklist

Read the draft once, then work this list top to bottom. Skip an item only when the README claims no such surface (no badges means the badge item does not apply). Anything the README does claim must pass.

## Structure

- [ ] Opens with the project name and a one-line tagline.
- [ ] The title block holds an opening paragraph, a facts list, and a 4 to 10 line example with output.
- [ ] Sections follow the fixed order: title block, Install, Quick start, core sections, Development, License.
- [ ] Core sections match the archetype in `section-templates.md`.
- [ ] No top-level section appears before Install or after License.
- [ ] A table of contents follows the title block when the file runs past about two screens.

## Content

- [ ] The opening paragraph says what the project does, how the reader benefits, and what differs from alternatives.
- [ ] Every number and differentiator in the facts list comes from the repo, the user, or a measurement.
- [ ] Install is complete and correct for the project's actual package manager.
- [ ] Quick start commands are copy-pasteable and reach a working result from a clean machine.
- [ ] Usage describes what the reader can do, not how the code is built.
- [ ] Examples run against the current API and produce the output shown.
- [ ] Development names the contributing workflow or links to `CONTRIBUTING.md`.
- [ ] License names the license and links to its full text.

## Accuracy

- [ ] No command needs a tool that Install does not name.
- [ ] No hardcoded path contradicts the project layout.
- [ ] No version number contradicts the manifest.
- [ ] No claimed feature is missing from the project.

## Presentation

- [ ] Every badge is proven by project files and loads with its real value.
- [ ] No relative link or heading fragment is broken.
- [ ] Every code block names its language.
- [ ] Bold is limited to facts-list keywords and one or two must-not-miss lines.
- [ ] No paragraph is too dense to skim; lists replace them where they fit.
- [ ] Heading levels stay consistent through the file.
