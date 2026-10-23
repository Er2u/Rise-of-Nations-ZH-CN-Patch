"""Build an unpublished local Workshop candidate, never install or upload it."""
import argparse
from pathlib import Path
import zipfile
from build import payload
from validate import ROOT, validate


def build_workshop(output, root=ROOT):
    _, errors = validate(root)
    if errors:
        raise ValueError('\n'.join(errors))
    files = {name: path for name, path in payload(root).items()
             if not name.startswith('launcher_res/')}
    with zipfile.ZipFile(output, 'x', zipfile.ZIP_DEFLATED) as archive:
        for name, path in sorted(files.items()):
            archive.write(path, 'RON_zhCN_Compatibility/' + name)
        # Keep preparation notes outside the actual upload directory.
        archive.write(root / 'WORKSHOP.zh-CN.md', 'READ-BEFORE-PUBLISH.zh-CN.md')
    return len(files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    print(f'{build_workshop(args.output)} local candidate files; unpublished, font distribution unresolved')
