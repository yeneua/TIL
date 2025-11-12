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
