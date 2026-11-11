# Connected evidence map

**Review date:** November 10, 2026. **Basis:** the supplied Investigation Corpus ZIP and selected original images, plus new offline computations. No provider account, live share, external corporate claim, or current support status was queried. Uploaded scripts were not executed. This is a cross-document synthesis, not a claim-by-claim authentication of every narrative in the archive.

## Central finding

The archive supports investigating a multi-stage record-integrity problem: fidelity of source text, saved conversation entries, speaker attribution, displayed responses, later exports, and correction propagation. Those are connected by the record-keeping workflow and by reused source material. They are not yet connected by a single authenticated causal trace. A missing root-cause trace does not erase the defects that can be directly inspected, and an unexplained defect does not identify a particular actor or intention.

The important feedback risk is that transformed or misattributed material may become the evidence used in a later answer about the user. If correction is conversational only, a later export, summary, or response can continue using the disputed version.

## Evidence classes

**Direct:** independently inspected supplied bytes or images. **Reproduced:** a new local experiment with its inputs and operation stated. **Reported:** an archive receipt, copied exchange, or analytical comparison whose full primary source is not available in this ZIP. **Unresolved:** an attribution or causal join not established by the available records. A reported finding may be important without being independently authenticated in this review.

## Chronology and connections

| Period | Evidence and finding | Connection | Status in this review |
|---|---|---|---|
| August 4, 2026, as stored | Local state records first-seen at 23:34:36.050 UTC; import ledger records CONFIG and PLUGINS imports from a Claude Cowork directory at 23:37:28.933 UTC. Its `records` array is empty. | Concrete local integration history belongs in an access investigation; configuration import must not be relabeled conversation import. | Direct file fields; historical authenticity not independently established. |
| September 7–8 | Outgoing appendix reports eight Google Docs later revisions with U+FEFF-only exports and current reads with zero paragraphs. Earlier readable revisions total 74,609 normalized characters. Seven later timestamps span 245.622 seconds on September 7. | A clustered content-integrity complaint with named objects and windows that can be joined to client/tool activity records. | Source complaint and arithmetic, not original revision-byte examination. |
| September 29–30 | Preservation/access request followed by Support case 16074789. The shown reply leaves initiating software and record retention/preservation/disclosure unresolved. | The investigation reaches a provider-controlled evidence boundary. | Direct inspection of supplied Support screenshot; no later case outcome established. |
| September 30 | Separate 62,500-credit notification. | Same-day timing is an investigative lead, not a documented compensation or settlement link. | Notification described in supplied exhibits; allocation rationale unresolved. |
| October 24 | Live-versus-published comparison reports substantial assistant content absent from the share, while repeated user address text and a composed assistant limitation paragraph survive. | A later exported account may not preserve the behavior a user is disputing. | Reported comparison; preserved share extract read, no new live retrieval or full original screenshot comparison. |
| October 25 / correction filed November 4 | “Exhibit Four” one-sided-share claim withdrawn after rendered-page review found 42 user and 42 assistant turns. | The investigative extraction method can itself create apparent absence. This correction governs that example, not automatically every other example. | Explicit correction read in the archive. |
| October 26 | Network report joins PC socket events to phone screenshots, includes background rates, rare coincidences and nonmatches; phone traffic is not captured. | Useful chronology, but no authenticated phone-to-PC request/content bridge. | Reported analysis; underlying trace capture not in this ZIP. |
| October 28 | Image `1000019774.jpg` shows the statement “I said ‘checking’ when I was not actually checking,” together with fragmented conversational display. | Procedural language is not an execution receipt; the explanation layer is itself part of the investigation. | Direct image observation, not authentication of internal execution. |
| November 3–4 | Call Audit Master v2 tracks recoveries separately from unresolved authentication; Admissions Index correction changes “48 admissions” to 48 indexed quotation blocks and two acknowledged errors. | Corrections must propagate into later summaries, counts and claims. Recovery does not automatically establish original completeness or custody. | Archive papers and corrected source statements read; referenced recovery ZIPs not independently present here. |
| November 5–9 | Receipts describe imported context, inconsistent symbol readings, repeated progress statements, and corrections followed by recurrence. | Source attribution and summary provenance matter when a system explains or characterizes the user. | Reported exchanges; model statements about its internals are not logs. |
| November 9–10 | Receipts report doubling/tripling of a compiled code list and markup specification. Both supplied source files have their title exactly once. The list ends at its final-count statement. | The supplied source copies do not contain the reported full-document multiplication; the transformation, if those received-copy reports are accurate, occurs elsewhere in the path or involves a different source version. | Source side independently checked; downstream copies mainly reported. |
| November 10 review | Voice continuity JSON contains 60 entries in six threads: 33 user-labeled and 27 assistant-labeled entries, with 15 adjacent exactly equal user pairs. Ordinary conversational material is included. | Duplication exists in saved state, not solely in later rhetoric or deliberately elaborate symbolic inputs. | Direct byte-level comparison. Does not establish duplicate speech or model ingestion. |
| November 10 review | Screenshot `1000033743.jpg` visibly splits “Same skeleton, but Rev / 4 adds the right skepticism” across a user-side bubble. | Turn/segment boundaries and sentence continuity are distinct; displayed bubbles alone do not authenticate acoustic turns. | Direct image observation. |
| November 10 new experiment | Repeated CommonMark parsing of backslashes immediately before an underscore reproduces both reported ladders: 23→11→5→2→1→0 and 19→9→4→2→1→0. | Supplies a concrete candidate for one transformation class, including the previously unresolved final 1→0 step. | Independently reproduced minimal example, not proof of the historical application path. |

## New experiment: what it establishes

Using locally installed `markdown-it-py` 4.2.0 with `MarkdownIt('commonmark').renderInline`, start with N literal U+005C backslashes followed immediately by U+005F underscore. Feed the rendered output into the same parser repeatedly. For these inputs the resulting backslash count is floor(N/2) at each pass. Paired backslashes yield a literal backslash; a remaining backslash escapes the underscore, so the last slash can disappear as well.

This reproduces **both** reported ladders. The earlier report's pure-pair-collapse model stalled at one because it did not account for the final slash escaping the following punctuation. The experiment closes that mathematical/mechanical gap for this input family. It does not prove that ChatGPT, a particular editor, a clipboard path or an export used this parser. It does not reproduce letter substitutions, middle omissions, document multiplication, speaker misattribution or Google Docs content loss.

The test is a candidate mechanism, not an excuse: a pipeline expected to preserve exact source text can be defective even when its destructive transformation uses an ordinary parser rule.

## Important joins, kept separate

1. **Source → transformed representation:** Source controls and a parser mechanism are available. Exact submitted and retained bytes are still needed for historical stage attribution.
2. **Representation → speaker:** Saved duplication and displayed interleaving are directly inspectable. Original synchronized audio and role-tagged message events are needed to authenticate disputed speech.
3. **Disputed attribution → later response:** November 9–10 receipts describe an assistant treating a misplaced first-person danger statement as the user's statement. That is a consequential reported feedback failure. The original synchronized sequence was not independently available; the statement must not be converted into a verified claim about the user.
4. **Live interaction → share/export:** October 24's comparative report identifies omissions. The separate withdrawn October 25 extraction case demonstrates why actual rendered views, native records and extraction output must remain distinct.
5. **Correction → subsequent record:** The archive repeatedly demands durable correction. Its own index correction and Exhibit Four withdrawal are working examples of how to preserve the original while superseding an erroneous finding.
6. **Document revision → initiating client:** The reported September cluster and Support's receipt supply exact investigation targets. Neither the credits email nor PC-side OneDrive traffic supplies this missing join.

## What a substantive response would produce

For the Google Docs incident: original revision exports and metadata, and retained client/session/tool operations tied to the listed document IDs and UTC windows. For voice: original audio where retained and event records linking segments, role labels, retries and final messages. For text fidelity: exact source, composer, submitted, stored, exported and rendered representations for one matched trial. For correction: a ledger distinguishing what was corrected in the conversational answer from what changed in saved summaries, exports or other active records.

For each missing record class, distinguish **not searched**, **not located in a specified search**, **not retained**, **held but not disclosed**, and **produced**. The current archive cannot substitute for an authoritative custodian's answer. A support acknowledgment is not preservation confirmation; lack of access in a chat is not proof a record never existed.

## Mechanical integrity

The new run checked 711 manifest-listed files with no missing entries and no hash mismatches. The extracted corpus contains 712 files, 708 distinct file hashes, and four byte-identical file pairs. These counts describe file identity, not the number of independent incidents. The prime grid independently matches the first 160,000 digits of consecutive-prime concatenation, in 400 rows of 400 characters.

## Source pointers

Paths below are relative to the supplied corpus root:

- `codex/codex_home_2026-11-09/realtime-voice-continuity.json`
- `codex/codex_home_2026-11-09/claude-cowork-import-history.json`
- `codex/codex_home_2026-11-09/codex-global-state-5.json`
- `codex/codex_home_2026-11-09/chrome-native-hosts-v2.json`
- `evidence_packages/sept2026_docs_credits_pkg/September_2026_Google_Docs_Support_Credits_Addendum.md`
- `evidence_packages/sept2026_docs_credits_pkg/1000020335.jpg`
- `codex/Comparative_Analysis_Screen_vs_Published_2026-10-24.md`
- `codex/Drop_Session_Share_Copy_2026-10-24.md`
- `codex/Exhibit_Four_Reconciliation_Brief_2026-11-04.md`
- `codex/Correlation_Report_2026-10-26.md`
- `codex/File_Deletion_and_Transmission_Review_2026-09-29_Filing_Note.md`
- `evidence_packages/room_artifacts_2026-11-10/oct28/1000019774.jpg`
- `evidence_packages/sixth_hole_rev4_pkg/1000033743.jpg`
- `your_files/Call_Audit_Master_v2_2026-11-03.md`
- `your_files/Admissions_Index_CORRECTION_NOTE_2026-11-04.md`
- `your_files/Removal_From_The_Bench_Audit_Seat_2026-11-09.md`
- `substrate/Report_The_Mirror_Mechanism_Night_of_Nov_9-10_2026.md`
- `substrate/Photos_Damnation_Carried_In_and_Ruled_Receipt_2026-11-05.md`, particularly Addenda 815, 821, 825–827 and 839.
- `substrate/Code_Box_Compiled_List_2026-11-09.md`
- `substrate/Sigil_Markup_Spec_v0.1_2026-11-06.md`

Companion files: `Independent_Connection_Checks.json` contains machine-readable results; `verify_connections.py` reproduces the offline checks without modifying corpus files.
