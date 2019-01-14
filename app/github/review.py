import re

from ..models import Commit, Entity

from typing import List

url_repo_extractor = re.compile(r'https://github\.com/([^/]+)/([^/]+)/.*')

def get_commits(client, username) -> List[Commit]:
    commits = client.search_commits(
            'author:{} author-date:2018-01-01..2018-12-31'.format(username),
            sort='author-date',
            order='desc'
    )

    commit_response: List[Commit] = []
    for c in commits:
        m = url_repo_extractor.match(c.commit.html_url)
        if not m:
            continue
        owner = m.group(1)
        repo_name = m.group(2)
        if ('github.io' in repo_name):
            continue
        commit_response.append(Commit(
                url=c.commit.html_url,
                message=c.commit.message,
                repo=owner + '/' + repo_name,
                lines_added=c.stats.additions,
                lines_deleted=c.stats.deletions
        ))
    return commit_response

def get_issues(client, username) -> List[Entity]:
    issues = client.search_issues(
            'author:{} created:2018-01-01..2018-12-31'.format(username),
            sort='created',
            order='desc'
    )

    issue_response: List[Entity] = []
    for issue in issues:
        m = url_repo_extractor.match(issue.html_url)
        if not m:
            continue
        owner = m.group(1)
        repo_name = m.group(2)
        issue_response.append(Entity(
                url=issue.html_url,
                message=issue.title,
                repo=owner + '/' + repo_name
        ))

    return issue_response
