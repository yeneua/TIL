### 프레임워크

**선택지**

1. react + capacitor
2. RN + RN for web
3. react + RN 각각

**필요한 기능**

- 웹
  - chart.js or highchart
  - FCM 알림
- 모바일
  - FCM 알림
  - 워치 연동

**코틀린은 대체 어디에 쓰는건데?**

⇒ 워치앱을 코틀린으로 만든다는 것

서버 ↔️ 모바일앱 ↔️ 워치 앱(kotlin)

- 근데 워치에서 무조건 모바일 앱을 거쳐야 하나??
  - 워치에서 직접 서버랑 통신하는 게 기술적으로는 가능하지만 거의 그렇게 사용하지 않고 모바일을 거치는 구조로 만든다
  - 가능하게 하는 방법
    - 인터넷이 연결된 워치에서 바로 서버랑 통신하게 함
    - LTE 모델 워치, wifi 모델 워치
  - 가능하지만 안하는 이유
    1. 배터리 소모
       - 워치 배터리로 통신을 직접 수행하면 배터리 소모량 ↑
    2. 데이터 동기화 복잡성
       - 모바일 앱, 웹, 워치 모두 각각 서버와 통신하면
       - 데이터 일관성 맞추기 어려움
    3. 오프라인 환경
       - 만약 인터넷이 없는 환경이라면
       - 워치 → 모바일로 데이터를 보내두고
       - 모바일이 인터넷에 연결되면 서버로 데이터 전송 가능
    4. 인증 처리
       - 워치에서 로그인 정보를 관리하는 건 어렵고 보안에도 좋지 않다
       - 모바일앱에서 인증 처리하고 데이터를 넘겨주는 게 좋음
- 궁금한거, 워치에서 모바일로는 데이터 어떻게 보내는데??
  - 인터넷 망을 사용하는 게 아닌 근거리 통신 채널을 이용함
  - ex. BLE, 로컬 wifi, NFC 등

**만약 react+capacitor로 개발한다면?**

> React + Capacitor만으로는 워치와 직접 통신 불가,
> 안드로이드 네이티브 모듈을 Capacitor 플러그인으로 작성해서 React에 연결해야함

1. 역할
   - react → 화면 ui 구성
   - kotlin → 워치 앱 제작
   - 모바일 플러그인 → 워치 + 앱 연동 코드 작성
2. 폴더 구조

   ```
   my-project/
    ├─ src/                        # React 코드 (웹/앱 UI)
    ├─ android/                    # 안드로이드 네이티브 프로젝트
       ├─ app/                     # 메인 안드로이드 앱
       └─ com/example/plugins/     # ⬅️ 여기 Kotlin 플러그인 추가
           └─ WearBridgePlugin.kt
   ```

3. 구현 과정

   1. capacitor 플러그인 작성 - react의 `android` 폴더에 작성

      ```kotlin
      @CapacitorPlugin(name = "WearBridge")
      class WearBridgePlugin : Plugin() {
          @PluginMethod
          fun sendToWatch(call: PluginCall) { ... }
      }
      ```

   2. react에서 사용

      ```tsx
      import { Plugins } from "@capacitor/core";
      const { WearBridge } = Plugins;

      WearBridge.sendToWatch({ message: "안전모 미착용!" });
      ```

   **⇒ 결론적으로**

   👉 React 메인 레포 = React 코드 + Capacitor 생성 android 폴더 + WearBridgePlugin(Kotlin) 코드

   👉 워치 레포 = 완전히 독립된 Kotlin 프로젝트

**결정**

- iOS x, android 만 필요 → 하이브리드라는 ionic의 장점을 살리기 어렵다
- emotion, tailwind 등 다른 디자인 시스템을 사용할 때 관리 복잡도가 올라감
- 학습 곡선 및 개발 일정 고려
- 모바일은 크게 디자인할 요소가 없기 때문
