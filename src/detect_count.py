import argparse

from ultralytics import YOLO

from count_utils import count_by_class


def parse_args():
    parser = argparse.ArgumentParser(description="이미지에서 총기류 종류/개수 탐지")
    parser.add_argument("source", help="이미지 파일 또는 폴더 경로")
    parser.add_argument("--weights", default="runs/detect/models/firearms_yolo/weights/best.pt")
    parser.add_argument("--conf", type=float, default=0.7)
    parser.add_argument("--save", action="store_true", help="박스가 그려진 결과 이미지 저장")
    return parser.parse_args()


def main():
    args = parse_args()
    model = YOLO(args.weights)
    results = model.predict(source=args.source, conf=args.conf, save=args.save)

    counts = count_by_class(results, model.names)
    print("탐지 결과 (클래스별 개수):")
    for name, count in counts.items():
        print(f"  {name}: {count}")
    print(f"총 개수: {sum(counts.values())}")
    if args.save and results:
        print(f"결과 이미지 저장 위치: {results[0].save_dir}")


if __name__ == "__main__":
    main()
