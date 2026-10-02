# Mounting research storage on a workstation

Verified 2026-10-01 against the IU Knowledge Base (KB). Read the main
`SKILL.md` first.

Slate, Slate-Scratch, Slate-Project, and Geode-Project can be mounted over
SMB. Off campus, connect to the IU VPN first (KB0025689, KB0025090).

Never put PHI on a workstation unless it has full-disk encryption and prior
written approval from a senior executive officer or the IRB (KB0025689,
KB0025090).

## Before you mount

- SMB access to Slate and Slate-Scratch is on for everyone (KB0025689).
- Slate-Project SMB access is off by default. The project owner asks HPFS to
  enable it (KB0025689).
- Geode-Project needs the owner to grant your ADS account access first. No
  supercomputer account is needed (KB0025090).
- With read-only Slate-Project access, append `-ro` to the share name
  (KB0025689).

## Share paths

| Space | Windows | macOS and Linux GUI | Source |
| --- | --- | --- | --- |
| Slate | `\\slate-smb.uits.iu.edu\slate` | `smb://slate-smb.uits.iu.edu/slate` | KB0025689 |
| Slate-Project | `\\slate-project-smb.uits.iu.edu\<project>` | `smb://slate-project-smb.uits.iu.edu/<project>` | KB0025689 |
| Slate-Scratch | `\\slate-scratch-smb.uits.iu.edu\scratch` | `smb://slate-scratch-smb.uits.iu.edu/scratch` | KB0025689 |
| Geode-Project | `\\geode-projects.rs.iu.edu\<project>` | `smb://geode-projects.rs.iu.edu/<project>` | KB0025090 |

Log in with the IU username and passphrase (KB0025689). For Geode-Project,
prefix the username with `ads\` (KB0025090).

## Linux command line

Run as root, with an empty mount point (KB0025689, KB0025090).

```bash
# Slate (KB0025689)
mount.cifs //slate-smb.uits.iu.edu/slate /mnt/slate \
  -o username=<username>,uid=<local_user>,domainauto

# Slate-Project (KB0025689); use <project>-ro for read-only access
mount.cifs //slate-project-smb.uits.iu.edu/<project> /mnt/proj \
  -o username=<username>,uid=<local_user>,domainauto

# Geode-Project (KB0025090)
mount.cifs //geode-projects.rs.iu.edu/<project> /mnt/geode \
  -o user=<username>,uid=<local_user>,sec=ntlmv2,domain=ads
```

Check the result with `findmnt /mnt/slate` or `df -h /mnt/slate`. These are
standard Linux commands, not KB instructions.

## Sources

URL form: `https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.
KB0025090, KB0025689. Titles are in the main `SKILL.md` Sources list.
