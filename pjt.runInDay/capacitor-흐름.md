### 1. `npm run build`

- `dist/` 폴더가 생김
- `dist`는 결과물로 브라우저가 이해할 수 있는 파일만 있음
  ![image.png](attachment:2eb2de56-2efd-4c58-9949-bf42c95c4368:image.png)

### 2. `npx cap sync`

- `dist/` 폴더 내용이 android 프로젝트의 아래 경로로 복사 됨
  ```swift
  android/app/src/main/assets/public/  ← 여기에 index.html, assets/ 가 통째로 들어감
  ```

### 3. 앱에서 로드

- 앱 실행할 때 WebView는 `file:///android_asset/public/index.html` 파일을 로드 → 이게 곧 `dist/index.html`임
- `dist/index.html`을 살펴보면 아래와 같은 코드가 있음
  ```html
  <script type="module" crossorigin src="/assets/index-Ddmpl_af.js"></script>
  ```
  - `index-Ddmpl_af.js`는 `main.tsx`(엔트리)를 번들한 결과임
- 엔트리 번들 실행 ← 번들 안에는 사실상 `main.tsx` 코드가 들어있음 (우리가 만든 리액트 프로젝트)
- react 앱 시작

<details>
<summary>엔트리 번들?</summary>
<div markdown="1">

- 엔트리
  - 프로젝트 실행의 시작점 파일
  - react + vite의 경우 `src/main.tsx`가 보통 엔트리
- 번들
  - 브라우저는 js만 이해 가능
  - `jsx`, `ts`, `css`, 이미지, 라이브러리 등을 js 파일로 묶음
  - 최종 실행 가능한 묶음
- 엔트리 번들
  - 엔트리 파일을 시작점으로 해서 번들링 된 최종 js 파일
  - `main.tsx` 코드, import한 모든 컴포넌트, 외부 라이브러리, css/이미지 등이 최적화 되어 들어가 있음
  </div>
  </details>
