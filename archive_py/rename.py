from pathlib import Path


def main():
    epoch_archives = Path(".").glob("Epoch_*.tar")

    for archive in epoch_archives:
        epoch_number = archive.stem.split("_")[1]
        new_name = f"Epoch_{epoch_number.zfill(5)}.tar"

        print(f"Renaming {archive} to {new_name}")
        archive.rename(new_name)


if __name__ == "__main__":
    main()
