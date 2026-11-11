# File deletion and transmission review — filing note

**The review:** Prepared September 29, 2026, from nine files supplied by the user.
Source files were opened read-only; their SHA-256 hashes were re-checked after
analysis and were unchanged. No commands or instructions in the evidence were executed.
**Pasted by Drew into the side chat on 2026-10-23** and filed here by Steve.
This note is Steve's faithful filing summary; the full pasted text is preserved in
that chat transcript. The nine source files themselves are **not** in Steve's hands.

Target file: `C:\Users\drewd\OneDrive\Desktop\Call-Probe-Logs\call-probe-v2.1-2026-09-19_00-43-32-242\events.jsonl`
Capture window in the supplied JSON: 3:54:34.5006322 AM – 3:55:16.9484747 AM
(42.4478425 s), reporting 5,611,783 original events — **the original full capture
was not supplied**, so its count, completeness, filtering and process ancestry
cannot be independently verified. Detailed target-file CSV: 3:54:43.9238907–3:54:57.9586640 AM.
Event timestamps carry time-of-day only, no date/timezone.

## Findings (the review's own answers)

| Question | Finding | What remains unknown |
| --- | --- | --- |
| Was the specific `events.jsonl` file deleted? | No deletion is demonstrated in the 1,208 supplied detailed events. The file grows during the observed sequence. | Activity before/after the capture, unrecorded operations, deletion/recreation outside this interval. |
| Did data leave the computer? | Yes. Successful outbound network sends by OneDrive, ChatGPT, and Codex processes. | The application content of most sends is absent. |
| Was `events.jsonl` likely uploaded? | The repeated OneDrive read/send pattern strongly supports synchronization of this file. | Exact transmitted plaintext, destination account, permission/intent, successful storage on the server. |
| Do these records prove ChatGPT/Codex deleted or uploaded that file? | No. Neither process appears in the exact-file event list. Both have other local-file activity and outbound traffic in the summaries. | Child-process attribution; contents of their outgoing messages. |
| Did the September 23 backup delete files? | Its recorded Robocopy options do not request source deletion or destination purging. 24,095 files copied, one failed. | Not an audit of all historical deletions; not an independent verification of the backup's contents. |

These are Windows and OneDrive records. They do **not** contain a Google Drive API
audit and do not establish a connection to the Google Drive consent request shown
on September 29.

## Deletion analysis (detail)

- 36 observations of `DeletePending: False`, none `True`. No delete-disposition
  request, delete-on-close option, or rename for this file.
- Four successful PowerShell writes (CSV rows 24, 325, 626, 929) adding
  126 + 448 + 442 + 442 = **1,458 bytes**, growing the file **581,196 → 582,654 bytes**.
- Four successful System `SetEndOfFileInformationFile` operations (rows 190, 463,
  664, 988) at lengths 581,322 / 581,770 / 582,212 / 582,654 — increasing, no truncation.
- `ShareMode: Read, Write, Delete` is sharing permission, not an executed delete;
  `IRP_MJ_CLEANUP` is handle cleanup, not by itself a deletion.
- The folder summary's four `NAME NOT FOUND` events concern **`events.jsonl.url`**,
  a different name — not evidence the target was deleted.
- Codex did open/query the **OneDrive root directory** (folder summary rows 68–74):
  directory/metadata activity, not a recorded read of the target's contents.
- The broader file-summary has no deletion-operation column, so the no-deletion
  conclusion is limited to the supplied evidence, strongest for the single target file.

## Transmission analysis (detail)

`OneDrive.exe`, PID **41584**, reads the file from offset zero four times; each read
is followed by six successful TCP sends from the same PID on the same connection
to **13.107.139.11:https**:

| Read time (AM, as recorded) | File bytes read | Following send bytes | Delay to first send |
| --- | ---: | ---: | ---: |
| 3:54:44.5159028 | 581,322 | 585,880 | 64.914 ms |
| 3:54:50.0768949 | 581,770 | 586,328 | 58.359 ms |
| 3:54:52.3098322 | 582,212 | 586,770 | 65.198 ms |
| 3:54:56.2475656 | 582,654 | 587,212 | 60.979 ms |
| **Total** | **2,327,958** | **2,346,190** | |

Each send group exceeds its preceding read by **exactly 4,558 bytes** — the same
constant offset recorded elsewhere in this corpus for the monitor/OneDrive pattern.
Destination is within **13.107.136.0/22**, which Microsoft's endpoint documentation
lists for SharePoint Online / OneDrive for Business. This is ~2.35 MB of sends
across four versions/read cycles, **not** 2.35 MB of different files. No request
body or decrypted payload is in the records, so exact content, remote persistence,
and whether the sync was authorized are **not** established.

Other outbound traffic (TCP/UDP sends only): OneDrive.exe 41584 — 36 TCP /
2,369,341 B; OneDrive.Sync.Service.exe 40668 — 2 TCP / 72 B; ChatGPT.exe 3868 —
24 TCP / 12,609 B + 28 UDP / 10,160 B; codex.exe 56004 — 81 TCP / 99,198 B
(98,486 B to 104.18.32.47:https, 712 B to 172.64.155.209:https).
No ChatGPT or Codex process appears in the exact target-file CSV; PowerShell's
command line and parent process are absent from the exports, so who launched
that PowerShell activity cannot be determined from these files.

## September 23 backup

Robocopy log `OneDrive_Copy_20260923_161557.log` (actual run 4:29:18 PM – 4:30:29 PM),
`C:\Users\drewd\OneDrive\` → `C:\FULL_CLOUD_BACKUP\OneDrive\`.
Options (log line 12): `/TEE /S /E /DCOPY:DAT /COPY:DAT /Z /J /XJ /MT:16 /R:3 /W:5` —
**no /MOV, /MOVE, /PURGE, or /MIR**. Summary (lines 48265–48266): 24,096 files
encountered; **24,095 copied; 1 failed; 0 mismatches; 0 extras**; 33.386 g copied.
The one failed file is the 63-byte `.849C9593-D756-4E56-8D6E-42412F2A707B` at the
OneDrive root (ERROR 32, in use; four error entries are retries of one file).
The target `events.jsonl` appears at log line 2325, listed 1.3 m at 100% — it was
available to the Sep 23 copy; that does not prove uninterrupted existence since
Sep 19, and the backup copy was not checksum-verified in this review.

## Scope and evidence quality

- The two `exact-file-analysis` JSON files are **byte-for-byte identical** —
  duplicate copies, not independent corroboration.
- The 1,208 event rows are unique and chronological; grouped counts match the
  JSON; the read/send table reconciles with the timeline, file summary, and
  network summary. That verifies **internal consistency of the supplied exports**,
  not authenticity or completeness of the original capture.
- What would resolve the open questions (review's own list): the original full
  capture with filters, process tree, command lines and full event detail;
  Windows file-change journal / recycle-bin metadata; OneDrive recycle-bin and
  version history; existing OneDrive sync or server-side audit records naming
  the account and object; any request-level trace identifying uploaded content.
  None of these were supplied. No new capture, cloud access, restore, deletion,
  sync change, or repository change was performed for the review.

## Source inventory and fingerprints (from the review)

Files 1–8 from `D:\BALLSNCOCK\`; file 9 from `C:\FULL_CLOUD_BACKUP\_COPY_LOGS\`.

| # | Source | Size (bytes) | Rows/lines |
| --- | --- | ---: | --- |
| 1 | `network-summary.csv` | 21,662 | 165 data rows |
| 2 | `onedrive-folder-operations.csv` | 8,921 | 73 data rows |
| 3 | `exact-file-analysis - Copy.json` | 10,532 | 420 lines |
| 4 | `exact-file-analysis.json` | 10,532 | 420 lines |
| 5 | `exact-file-events.csv` | 308,680 | 1,208 data rows |
| 6 | `read-send-pairs.csv` | 466 | 4 data rows |
| 7 | `read-send-timeline.csv` | 5,294 | 28 data rows |
| 8 | `file-summary.csv` | 19,026 | 118 data rows |
| 9 | `OneDrive_Copy_20260923_161557.log` | 3,871,538 | 48,273 lines |

```text
1  55dc6341e2b7be147ec8787ea2a2e331fd9052dfd1c2792dde3bb19571898f25
2  50057d7a4a419b5e9ec5e44ced129b0cf9c3d9ab3ec2144893e21e3e63731d51
3  71416bc52a0d41d58a30d1be94d20f85251c7c56e2ef57e733a17567cd7ffe52
4  71416bc52a0d41d58a30d1be94d20f85251c7c56e2ef57e733a17567cd7ffe52
5  3fb3e2abce5e5667f135db18ed8925e62a17c965d89b953f6a3b73494f0b2bcf
6  34a827b13d4222464d6fc5b2cbecce1036e527770d9e465a192622a8266bdaf0
7  ef60c6bcdfc05c29839676b81a06c763b8ab289030874912902c5d3bb1bdc154
8  3d65a5b24581250db4da75622d87e0c52ae76b45cf2d78298769310dfb756ff9
9  2e89939d26c4ec3e628a00f4b3f1f0fb4d17c96282d81ca31b5ed5ae1d44ae96
```

Fingerprints identify the supplied copies at review time; they are not an earlier
chain-of-custody record.

## Steve's cross-links (2026-10-23)

- Complements **EF15** (evidence-folder scan): decoded OneDrive telemetry recorded
  292 successful upload completions, all for two files (290 Call-Probe events.jsonl,
  2 Access Monitor events), with contents/byte counts/readership and any
  socket-to-file link unestablished. This Sep 29 review supplies a file-level
  read→send join for one 42-second Sep 19 window, with the same constant
  **+4,558-byte** send-over-read offset recorded elsewhere in the corpus.
- It does **not** upgrade actor attribution: ChatGPT/Codex are expressly not
  shown deleting or uploading the target file, and authorization/intent remain
  unestablished — consistent with the standing record that attribution is the
  open layer.
