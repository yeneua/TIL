## Default Export

Default로 선언된 모듈은 하나의 파일에서 단 하나의 변수 또는 클래스 등만 export 가능

```tsx
// import
import MyComponent from "./MyDefaultExport";

// export
const MyComponent = () => {};
export default MyComponent;
```

default로 내보낸 모듈은 어떤 이름으로든지 import 가능

```tsx
// import
import MyDefaultComponent from "./MyDefaultExport";

// import
import NewComponent from "./MyDefaultExport";

// export
const MyComponent = () => {};
export default MyComponent;
```

## Named Export

한 파일 내에서 여러 변수/클래스 등을 export 가능

```jsx
// imports
// ex. importing a single named export
import { MyComponent } from "./MyComponent";

// ex. importing multiple named exports
import { MyComponent, MyComponent2 } from "./MyComponent";

// exports from ./MyComponent.js file
export const MyComponent = () => {};
export const MyComponent2 = () => {};
```

해당 모듈을 불러오고자 하는 파일에서 **중괄호**로 감싸서 불러와야 합니다.

[[JavaScript] default export와 named export의 차이점을 알아보자!](https://chiefcoder.tistory.com/47)
