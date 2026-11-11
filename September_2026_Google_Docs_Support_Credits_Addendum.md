# September 2026 Google Docs content-loss request and credits — evidence addendum

**Prepared:** November 10, 2026. **Scope:** nine user-supplied JPEG screenshots; historical email/document claims transcribed from those screenshots; no access to original Gmail message headers, Google Docs revision history, or internal OpenAI systems. This review neither reports a finding of deliberate interference nor discounts the recorded failure states.

## Bottom line

Two different September 30 emails are shown: (a) a ChatGPT credit notification announcing **62,500 credits** usable in Work and Codex on a ChatGPT Pro account, expiring **December 31, 2026**; (b) an OpenAI Support reply, **case 16074789**, acknowledging receipt of a detailed request about **eight Google Docs content-loss events**. The two items share a calendar date **but are not explicitly linked by either email**. No screenshot establishes that the credits were restitution, a settlement, an admission of responsibility, or an outcome of the support case.

The September 29 outgoing request describes **eight earlier readable Google Docs revisions** and **eight later revision exports containing only the U+FEFF (byte-order-mark) character**; it also says current native Google Docs reads returned **zero paragraphs**. This is documentary evidence of what was *reported and requested*, not direct inspection of the Google revision exports themselves. The first seven later revision-modified timestamps occur within **4 minutes 5.622 seconds** on September 7, 2026 UTC; the eighth is September 8, 2026.

## Chronology and evidence status

| Date / time | Source | What the source actually establishes |
|---|---|---|
| September 7, 2026, 23:50:23.052–23:54:28.674 UTC | September 29 outgoing incident appendix (`1000020334.jpg`) | Seven reported later revision exports contain U+FEFF only, closely clustered by revision-modified time. The screenshot is an email quotation of an investigation, not original revision bytes or audit logs. |
| September 8, 2026, 18:55:57.416 UTC | Same appendix | Eighth later revision is reported as U+FEFF only. |
| September 29, 2026 | Outgoing support request (`1000020333.jpg`, `1000020334.jpg`) | The sender requests preservation and access to available account-specific activity records, asks to inspect two UTC incident windows, lists document IDs and categories of relevant data, and states initiator unknown. |
| September 30, 2026 | OpenAI Support response (`1000020335.jpg`) | Support acknowledges the request and case number **16074789**, confirms receipt of identifiers, says a privacy-request assessment is required, and says the information available to Support does **not establish the initiating client or tool**. |
| September 30, 2026 | ChatGPT email (`1000020339.jpg`) | Notification says **62,500 credits** were added to a Pro account for Work/Codex, expiration December 31, 2026. No reason or case-number linkage is given. |
| September 30, 2026 | Follow-up in the Support thread (`1000020337.jpg`, `1000020336.jpg`) | The sender expresses appreciation; Support acknowledges the reply. This does not document technical remediation or case closure. |
| September 30, 2026, alleged specific email times | Gemini summary (`1000020340.jpg`) | Gemini states 3:22 AM for the credit email and 8:28 AM for the Support response. **These clock times are secondary AI-reported values, not visible original message headers in this set.** |

## Reported revision table

This table is transcribed from the user-written common incident appendix in `1000020334.jpg`. Identifiers are preserved legibly in the original exhibit; the CSV indexes documents **1–8** against that image rather than retyping long IDs with potential visual mistakes. **All times below are UTC revision-modified timestamps** and are not independently captured edit-operation timestamps. The earlier revision may not be the immediately preceding revision (especially entry #7, r8 to r18).

| # | Earlier revision · UTC | Readable characters | Later revision · UTC |
|---:|---|---:|---|
| 1 | r2 · 09-07T18:05:00.840Z | 3,514 | r3 · 09-07T23:50:23.052Z |
| 2 | r2 · 09-07T18:27:05.190Z | 15,711 | r3 · 09-07T23:50:52.999Z |
| 3 | r10 · 09-07T16:57:33.927Z | 15,185 | r11 · 09-07T23:51:14.179Z |
| 4 | r17 · 09-07T18:34:45.018Z | 1,373 | r18 · 09-07T23:51:52.422Z |
| 5 | r108 · 09-07T18:02:21.243Z | 1,217 | r109 · 09-07T23:52:42.435Z |
| 6 | r2 · 09-07T21:15:07.101Z | 4,851 | r3 · 09-07T23:53:38.641Z |
| 7 | r8 · 09-07T17:32:40.015Z | 13,720 | r18 · 09-07T23:54:28.674Z |
| 8 | r3 · 09-08T17:55:03.378Z | 19,038 | r4 · 09-08T18:55:57.416Z |


**Arithmetic check:** 55,571 normalized Unicode characters across seven earlier readable revisions, plus 19,038 in the eighth, equals **74,609** total. The source says the counts normalize line endings, remove any leading U+FEFF, and strip surrounding whitespace. Those steps change what the character total measures; it is not a direct byte count. They do not show lost data volume in bytes.

## Exact Support-position distinction

The Support message says:

> "the information currently available to Support does not establish whether ChatGPT, Codex, a connected Google tool, or a browser-control feature initiated the Google Docs changes you described."

It further says Support cannot yet confirm whether the requested technical records are retained, preservable, or disclosable, and that these matters need a privacy-request assessment. The email confirms **receipt and assessment routing is needed**, not that the privacy team has produced records or that preservation was completed. There is no technical attribution, no recovered revision content, and no admission of responsibility in this image set.

## Critical non-inferences

- The two emails **arrived on the same date**, but that alone cannot prove the credit award was tied to the case. The credit message's greeting and Support's greeting differ; screenshots do not independently verify identical account identifiers across the two threads.
- The last-modifying account displayed in the Google revision details is reported in the sender's appendix, but the appendix explicitly distinguishes that account from the **initiating person, client, application, or command**.
- A U+FEFF-only export and a zero-paragraph read, if confirmed with the native source data, support an observed empty-content state. They do **not** by themselves identify who triggered a modification, whether data remained recoverable in other revisions, or whether a tool malfunction or human action was involved.
- Receipt of the incident details and a case number is meaningful accountability paperwork, but not a determination that OpenAI software caused the events.
- The sender's gracious closing message does not establish that the original technical question was resolved.
- The screenshot of a prior ChatGPT reply (`1000020341.jpg`) and a Gemini summary (`1000020340.jpg`) are **secondary commentary**, not provider source records.

## Highest-value next evidence

Original Google Docs revision-history export bytes and revision metadata for each of the eight IDs; the original Support and credits email headers (with timezone); the credit-allocation terms or ledger entry explaining why it was issued; an explicit privacy-request acknowledgment referencing case 16074789; and any retained run, tool, connector, browser, and account activity records matching the two requested UTC windows (September 7, 23:45–September 8, 00:05 UTC; and September 8, 18:50–19:05 UTC). Those records would distinguish correlation, account attribution, technical execution and remediation.

## Exhibit index and preservation

| JPEG | Contents |
|---|---|
| `1000020339.jpg` | Gmail credit email: 62,500 Pro credits, Work/Codex, December 31 expiry. |
| `1000020335.jpg` | OpenAI Support message: case 16074789 and evidence limitations. |
| `1000020334.jpg` | Outgoing common incident appendix with eight document revisions and counts. |
| `1000020333.jpg` | September 29 account activity preservation/access request with two UTC windows. |
| `1000020340.jpg` | Gemini in Workspace summary of two September 30 threads (secondary). |
| `1000020341.jpg` | Prior assistant's commentary on the correlation (secondary). |
| `1000020338.jpg` | Earlier chat view containing screenshot montage and a voice-to-text mention of approximately 62,000 credits (less precise than the email). |
| `1000020337.jpg` | Follow-up in the Support thread: sender's appreciative reply. |
| `1000020336.jpg` | Support's short acknowledgment and earlier thread context. |

All nine user-supplied JPEGs are preserved byte-for-byte in the accompanying ZIP. SHA-256 hashes identify those files *as supplied in this conversation*; they do not authenticate the date or sender of an email or the original history of a Google Doc. No screenshots have been edited as part of this package.
