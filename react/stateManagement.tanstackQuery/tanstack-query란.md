## > 개념

> **서버 상태를 관리하기 위한 라이브러리**
> 네트워크에서 가져온 데이터를 상태 관리할 수 있게 도와주는 도구

<details>
<summary>서버 상태</summary>

1. 로딩(Loading)
   <br/>

- 데이터를 서버로부터 가져오는 동안의 상태를 나타냄
  <br/>
- 서버 요청이 진행 중이고 응답을 기다리는 동안 로딩 상태가 활성화됨
  <br/>

2. 성공(Success)
   <br/>

- 서버 요청이 성공적으로 완료되었고 데이터를 성공적으로 받아왔을 때의 상태
  <br/>
- 서버로부터 받은 데이터를 활용하여 화면을 업데이트하거나 다른 작업을 수행 가능
  <br/>

3. 실패(Error)
   <br/>

- 서버 요청이 실패했을 때의 상태
  <br/>
- 서버 요청 중에 오류가 발생하거나 서버로부터 예상치 못한 응답을 받았을 때 실패 상태가 발생
  <br/>

4. 캐싱(Caching)
   <br/>

- 서버에서 가져온 데이터를 캐시에 저장하여 이후에 같은 요청이 있을 때 서버로부터 데이터를 다시 가져오지 않고 캐시된 데이터를 사용할 수 있음
  <br/>
- 이를 통해 애플리케이션의 응답 속도를 향상시킬 수 있음
  <br/>

5. 리프레시(Refreshing)
   <br/>

- 서버로부터 데이터를 갱신하는 동안의 상태
  <br/>
- 새로운 데이터를 가져오거나 업데이트 된 데이터로 기존 데이터를 대체하는 과정에서 리프레시 상태가 활성화됨
</details>

### 옵저버 패턴

- Subject
  - 자신의 상태를 가짐
  - 상태가 변경되면 자신을 구독하는 observer에게 알림을 보냄
- Observer
  - subject를 구독(등록)함
  - 알림을 받으면 특정 동작 수행

**tanstack query에서**

- Subject
  - 캐시(Cache)에 저장된 `query`(데이터)
- Observer
  - `useQuery` 훅을 사용한 react 컴포넌트
  - `useQuery`를 호출하는 것 === 옵저버로 등록하는 행위

## > 핵심 기능

1. 강력한 캐싱 (Caching)

   - `queryKey`라는 고유한 키를 기준으로 API 응답 데이터를 메모리에 캐싱
   - 동일한 `queryKey`로 다시 데이터를 요청하면 API를 또 호출하는 대신 캐시된 데이터를 즉시 반환함

1. 자동 리패칭 (Automatic Refetching)

   - 데이터가 **오래되었을(stale)** 때 자동으로 최신 데이터를 다시 가져옵니다.
   - 기본 트리거
     - 컴포넌트가 마운트될 때
     - 브라우저 창이 다시 포커스될 때
     - 네트워크가 재연결될 때

1. 간편한 UI 상태 관리

   - 데이터를 가져오는 중(`isLoading`), 실패(`isError`), 성공(`isSuccess`) 상태와 실제 데이터(`data`), 에러 객체(`error`)를 자동으로 관리하고 반환해줌
   - 이로 인해 수많은 `useState`와 `useEffect` 보일러플레이트 코드가 사라짐

1. 데이터 수정 (Mutations)

   - `useMutation` 훅을 사용해 데이터를 생성(Create), 수정(Update), 삭제(Delete)하는 작업을 쉽게 처리할 수 있음
   - 데이터 수정 성공 시 관련된 `useQuery` 캐시를 자동으로 무효화(invalidate)시켜 데이터를 최신 상태로 업데이트할 수

1. 페이지네이션 및 무한 스크롤
   - `useInfiniteQuery` 같은 전용 훅을 제공하여 까다로운 페이지네이션과 무한 스크롤 로직을 쉽게 구현할 수 있음

## > 사용하기

### 1. 환경 설정

앱 전체를 `QueryClientProvider`로 감싸야함

```tsx
// main.tsx
import ReactDOM from 'react-dom/client';
import App from './App';
**import { QueryClient, QueryClientProvider } from '@tanstack/react-query';**

// 1. QueryClient 인스턴스 생성
**const queryClient = new QueryClient();**

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {/* 2. 앱 전체에 client 제공 */}
    **<QueryClientProvider client={queryClient}>**
      <App />
    **</QueryClientProvider>**
  </React.StrictMode>
);
```

### 2. 데이터 가져오기 (useQuery - GET)

```tsx
// types.ts (공통 타입 정의)
export interface Todo {
  id: number;
  title: string;
  completed: boolean;
}

// Todos.tsx
**import { useQuery } from '@tanstack/react-query';**
import { Todo } from './types'; // 0. Todo 타입을 import

// 1. API 호출 함수 (Promise<Todo[]> 반환 타입 명시)
const fetchTodos = async (): Promise<Todo[]> => {
  const response = await fetch('https://api.example.com/todos');
  if (!response.ok) {
    throw new Error('데이터를 불러오는 데 실패했습니다.');
  }
  return response.json();
};

function Todos() {
  // 2. useQuery 사용(호출) (제네릭으로 TData와 TError 타입을 명시)
  **const { isLoading, isError, data, error } = useQuery<Todo[], Error>({
    queryKey: ['todos'], // 👈 이 쿼리를 식별하는 고유 키
    queryFn: fetchTodos, // 👈 데이터를 가져올 함수
  });**

  // 3. 로딩 상태 처리
  if (isLoading) {
    return <span>로딩 중...</span>;
  }

  // 4. 에러 상태 처리
  if (isError) {
    // error가 Error 타입으로 지정되었으므로 .message 접근 가능
    return <span>에러 발생: {error.message}</span>;
  }

  // 5. 성공 상태 처리
  return (
    <ul>
      {/* data가 Todo[] | undefined 이므로, 옵셔널 체이닝(?.map) 사용 */}
      {data?.map((todo) => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  );
}
```

1. **`useQuery` 훅 호출 및 설정**

- `queryKey: ['todos']` (필수)
  - 데이터 요청을 식별하는 고유한 ID
  - 이 `queryKey`를 사용해 데이터를 캐싱(저장)함
  - 만약 앱의 다른 컴포넌트에서 `useQuery`를 `queryKey: ['todos']`로 또 호출하면 TanStack Query는 API를 다시 호출하는 대신 캐시된 데이터를 즉시 반환함
- `queryFn: fetchTodos` (필수)
  - 실제로 데이터를 가져오는 함수입니다.
  - `queryFn`은 반드시 Promise를 반환하는 함수여야 함 (코드의 `fetchTodos`가 `async` 함수이므로 Promise를 반환함)
  - `queryKey`에 해당하는 데이터가 캐시에 없거나 데이터가 오래되었을(stale) 때 이 함수가 자동으로 실행됩니다.
- `useQuery<Todo[], Error>` (타입스크립트)
  - 제네릭을 사용해 `useQuery`에게 타입을 알려주는 것
  - `<Todo[], Error>`는 "_이 쿼리가 성공하면 `data`의 타입은 `Todo[]`가 될 것이고, 실패하면 `error`의 타입은 `Error`가 될 것이다_"라고 명시하는 것
  - `data` 변수는 `Todo[]` 타입으로 `error` 변수는 `Error` 타입으로 자동 완성 및 타입 체크가 가능해짐

**2. `useQuery`가 반환하는 상태값**

`useQuery`는 `useState`와 `useEffect`를 합친 것과 같음

데이터 요청의 현재 상태를 나타내는 값들을 객체로 반환함

```tsx
const { isLoading, isError, data, error } = useQuery(...)
```

- `isLoading: boolean`
  - "지금 데이터를 처음 가져오는 중인가?"를 나타냄
  - 데이터가 아직 캐시에 없고 `queryFn`(fetchTodos)이 실행되어 응답을 기다리는 동안 `true`가 됨
  - 코드는 이 값을 사용해 "로딩 중..." 메시지를 표시함
- `isError: boolean`
  - "데이터 요청이 실패했는가?"를 나타냅니다.
  - `queryFn`이 Promise `reject`를 하거나 `throw new Error()`를 실행하면 `true`가 됨
  - 코드는 이 값을 사용해 "에러 발생..." 메시지를 표시함
- `error: Error`
  - `isError`가 `true`일 때 `queryFn`에서 발생한 실제 에러 객체가 여기에 담깁니다.
  - `useQuery<..., Error>`라고 타입을 지정했기 때문에 `error.message` 속성을 안전하게 사용할 수 있습니다.
- `data: Todo[] | undefined`
  - "데이터 요청이 성공했을 때의 실제 데이터"입니다.
  - `isLoading`이 `true`일 때는 `data`가 `undefined`임 (아직 데이터가 없으므로)
  - `fetchTodos`가 성공적으로 `Todo[]`를 반환하면 그 데이터가 여기에 저장되고 컴포넌트가 리렌더링됨

### 3. 데이터 생성하기 (useMutation - POST)

```tsx
// AddTodo.tsx
**import { useMutation, useQueryClient } from '@tanstack/react-query';**
import { useState } from 'react';
import { Todo } from './types'; // 0. Todo 타입을 import

// 1. POST 요청을 보낼 API 함수 (인자 및 반환 타입 명시)
const addTodo = async (newTodoTitle: string): Promise<Todo> => {
  const response = await fetch('https://api.example.com/todos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: newTodoTitle, completed: false }),
  });
  if (!response.ok) {
    throw new Error('Todo 추가 실패');
  }
  return response.json();
};

function AddTodo() {
  const [title, setTitle] = useState<string>('');
  **const queryClient = useQueryClient(); // 👈 QueryClient 인스턴스 가져오기**

  **// 2. useMutation 사용
  // mutationFn(addTodo)의 타입을 기반으로 TData(Todo), TVariables(string)가 추론됨
  const mutation = useMutation({
    mutationFn: addTodo, // 👈 데이터를 수정/생성할 함수
    onSuccess: () => {
      // 3. 뮤테이션 성공 시, 'todos' 쿼리를 무효화시킴
      queryClient.invalidateQueries({ queryKey: ['todos'] });
      setTitle(''); // 입력창 비우기
    },
    onError: (error: Error) => { // error 타입을 명시적으로 Error로 지정
      console.error(error.message);
    },
  });**

  // 폼 이벤트 타입 명시
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (title) {
      // 4. mutate 함수 호출 (인자 title은 'addTodo'의 인자 타입(string)과 일치)
      mutation.mutate(title);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        // input 이벤트 타입 명시
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)}
        disabled={mutation.isPending} // 👈 로딩 중일 때 입력 비활성화
      />
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? '추가 중...' : 'Todo 추가'}
      </button>
    </form>
  );
}
```

**1. useMutation 훅 설정**

- `mutationFn: addTodo` (필수)
  - "이 뮤테이션이 실행될 때, 실제로 어떤 함수를 호출해야 하나요?"를 의미합니다.
  - 여기서는 `// 1.`에서 정의한 `addTodo` (POST 요청) 함수를 지정함
  - `useMutation`은 `addTodo` 함수의 타입(인자로 `string`을 받고 `Promise<Todo>`를 반환)을 자동으로 추론함
- `onSuccess: () => { ... }` (성공 시 콜백)
  - `mutationFn`(즉, `addTodo` 함수)이 성공적으로 완료되면 이 함수가 실행됨
  - 이 부분이 `useMutation`의 핵심
- `onError: (error: Error) => { ... }` (실패 시 콜백)
  - `mutationFn`이 `throw new Error()` 등으로 실패하면 이 함수가 실행됨

**2. useQueryClient와 invalidateQueries**

- `useQueryClient()`: TanStack Query의 "두뇌" 또는 "제어 센터"에 접근하는 훅입니다.
- `queryClient.invalidateQueries(...)`: "쿼리 무효화"를 의미합니다.
  - 이 코드는 `queryClient`에게 **"야, `queryKey`가 `['todos']`인 데이터는 이제 낡았어(stale)! 더 이상 최신 데이터가 아니야!"**라고 알려주는 것입니다.
- 그럼 어떻게 되나요?:
  - 이전에 `Todos.tsx` 컴포넌트에서 `useQuery({ queryKey: ['todos'], ... })`를 사용했었죠?
  - `invalidateQueries`가 호출되는 즉시, TanStack Query는 `['todos']` 키를 구독(observing)하고 있던 모든 `useQuery`를 찾아냅니다.
  - 그리고 데이터가 낡았으니 자동으로 다시 가져와(refetch) \*\*라고 명령합니다.
  - 결과적으로, `Todos.tsx` 컴포넌트는 `fetchTodos`를 자동으로 다시 호출하고 방금 추가된 `todo` 항목이 포함된 새 목록을 서버에서 받아와 화면을 업데이트함

⇒ AddTodo 컴포넌트는 Todos 컴포넌트의 존재나 setTodos 같은 상태 업데이트 함수를 전혀 알 필요가 없음. "데이터가 낡았다"고 선언만 하면 관련된 모든 UI가 알아서 최신 상태로 동기화됩니다.

### queryKey

- `queryKey`는 전역적(globally)으로 동작
- 어떤 컴포넌트에서든 동일한 `queryKey`를 사용하면 동일한 캐시 데이터를 공유하고 구독하게 됩니다.
- 어떤 컴포넌트에서든 그 `queryKey`를 `invalidate`(무효화)시키면, 그 키를 구독하던 모든 컴포넌트가 자동으로 리패치(refetch)됨

## > 참고

[Tanstack Query(react-query) 자세히보기 🔎](https://velog.io/@boyeon_jeong/Tanstack-Query-%EC%BA%90%EC%8B%9C-%ED%99%9C%EC%9A%A9)

[TanStack Query(React Query) 핵심 정리https://www.heropy.dev/p/HZaKIE](https://www.heropy.dev/p/HZaKIE)
