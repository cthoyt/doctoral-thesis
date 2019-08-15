import os
from typing import Any, Collection, Iterable, Optional, Tuple

import click
from git import Repo


def iterate_commits(directory: str, authors: Optional[Collection[str]]) -> Iterable[Tuple[str, str, Any]]:
    for subdirectory_name in os.listdir(directory):
        subdirectory = os.path.join(directory, subdirectory_name)
        if not os.path.isdir(subdirectory):
            continue
        for subsubdirectory_name in os.listdir(subdirectory):
            subsubdirectory = os.path.join(directory, subdirectory_name, subsubdirectory_name)
            if not os.path.isdir(subsubdirectory):
                continue
            if '.git' not in os.listdir(subsubdirectory):
                continue

            repo = Repo(subsubdirectory)
            branch = repo.active_branch
            for commit in repo.iter_commits(branch):
                if authors and commit.author.name not in authors:
                    continue

                yield (
                    subdirectory_name,
                    subsubdirectory_name,
                    commit,
                )


HEADER = [
    'category',
    'repository',
    'sha',
    'datetime',
    'author',
]


@click.command()
@click.option('-d', '--directory', default=os.path.join(os.path.expanduser('~'), 'dev'))
@click.option('-a', '--authors', multiple=True, default=['Charles Tapley Hoyt'])
@click.option('-o', '--output', default='commits.tsv', type=click.File('w'))
def main(directory, authors, output):
    print(*HEADER, sep='\t', file=output)
    for category, name, commit in iterate_commits(directory, authors):
        print(
            category,
            name,
            str(commit.hexsha)[:8],
            commit.committed_datetime.isoformat(),
            commit.author.name,
            sep='\t',
            file=output,
        )


if __name__ == '__main__':
    main()
