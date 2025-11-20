### 주저리

25.11.20 세번째 프로젝트, 자율 프로젝트가 끝났다.

싸피에서는 깃랩을 사용하기 때문에 보통 프로젝트가 마무리 되면 소스코드를 깃허브로 옮긴다.

소스코드를 옮길 때 미러링 방식을 사용하면 커밋 로그가 전부 남아서 이 방식을 주로 사용한다는 얘기를 들었다.

근데 그냥 깃 저장소를 push해도 커밋 로그는 남는데 ??! 하는 생각이 들어서 어떤 차이가 있는지 찾아봤다.

## 1. 일반적인 clone & push

```bash
# gitlab에서 clone
git clone [Gitlab 주소]

# 새로운 github 원격 추가
cd [프로젝트 폴더]
git remote add origin [github 주소]

# github로 push
git push origin main
git push -u origin --all # 모든 브랜치 푸시
git push origin --tags # 모든 태그 푸시
```

## 2. 미러링(mirroring) 방식

- `--mirror` 옵션을 사용하면 저장소의 모든 것을 있는 그대로 복제하여 옮길 수 있음
- 저장소를 완전히 이전할 때 권장되는 방법
- `--mirror`를 사용하면 저장소의 모든 내부 구조와 이력이 손실 없이 완벽하게 복사됨

```bash
# gitlab 저장소 미러링 클론
git clone --mirror [gitlab 주소]

# github 주소로 원격 설정 변경
cd [프로젝트 폴더].git # 미러 클론시 자동으로 .git 확장자 폴더가 생성됨
git remote set-url origin [github 주소]
git remote add origin [github 주소]

# github로 미러 푸시
git push --mirror

```

##

그럼 mr은??
모든 브랜치 복사랑 미러링 무슨 차이?

## 궁금한거

**push할때 `--all` 태그로 모든 브랜치를 푸시하는 거랑 `--mirror`랑 뭐가 달라**

- 일반적인 clone&push는 기본적으로 작업 환경을 만드는 것이 목적임

- 모든 브랜치와 태그를 푸시하더라도 일부 정보가 누락될 수 있음

- git 저장소 : 단순히 소스코드 파일뿐만이 아니라 git이 프로젝트의 이력과 상태를 관리하는 데 필요한 모든 데이터를 말함(커밋, 브랜치, 태그, 참조 등)

**미러링하면 MR 기록도 다 남나??**

- 아니다
- 미러링은 git 저장소 자체의 이력(커밋, 브랜치, 태그 등)을 완벽하게 복제하는 기능임
- MR이나 PR 같은 기록은 git 저장소 정보가 아니라 gitlab, github 서비스의 종속적인 정보임

**미러링 푸시하려면 미러링 클론이 필요한가?**

- 그렇다.
- 미러링 클론을 해서 저장소를 복제해야함
- 미러링 푸시를 하지 위해서는 로컬 저장소가 bare repository 형태로 준비되어 있어야 함
- 미러링 클론을 하면 로컬에 소스 코드 파일은 없는 순수한 bare repository가 생성됨
- 이 bare 저장소에는 저장소의 모든 이력, 브랜치, 태그, 참조 정보가 완벽하게 복사되어 들어옴
- 이 시점에서 모든 정보는 로컬에 있음
