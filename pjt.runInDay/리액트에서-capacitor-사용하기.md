## 환경 설정

### **1. node 설치**

```bash
node --version
# v22.18.0 -> 25.08.25 기준 LTS
```

### 2. 안드로이드일 경우

1. Android Studio
   - capacitor 7 → android studio 2024.2.1 이상 필요
2. Android SDK
   - API 23 이상 버전 필요

## react 프로젝트에 capacitor 추가하기

```bash
# 1. capacitor 패키지 설치
npm i @capacitor/core
npm i -D @capacitor/cli

# 2. capacitor 프로젝트 초기화
npx cap init # appName, appId, webDir 입력(vite일 경우 dist)

# 3. 플랫폼 추가
npm i @capacitor/android
npx cap add android

# 4. react 앱 빌드
npm run build

# 5. capacitor에 빌드 결과물 복사
npx cap sync
```

1. `npx cap init`
   - capacitor 프로젝트 초기화 할 때 실행
   - `capacitor.config.ts` 파일을 만들어줌
   - 기본 설정 지정함(appId, appName, webDir)
2. `npx cap add android`
   - capacitor 프로젝트에 android 플랫폼 추가해줌
   - 이때 react를 네이티브 앱으로 감싸는 구조가 됨
3. `npm run build` + `npx cap sync`
   - react 빌드하고
   - 앱 실행됨

<br/>

✅ `npm run build` + `npx cap sync` 언제 실행해야 하나?

| 상황                                                                      | `npm run build`   | `npx cap sync`      |
| ------------------------------------------------------------------------- | ----------------- | ------------------- |
| **React 코드 변경** (UI, 로직 등)                                         | ✅ 꼭 실행해야 함 | ✅ 함께 실행해야 함 |
| **Capacitor 관련 설정 변경**(예: `capacitor.config.ts`, 플러그인 추가 등) | ❌ 필요 없음      | ✅ 꼭 실행해야 함   |
| **Android 프로젝트 생성 직후 or 업데이트**                                | ✅ 한 번 실행     | ✅ 한 번 실행       |
| **React 코드만 수정** (예: 화면 변경)                                     | ✅ 매번 필요      | ✅ 매번 필요        |
| **앱 배포용으로 빌드할 때**                                               | ✅ 필요           | ✅ 필요             |

## 참고한 글

[Capacitor - Cross-platform Native Runtime for Web Apps | Capacitor Documentation](https://capacitorjs.com/docs)

[시리즈 | React에서 Capacitor 사용하기 - jypapapaa.log](https://velog.io/@jypapapaa/series/React%EC%97%90%EC%84%9C-Capacitor-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0)
