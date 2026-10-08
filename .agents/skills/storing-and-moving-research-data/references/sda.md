# Scholarly Data Archive (SDA) in detail

Verified 2026-10-07 (KB0024053 only) against the IU Knowledge Base (KB).
Other sources were verified 2026-10-01. Read the main `SKILL.md` first. This file holds the command-level detail.

The SDA is a tape archive. Write a few large files, read them rarely, and
never treat a deletion as reversible (KB0024366, KB0024406).

## Check the account before writing

Check the live account rather than trusting the numbers below.

- Run `quota` on a supercomputer; it reports SDA usage where applicable
  (KB0024053, KB0022605).
- Inside `hsi`, run `du -ka` for the file count and bytes used
  (KB0026076).
- Run `cd <dir>` then `du -ka` inside `hsi` for one directory (KB0026076).
- Run `ls -U <file>` inside `hsi` to see a file's class of service
  (KB0024976).

## Choose an access method

| Method | Where it runs | Use it for | Source |
| --- | --- | --- | --- |
| HSI | Supercomputers after `module load hpss`; Linux workstations on campus | Scripted puts and gets, staging, checksums | KB0022463 |
| HTAR | Same as HSI | Writing a directory straight into a `.tar` on the SDA | KB0023281 |
| SFTP or SCP | Any host, `sftp.sdarchive.iu.edu`, Duo required | Off-campus access, PHI in transit, GUI clients | KB0022499, KB0024368 |
| Globus | `https://globus.iu.edu`, collection `IURT - Scholarly Data Archive` | Large or scheduled transfers, off-campus, PHI in transit | KB0025535, KB0024368 |

- HSI and HTAR are not allowed from off campus. Use Globus or SFTP instead
  (KB0022463, KB0024406).
- A local HSI or HTAR client must be version 10.3 (KB0022463).
- In RED, the SDA is under Applications > Storage > Scholarly Data Archive
  (KB0024406).
- The SDA is offline every Sunday, 7am to 10am (KB0024406).

## HSI

```bash
module load hpss
hsi                 # interactive; ? is the HSI prompt
? put results.tar   # checksums are computed by default at IU
? get results.tar
? stage -w big.tar  # copy from tape to disk cache and wait
? hashverify results.tar
? exit
```

- HSI commands resemble SFTP commands (KB0022463).
- Retrieval stages a file from tape to disk first. Pre-stage with `stage`, or
  `stage -w` to wait (KB0022483).
- Staged files can be evicted from cache under load, which adds delay
  (KB0022483).
- `put -c on`, `hashlist`, `hashcreate`, and `hashverify` manage checksums.
  The default algorithm is md5 (KB0023774).
- A failed `put` on a listed file may be a broken symbolic link. Try SFTP
  next, then email Research Storage (KB0025030).
- Behind a firewall, set `HPSS_PFTPC_PORT_RANGE` or open inbound traffic
  (KB0023364).

### Unattended scripts

Use a Kerberos keytab so a script never holds a plaintext password
(KB0024387). Set it with `hsi -A keytab -k <keytab> -l <username>`
(KB0022463). The same works through `~/.hsirc` or `HPSS_AUTH_METHOD`,
`HPSS_KEYTAB_PATH`, and `HPSS_PRINCIPAL` (KB0022463, KB0023281). Keep
`~/.hsirc` on the client host, never in the SDA home directory (KB0022463).
`hsi -A combo` is a common fix for authentication trouble (KB0022463).

### Set up a keytab

The person creates the keytab, because it needs their passphrase. An agent
never types it. With MIT Kerberos (KB0024956):

```text
$ ktutil
ktutil: addent -password -p <username>@ADS.IU.EDU -k 1 -e aes256-cts
Password for <username>@ADS.IU.EDU:
ktutil: wkt <username>.keytab
ktutil: quit
$ chmod 600 <username>.keytab
$ hsi -A keytab -k <username>.keytab -l <username> pwd
```

- Anyone who can read the keytab can use it. Restrict it to the owner
  (KB0024956).
- A passphrase change invalidates every keytab. Recreate them (KB0024956).
- `klist -k <keytab>` lists the keys in it (KB0024956).
- **Practice:** `ktutil` does not check the passphrase. A typo surfaces
  later as `Ticket expired on krb5_mk_req`. Delete the file and recreate it.
- **Practice:** `wkt` appends to an existing file. Delete an old keytab
  before writing a new one with the same name.
- **Practice:** test right away with the `hsi ... pwd` line above. An earlier
  interactive HSI session can hide a broken configuration.
- **Practice:** the startup file is `~/.hsirc`. A misnamed file is silently
  ignored.
- When the keytab's principal differs from the local login name, pass
  `-l <username>` or set `principal` in `~/.hsirc` (KB0022463).

### HSI errors

| Error | Likely cause | Fix |
| --- | --- | --- |
| `No credentials cache found` with `Not running interactively` | No keytab or Kerberos credentials, so non-interactive login fails | Set up a keytab, above. **Observed 2026-10-02** on Quartz |
| `Ticket expired on krb5_mk_req` | Keytab made with a wrong or old passphrase | Recreate the keytab (**Practice**) |
| Error `-50` on a host with several addresses or behind NAT | HSI advertises the wrong local address | `export HPSS_HOSTNAME=<host's reachable IP>` in the shell profile; setting it in `~/.hsirc` did not work (**Practice**) |
| Transfers hang behind a firewall | Data connections blocked | `HPSS_PFTPC_PORT_RANGE`, or open inbound traffic (KB0023364) |
| `Too many regions in file (-1420)` | A sparse file | Bundle it with `tar --sparse` first (**Practice**) |
| Other negative numbers | An HPSS error code | Look it up in the HPSS Error Manual, then email store-admin@iu.edu with the account, file sizes, commands, and log lines (**Practice**) |

### Check where a file is and that it arrived

- **Practice:** `ls -lU <file>` in HSI shows the class of service and whether
  a copy is on disk or only on tape. `ls -X <file>` shows each storage level.
  A level-0 line saying "no data at this level" means tape only; `stage` it
  before a large `get`.
- **Practice:** compare `hsi hashlist <file>` with `md5sum <file>` on the
  source. Matching sums prove the archive copy before you delete the source.

## HTAR

HTAR writes a `.tar` straight to the SDA and builds a `.idx` index beside it
(KB0023281).

```bash
module load hpss
htar -c -f archives/run42.tar run42          # create; relative path, no ~
htar -c -f new/dir/run42.tar -P run42         # -P creates missing SDA dirs
htar -tf archives/run42.tar                   # list members
htar -xvf archives/run42.tar run42/a.csv      # extract one member
htar -Xf old.tar                              # rebuild a missing index
```

- Never put `~` in the file list. The archive then stores absolute paths,
  and extraction nests them under the current directory (KB0023281).
- HTAR overwrites an existing archive of the same name without asking
  (KB0023281).
- HTAR extracts into the current directory. `cd` to the target first
  (KB0023281).
- Wildcards do not select archive members on extraction (KB0023281).

HTAR limits are stricter than the SDA's own (KB0023281, KB0024406):

| Limit | HTAR | SDA (HPSS) |
| --- | --- | --- |
| One file's size | 68 GB per member | 10 TB (KB0025237) |
| Directory path | 154 characters | 1,024 characters |
| File name | 99 characters | 256 characters |
| Files per archive | 1 million | Account file quota |

SDA names allow only ASCII 0x20 to 0x7e. Rename Unicode names before
transfer (KB0024406).

## SFTP and SCP

- Host: `sftp.sdarchive.iu.edu`. Duo is required (KB0022499).
- The home path is `/hpss/<first letter>/<second letter>/<username>`.
  Most clients show it with `/cos1` in front (KB0022499).
- If Duo prompts repeatedly, allow one connection at a time. Set timeouts to
  at least 120 seconds (KB0022499).
- In WinSCP, disable Endurance, or uploads report a permissions or timestamp
  error (KB0022499).
- To write into another class of service, change to the `/cosN` form of the
  path. An SFTP `symlink` makes this easy for later SCP use (KB0022499).

## Classes of service

The SDA picks a class by file size unless you set one first (KB0024976).

| COS | For | Copies | Optimal size | Maximum size |
| --- | --- | --- | --- | --- |
| 1 | Small files | 2 | 1 to 4 MB | 10 GB |
| 2 | Medium files | 2 | 4 to 64 MB | 40 GB |
| 3 | Large files | 2 | 64 MB to 1 TB | 10 TB |
| Ask Research Storage | Parallel large transfers | 2 | 500 GB to 50 TB | 50 TB |

- Piped data has no known size, so it lands in COS 1 (KB0024976).
- Use a dual-copy class for important files. COS 13 is single-copy, for
  data you can regenerate (KB0024976).
- Set the class before the transfer: `cos=N` in HSI, a `/cosN` path in SFTP,
  or `,,N` after a GridFTP target name (KB0024976).

## Many small files

The SDA performs badly with many small files. Individual files should be at
least 1 MB (KB0024406, KB0025838).

- Bundle a collection of 100 or more files into one or more archives
  (KB0025237).
- Split archives by how you will retrieve them later (KB0025237).
- Prefer HTAR when you will pull single files back, since its index avoids
  reading the whole archive (KB0025237).
- Do not use the SDA for files you retrieve one by one, often (KB0025237).
- Add a README with dates, origin, method, people, and grant numbers
  (KB0025237).
- Verify file counts and sizes after each transfer, or use HSI checksums
  (KB0025237).

### Recurring archive from a workstation

KB0025838 describes this pattern:

1. Make a local directory for archives.
2. Schedule a local job that tars a working directory into it.
3. In Globus, transfer that directory to `IURT - Scholarly Data Archive`.
4. Choose sync by checksum, delete files missing at the source, preserve
   modification times, skip errored files, and fail on quota errors.
5. Set a schedule and a repeat interval.

The transfer fails, with an email, if the workstation is asleep at run time
(KB0025838). Deletion on the source propagates to the SDA, where it is
permanent (KB0025838, KB0024366).

## Troubleshoot a connection

KB0024997 gives this order:

1. Check the local network and other websites.
2. Check Status.IU for an outage or maintenance.
3. Try the Globus web app.
4. Try HSI from a supercomputer.
5. If both fail, email store-admin@iu.edu.

## Sources

URL form: `https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.
KB0022463, KB0022483, KB0022499, KB0022605, KB0023281, KB0023364, KB0023774,
KB0024053, KB0024366, KB0024368, KB0024387, KB0024406, KB0024976, KB0024997,
KB0025030, KB0025237, KB0025535, KB0025838, KB0026076. Titles are in the
main `SKILL.md` Sources list, except
[KB0024956](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024956)
Use a keytab (read 2026-10-02).
