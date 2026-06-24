# 국방 장비 재고 관리 앱 (Flutter)

총기류(K-2 · K-1A · K2C1 · M16A1) 재물조사를 사진 촬영 기반으로 수행하고,
정기 검사(재물조사 / 전투장비지휘검열) 시점별 수량을 대조하는 모바일 앱입니다.

HTML 프로토타입을 Flutter / Dart 로 변환한 코드입니다.

## 실행

```bash
flutter create . --project-name defense_inventory   # 플랫폼 폴더(android/ios) 생성
flutter pub get
flutter run
```

> 이미 Flutter 프로젝트가 있다면 `lib/` 와 `pubspec.yaml` 만 덮어쓰면 됩니다.

## 구조

```
lib/
├── main.dart                       앱 진입점 + 하단 탭 셸(MainShell)
├── theme.dart                      색상 팔레트(AppColors) · 텍스트 헬퍼(T)
├── widgets/
│   └── bottom_nav.dart             하단 내비게이션(아이콘만, 가운데 촬영 FAB)
└── screens/
    ├── home_screen.dart            홈 — 통계·부족 재고·기종별 재고
    ├── inventory_list_screen.dart  기종별 상세 재고(검색·필터·총번 펼침)
    ├── capture_screen.dart         촬영 → 인식 → 수량 입력(전체화면)
    ├── history_screen.dart         검사 내역(분기별/연도별 수량 대조)
    └── settings_screen.dart        설정 — 마이페이지 + 항목
```

## 화면 동작

- **홈 / 재고 / 이력 / 설정** 은 하단 탭으로 전환(`IndexedStack` 으로 상태 유지).
- 가운데 **촬영** 버튼은 `CaptureScreen` 을 전체화면으로 push.
- **촬영 화면**: 셔터 → 등록 폼 전환. 기종 칩을 탭하면 총번·편제 정수가 갱신되고,
  수량 스테퍼로 편제 대비 부족/초과/일치를 자동 판정. "재고 저장" → 완료 다이얼로그.
- **재고 화면**: 기종 카드를 탭하면 총번 목록(양호/정비요/미점검)이 펼쳐짐.
- **이력 화면**: 분기별/연도별 토글, 검사 일지를 탭하면 비교 기준이 바뀌며 대조표·증감 재계산.

## 색상 팔레트 (theme.dart)

| 용도 | 색상 |
|---|---|
| 배경(매트 차콜) | `#2A2A2C` |
| 카드 | `#363539` |
| 브랜드/활성/정상·일치/증가 | 골드 `#D8A94A` |
| 커밋 액션/결손·초과 | 브릭 레드 `#C0433E` |
| 부족/정비요 경고 | 테라코타 `#CB6B52` |

## 참고

- 아이콘은 디자인의 커스텀 SVG 대신 Material 기본 아이콘으로 매핑했습니다.
  브랜드 정합이 필요하면 `flutter_svg` 로 교체하세요.
- 데이터는 각 화면에 하드코딩된 더미입니다. 실제 연동 시 리포지토리/상태관리
  (Riverpod, Bloc 등)로 분리하는 것을 권장합니다.
- 카메라는 UI 목업입니다. 실제 촬영은 `camera` 패키지로 뷰파인더를 대체하세요.
