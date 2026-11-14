# Montanha: Zero Day — 한국어판 (비공식)

*그가 글레를 구하러 갔다. 이제 그녀가 그를 찾아 나선다.*

바닐라 JS + 캔버스로 만든 사이버펑크 액션 플랫포머 **Montanha: Zero Day**의 비공식 한국어판입니다.

- 배포(플레이): https://sigco3111.github.io/montanha-zero-day-ko/
- 원작: **tiagovilasboas/montanha-zero-day** — https://github.com/tiagovilasboas/montanha-zero-day
- 원작 데모: https://tiagovilasboas.github.io/montanha-zero-day/
- 이 저장소: https://github.com/sigco3111/montanha-zero-day-ko

## 원작 소개

**네오삼파, 2099년.** 침략형 AI **널 리전(LEGIÃO NULL)**이 행성의 네트워크를 장악했습니다. 글레(Gle)는 납치되어 캡슐에 갇혔습니다.
1스테이지에서는 제트팩·해킹 워치·보조 로봇 **BYTE**를 든 몬타냐를, 2·3스테이지에서는 황금 건틀릿과 빛의 부츠를 갖춘 글레를 조작합니다.
터미널 해킹 퍼즐(순서·2진수·노드 그리드), 아군으로 돌릴 수 있는 터렛, EMP 펄스, 리듬으로 켜지는 펄스 빔, 그리고 보스 **TITAN**의 방화벽 페이즈까지 이어집니다.
pc·모바일 브라우저 모두에서 동작하며, 키보드와 터치 패드를 함께 지원합니다.

## 한글화 방식

원작 코드(js/i18n.js)의 언어 체계를 그대로 쓰고, **ko 사전을 별도 파일로 더하는 방식**입니다. 원문(en/pt)은 손대지 않습니다.

- `js/i18n.ko.js` — 한국어 사전. `KO.ui`(UI 111키) + `KO.lines`(대사 56줄, 키 = 포르투갈어 원문).
- `js/i18n.js` — ko 언어 추가(약 10곳 패치): `import { KO }`, `UI.ko = KO.ui`, `LINES_KO`, `tr()`의 ko 분기, `detectLang()`, `applyDom()`, `toggleLang()`.
- `tools/ko_build.py` — 원작 저장소에서 코드만 받아 위 패치를 재현하는 빌드 스크립트(패치 실패 시 리포트에 MISS로 남고 종료 코드 1).

### 언어 바꾸기

- 타이틀 화면의 언어 버튼이 **영어 → 한국어 → 포르투갈어 → 영어** 순으로 순환합니다.
- 선택은 `localStorage`의 `mzd-lang`에 저장됩니다.
- 저장된 선택이 없으면 **브라우저 언어가 한국어(ko)면 한국어**, 그 외에는 원작 규칙(브라질 시간대 + 포르투갈어 → pt, 나머지 → en)을 따릅니다.
- 사전에 없는 문장은 영어 원문으로 표시되고 게임은 깨지지 않습니다.

### 폰트

캔버스 텍스트는 원작의 픽셀 웹폰트(Press Start 2P / VT323)를 씁니다. 한글 글리프가 없는 폰트라 한국어는 **시스템 한글 폰트**로 대체됩니다:

`Apple SD Gothic Neo` → `Malgun Gothic` → `Noto Sans KR` → `Noto Sans CJK KR` → monospace

- `css/style.css`에 `html[lang="ko"]` 블록을 추가해 UI 글꼴 우선순위를 바꾸고,
- 캔버스 문자열(`ctx.font`)에도 같은 폴백을 넣었습니다.
- OFL 픽셀 한글 폰트(Galmuri11 등)는 **싣지 않았습니다**: 라이선스 표기가 필요하고 파일이 커서, 우선은 시스템 폰트로 두었습니다. 원하면 `css/style.css`의 `html[lang="ko"]` 블록에 `@font-face`를 더하면 됩니다.

## 라이선스와 에셋 처리 (중요)

원작 `LICENSE` 전문:

- **코드**: MIT License, Copyright (c) 2026 Tiago Vilas Boas. (이 저장소도 같은 MIT 조건을 유지하며, 원문 라이선스 파일을 `LICENSE`에 그대로 두었습니다.)
- **에셋·이름·스토리**: `assets/`, `icons/`, `docs/screenshots/` 전체와 **Montanha·Gle·BYTE의 이름과 스토리**는 © 2026 Tiago Vilas Boas, **All rights reserved**.

그래서 이 저장소는 **원작 이미지·소리·아이콘을 한 개도 복사하지 않습니다.** 대신:

- `js/assets.js`의 `ASSET_BASE`가 원작 Pages(`https://tiagovilasboas.github.io/montanha-zero-day/`)를 가리키고, 게임은 실행 중에 그곳에서 `assets/*.webp`와 `assets/anims.json`을 **직접 불러옵니다**(핫링크). 저장소와 배포 산출물에는 ARR 파일이 없습니다.
- 2026-11 기준 확인: 원작 Pages는 `access-control-allow-origin: *`를 보내므로 교차 출처 `fetch(anims.json)`와 `<img>` 로드가 모두 동작합니다. 에셋 33종 URL을 HEAD로 확인해 전부 200이었습니다(`docs/build-report.txt`).
- 원작이 내려가거나 에셋 경로가 바뀌면 그림 없이 게임 로직만 남습니다. 그때는 `ASSET_BASE`만 고치면 됩니다.
- 캔버스는 픽셀을 읽지 않으므로(getImageData 없음) 교차 출처 이미지로 화면이 오염되지 않습니다.

번역문(한국어)은 MIT 코드 파일에 덧붙인 데이터로, 원작 대사·이름의 권리는 원작자에게 있습니다. **원작자가 내리라고 하면 저장소와 배포 페이지를 즉시 내립니다.**

## 제거한 외부 기능

- **Google Fonts**(fonts.googleapis.com / fonts.gstatic.com) 링크 제거 — 외부 서버 호출을 남기지 않기 위해서입니다.
- **서비스 워커 / PWA**: `sw.js`, `manifest.webmanifest`, `icons/`를 싣지 않고 `main.js`의 `serviceWorker.register('sw.js')` 호출을 껐습니다. 오프라인 캐시가 원작 ARR 에셋을 내 저장소 오리진에 복제하는 구조를 피하려는 선택입니다. `앱 설치` 버튼은 자동으로 숨겨집니다.
- 원작 코드에는 **분석·통계·텔레메트리 호출이 없습니다**(저장소 전체에서 외부 URL은 위 폰트뿐). 그래서 따로 걷어낼 것은 없었습니다.
- 저장은 브라우저 `localStorage`(`montanha-zero-day-v1`)에만 남습니다.

## 번역 범위

| 영역 | 상태 |
|---|---|
| UI 111키(타이틀·일시정지·미션맵·HUD·해킹 퍼즐·크레딧·언어 버튼) | 전부 번역 |
| 대사·스테이지 이름·보스 대사 56줄 | 전부 번역 |
| 아트에 그려진 글자(간판·타이틀 로고) | 원본 이미지 그대로(ARR, 수정 불가) |

용어 고정표는 `docs/glossary.md`에 있습니다. 남은 작업: 캔버스에 박힌 이미지 속 텍스트, 그리고 원하면 OFL 픽셀 한글 폰트 도입.

## 번역 외 변경 (diff 요약)

1. `js/assets.js`: `ASSET_BASE` 상수 + `assetPath`/`anims.json` 경로를 원작 Pages로.
2. `js/i18n.js`: ko 언어 추가(11곳, 위 "한글화 방식" 참고).
3. `js/main.js`: 서비스 워커 등록 제거.
4. `css/style.css`: `--font-display`/`--font-body`에 한글 폴백, `html[lang="ko"]` 블록 추가.
5. `js/*.js`: 캔버스 폰트 문자열에 한글 폴백 추가(1개 파일).
6. `index.html`: Google Fonts 링크 3개, manifest 링크 1개, 아이콘 링크 2개 제거.
7. 원작에서 `build.py`, `game.html`, `tools/`(아트 생성기), `docs/screenshots/`, `README.pt-BR.md`, dev.to 글은 가져오지 않았습니다(`index.html`은 원작 생성물을 그대로 받아 위 링크만 지웠습니다).
8. 루트 절대경로 참조 0건 확인(하위 경로 배포 안전), 로컬 `assets/` 참조 0건 확인.

## 다시 빌드하기

```bash
python3 tools/ko_build.py     # 원작을 받아 코드 반영 + 패치 + 검증 + docs/build-report.txt
```
로컬에서 미리 보려면 `python3 -m http.server 8000` 후 `http://localhost:8000`(원작 에셋은 원격에서 로드됩니다).

## 확인한 것 / 확인하지 못한 것

- 확인: 배포 URL에서 타이틀 화면·오프닝 컷신·인게임 대사가 한국어로 표시됨, 원작 아트가 원격에서 정상 로드됨, 언어 버튼 3단 순환, 에셋 33종 200 응답, CORS `*`.
- 확인하지 못함: 2·3스테이지 끝까지의 전체 플레이(캔버스 액션이라 자동 클릭으로 보스·엔딩까지 진행하지 못했습니다), 실제 모바일 기기 터치 조작, 해킹 퍼즐 3종의 문구 배치(줄바꿈) 미세 조정.

## 크레딧

- 원작 게임·코드·스토리·아트: **Tiago Vilas Boas** (https://github.com/tiagovilasboas) — 아트는 Artlist(Nano Banana 2, Seedance)로 제작, 음악·효과음은 WebAudio 실시간 합성.
- 한국어 번역·빌드: sigco3111
- 이 저장소는 비공식 팬 번역이며 원작자와 무관합니다.
