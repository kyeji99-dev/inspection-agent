"""Download demo inspection images from Hugging Face Voxel51/mvtec-ad."""
import argparse
from pathlib import Path

from datasets import load_dataset


def main():
    p = argparse.ArgumentParser(description="Download MVTec AD demo images.")
    p.add_argument("--n", type=int, default=50, help="Number of images")
    p.add_argument("--out", default="images", help="Output directory")
    p.add_argument(
        "--stride",
        action="store_true",
        help="Sample N images evenly across the whole dataset (for category diversity)",
    )
    p.add_argument(
        "--prefix", default="mvtec", help="Filename prefix"
    )
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if args.stride:
        print(f"Loading full dataset to compute stride...")
        ds = load_dataset("Voxel51/mvtec-ad", split="train")
        total = len(ds)
        indices = [int(i * total / args.n) for i in range(args.n)]
        print(f"Sampling {args.n} images evenly from {total} rows (stride ~{total // args.n})")
    else:
        print(f"Loading first {args.n} images from Voxel51/mvtec-ad...")
        ds = load_dataset("Voxel51/mvtec-ad", split=f"train[:{args.n}]")
        indices = list(range(args.n))

    for k, i in enumerate(indices):
        img = ds[i]["image"]
        path = out / f"{args.prefix}_{k:03d}_idx{i:04d}.png" if args.stride else out / f"{args.prefix}_{k:03d}.png"
        img.save(path)
        if k < 3 or (k + 1) % 10 == 0:
            print(f"  [{k+1}/{args.n}] {path.name}  {img.size}")

    print(f"\nDone. {args.n} images saved to {out}/")


if __name__ == "__main__":
    main()
