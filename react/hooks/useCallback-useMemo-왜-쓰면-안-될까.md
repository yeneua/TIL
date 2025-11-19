# useCallback-useMemo-왜-쓰면-안-될까

## 개념

### `useCallback` - 함수를 기억

```jsx
const fn = useCallback(() => { ... }, [deps]);
```

- 언제: 자식 컴포넌트에 함수 전달할 때

```jsx
// deps가 안 바뀌면 같은 함수 참조 유지
const handleClick = useCallback(() => {
  console.log(count);
}, [count]);

<Child onClick={handleClick} />;
```

### `useMemo`- 값을 기억

```jsx
const value = useMemo(() => 계산식, [deps]);
```

- 언제: 비싼 계산 결과를 재사용할 때

```jsx
// deps가 안 바뀌면 이전 결과 재사용
const filtered = useMemo(() => items.filter((item) => item.active), [items]);
```

## 왜 쓰면 안될까?

### 1. 최적화에도 비용이 든다

`useCallback`, `useMemo` 자체에도 비용이 든다

```jsx
//  불필요한 최적화
function Component() {
  const handleClick = useCallback(() => {
    console.log("clicked");
  }, []);

  return <button onClick={handleClick}>Click me</button>;
}

// 더 간단하고 빠름
function Component() {
  const handleClick = () => {
    console.log("clicked");
  };

  return <button onClick={handleClick}>Click me</button>;
}
```

- 첫 번째 함수에서 `useCallback`은 함수를 메모리에 저장하고, 의존성 배열을 비교하여, 필요시 새 함수를 생성하고 있음
- 일반 함수 선언보다 더 많은 작업을 하고 있음
- 캐시해야 핳 값과 함수가 많아지면 메모리 사용량이 증가함
- 함수 생성 비용이나 값 계산 비용이 비교 연산 비용보다 싸면은 `useCallback`, `useMemo`를 사용하는 것이 오히려 성능을 저하시킴

### 2. 가독성 저하 및 코드 복잡도 증가

불필요한 useCallback과 useMemo는 코드를 읽기 어렵게 만들고, 유지보수 비용을 높임

- 가독성 저하: 일반 변수 할당이나 함수 정의보다 코드가 장황해져서 핵심 로직을 파악하기 어려움

- 의존성 누락 버그: useCallback이나 useMemo를 사용할 때 의존성 배열을 실수로 누락하면 함수나 값 내부에서 오래된(Stale) 상태나 프롭스 값을 참조하는 심각한 버그가 발생함.
