## 1. 기존 코드 문제

```tsx
const [graphData, setGraphData] = useState<GraphVisualizationResponse | null>(
  null
);
const [isLoading, setIsLoading] = useState(true);

useEffect(() => {
  const fetchGraphView = async () => {
    try {
      setIsLoading(true);
      const response = await graphAPI.getGraphVisualization();
      setGraphData(response);
    } catch (error) {
      console.error("그래프 데이터를 불러오는데 실패했습니다:", error);
    } finally {
      setIsLoading(false);
    }
  };
  void fetchGraphView();
}, []);
```

- 서버에서 가져온 상태를 `useState`를 이용해서 직접 관리하고 있음 ⇒ 클라이언트 상태 관리

## 2. 수정

### 2.1. 새로운 커스텀 훅 생성

```tsx
// useGraphVisualization.ts
export function useGraphVisualization() {
  return useQuery({
    queryKey: ["graphs", "visualization"],
    queryFn: () => graphAPI.getGraphVisualization(),
    staleTime: 2 * 60 * 1000, // 2분 캐시
    retry: 2, // 실패 시 2번 재시도
  });
}
```

- `queryKey`를 `['graphs', 'visualization']`으로 설정
- 자동 캐싱 (2분)
- 자동 재시도 (2회)

### 2.2. Graph 컴포넌트 최적화

**변경 전**

```tsx
// Graph.tsx
const [graphData, setGraphData] = useState<GraphVisualizationResponse | null>(
  null
);
const [isLoading, setIsLoading] = useState(true);

useEffect(() => {
  const fetchGraphView = async () => {
    try {
      setIsLoading(true);
      const response = await graphAPI.getGraphVisualization();
      console.log("response", response);
      setGraphData(response);
    } catch (error) {
      console.error("그래프 데이터를 불러오는데 실패했습니다:", error);
    } finally {
      setIsLoading(false);
    }
  };
  void fetchGraphView();
}, []);
```

**변경 후**

```tsx
const { data: graphData, isLoading, isError } = useGraphVisualization();

// 성능 최적화: 콜백 메모이제이션
const nodeColorCallback = useCallback(() => "#FFFFFF", []);
const linkWidthCallback = useCallback(
  (link: { score: number }) => link.score * 2,
  []
);
const particleWidthCallback = useCallback(
  (link: { score: number }) => link.score * 1.5,
  []
);

// 성능 최적화: 데이터 객체 메모이제이션
const memoizedGraphData = useMemo(() => {
  if (!graphData) return { nodes: [], links: [] };
  return {
    nodes: graphData.nodes,
    links: graphData.links,
  };
}, [graphData?.nodes, graphData?.links]);
```

## 3. 주요 개선 사항

### 3.1. TanStack Query 도입

- 이전: 수동 `useState` + `useEffect` 관리
- 현재: React Query로 자동 캐싱 & 에러 처리

### 3.2. 성능 최적화

- 메모이제이션된 콜백: ForceGraph3D에 전달되는 모든 함수를 `useCallback`으로 최적화
- 메모이제이션된 데이터: `graphData` 객체를 `useMemo`로 최적화

## 4. React 19 컴파일러 대응

현재 프로젝트는 React 18.3.1을 사용 중이므로:

- `useCallback`/`useMemo` 최적화가 필수
- 특히 3D 라이브러리 같은 무거운 컴포넌트는 수동 최적화 효과가 큼
- React 19로 업그레이드 시 일부 메모이제이션 제거 가능 (하지만 ForceGraph3D 같은 외부 라이브러리는 여전히 필요)
