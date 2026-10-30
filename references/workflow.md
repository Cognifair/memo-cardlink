# Markji single-direction and bidirectional reference workflow

Use this procedure for one-way navigation, bidirectional hub-and-spoke links, links among corresponding cards in several decks, repairs to incorrect `Card` references, and post-change audits.

## 1. Establish scope and authorization

Extract the exact decks, cards, link labels, insertion locations, and directions requested by the user. Do not infer permission to create, move, rename, reorder, or edit other cards.

An explicit request to implement links authorizes those directions and card edits, including resolving IDs and choosing an ordinary insertion location. Show a precise preview; do not ask again for already-authorized work. Ask only when unresolved ambiguity or additional scope needs a user decision. An audit request authorizes reads only. Select modes using SKILL.md and record each requested directed edge separately.

Keep secrets only in process memory or the approved credential mechanism. Never print a full token in logs or responses. If the user pastes one, do not repeat it.

## 2. Resolve decks and cards

Use the official MaiMemo OpenAPI; verify current authentication, pagination, and update rules against the current official reference. The endpoints and checks in this workflow are the local fallback, not a substitute for a changed official contract.

1. Paginate deck listings until the exact requested deck names and IDs are resolved; do not assume the first page is complete.
2. Traverse the relevant chapters and cards to find the hub/library card and each corresponding target card.
3. Match with evidence from titles and body text, not position alone. If multiple cards plausibly match, stop and show the candidates.
4. Record for every participating card: deck ID, actual `card_id`, stable `root_id`, current body, current `grammar_version`, and relevant chapter context.
5. Resolve every `root_id` already present in affected `Card` references when determining whether a link is correct, stale, or duplicated.

Never substitute a `card_id` for a `root_id` inside card grammar. Never use a `root_id` as the card identifier in an update URL.

## 3. Build an exact mutation manifest

Prepare one row per card containing:

- mode and directed edges (A → B or A → B plus B → A);
- owning deck ID and actual card ID;
- expected latest version or equivalent concurrency field, when exposed;
- exact old fragment or insertion anchor;
- exact new fragment;
- references expected after the edit;
- references required to disappear;
- unchanged `grammar_version`.

For A → B, only A is a write target and its reference uses B's stable root ID. Read B to validate it; do not add or remove links in B. For A ↔ B, each endpoint uses the other card's stable root ID. If one endpoint is already correct, only write the missing endpoint. Preserve requested display text exactly. Removing a pre-existing reverse edge requires an explicit removal request. Validate and edit each occurrence by its intended anchor; unrelated valid references elsewhere are preserved.

Before writing, require each replacement or insertion anchor to occur exactly once. Reject the manifest if:

- an anchor is absent or occurs more than once;
- a requested edge is duplicated at its intended anchor and deduplication has not been authorized;
- an existing reference cannot be assigned to a target unambiguously;
- the edit would alter unrelated text, images, formatting, or card grammar;
- an expected referenced root cannot be resolved to a real card.

An already-correct single reference is a no-op, not an error. Do not add a second copy.

## 4. Refresh and apply safely

Immediately before each update, read the card again and compare it with the manifest's source body and concurrency metadata. Recompute the narrow edit against the fresh body. If the anchor, version, or surrounding content changed in a way that invalidates the manifest, stop that write and report the conflict.

Update only designated existing cards through the official endpoint (verify this against the current API reference before use):

`POST /markji/decks/{deck_id}/cards/{card_id}`

Send the current API-required fields and preserve `grammar_version` exactly. Do not normalize whitespace, rewrite the whole card from a stale snapshot, or alter unrelated syntax. Apply writes in an order that remains easy to audit, and stop on an unexpected API response before proceeding blindly.

For a two-card or batch operation, do not assume atomicity. If a later write fails, stop and report which directed edges succeeded and which remain pending. Do not blindly roll back newer content. On an authorized retry, refresh and re-plan, keeping already-correct edges as no-ops. Follow current API rate limits; after an uncertain write result, read back before retrying.

## 5. Read back and audit every changed card

Fetch every written card from the API again. Validate the returned body, not merely the update response.

Check all of the following:

- every expected `[Card#ID/<root_id>#<label>]` occurs exactly once at the intended location;
- every old or incorrect reference designated for removal is absent;
- no unexpected, missing, or duplicate reference was introduced by this operation; unrelated existing references remain unchanged;
- returned `card_rids` agrees with the root IDs referenced in the body, accounting only for documented API behavior;
- every referenced root resolves to an existing card;
- every requested directed edge resolves to its intended target; require reciprocal edges only for bidirectional mode, never for single-direction mode;
- original text, images, formatting, and unrelated grammar remain byte-for-byte unchanged outside the narrow edits;
- `grammar_version` remains unchanged;
- bracketed structures are balanced, nesting is legal, and no placeholder, diff marker, tool output, or visible source residue was introduced.

If the API exposes version information, confirm the final versions are the ones produced by this operation. Treat any mismatch as an incomplete verification, not success.

## 6. Render in the real client when possible

Open each changed card in the Markji client and inspect the structural area affected by the edit. Confirm labels and surrounding content render normally and raw grammar such as `[Card#`, `[T#`, or unmatched delimiters is not visible.

Attempt each requested navigation direction only when the client exposes an actionable link. The Markji web editor may render card references without performing cross-card navigation. In that case, report rendering as verified and clickable navigation as unverified; never claim a click succeeded based only on visible styling.

## 7. Final report

Report concisely:

- the number and identity of changed cards, without secrets;
- which directed edges passed API read-back, distinguishing one-way links from completed bidirectional pairs;
- whether `card_rids`, grammar, and preservation checks passed;
- what was rendered in the client;
- which link clicks, if any, were actually exercised;
- any conflict, ambiguity, no-op, or validation limitation.

Do not expose raw authorization headers, full tokens, or unrelated card content.
