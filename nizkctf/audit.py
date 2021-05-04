import requests
from hashlib import sha256
from base64 import b64decode
import pysodium

from .acceptedsubmissions import AcceptedSubmissions
from .challenge import Challenge
from .settings import Settings
from .repo import contents

# last milliseconds to remove from data, to cope with eventual consistency
TOLERANCE = 30*1000


def audit():
    contents.pull()

    r = requests.get(Settings.teams_url)
    r.raise_for_status()
    teams = r.json()

    r = requests.get(Settings.audit_url)
    r.raise_for_status()
    log = r.json()

    r = requests.get(Settings.score_url)
    r.raise_for_status()
    plat_score = AcceptedSubmissions(r.json())

    team_by_id = {}
    for team in teams:
        assert team['id'] == sha256(team['name'].encode('utf-8')).hexdigest()
        team_by_id[team['id']] = team['name']

    score = AcceptedSubmissions()
    for log_entry in log:
        chall = Challenge(log_entry['challengeId'])
        team_id = log_entry['teamId']
        proof = b64decode(log_entry['flag'])
        accepted_time = int(log_entry['moment'])

        team_name = team_by_id[team_id]

        open_proof = pysodium.crypto_sign_open(proof, chall['pk']).decode('utf-8')
        assert open_proof == team_id, 'Invalid proof for team {!r}, challenge {!r}'.format(
            team_name, chall.id)

        score.add(accepted_time, chall, team_name)

    score.remove_recent_solves(TOLERANCE)
    plat_score.remove_recent_solves(TOLERANCE)

    score.refresh()
    plat_score.refresh()

    assert score == plat_score, 'Wrong scoreboard!'

    return teams, log, score
