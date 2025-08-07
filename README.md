# Comphy · Computational Physics Toolkit

[![pnpm](https://img.shields.io/badge/pnpm-workspace-blue?logo=pnpm)](https://pnpm.io/workspaces)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?logo=typescript)](https://www.typescriptlang.org/)
[![Prettier](https://img.shields.io/badge/Prettier-3.0-pink?logo=prettier)](https://prettier.io/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Comphy**는 계산물리학 도구들을 모아놓은 모노레포입니다. 현재는 Transfer Matrix Method (TMM) 계산기를 다양한 기술 스택으로 구현한 버전들을 포함하고 있습니다.

## 🏗️ 프로젝트 구조

```
comphy/
├── apps/                    # 최신 애플리케이션
│   └── tmm/                # React + Vite 기반 TMM 계산기
│       ├── src/            # 소스 코드
│       ├── package.json    # 의존성 관리
│       └── README.md       # 상세 문서
├── legacy/                 # 레거시 구현체들
│   ├── python_tmm/         # PySide6 기반 GUI TMM
│   └── WebTMM/            # Django + Angular 기반 웹 TMM
├── package.json           # 워크스페이스 설정
├── pnpm-workspace.yaml    # pnpm 워크스페이스 설정
└── run_tmm.bat           # Windows 실행 스크립트
```

## 🚀 빠른 시작

### 요구사항

- **Node.js** 18.0.0 이상
- **pnpm** (권장) 또는 npm
- **Python** 3.10+ (레거시 버전용)

### 설치 및 실행

1. **저장소 클론**
   ```bash
   git clone https://github.com/jaehakl/comphy.git
   cd comphy
   ```

2. **의존성 설치**
   ```bash
   pnpm install
   ```

3. **최신 TMM 앱 실행**
   ```bash
   pnpm dev          # React + Vite 버전
   # 또는
   pnpm run_tmm      # Windows 배치 파일 사용
   ```

## 📦 애플리케이션별 가이드

### 🌟 **TMM JS** (최신) - `apps/tmm/`

**React 19 + Vite 기반의 현대적인 웹 TMM 계산기**

- **특징**: 브라우저에서 직접 실행, 100KB 미만 번들 크기
- **기술 스택**: React 19, Vite 5, RSuite, Plotly.js
- **실행**: `pnpm --filter tmm dev`
- **문서**: [apps/tmm/README.md](apps/tmm/README.md)

```bash
# TMM JS만 실행
cd apps/tmm
pnpm dev
```

### 🐍 **Python TMM** (레거시) - `legacy/python_tmm/`

**PySide6 기반 데스크톱 GUI TMM 계산기**

- **특징**: 네이티브 데스크톱 애플리케이션
- **기술 스택**: Python 3.10, PySide6, Matplotlib
- **실행**: `legacy/python_tmm/run.bat`

```bash
# Python TMM 실행
cd legacy/python_tmm
./run.bat
```

### 🌐 **WebTMM** (레거시) - `legacy/WebTMM/`

**Django + Angular 기반 웹 TMM 계산기**

- **특징**: 서버-클라이언트 아키텍처, CIE 다이어그램 지원
- **기술 스택**: Django, Angular, Python 3.10
- **실행**: `legacy/WebTMM/run.bat`

```bash
# WebTMM 실행
cd legacy/WebTMM
./run.bat
```

## 🔧 개발 도구

### 스크립트

| 명령어 | 설명 |
|--------|------|
| `pnpm dev` | TMM JS 개발 서버 실행 |
| `pnpm build` | TMM JS 프로덕션 빌드 |
| `pnpm start` | TMM JS 프로덕션 서버 실행 |
| `pnpm lint` | 코드 스타일 검사 |

### 코드 품질

- **Prettier**: 코드 포맷팅
- **TypeScript**: 타입 안전성
- **ESLint**: 코드 품질 검사

## 📊 기능 비교

| 기능 | TMM JS | Python TMM | WebTMM |
|------|--------|------------|--------|
| **실행 환경** | 브라우저 | 데스크톱 | 웹 서버 |
| **설치 필요** | ❌ | ✅ | ✅ |
| **번들 크기** | < 100KB | MB | MB |
| **실시간 계산** | ✅ | ❌ | ❌ |
| **레이어 수** | 무제한 | 제한적 | 제한적 |
| **오프라인 지원** | ✅ | ✅ | ❌ |
| **CIE 다이어그램** | ❌ | ❌ | ✅ |

## 🎯 사용 시나리오

### TMM JS (권장)
- **연구실에서**: 빠른 프로토타이핑
- **강의실에서**: 실시간 데모
- **출장 중**: 오프라인 작업
- **협업**: GitHub Pages 배포

### Python TMM
- **고성능 필요**: 대용량 계산
- **네이티브 UI**: 데스크톱 환경
- **Python 생태계**: NumPy, SciPy 활용

### WebTMM
- **색상 분석**: CIE 다이어그램 필요
- **서버 환경**: 기존 웹 인프라 활용
- **사용자 관리**: Django 백엔드 활용

## 🔬 Transfer Matrix Method

모든 구현체는 동일한 TMM 알고리즘을 사용합니다:

1. **전송행렬 계산**: 각 경계면에서의 복소수 전송행렬
2. **행렬 곱셈**: 모든 레이어의 전송행렬을 순차적으로 곱셈
3. **반사율/투과율**: 최종 행렬에서 광학 특성 추출

### 수학적 표현
```
Q = [q₀₀  q₀₁]    (각 경계면의 전송행렬)
    [q₁₀  q₁₁]

F = Qₙ ⋯ Q₂ Q₁    (전체 전송행렬)

r = -F₁₀/F₁₁      (반사율)
t = F₀₀ + F₀₁r    (투과율)
```

## 🤝 기여하기

1. **Fork** 저장소
2. **Feature branch** 생성 (`git checkout -b feature/amazing-feature`)
3. **Commit** 변경사항 (`git commit -m 'Add amazing feature'`)
4. **Push** 브랜치 (`git push origin feature/amazing-feature`)
5. **Pull Request** 생성

### 기여 영역
- **알고리즘 개선**: TMM 계산 정확도 향상
- **UI/UX 개선**: 사용자 경험 향상
- **성능 최적화**: 계산 속도 개선
- **새로운 기능**: 추가 광학 계산 도구

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📚 참고 자료

- [Transfer Matrix Method 이론](https://en.wikipedia.org/wiki/Transfer-matrix_method_(optics))
- [다층 박막 광학](https://en.wikipedia.org/wiki/Thin-film_optics)
- [복소수 광학 계산](https://en.wikipedia.org/wiki/Complex_refractive_index)

## 🙏 감사의 말

- 기존 Python TMM 구현체 개발자들
- React, Vite, PySide6, Django, Angular 커뮤니티
- 계산물리학 연구자들

---

**Comphy** - 계산물리학을 위한 현대적인 도구 모음

*Made with ❤️ for the computational physics community*
