## 상황

```typescript
import { useState, useEffect } from 'react'
import { userAPI } from '@api/user'
import type { UserMeResponse } from '@/types/User'
import { useToast } from '@/hooks/useToast'


const ProfileView = () => {
  const { error } = useToast()
  const [myInfo, setMyInfo] = useState<UserMeResponse | null>(null)

  useEffect(() => {
    const fetchMyInfo = async () => {
      try {
        const myData = await userAPI.getUserMeInfo()
        setMyInfo(myData)
      } catch (err) {
        error('내 정보를 불러오는 데 실패했습니다.')
      }
    }

    fetchMyInfo()
  }, []) // 이 부분
```

**⚠️에러 메시지**

```
React Hook useEffect has a missing dependency: 'error'. Either include it or remove the dependency array.eslintreact-hooks/exhaustive-deps
```

## 원인

에러 원인 -> `useEffect` 내부에서 사용한 `error`가 의존성 배열에 없기 때문

useEffect 내부에서 참조하는 모든 외부 변수나 함수가 의존성 배열에 포함되었는지 검사함

👉왜??

1. 최신 값 보장

- `useEffect` 안에서 `error()`를 사용하는데
- error`를 의존성 배열에 안넣으면
- 옛날의 `error()` 함수를 계속 사용함
- 최신 로직 반영 X

2. 함수 재생성 대비

- 함수는 내부에서 재생성될 가능성 o
- 의존성 배열에 안넣으면 업데이트 반영 안됨

3. react 규칙

- 외부 참조 값을 반드시 의존성 배열에 넣어야함

## 해결

✅ 에러 메세지 대로 `error`를 의존성 배열에 추가

무한 호출이 발생...

👉 어떻게 해야할까?

## 참고한 글

[React 오류: React Hook useEffect has a missing dependency: 'selectedItems'. Either include it or remove the dependency array.](https://improvise0828.tistory.com/203)

[[ERROR] React Hook useEffect has missing dependencies: ... Either include them or remove the dependency array react-hooks/exhaustive-deps](https://mungchstudy.tistory.com/95)

[useEffect 리액트 공식 문서](https://ko.react.dev/reference/react/useEffect#wrapping-effects-in-custom-hooks)

[[에러 해결] React Hook useEffect has missing dependencies: ... Either include them or remove the dependency array react-hooks/exhaustive-deps](https://velog.io/@wlwl99/Github-Actions-%EB%B9%8C%EB%93%9C-%EC%A4%91-React-Hook-useEffect-has-missing-dependencies-...-Either-include-them-or-remove-the-dependency-array-react-hooksexhaustive-deps)

[Fix the "Function makes the dependencies of useEffect Hook change on every render" warning in React
](https://typeofnan.dev/fix-function-makes-the-dependencies-of-useEffect-hook-change-on-every-render-warning-in-react/)
