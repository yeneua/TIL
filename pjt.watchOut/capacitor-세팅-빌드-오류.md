## 문제 상황

> 프로젝트에 capacitor 설정 중 `pnpm build` 명령어 입력 후 오류

## 트러블 슈팅

<details>
<summary>⚠️ 에러 전문</summary>
<div markdown="1">

pnpm build

> frontend-repo@0.0.0 build C:\Users\SSAFY\Desktop\S13P21E102\frontend-repo
> tsc -b && vite build

node*modules/.pnpm/vite@7.1.5*@types+node@24.3.1/node*modules/vite/dist/node/index.d.ts:7:41 - error TS2307: Cannot find module 'rollup/parseAst' or its corresponding type declarations.
There are types at 'C:/Users/SSAFY/Desktop/S13P21E102/frontend-repo/node_modules/.pnpm/vite@7.1.5*@types+node@24.3.1/node_modules/rollup/dist/parseAst.d.ts', but this result could not be resolved under your current 'moduleResolution' setting. Consider updating to 'node16', 'nodenext', or 'bundler'.

7 import { parseAst, parseAstAsync } from "rollup/parseAst";

```

src/App.tsx:2:10 - error TS17004: Cannot use JSX unless the '--jsx' flag is provided.

2 return <div>App</div>
~~~~~

src/main.tsx:3:17 - error TS5097: An import path can only end with a '.tsx' extension when 'allowImportingTsExtensions' is enabled.

3 import App from './App.tsx'
~~~~~~~~~~~

src/main.tsx:3:17 - error TS6142: Module './App.tsx' was resolved to 'C:/Users/SSAFY/Desktop/S13P21E102/frontend-repo/src/App.tsx', but '--jsx' is not set.

3 import App from './App.tsx'
~~~~~~~~~~~

src/main.tsx:6:3 - error TS17004: Cannot use JSX unless the '--jsx' flag is provided.

6 <StrictMode>
~~~~~~~~~~~~

src/main.tsx:7:5 - error TS17004: Cannot use JSX unless the '--jsx' flag is provided.

7 <App />
~~~~~~~

src/styles/GlobalStyles.tsx:4:3 - error TS17004: Cannot use JSX unless the '--jsx' flag is provided.

4 <Global
~~~~~~~
5 styles={css`
~~~~~~~~~~~~~~~~
...
79 `}
~~~~~~
80 />
~~~~

vite.config.ts:2:19 - error TS2307: Cannot find module '@vitejs/plugin-react' or its corresponding type declarations.
There are types at 'C:/Users/SSAFY/Desktop/S13P21E102/frontend-repo/node_modules/@vitejs/plugin-react/dist/index.d.ts', but this result could not be resolved under your current 'moduleResolution' setting. Consider updating to 'node16', 'nodenext', or 'bundler'.

2 import react from '@vitejs/plugin-react'
```

vite.config.ts:4:8 - error TS1259: Module '"node:path"' can only be default-imported using the 'esModuleInterop' flag

4 import path from 'node:path'

```

node_modules/.pnpm/@types+node@24.3.1/node_modules/@types/node/path.d.ts:191:5
191 export = path;
```

This module is declared with 'export =', and can only be used with a default import when using the 'esModuleInterop' flag.

Found 9 errors.

ELIFECYCLE  Command failed with exit code 2.

</div>
</details>

<br/>
👉 typecheck, build 명령어 분리

`pnpm run build`는 `tsc -b` (타입스크립트 빌드)도 같이 돌기 때문에 에러 발생

→ vite는 자체 번들러만 써서 ts 설정 충돌 X

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build", // "build" : "tsc -b && vite build"
    "typecheck": "tsc -b"
  }
}
```

- 타입 체크 시 : `pnpm run typecheck`
- 배포 전 빌드 : `pnpm run build`

✅ 빌드 에러 해결
