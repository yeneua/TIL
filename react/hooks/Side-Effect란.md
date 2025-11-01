# Side Effect란?

useEffect 훅을 공부하다가 side effect에 대해 정리해본다.

## 개요

- react의 함수 컴포넌트는 순수 함수(pure function)를 지향함
- 동일한 입력(props, state)에 대해 항상 동일한 출력(JSX)을 반환해야함
- 이 과정에서 시스템의 다른 부분과 상호작용하는 모든 작업을 **Side Effect**라고 함
- 컴포넌트가 화면에 렌더링된 이후에 비동기로 처리되어야하는 부수적인 효과들

## 예시

1. API 호출(data fetching)

- 컴포넌트의 외부 상태와 상호작용하는 것

2. DOM 직접 조작

- react는 virtual DOM을 통해 렌더링을 관리함
- `document.getElementById(...)`를 통해 직접 DOM을 조작하는 것은 side effect임

3. 구독(subscriptions)

- `window.addEventListener('',...)` <- 브라우저 이벤트를 구독하는 해우이
- 타이머 함수 사용
- websocket, firebase 같은 실시간 데이터 소스에 연결하고 구독하는 행위

4. 브라우저 API 사용

- `localStorage`나 `sessionStorage`에 데이터를 읽거나 쓰는 작업
- 브라우저라는 외부 저장소와 상호작용하는 것

## 왜 `useEffect`로 분리해야 할까?

1. 렌더링과 직접적인 관련이 없다.

- ui를 그리는 과정동안 API 호출이 완료되기를 기다릴 필요가 없음

2. 실행 시점 제어 必

- 값에 따라 실행 시점이 다름

3. 정리 필요

- `setInterval`이나 `addEventListener`는 컴포넌트가 사라질 떄 해제해야함 -> 메모리 누수(memory leak) 일으킴

<details>
<summary>왜 메모리 누수??</summary>
<div markdown="1">

1. 컴포넌트가 처음 마운트될 때 타이머 함수, 이벤트 리스너가 등록됨
2. 사용자가 다른 페이지로 이동하거나 화면에서 컴포넌트가 사라지면 등록된 작업을 해제해야됨
   -> 그렇지 않으면 계속 메모리에 작업이 쌓이게 됨

**해결책**

- `setInterval` 함수 -> `clearInterval` 함수 호출
- `addEventListener` 함수 -> `removeEventListener` 호출

```js
useEffect(() => {
  // 1. 임무 등록 (setInterval)
  const timerId = setInterval(() => {
    console.log("1초가 지났습니다...");
  }, 1000);

  // 2. 임무 등록 (addEventListener)
  const handleScroll = () => {
    console.log("스크롤 중...");
  };
  window.addEventListener("scroll", handleScroll);

  // 3. 뒷정리 함수(임무 해제)를 반환
  // 이 함수는 컴포넌트가 사라지기 직전에 실행됩니다.
  return () => {
    console.log("컴포넌트가 사라집니다. 뒷정리 시작!");

    // 등록했던 타이머 해제
    clearInterval(timerId);

    // 등록했던 이벤트 리스너 해제
    window.removeEventListener("scroll", handleScroll);
  };
}, []); // 빈 배열: 마운트 시 1회만 실행
```

</div>
</details>

## 결론

- `useEffect`는 이러한 side effect들을 react의 순수한 렌더링 흐름과 분리하여
- **렌더링이 완료된 후** 혹은 **특정 값이 변경된 후**에만 실행되도록 스케줄링
