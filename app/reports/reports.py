from collections import defaultdict
from datetime import date
from dataclasses import asdict

from .. import github
from ..models import RepoLanguages, RepoStats

from typing import List, Set

COMMIT_WEIGHT = 0.7
ISSUE_WEIGHT = 0.2
STAR_WEIGHT = 0.1

def build_report(client):
    user = client.get_user()
    response = {}
    owned_repos = []

    rps = user.get_repos()
    owned_repo_names = set()
    first_repo_created_at = None
    first_repo_name = None
    for rp in rps:
        if rp.fork:
            continue
        if not first_repo_created_at or rp.created_at < first_repo_created_at:
            first_repo_created_at = rp.created_at
            first_repo_name = rp.full_name
        updated_at = rp.updated_at.date()
        if updated_at < date(2018, 1, 1) or updated_at > date(2018, 12, 31):
            continue
        owned_repos.append(RepoStats(
            repo=rp.full_name,
            languages=rp.get_languages(),
            created_at=rp.created_at,
            stars=rp.stargazers_count,
            forks=rp.forks,
            score=rp.stargazers_count + rp.forks * 2 + rp.watchers_count * 0.2
        ))
        owned_repo_names.add(rp.full_name)
    owned_repos.sort(key=lambda r: r.score, reverse=True)
    starred_repos = user.get_starred()

    commits = github.get_commits(client, user.login)
    issues = github.get_issues(client, user.login)

    all_repo_languages: Set[RepoLanguages] = set(owned_repos)
    contributed_repo_full_names: List[str] = [ent.repo for ent in commits + issues]
    for repo_name in contributed_repo_full_names:
        repo = client.get_repo(repo_name, lazy=True)
        all_repo_languages.add(RepoLanguages(repo_name, repo.get_languages()))

    language_weight_by_repo = {r.repo: r.language_scores for r in all_repo_languages}
    language_sores = defaultdict(int)
    total_lines_in_commits = sum(c.total for c in commits)
    commits_by_repo = defaultdict(lambda: defaultdict(int))
    total_lines_committed = 0
    for c in commits:
        commits_by_repo[c.repo]['count'] += 1
        commits_by_repo[c.repo]['lines_added'] += c.lines_added
        commits_by_repo[c.repo]['lines_deleted'] += c.lines_deleted
        total_lines_committed += c.total
        language_weights = language_weight_by_repo[c.repo] or {}
        num_lines_weight = c.total / total_lines_in_commits
        for lang, lang_weight_in_repo in language_weights.items():
            language_sores[lang] += num_lines_weight * lang_weight_in_repo * COMMIT_WEIGHT
    issues_by_repo = defaultdict(list)
    total_issues = 0
    for issue in issues:
        issues_by_repo[issue.repo].append(issue)
        total_issues += 1
    for repo, issues in issues_by_repo.items():
        language_weights = language_weight_by_repo[c.repo] or {}
        for lang, lang_weight_in_repo in language_weights.items():
            language_sores[lang] += len(issues) / len(issues) * lang_weight_in_repo * ISSUE_WEIGHT

    for starred_repo in starred_repos:
        langs = starred_repo.get_languages()
        total_bytes = sum(langs.values())
        for lang, num_bytes in langs.items():
            language_sores[lang] += 1 / starred_repos.totalCount * num_bytes / total_bytes * STAR_WEIGHT
    response['issues'] = { k: [asdict(vv) for vv in v] for k, v in issues_by_repo.items() }
    response['total_issues'] = total_issues
    response['total_commits'] = len(commits)
    response['total_lines_committed'] = total_lines_committed
    response['language_scores'] = sorted(
            language_sores.items(),
            key=lambda x: x[1],
            reverse=True
    )
    response['most_liked_repo'] = asdict(owned_repos[0]) if owned_repos else None

    fav, fav_not_owned = get_fav_repo(contributed_repo_full_names, owned_repo_names, commits_by_repo, issues_by_repo)
    response['favorite_repo'] = fav
    response['favorite_3p_repo'] = fav_not_owned

    response['first_repo_name'] = first_repo_name
    
    user_dict = {}
    response['user'] = user_dict
    user_dict['login'] = user.login
    user_dict['name'] = user.name
    user_dict['days_since'] = (date(2019, 1, 1) - user.created_at.date()).days
    if first_repo_created_at:
        user_dict['days_since_first_repo'] = (date(2019, 1, 1) - first_repo_created_at.date()).days
    return response

def get_fav_repo(all_repo_names, owned_repos, commits_by_repo, issues_by_repo):
    scores_by_repo = defaultdict(float)
    for repo in all_repo_names:
        if repo in commits_by_repo:
            scores_by_repo[repo] += commits_by_repo[repo]['count']
        if repo in issues_by_repo:
            scores_by_repo[repo] += len(issues_by_repo[repo]) * 0.5
    repo_scores = sorted(scores_by_repo.items(), key=lambda x: x[1], reverse=True)
    fav = None
    fav_not_owned = None

    def gen_output(repo):
        issues = issues_by_repo.get(repo, [])
        return {
            'repo': repo,
            'commits': commits_by_repo[repo]['count'] if repo in commits_by_repo else 0,
            'issues': len([entity.type == 'Issue' for entity in issues]),
            'prs': len([entity.type == 'PR' for entity in issues]),
        }

    for repo, _ in repo_scores:
        if not fav:
            fav = gen_output(repo)
        if repo not in owned_repos:
            if not fav_not_owned:
                fav_not_owned = gen_output(repo)
        if fav and fav_not_owned:
            break
    return fav, fav_not_owned