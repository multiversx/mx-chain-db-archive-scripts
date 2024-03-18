import shutil
import subprocess
import tarfile
from argparse import ArgumentParser
from pathlib import Path
from typing import List

from constants import SHARDS


def main():
    """
    python3 ./archive_py/gcp_rsync_static.py \
        --archives-folder ~/deep-history-archives \
        --workspace-folder ~/deep-history-archives-static-workspace \
        --gcp-bucket-url gs://multiversx-deep-history-archives-mainnet \
        --gcp-project multiversx-deep-history
    """
    parser = ArgumentParser()
    parser.add_argument("--archives-folder", required=True)
    parser.add_argument("--workspace-folder", required=True)
    parser.add_argument("--gcp-bucket-url", required=True)
    parser.add_argument("--gcp-project", required=True)
    args = parser.parse_args()

    archives_folder = Path(args.archives_folder).expanduser()
    workspace_folder = Path(args.workspace_folder).expanduser()
    gcp_bucket_url = args.gcp_bucket_url
    gcp_project = args.gcp_project

    print("Archives folder:", archives_folder)
    print("Workspace folder:", workspace_folder)
    print("GCP bucket URL:", gcp_bucket_url)
    print("GCP project:", gcp_project)

    print("Extracting Static archives...")

    for shard in SHARDS:
        static_archive_path = archives_folder / f"shard-{shard}" / f"Static.tar"
        static_output_folder = workspace_folder / f"shard-{shard}"

        shutil.rmtree(static_output_folder, ignore_errors=True)
        static_output_folder.mkdir(parents=True, exist_ok=True)

        print("Extracting for shard", shard, "...")

        tar = tarfile.open(static_archive_path, "r")
        tar.extractall(static_output_folder)
        tar.close()

    for shard in SHARDS:
        print("Syncing for shard", shard, "...")

        gcp_rsync(workspace_folder, gcp_bucket_url, gcp_project, shard, dry_run=False)

    print("Done.")


def gcp_rsync(workspace_folder: Path, gcp_bucket_url: str, gcp_project: str, shard: str, dry_run: bool = True):
    """
    See: https://cloud.google.com/storage/docs/gsutil/commands/rsync
    """

    source = workspace_folder / f"shard-{shard}/Static"
    destination_url = f"{gcp_bucket_url}/shard-{shard}/Static"

    command: List[str] = []
    command.append("gsutil")
    command.extend(["-u", gcp_project])
    command.append("-m")        # multi-threaded
    command.append("rsync")
    command.append("-r")        # recursively
    command.append("-c")        # compare checksums (instead of comparing mtime)
    command.append("-d")        # delete files in destination that are not in source

    if dry_run:
        command.append("-n")    # dry run

    command.extend([str(source), destination_url])

    subprocess.run(command)


if __name__ == "__main__":
    main()
