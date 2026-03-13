# Todo+

Flask와 SQLite 기반의 스마트 할일 관리 웹 애플리케이션입니다.

## 주요 기능

- **할일 목록**: 카테고리, 우선순위, 완료 상태별 필터링을 지원하는 할일 리스트
- **CRUD 기능**: 제목, 설명, 카테고리, 우선순위(높/중/낮), 마감일을 포함한 할일 등록/수정/삭제
- **통계 대시보드**: 완료율, 카테고리별 분포, 우선순위별 현황을 시각적으로 확인

## 기술 스택

- Python 3
- Flask
- SQLite
- Jinja2
- HTML/CSS

## 시작하기

### 사전 요구사항

- Python 3.8 이상
- pip

### 설치 및 실행

```bash
# 저장소 클론
git clone https://github.com/lsmin3388/todo-plus.git
cd todo-plus

# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
python app.py
```

브라우저에서 [http://localhost:5000](http://localhost:5000)을 열어 접속합니다.

### Docker로 실행

```bash
# 이미지 빌드
docker build -t todo-plus .

# 컨테이너 실행
docker run -p 5000:5000 todo-plus
```

또는 GHCR에서 이미지를 받아 실행할 수 있습니다:

```bash
docker pull ghcr.io/lsmin3388/todo-plus:latest
docker run -p 5000:5000 ghcr.io/lsmin3388/todo-plus:latest
```

## 프로젝트 구조

```
todo-plus/
├── app.py                    # Flask 라우트 및 앱 설정
├── models.py                 # SQLite 데이터베이스 모델 및 쿼리
├── templates/
│   ├── base.html             # 공통 레이아웃 템플릿
│   ├── index.html            # 할일 목록 페이지
│   ├── form.html             # 등록/수정 폼
│   └── stats.html            # 통계 대시보드
├── static/
│   └── style.css             # 스타일시트
├── tests/
│   └── test_app.py           # 단위 테스트
├── .github/workflows/
│   ├── ci.yml                # CI 워크플로우 (테스트 + 린트)
│   └── cd.yml                # CD 워크플로우 (GHCR 배포)
├── Dockerfile                # Docker 컨테이너 설정
├── requirements.txt          # Python 의존성
└── README.md
```

## CI/CD

| 워크플로우 | 트리거 | 내용 |
|------------|--------|------|
| **CI** | push/PR (main, develop) | Python 3.10~3.12 매트릭스 테스트 + flake8 린트 |
| **CD** | `v*` 태그 push | Docker 이미지 빌드 후 GHCR에 배포 |

## 테스트 실행

```bash
pip install pytest
pytest tests/ -v
```

## 스크린샷

### 할일 목록
카테고리, 우선순위, 완료 상태별로 할일을 필터링할 수 있습니다.

### 통계 대시보드
시각적 차트를 통해 생산성을 확인할 수 있습니다.

## 라이선스

이 프로젝트는 [MIT License](LICENSE) 하에 오픈소스로 제공됩니다.
