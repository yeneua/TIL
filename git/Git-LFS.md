LFS란?

- Git Large File Storage
- 깃에서 용량을 큰 파일을 업로드하거나 다운로드 할 때 사용하는 기능
- 대용량 파일 관리 기능
- git lfs를 사용하면 git 저장소 외부에 대용량 파일을 저장하고 git 저장소에는 대용량 파일의 참조만 저장함

## 장점

- git 저장소 크기를 줄일 수 있음
- git 저장소를 복제하거나 전송하는 데 시간 단축

## 사용법

1. git 저장소에 git lfs 추가

```bash
git lfs install
```

2. 대용량 파일을 git 저장소에 추가

```bash
git add my_large_file
```

3. 대용량 파일을 lfs에 등록

```bash
git lfs track my_large_file
```

4. 대용량 파일 커밋

```bash
git commit -m "Add large file"
```

### 그러면 대용량 파일은 어디에 저장되는데?

- 실제 대용량 파일은 별도의 Git LFS 서버에 저장됨
