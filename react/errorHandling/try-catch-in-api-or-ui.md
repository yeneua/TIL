# try-catch 문 : api 호출하는 곳 vs 사용하는 곳

gemini와 gpt의 답변이 달라서…

## 상황

어제의 순간 api 로직을 작성하는데 습관처럼 api 호출 함수에서 `try-catch`문을 쓰고 있었음

근데 우리는 api 함수를 호출해서 사용하는 곳에서도 `try-catch`문을 쓰고 있는데!! 두 번 작성하는 게 맞나?라는 생각이 들었음

문제의 그 코드

```tsx
import apiClient from '@api/client'
import type { RankingResponse } from '@/types/moment'

export const momentAPI = {
  getDailyMoment: async (): Promise<RankingResponse> => {
    try {
      const response = await apiClient.get('/gallery/ranking/daily')
      return response.data
    } catch (err) {
      console.log(err)
      throw err
    }
  },
}
```

## 둘 다 사용

각각 사용하는 게 맞다

왜?? 각각 역할이 다르기 때문에

`api.ts`

- API 통신 자체 오류를 다룸
- 오류 로깅 혹은 더 구체적인 오류 메시지를 호출자에게 전달

`호출하는 곳`

- API 호출이 실패했을 때 사용자에게 보여줄 ui를 업데이트.. 등
- 사용자 경험과 관련된 오류 처리

⇒ API 호출 로직과 UI+비즈니스 로직을 분리

## 한쪽에서만 써도 될듯

```tsx
export const momentAPI = {
  getDailyMoment: async (): Promise<RankingResponse> => {
    const response = await apiClient.get('/gallery/ranking/daily')
    return response.data
  },
}
```

위처럼 작성하면 오류가 발생했을 때 호출부로 `throw err`가 전달됨

- API 응답 에러에 대해서 특정 로깅이 필요하거나 변환을 해야 할 경우 api 호출 함수에서도 `try-catch`문을 사용하고
- 단순히 호출만 할 경우에는 호출부에서만 `try-catch` 사용으로 충분

## 아!!

아 그래서 `catch` 문에서 그냥 `throw err`를 하면 lint 오류가 났었구나

![alt text](images/try-catch-in-api-or-ui.image-1.png)

쓸모없는 `try-catch`문이라는 뜻이 이제 이해가 됐다.

## 결론

따로 특별하게 에러 핸들링하는 게 없고 `throw err`로 에러만 전달하니 api 호출 함수에서는 `try-catch`문을 생략해도 괜찮을 것 같다.
