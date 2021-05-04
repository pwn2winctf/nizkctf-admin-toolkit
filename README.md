# NIZKCTF admin toolkit

This repository contains a set of tools which are useful for CTF admins and for people wishing to audit the CTF scoreboard.

## Setup

We recommend setting up a virtualenv:

```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Make sure your current user has a SSH key and your key is registered to a GitHub account, otherwise cloning the git repositories will fail. Run:

```bash
./ctf init
```


## Auditing the scoreboard

Run:

```bash
./ctf audit
```

If anything fails the audit, it will return an AssertionError.

If everything is fine, it will print `OK`.


## Verifying the audit trail

We record a signed and timestamped version of the audit trail at the [nizkctf-audit-trail](https://github.com/pwn2winctf/nizkctf-audit-trail) repository.

### Optional: support for timestamps

Timestamps are recorded to the Bitcoin blockchain using [OpenTimestamps](https://github.com/opentimestamps). If you want to check them, install it as follows:

```bash
pip install opentimestamps-client
curl -o .venv/bin/ots-git-gpg-wrapper.sh https://raw.githubusercontent.com/opentimestamps/opentimestamps-client/master/ots-git-gpg-wrapper.sh
chmod +x .venv/bin/ots-git-gpg-wrapper.sh
cd trail
git config commit.gpgsign true
git config gpg.program ots-git-gpg-wrapper.sh
```

### Verifying commits

```bash
cd trail
git log --show-signature
```


## Tools for CTF admins

 * `./ctf audit --record` to audit *and* record results to the audit trail repository.
 * `./ctf add_chall` to add challenges.
 * `./ctf publish_chall` to publish challenges.
 * `./ctf add_news` to add news.

