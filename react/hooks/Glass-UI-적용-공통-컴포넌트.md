**공통 컴포넌트가 필요한 요소**

1. 버튼
   1. 삭제
   2. 노트 작성
   3. 뒤로가기
   4. 연관 노트
   5. 프로필
2. input
   1. 검색창
   2. 선택 체크박스
3. div
   1. 노트 목록
   2. 우측 노트 패널
   3. 드롭다운
   4. 삭제 확인창

라이브러리? 안씀

쓰니까 hover가 이상한 데 생기고 내 입맛대로 사용하기 어렵더라

근데 또 안쓰니까 **맛**이 안남

그래서?? 라이브러리 코드 뜯어서 스타일 가져오기

- html 코드

  ```html
  <!DOCTYPE html>
  <html lang="ko">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <style>
        /* 페이지 배경 */
        body {
          display: grid;
          place-items: center;
          min-height: 100vh;
          margin: 0;
          font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
            Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
          background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20230527/pngtree-nature-wallpapers-image_2683049.jpg");
        }

        /* 래퍼 */
        .glass-wrapper {
          position: relative;
        }

        /* 유리 버튼 본체 */
        .glass-element {
          background: rgba(255, 255, 255, 0.15);
          backdrop-filter: blur(3.5px) saturate(180%);
          -webkit-backdrop-filter: blur(3.5px) saturate(180%);
          border-radius: 24px;
          box-shadow: 0px 12px 40px rgba(0, 0, 0, 0.25);
          padding: 24px 32px;
          color: white;
          font-size: 20px;
          font-weight: 500;
          text-shadow: 0px 2px 12px rgba(0, 0, 0, 0.4);
          cursor: pointer;
          position: relative;
        }

        .glass-border {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          border-radius: 24px;
          pointer-events: none;

          box-shadow: 0 0 0 0.5px rgba(255, 255, 255, 0.5) inset, 0 1px 3px rgba(
                255,
                255,
                255,
                0.25
              ) inset, 0 1px 4px rgba(0, 0, 0, 0.35);

          padding: 1px;

          z-index: 1;

          -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(
              #000 0 0
            );
          -webkit-mask-composite: xor;
          mask-composite: exclude;
        }

        .border-1 {
          mix-blend-mode: screen;
          opacity: 0.2;
        }

        .border-2 {
          mix-blend-mode: overlay;
        }
      </style>
    </head>
    <body>
      <div class="glass-wrapper" id="glass-wrapper">
        <div class="glass-element">Glass UI</div>
        <span class="glass-border border-1" id="border-1"></span>
        <span class="glass-border border-2" id="border-2"></span>
      </div>

      <script>
        const wrapper = document.getElementById("glass-wrapper");
        const border1 = document.getElementById("border-1");
        const border2 = document.getElementById("border-2");

        window.addEventListener("mousemove", (e) => {
          const rect = wrapper.getBoundingClientRect();
          const centerX = rect.left + rect.width / 2;
          const centerY = rect.top + rect.height / 2;

          let mouseX = ((e.clientX - centerX) / rect.width) * 100;
          let mouseY = ((e.clientY - centerY) / rect.height) * 100;

          mouseX = Math.max(-100, Math.min(100, mouseX));
          mouseY = Math.max(-100, Math.min(100, mouseY));

          const absMouseX = Math.abs(mouseX);

          // 1. 테두리 1 (screen)
          const angle1 = 135 + mouseX * 1.2;
          const opacity1_1 = 0.12 + absMouseX * 0.008;
          const stop1_1 = Math.max(10, 33 + mouseY * 0.3);
          const opacity1_2 = 0.4 + absMouseX * 0.012;
          const stop1_2 = Math.min(90, 66 + mouseY * 0.4);

          // 2. 테두리 2 (overlay)
          const angle2 = 135 + mouseX * 1.2;
          const opacity2_1 = 0.32 + absMouseX * 0.008;
          const stop2_1 = Math.max(10, 33 + mouseY * 0.3);
          const opacity2_2 = 0.6 + absMouseX * 0.012;
          const stop2_2 = Math.min(90, 66 + mouseY * 0.4);

          border1.style.background = `linear-gradient(${angle1}deg, 
                  rgba(255, 255, 255, 0.0) 0%, 
                  rgba(255, 255, 255, ${opacity1_1}) ${stop1_1}%, 
                  rgba(255, 255, 255, ${opacity1_2}) ${stop1_2}%, 
                  rgba(255, 255, 255, 0.0) 100%)`;

          border2.style.background = `linear-gradient(${angle2}deg, 
                  rgba(255, 255, 255, 0.0) 0%, 
                  rgba(255, 255, 255, ${opacity2_1}) ${stop2_1}%, 
                  rgba(255, 255, 255, ${opacity2_2}) ${stop2_2}%, 
                  rgba(255, 255, 255, 0.0) 100%)`;
        });
      </script>
    </body>
  </html>
  ```

근데 요거는 css만 있는게 아니라 js도 같이 포함되어 있음

버튼에 마우스를 갖다 대면 마우스 위치에 따라 테두리에 비치는 빛 각도가 달라짐

처음엔 공통 css 파일을 작성하려고 했으나 위와 같은 코드 구조 때문에 css랑 script 코드를 분리할 수 없다고 판단

⇒ 공통 컴포넌트 하나 만들기

- type으로 button | input | div를 받음
- 표시할 아이콘, 동작할 함수, children을 props로 받기

```html
- button - 아이콘 - 기능할 함수 - input - 크기 <- input이 쓰이는 곳은 선택
체크박스랑 검색창 - 아이콘 - 기능할 함수 - div - children
```

## 다형성 컴포넌트란

> 같은 자료형에 여러가지 타입의 데이터를 대입하여 다양한 결과를 얻어낼 수 있는 성질

- 하나의 컴포넌트가 상황에 따라 여러 다른 HTML 태그(요소)로 렌더링될 수 있는 컴포넌트를 의미합니다.
- "여러(Poly) 형태(Morph)"를 가질 수 있는 컴포넌트입니다.

### 핵심 개념

- 다형성 컴포넌트는 보통 `as` prop (또는 `component`, `is` 등의 이름)을 받음
- `as` prop에 원하는 HTML 태그 이름이나 다른 컴포넌트를 전달하면, 해당 컴포넌트가 그 요소로 렌더링됨

### 왜 사용?

- 컴포넌트의 스타일과 기능은 그대로 재사용하면서
- 시맨틱(의미론적) HTML 태그만 유연하게 변경하고 싶을 때 매우 유용

### 간단한 예시: `Button` 컴포넌트

예를 들어 공통 스타일을 가진 `Button` 컴포넌트가 있다고 가정

1. 기본 버튼 (Default)
   - 코드: `<Button>클릭하세요</Button>`
   - 결과: `<button class="my-button-style">클릭하세요</button>`
2. 링크(a 태그)로 사용
   - 코드: `<Button as="a" href="/home">홈으로</Button>`
   - 결과: `<a class="my-button-style" href="/home">홈으로</a>`
   - (버튼처럼 보이지만, 실제로는 `<a>` 태그로 동작합니다.)
3. 단순 텍스트(span 태그)로 사용
   - 코드: `<Button as="span">제목</Button>`
   - 결과: `<span class="my-button-style">제목</span>`
   - (버튼 스타일을 가졌지만, 기능이 없는 `<span>` 태그입니다.)

> `Button` 컴포넌트 하나로 `button`, `a`, `span` 등 다양한 형태로 "변신"시켜 사용할 수 있습니다.
