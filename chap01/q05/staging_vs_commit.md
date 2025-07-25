# Git: 스테이징 영역과 커밋의 차이

Git에서 버전을 관리할 때 가장 기본이 되는 개념 중 두 가지가 바로 **스테이징 영역(Staging Area)**과 **커밋(Commit)**입니다. 이 둘의 차이를 이해하는 것은 Git을 효과적으로 사용하는 데 매우 중요합니다.

---

## 1. 스테이징 영역 (Staging Area / Index)

스테이징 영역은 **"다음 커밋에 포함될 변경 사항들을 미리 준비해두는 곳"**이라고 생각할 수 있습니다. 작업 디렉토리에서 수정한 파일 중 다음 커밋에 포함하고 싶은 변경 사항들만 골라 이 영역에 추가합니다.

* **역할**: 작업 디렉토리(`Working Directory`)와 실제 저장소(`Repository`) 사이의 중간 단계입니다.
* **명령어**: 주로 `git add <file_name>` 또는 `git add .` 명령어를 사용하여 파일을 스테이징 영역에 추가합니다.
* **특징**:
    * **선택적 포함**: 전체 파일을 한꺼번에 스테이징 할 수도 있고, 파일 내의 특정 변경 사항(덩어리/hunk)만 스테이징 할 수도 있습니다. 이를 통해 불필요한 변경 사항을 커밋에서 제외할 수 있습니다.
    * **임시 저장**: 스테이징 영역에 추가된 변경 사항은 아직 Git 저장소에 영구적으로 기록된 것이 아닙니다. Git은 이 영역에 있는 내용만을 바탕으로 커밋을 생성합니다.
    * **변경 사항 미리 보기**: `git status` 명령어를 통해 스테이징 된 파일 목록을 확인할 수 있으며, `git diff --staged` 명령어를 통해 스테이징 된 변경 사항이 실제 커밋될 내용과 어떻게 다른지 미리 볼 수 있습니다.

---

## 2. 커밋 (Commit)

커밋은 **"스테이징 영역에 준비된 변경 사항들을 Git 저장소에 영구적으로 기록하는 작업"**입니다. 각 커밋은 프로젝트의 특정 시점 스냅샷을 나타내며, 고유한 ID(해시 값)를 가집니다.

* **역할**: 스테이징 영역의 스냅샷을 찍어 Git 데이터베이스에 저장하고, 해당 변경 사항에 대한 메시지를 기록합니다.
* **명령어**: `git commit -m "커밋 메시지"` 명령어를 사용하여 커밋을 생성합니다.
* **특징**:
    * **영구 기록**: 커밋된 변경 사항은 Git 저장소의 히스토리에 추가되며, 언제든지 이 커밋 상태로 되돌아갈 수 있습니다.
    * **버전 생성**: 커밋 하나하나가 프로젝트의 중요한 버전이 됩니다.
    * **메시지 중요성**: 커밋 시 작성하는 메시지는 해당 커밋에서 어떤 변경이 있었는지 설명하는 중요한 문서입니다. 다른 개발자나 미래의 자신을 위해 명확하고 간결하게 작성하는 것이 좋습니다.
    * **롤백 가능**: 커밋 히스토리를 통해 특정 시점으로 되돌리거나, 변경 사항을 취소하는 등의 작업이 가능해집니다.

---

## 주요 차이점 요약

| 특징           | 스테이징 영역 (`git add`)                       | 커밋 (`git commit`)                                |
| :------------- | :---------------------------------------------- | :------------------------------------------------- |
| **목적** | 다음 커밋에 포함될 변경 사항 준비/선택          | 준비된 변경 사항을 저장소에 영구 기록             |
| **상태** | 임시 저장, 아직 저장소에 반영되지 않음         | 영구 저장, 저장소 히스토리에 반영됨                 |
| **저장 내용** | 현재 작업 중인 파일에서 다음 커밋에 넣을 변경분 | 스테이징 영역에 있던 모든 변경분                 |
| **명령어** | `git add`                                       | `git commit`                                       |
| **확인 명령어**| `git status`, `git diff --staged`               | `git log`                                          |

---

Git은 이 스테이징 영역이라는 중간 단계를 통해 개발자가 더 세밀하게 커밋 내용을 제어할 수 있도록 돕습니다. 원하는 변경 사항만을 깔끔하게 커밋하여 프로젝트의 히스토리를 명확하게 유지하는 데 활용할 수 있습니다.

final study kungmin junseo dongjo woojin