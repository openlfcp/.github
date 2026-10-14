# MVP 0.2 pilot — install guide (draft)

**Status:** DRAFT (LFCP-02-103), not in use. Written for people who do not
write code. Take it slowly; there is nothing to break if you follow the
steps. `<…>` marks a value the owner settles.

> **Before you start.** This is early MVP software. **Keep a copy of your
> vault, or use a test vault.** Once Shared Tasks 0.4 starts the first time,
> that device cannot go back to the old 0.3.x version (your notes are safe;
> only the plugin's own sync data changes). Don't use it yet for anything
> you can't afford to lose.

You need Obsidian **1.13.4 or later** on a **desktop** (macOS, Windows or
Linux). On phones and tablets sections are read-only.

## 1. Install Shared Tasks

1. Open **Settings → Community plugins**.
2. If community plugins are off, turn them on (**Turn on community
   plugins**).
3. Click **Browse**, search for **Shared Tasks**, **Install**, then
   **Enable** it.

If you already have Shared Tasks 0.3.x, click **Check for updates** in
**Settings → Community plugins** and update it instead.

## 2. Check your version

- In **Settings → Community plugins**, find **Shared Tasks**. It should read
  **`0.4.0`** (or a later 0.4.x).
- Write this version down — it is your **build ID** for the feedback form.
- If you installed it earlier through BRAT, remove `openlfcp/obsidian` from
  BRAT's beta plugin list so that Obsidian's own updates apply.

Your identity, collaborations and settings are kept across updates. The
plugin uses the project server `sync.openlfcp.org`.

## 3. Your first share and invite

1. Open a note with a heading and a few tasks under it (use the synthetic
   example from the facilitator, not private notes).
2. Put the cursor **on the heading, or just under it**.
3. Run **"Share section…"**. A preview shows exactly what will be shared and
   what stays private. Confirm.
4. Run **"Invite collaborator…"** (also in the section's details) to get a
   **one-time link**. Send it to your partner the way you agreed.
   - The link is a secret: don't post it anywhere public, and don't include
     it in feedback.

Your partner then runs **"Join collaboration"** with the link, and
**"Insert shared section…"** in a note of their own.

## 4. What the marks mean

- A **double tick ✓✓** after a shared heading means **"shared"**. It turns
  green when the section is current. ✓✓ does **not** mean the other person
  has seen your change.
- A **separate icon** next to it shows **sync progress**. Hover to read it:

  | You see | It means |
  | --- | --- |
  | (no icon) | Everything is sent and accepted |
  | Saved locally; waiting to sync | Safe on your device, not sent yet |
  | Sending local updates | On its way to the server |
  | Offline; local updates will wait | No connection; your edits are kept |
  | Needs your attention | Open the details and make a choice |

- Click the icon, or run **"Open shared section details"**, to see the
  status, what is shared, and **who has access**.

## 5. If a section needs attention

Open **"Open shared section details"** and read what it says. For a
disagreement (a conflict), use **"Review conflicts…"** and answer the
question. For a damaged section, run **"Repair shared sections in this
note"**. Nothing is thrown away while you decide, and your note keeps your
text.

## 6. Sending a diagnostics report

If something goes wrong and the facilitator asks for details:

1. Run **"Export diagnostics…"**.
2. **Read the report** — it is shown to you in full first. It contains **no
   note text, names, paths, keys or invitation links**.
3. Copy it or save it as a file and send it **only if you choose to**,
   **privately to the facilitator**. Never post it in Discussions or
   anywhere public.

## 7. Getting help

- Ask in [GitHub Discussions of the openlfcp
  organization](https://github.com/orgs/openlfcp/discussions), category
  **Pilot**. Don't post invitation links, note text or diagnostics there.
- Your facilitator: **`<…>`**.
- Ask whenever you are stuck — needing help is useful information for the
  pilot, not a failure.

Thank you. Your plain-language feedback is exactly what this pilot is for.
