# Restore test: sync.openlfcp.org

**Status:** DRAFT, for the project owner (LAUNCH-003 (b)). Run it after
server `0.3.0` is deployed.

This page checks that a restore of the public server's store from a backup
does not stall collaborations: clients re-supply what the server lost
(spec `adr/0008-recovery-after-server-data-loss.md`, "Vectors and tests").
The backup and restore themselves follow the stack runbook,
`devbox-asstnt: stacks/openlfcp/README.md`, sections "Backup" and
"Восстановить". This page does not repeat them.

## Before you start

- **Server:** `0.3.0` on the box. Check it with
  `lfcp-admin status` over the SSH tunnel: its `version` field. The
  server log level must be `info` (the default) to see the lines below.
- **Clients:** `lfcp-todo` built from `openlfcp/examples` at a commit that
  pins sdk-ts `0.1.2` (the W0 release). An older `lfcp-todo` does not
  re-supply lost units, and case 1 then stays refused (see "If it fails").
- **Homes:** three local homes, `./a`, `./b` and `./c`, each with its own
  Principal (`lfcp-todo --home ./a principal create`, and so on). Use only
  test data: the collaborations below are throwaway.
- **Time:** about 30 minutes. Users of the public server see one short
  restart per case. Announce it, as for any restore (stack runbook).

`E=wss://sync.openlfcp.org/v1/ws` below.

## Case 1: the writer comes back first

The writer's next unit names a unit the server lost. The server refuses it
(`UNKNOWN_PREVIOUS`); the writer re-uploads the lost unit, and then the
new one.

1. A creates and hosts a collaboration, writes three tasks, invites B:

   ```sh
   lfcp-todo --home ./a resource create "Restore test 1" --endpoint "$E"
   lfcp-todo --home ./a resource host
   lfcp-todo --home ./a task add "one"
   lfcp-todo --home ./a task add "two"
   lfcp-todo --home ./a task add "three"
   lfcp-todo --home ./a sync
   lfcp-todo --home ./a invite create          # prints a SECRET link
   lfcp-todo --home ./b invite accept '<link>'
   lfcp-todo --home ./b task list              # one, two, three
   ```

2. Take a backup (stack runbook, "Backup"). Note its time T.
3. A writes a fourth task and syncs; B fetches it:

   ```sh
   lfcp-todo --home ./a task add "four"
   lfcp-todo --home ./a sync                   # acknowledged by the server
   lfcp-todo --home ./b sync
   lfcp-todo --home ./b task list              # one … four
   ```

4. Restore the backup of step 2 (stack runbook, "Восстановить").
5. A writes a fifth task first:

   ```sh
   lfcp-todo --home ./a task add "five"
   lfcp-todo --home ./a sync
   ```

6. **Expected:**
   - `sync` succeeds. The server log shows a
     `DATA_PUT with an unknown previous` line for A's unit 5; A then
     uploads unit 4 and unit 5, and both are accepted;
   - `lfcp-todo --home ./b sync` and `task list` show one … five, with no
     "no progress";
   - C joins with a new invitation from A and lists one … five.

## Case 2: the writer stays away

Another member re-supplies the writer's lost unit (relay).

1. Repeat case 1, steps 1–4, with "Restore test 2". Do not use `./a` after
   the restore.
2. B syncs first: `lfcp-todo --home ./b sync`. B holds A's unit 4 and
   uploads it.
3. **Expected:** a new member C, invited by B before the backup or by A
   later, lists one … four without A ever connecting. When A comes back and
   syncs, nothing is refused and everyone lists A's later tasks.

   B can invite only if it holds `invite/claim`; if it does not, invite C
   in step 1, before the backup, and let C join after the restore.

## Case 3: the collaboration was hosted after the backup

The server lost the whole Resource. A client that saw it hosted re-hosts it
with its Genesis and re-uploads the rest.

1. Take a backup.
2. A creates, hosts and fills "Restore test 3", and B joins (as in case 1,
   step 1).
3. Restore the backup of step 1.
4. `lfcp-todo --home ./a sync`.
5. **Expected:** `sync` succeeds: A re-hosts the collaboration, then
   uploads its Control Records, units and Key Packages. B syncs and lists
   every task. The server log shows a `hosted` line for the Resource, and
   `hosted_resources` in `lfcp-admin status` counts it again.

## Record the result

Write the date, the server and client versions, the backup used and each
case's result into:
- the stack runbook's rehearsal record (`devbox-asstnt:
  stacks/openlfcp/README.md`);
- LAUNCH-003 (b) in [BACKLOG-MVP-0.1.md](../BACKLOG-MVP-0.1.md).

## If it fails

- **Unit 5 stays refused in case 1:** A runs an `lfcp-todo` without the
  0.1.2 reconciliation. Check its version. Any 0.1.2 member's sync (case 2)
  unblocks it.
- **B reports "no progress":** the server accepted a unit over a lost
  predecessor, so the server is not 0.3.0. Check the deployed image.
- **A sync of case 3 fails with `HOSTING_DENIED`:** the server's hosting
  policy does not let A host. Check `lfcp-admin hosting get`; in quota
  mode, A's quota.
- **A `CONTROL_CONFLICT`:** a member proposed a Control Record before the
  lost one came back (for example an invitation created right after the
  restore). This is the known limitation of server 0.3.0; abandon that
  test collaboration.

Keep the server logs of the test window until the result is recorded.
