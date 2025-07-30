## 상황

로그인 페이지에 `[ ] 자동 로그인` 체크 박스 존재

백에서는 autoLogin 이라는 체크 옵션을 받고 있지 않음!

그럼 자동 로그인을 어떻게 구현해야될까?

## 생각

현재 우리는 jwt 토큰 인증 방식 과정임

로그인을 하면 accessToken, refreshToken 응답이 오고

accessToken은 localStorage, refreshToken은 HttpOnly 쿠키로 저장되고 있음

<details>
<summary>토큰 코드</summary>
<div markdown="1">

```java
@Override
    public LoginResponse login(LoginRequest loginRequest, HttpServletResponse response) {
        User user = userRepository.findByEmail(loginRequest.getEmail())
            .orElseThrow(() -> new RuntimeException("아이디 또는 비밀번호가 일치하지 않습니다."));

        if (!encoder.matches(loginRequest.getPassword(), user.getPassword())) {
            throw new RuntimeException("아이디 또는 비밀번호가 일치하지 않습니다.");
        }

        String token = jwtUtil.generateToken(user.getUuid());
        String refreshToken = jwtUtil.generateRefreshToken(user.getUuid());

        // 쿠키에 refreshToken 저장
        Cookie refreshTokenCookie = new Cookie("refreshToken", refreshToken);
        refreshTokenCookie.setHttpOnly(true); // JS에서 접근 못하도록
        refreshTokenCookie.setSecure(true); // HTTPS에서만 전송되도록
        refreshTokenCookie.setPath("/"); // 모든 경로에서 접근 가능하도록
        refreshTokenCookie.setMaxAge(7 * 24 * 60 * 60);

        response.addCookie(refreshTokenCookie);

        return LoginResponse.builder()
            .accessToken(token)
            .userUuid(user.getUuid())
            .nickname(user.getNickname())
            .profileUrl(user.getProfileUrl())
            .build();
    }

```

</div>
</details>
<br/>
그리고 accessToken 만료 시 재발급 요청 로직을 작성해둠

<br/>
따라서

| accessToken | refreshToken |                                                                                                                                                             |
| ----------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 유효        | 유효         | 정상 동작                                                                                                                                                   |
| 만료        | 유효         | refreshToken을 이용해서 accessToken 재발급 로직 처리                                                                                                        |
| 유효        | 만료         | accessToken이 만료되기 전까지 정상적으로 사용 가능, accessToken이 만료되거나 로그아웃하면 재로그인 必, 재로그인 시 accessToken, refreshToken 새로 발급 받음 |
| 만료        | 만료         | 재로그인 必                                                                                                                                                 |

… refreshToken이 만료되어서 재로그인 해야되는 경우 사용자에게 “세션 만료” 문구를 띄워주는게 ux적으로 좋을듯

## 결론

이미 자동 로그인 방식으로 동작하고 있기 때문에<br/>
자동 로그인 박스 없애기
