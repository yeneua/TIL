## `import React from 'react'`를 꼭 해야할까?

**👉 react 17부터는 안해도됨**

17 버전 이전에는 jsx 변환을 위해 react를 import 해왔음

- 브라우저는 jsx를 완전히 이해하지 못하기 때문에
- Babel이나 Typescript 같은 컴파일러로 jsx를 vanila javascript로 변환했었음

```javascript
import React from 'react'

const App = () => <h1>Hello, world!</h1>
```

위와 같은 코드를 아래와 같이 바꿔서 브라우저는 이해함

```javascript
const element = React.createElement('h1', null, 'Hello world!')
```

Babel이 jsx 코드를 변환할 때 `React.createElement`를 쓰기 때문에 import React가 필요했었음

<br/>

**👉 17 버전으로 업그레이드하면서 React를 import 하지 않고도 jsx 사용이 가능해짐**

따라서 import React 생략 가능!

## 참고한 글

[Introducing the New JSX Transform](https://legacy.reactjs.org/blog/2020/09/22/introducing-the-new-jsx-transform.html)

[React를 import 하지 않아도 되는 이유](https://velog.io/@nearworld/React%EB%A5%BC-import-%ED%95%98%EC%A7%80-%EC%95%8A%EC%95%84%EB%8F%84-%EB%90%98%EB%8A%94-%EC%9D%B4%EC%9C%A0)

[import React from 'react' 생략하는 법](https://feb-dain.tistory.com/6)
