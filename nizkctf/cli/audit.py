import json
from ..audit import audit
from ..repo import trail


def write_trail(filename, data):
    with open(trail.get_path(filename), 'w') as f:
        f.write(json.dumps(data, sort_keys=True, indent=1))


def audit_record():
    teams, log, score = audit()
    write_trail('teams.json', teams)
    write_trail('log.json', log)
    write_trail('score.json', score)
    trail.add()
    trail.push(commit_message='Update audit trail')
