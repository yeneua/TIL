# 프로젝트에 zustand 도입하기

## 1. 관리할 상태 설계

1. `accessToken`

- `accessToken`을 메모리에 저장

2. `user`

- 로그인한 유저 정보
- 필요성 느낀 부분) 회원 정보 수정 화면에서 프로필 이미지를 수정하면 헤더에 바로 반영되지 않음 <- 전역 상태 관리로 해결 가능하다고 생각
- 프로필, 회원 정보 수정, 헤더 '내 정보'를 나타내는 곳이 여러 곳

3. `isLoggedIn`

- `accessToken`이 있다면 `true`, 만료되었다면 `false`로 처리
- `App.tsx`에서 로그인 여부에 따른 컴포넌트 표시 가능

### 토큰 관련 로직

`accessToken`을 메모리에 저장하기 때문에 새로고침하면 사라짐

1. 새로고침 시

   `{withCredentials : true}` 저장되어 있는 `refreshToken`을 이용해 `accessToken` 재발급

2. 사용 중

   accessToken이 만료 -> 401 에러<br/>
   -> `{withCredentials : true}`로 `accessToken` 재발급<br/>
   -> 만약 `refreshToken`이 유효하지 않다면 로그아웃 처리<br/>

<br/>

401 에러는 api 요청을 보냈을 때 응답으로 받을 수 있는것<br/>
그래서 만약 `accessToken`이 만료됐는데 api 요청을 하지 않아서 401에러를 응답받지 못하면?<br/>
-> 아무 요청도 보내지 않기 때문에 문제가 되지않음<br/>
서버 리소스에 접근하지 않기 때문임<br/>
내가 생각했던, `setInterval` 함수로 토큰 만료를 체크하거나 `accessToken` 만료 시간을 계산해 토큰 유효 여부를 체크하는 로직은 계속 네트워크 요청이 가기 때문에 비효율적이라 판단<br/>
-> api 요청이 있을때만 유효성 검사

## 2. zustand 스토어 설정

`authStore.ts`

로그인했을때 accessToken, isLoggedIn 상태 처리를 하고 싶다. 어디에 작성해야하지?
auth.ts의 login함수에서는 api 통신과 관련된 로직만 담는게 좋다.
로그인 페이지 컴포넌트에서 처리

로그인했을때 유저 정보도 함께 상태 세팅해주는 게 좋을 듯 하다 왜? 내비게이션에 항상 유저 정보가 보이니까

```typescript
import { create } from 'zustand'
import type { UserMeResponse, UserMeInfoPatchRequest } from '@/types/User'
import { userAPI } from '@/api/user'

interface AuthState {
  user: UserMeResponse | null
  accessToken: string | null
  isLoggedIn: boolean
  isAuthChecking: boolean // flag 변수
  setAuth: (token: string, userData: UserMeResponse | null) => void
  setUser: (
    partialUser: Partial<UserMeInfoPatchRequest>
  ) => Promise<UserMeResponse> // 유저 상태 일부 업데이트
  logout: () => void
  setAuthChecked: (checked: boolean) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  accessToken: null,
  isLoggedIn: false,
  isAuthChecking: true,

  setAuth: (token: string, userData: UserMeResponse | null) =>
    set({
      accessToken: token,
      isLoggedIn: true,
      user: userData ?? null, // 로그인 할때 유저 정보 불러오기
    }),

  setUser: async (payload) => {
    const updated = await userAPI.patchUserMeInfo(payload)
    set({ user: updated })
    return updated
  },

  logout: () =>
    set({
      accessToken: null,
      isLoggedIn: false,
      user: null,
    }),

  setAuthChecked: (checked) => set({ isAuthChecking: checked }),
}))
```

- `user`

  - 현재 로그인한 유저 정보
  - 로그인 했을 때 유저 정보 가져와서 세팅

- `setAuth`

  - setAuth 액션으로 accessToken, 유저 정보 세팅(최초 로그인 시)

- `setUser`

  - 유저 정보 patch

- `logout`

  - 인증 정보 초기화

- `isAuthChecking`
  - 지금 인증 상태를 확인 중인지 나타내는 flag 변수
  - 인증 확인 중 : true
  - 인증 확인이 끝나면 : false
  - 초기 인증 시에 로딩 화면 표시

## 3. 프로젝트에 상태 연결

### `App.tsx`

```typescript
const location = useLocation()
const setAuth = useAuthStore((state) => state.setAuth)
const setAuthChecked = useAuthStore((state) => state.setAuthChecked)
const logout = useAuthStore((state) => state.logout)
const isAuthChecking = useAuthStore((state) => state.isAuthChecking)
const isLoggedIn = useAuthStore((state) => state.isLoggedIn)

useEffect(() => {
  const handleInitialRefresh = async () => {
    try {
      const response = await reissueToken()
      const me = await userAPI.getUserMeInfo()
      const accessToken = response.accessToken
      setAuth(accessToken, me)
    } catch {
      logout()
    } finally {
      setAuthChecked(false)
    }
  }
  handleInitialRefresh()
}, [setAuth, logout, setAuthChecked])

if (isAuthChecking) {
  return <div>로딩 중...</div>
}

const showHeader = isLoggedIn && !location.pathname.startsWith('/film/room/')
```

- 선택적 구독으로 필요한 상태와 액션만 가져옴
- `App.tsx`는 프로젝트의 첫 진입점임
- zustand는 메모리 기반이라 새로고침하면 날아감
- 따라서 `App.tsx`에 인증 로직 작성
- 토큰 재발급 + 내 정보 조회 => `setAuth`로 초기 상태 저장
- 완료 시에는 인증 상태를 나타내는 flag 변수 `isAuthChecking` `false`로 지정

<br/>

- 인증 과정 중(`isAuthChecking === true`)에는 '로딩 중' 화면 표시
- 로그인 여부에 따라 헤더 표시 여부 결정
  <br/>

- `App.tsx` 진입할때
  - 쿠키가 있으면(`refreshToken` 존재) -> 자동 로그인 성공
  - 없거나 만료 -> `catch`에서 `logout()`

### `Login.tsx`

```typescript
const setAuth = useAuthStore((state) => state.setAuth)
const setAuthChecked = useAuthStore((state) => state.setAuthChecked)

const handleSubmit = async () => {
  const submitData = {
    email,
    password,
  }

  try {
    const response = await authAPI.login(submitData)
    const me = await userAPI.getUserMeInfo()
    setAuth(response.accessToken, me)
    setAuthChecked(false)
    navigate('/gallery')
  } catch (err) {
    console.log(err)
    error('로그인에 실패했습니다.')
  }
}

// 로그아웃
const logout = useAuthStore((state) => state.logout)
const handleLogout = async () => {
  try {
    await authAPI.logout()
    navigate('/login')
    logout()
  } catch {
    error('로그아웃에 실패했습니다. 다시 시도해주세요.')
  }
}
```

- 최초 로그인 시 `accessToken`, 유저 정보 `setAuth`로 저장
- 로그인 완료 후 인증 상태 변수 `false` 설정

### `client.ts`

```typescript
import axios, { AxiosError } from 'axios'
import type { InternalAxiosRequestConfig } from 'axios'
import type { TokenReissueResponse } from '@/types/auth'
import { useAuthStore } from '@/store/authStore'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
})

// 리프레시 중인지 플래그 + 대기열
let isRefreshing = false
let subscribers: Array<(token: string) => void> = []

const onTokenRefreshed = (token: string) => {
  subscribers.forEach((cb) => cb(token))
  subscribers = []
}
const addSubscriber = (cb: (token: string) => void) => subscribers.push(cb)

// 리프레시 요청은 Authorization 없이, 인터셉터도 안 타는 별도 인스턴스 권장
const refreshClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
})

export const reissueToken = async (): Promise<TokenReissueResponse> => {
  const { data } = await refreshClient.post('/auth/tokens')
  return data
}

// 요청 인터셉터
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const { accessToken } = useAuthStore.getState()
    // 토큰 재발급 엔드포인트는 Authorization 금지
    if (!config.url?.includes('/auth/tokens') && accessToken) {
      config.headers['Authorization'] = `Bearer ${accessToken}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const { logout, setAuth } = useAuthStore.getState()

    // 널 가드
    const status = error.response?.status
    const originalRequest = error.config as
      | (InternalAxiosRequestConfig & { _retry?: boolean })
      | undefined

    if (!originalRequest || !(status === 401 || status === 403))
      return Promise.reject(error)

    // 리프레시 요청 자체가 401이면 더 이상 시도하지 않고 로그아웃
    if (originalRequest.url?.includes('/auth/tokens')) {
      logout()
      window.location.href = '/login'
      return Promise.reject(error)
    }

    // 이미 리트라이한 요청은 그대로 실패
    if (originalRequest._retry) {
      return Promise.reject(error)
    }
    originalRequest._retry = true

    try {
      if (!isRefreshing) {
        isRefreshing = true
        const { accessToken } = await reissueToken()
        // 전역 상태 갱신
        setAuth(accessToken, null)
        // 기본 헤더 갱신
        apiClient.defaults.headers.common[
          'Authorization'
        ] = `Bearer ${accessToken}`
        isRefreshing = false
        onTokenRefreshed(accessToken)

        originalRequest.headers = originalRequest.headers ?? {}
        originalRequest.headers['Authorization'] = `Bearer ${accessToken}`
        return apiClient(originalRequest) // 즉시 재시도 (첫 요청이 대기 안 함)
      }

      // 리프레시 중이면 큐에 넣고, 끝나면 재시도
      return new Promise((resolve, reject) => {
        addSubscriber((newToken: string) => {
          try {
            originalRequest.headers = originalRequest.headers ?? {}
            originalRequest.headers['Authorization'] = `Bearer ${newToken}`
            resolve(apiClient(originalRequest))
          } catch (e) {
            reject(e)
          }
        })
      })
    } catch (e) {
      isRefreshing = false
      logout()
      window.location.href = '/login'
      return Promise.reject(e)
    }
  }
)

export default apiClient
```
