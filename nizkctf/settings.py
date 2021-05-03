API_URL = 'http://localhost:8080'

class Settings:
    contents_repo = "git@github.com:pwn2winctf/nizkctf-content.git"
    trail_repo = "git@github.com:pwn2winctf/nizkctf-audit-trail.git"

    teams_url = '{}/teams'.format(API_URL)
    audit_url = '{}/audit'.format(API_URL)
    score_url = '{}/score'.format(API_URL)

    max_size_chall_id = 30
    dynamic_scoring = {"K": 80.0, "V": 3.0, "minpts": 50, "maxpts": 500}
