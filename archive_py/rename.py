from pathlib import Path


def main():
    epoch_archives = Path(".").glob("Epoch_*.tar")
    epoch_archives = sorted(epoch_archives)

    for archive in epoch_archives:
        epoch_number = archive.stem.split("_")[1]
        old_name = archive.name
        new_name = f"Epoch_{epoch_number.zfill(5)}.tar"

        if new_name != old_name:
            print(f"Renaming {archive} to {new_name}")
            archive.rename(new_name)


if __name__ == "__main__":
    main()
