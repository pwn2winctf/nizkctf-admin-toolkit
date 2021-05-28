from .scoring import compute_points
from .challenge import Challenge


class AcceptedSubmissions(dict):
    def __init__(self, other=None):
        super(AcceptedSubmissions, self).__init__()
        self.setdefault('tasks', [])
        self.setdefault('standings', [])
        if other:
            self.update(other)

    def get_team_standing(self, team_name):
        for team_standing in self['standings']:
            if team_standing['team'] == team_name:
                return team_standing

        team_standing = {'team': team_name,
                         'taskStats': {},
                         'score': 0}
        self['standings'].append(team_standing)
        return team_standing

    def get_solves(self, chall_id):
        solves = set()
        for team_standing in self['standings']:
            if chall_id in team_standing['taskStats']:
                solves.add(team_standing['team'])
        return solves

    def compute_points(self, chall, additional_solves=0):
        num_solves = len(self.get_solves(chall.id)) + additional_solves
        return compute_points(chall, num_solves)

    def recompute_score(self, chall):
        points = self.compute_points(chall)
        chall_id = chall.id
        # update affected team's standings
        for team_standing in self['standings']:
            task_stats = team_standing['taskStats']
            if chall_id in task_stats:
                task_stats[chall_id]['points'] = points
                team_standing['score'] = sum(task['points']
                                             for task in task_stats.values())

    def rank(self):
        standings = self['standings']
        for standing in standings:
            standing['lastAccept'] = max(task['time']
                                         for task in standing['taskStats'].values())
        standings.sort(key=lambda standing: (standing['score'],
                                             -standing['lastAccept']),
                       reverse=True)
        for i, standing in enumerate(standings):
            standing['pos'] = i + 1

    def update_tasks(self):
        tasks = set()
        for standing in self['standings']:
            tasks.update(standing['taskStats'].keys())
        self['tasks'] = sorted(tasks)

    def add(self, accepted_time, chall, team_name, refresh=False):
        chall_id = chall.id

        if chall_id not in self['tasks']:
            self['tasks'].append(chall_id)

        team_standing = self.get_team_standing(team_name)

        if chall_id in team_standing['taskStats']:
            # Challenge already submitted by team
            return

        team_standing['taskStats'][chall_id] = {'points': 0,
                                                'time': accepted_time}
        team_standing['lastAccept'] = accepted_time

        if refresh:
            self.recompute_score(chall)
            self.rank()

    def refresh(self):
        self.update_tasks()
        for chall_id in self['tasks']:
            self.recompute_score(Challenge(chall_id))
        self.rank()

    def remove_since(self, cut_at):
        standings = []
        for standing in self['standings']:
            standing['taskStats'] = {chall_id: task_info
                                     for chall_id, task_info in standing['taskStats'].items()
                                     if task_info['time'] <= cut_at}
            if not standing['taskStats']:
                continue
            standing['lastAccept'] = max(task_info['time']
                                         for task_info in standing['taskStats'].values())
            standings.append(standing)
        self['standings'] = standings
