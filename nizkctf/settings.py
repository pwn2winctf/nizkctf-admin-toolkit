# -*- encoding: utf-8 -*-
class Settings:
    contents_repo = "git@github.com:pwn2winctf/nizkctf-content.git"
    trail_repo = "git@github.com:pwn2winctf/nizkctf-audit-trail.git"

    teams_url = 'http://localhost:8080/teams'
    audit_url = 'http://localhost:8080/audit'

    max_size_chall_id = 30
    dynamic_scoring = {"K": 80.0, "V": 3.0, "minpts": 50, "maxpts": 500}
