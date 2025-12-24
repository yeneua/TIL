antigravity를 이용해서 바이브 코딩 프로젝트 진행 중에 아래와 같은 메시지를 받았다.

```bash
Vite 설정 파일의 lint 오류를 수정하겠습니다.

path 모듈과 __dirname을 사용하는 대신 Vite의 내장 기능을 사용하겠습니다.

…\toss-apply-demo > npm install -D @types/node
```

lint 오류 수정을 위해 `@types/node`를 설치하는다는 말 같은데

환경세팅할때 크게 생각하지 않고 설치했던 `@types/node` 패키지에 대해 알아보았다.

### 그래서

- 해당 패키지를 설치하면 Node.js 환경에서 쓰는 변수들의 타입을 정의해줌
- ts는 기본적으로 브라우저 환경(DOM, Window 등) 변수들만 알고 있음
- `@types/node` 패키지를 설치하면 대표적으로 아래와 같은 것들의 타입을 ts가 이해함
  | 구분 | 주요 항목 | 역할 |
  |------|----------|------|
  | 전역 변수 | `__dirname`, `__filename` | 현재 파일의 폴더 경로와 파일 이름 |
  | 전역 객체 | `process` | 현재 실행 중인 프로세스 정보 (환경 변수 `process.env` 등) |
  | 내장 모듈 | `path`, `fs`, `os`, `http` | 파일 경로 조작, 파일 시스템 읽기/쓰기, 운영체제 정보 등 |
  | 기능 / 함수 | `Buffer`, `setTimeout` 등 | 바이너리 데이터 처리 및 Node 방식의 타이머

### Vite 설정에서 필요한 이유

- Vite 설정 파일(`vite.config.ts`)는 브라우저가 아니라 Node.js 환경에서 실행됨(빌드 도구이기 때문)
- Vite 설정 파일에서 파일을 합치거나 경로를 지정하려면 `path`, `__dirname` 같은 Node.js 도구 필요
- ts에 Node.js 도구의 타입을 알려주는 것
- `path` : 경로 계산용
- `__dirname` : 현재 폴더
