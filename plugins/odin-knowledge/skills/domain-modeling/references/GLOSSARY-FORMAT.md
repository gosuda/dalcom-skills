# GLOSSARY.md format

## Entry format

```markdown
# Context name

One or two sentences defining the context and why it exists.

## Language

**Order**:
A request from a customer to provide specific goods or services.
_Avoid_: Purchase, transaction

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Pick one word.** Be opinionated. Put rejected synonyms on the `_Avoid_` line.
- **Keep definitions tight.** Use one or two sentences. Define what the term is, not what it does.
- **Keep the glossary domain-specific.** Include only terms from this project's domain. Exclude general programming concepts.
- **Group terms when clusters emerge.** Add subheadings for natural groups. Keep a flat list when every term belongs to one area.

## Recording resolutions

- Write the entry the moment a term resolves; never batch entries for later.
- Every entry has exactly three parts: canonical term, definition, `_Avoid_` synonyms.
- When a use contradicts an entry, surface both meanings and record the ruling before overwriting the entry.

## Single context

Most repositories keep one shared glossary at the root:

```markdown
# Storefront

The customer-facing ordering context: what can be bought and how orders are taken.

## Language

**Order**:
A request from a customer to provide specific goods or services.
_Avoid_: Purchase, transaction
```

## Bounded contexts

When the repository holds several contexts, keep a root map plus one glossary beside each context source:

```markdown
# Glossary map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): receives and tracks customer orders
- [Billing](./src/billing/GLOSSARY.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/GLOSSARY.md): manages warehouse picking and shipping

## Relationships

- **Ordering -> Fulfillment**: Ordering emits `OrderPlaced`; Fulfillment consumes it to start picking.
- **Fulfillment -> Billing**: Fulfillment emits `ShipmentDispatched`; Billing consumes it to create an invoice.
- **Ordering <-> Billing**: Both contexts use the `CustomerId` and `Money` domain types.
```

A project that already keeps a `GLOSSARY.md` beside a context source keeps that file in place; the map points at it. Never invent a second scheme alongside the detected one.
