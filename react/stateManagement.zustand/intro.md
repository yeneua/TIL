# zustand란?

> 상태 관리 라이브러리

[공식 사이트](https://zustand-demo.pmnd.rs/)

## 사용법

### 스토어 생성

```typescript
import { create } from 'zustand'

interface CounterState {
  // 스토어의 상태 구조 정의
  count: number // 현재 숫자(상태)
  increase: () => void // 숫자 증가 함수
  decrease: () => void // 숫자 감소 함수
}

const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increase: () => set((state) => ({ count: state.count + 1 })),
  decrease: () => set((state) => ({ count: state.count - 1 })),
}))

export default useCounterStore
```

`create()` : 전역 상태 저장소(스토어)를 만드는 함수

`set()` : 상태를 업데이트할 때 쓰는 함수,
새로운 상태를 받거나 현재 상태를 기반으로 상태 변경 가능

### 컴포넌트에서 사용하기

```typescript
import useStore from './store'

export default function Counter() {
  const { count, increase, decrease } = useStore()

  return (
    <div>
      <p>{count}</p>
      <button onClick={increase}>+</button>
      <button onClick={decrease}>-</button>
    </div>
  )
}
```

### 선택적 구독

```typescript
const { count, increase } = useCounterStore()
```

위와 같은 방식으로 가져오게 되면

- count가 변하면 컴포넌트 전체가 리렌더링
- 이 컴포넌트에서 increase만 사용해도 count가 변하면 전체가 리렌더링됨

👉 그래서 선택적 구독 방식 사용

```typescript
const count = useCounterStore((state) => state.count)
const increase = useCounterStore((state) => state.increase)
```

- `(state) => state.값`
- 값이 변할 때만 해당 훅을 쓰는 컴포넌트가 리렌더링

특정 상태가 변할 때만 그 상태를 사용하는 컴포넌트가 다시 실행되도록 함

### 로컬 스토리지에 저장하기

zustand는 메모리 기반이기 때문에 새로고침하면 상태가 초기화 됨<br/>
`persist` 미들웨어를 사용해서 localStorage, sessionStorage에 보관 가능

#### i) 기본 사용법

```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface CounterState {
  count: number
  increase: () => void
  decrease: () => void
  reset: () => void
}

export const useCounterStore = create<CounterState>()(
  persist(
    (set) => ({
      count: 0,
      increase: () => set((s) => ({ count: s.count + 1 })),
      decrease: () => set((s) => ({ count: s.count - 1 })),
      reset: () => set({ count: 0 }),
    }),
    {
      name: 'counter', // localStorage key 이름
    }
  )
)
```

#### ii) 일부만 저장하고 싶을 때

```typescript
export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      accessToken: null,
      nickname: '',
      theme: 'light',
      setToken: (t) => set({ accessToken: t }),
      setNickname: (n) => set({ nickname: n }),
      toggleTheme: () =>
        set({ theme: get().theme === 'light' ? 'dark' : 'light' }),
    }),
    {
      name: 'auth',
      // storage에 저장할 필드만 선택
      partialize: (state) => ({
        accessToken: state.accessToken,
        theme: state.theme,
      }),
    }
  )
)
```

#### iii) sessionStorage에 저장

```typescript
import { createJSONStorage, persist } from 'zustand/middleware'

export const useTempStore = create<{ step: number; next: () => void }>()(
  persist(
    (set) => ({
      step: 1,
      next: () => set((s) => ({ step: s.step + 1 })),
    }),
    {
      name: 'wizard',
      storage: createJSONStorage(() => sessionStorage),
    }
  )
)
```
