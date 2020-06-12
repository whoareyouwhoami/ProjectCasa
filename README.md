
# Project Casa

[개별 프로젝트 문서](docs/)

### 프로젝트 개요

서울에 위치한 아파트 가격을 예측해주는 시스템을 구축하는 프로젝트이다.

### 사용자 가이드

1.  [Project Casa](https://github.com/whoareyouwhoami/ProjectCasa.git)
    레포를 클론 한다.

2.  가상환경을 활성화 시킨 후 `pip -r requirements.txt`를 실행시켜 필요한 패키지들을 설치한다.

3.  아래와 같이 실행 시키면 된다.

<!-- end list -->

    $ sh casa.sh --apt_name 아파트이름 --apt_area 아파트 면적 --predict_num 예측 기간

**예시:**

    ==== 실행 ====
    $ sh casa.sh --apt_name 당산반도유보라팰리스 --apt_area 108 --predict_num 4
    
    ==== 결과 ====
            Price
    1,114,069,085
    1,117,512,744
    1,120,956,402
    1,124,400,061

실행 방법에 대한 자세한 내용은 `$ sh casa.sh` 를 통해 확인하면 된다.

**이미 패키지들을 설치 했으면 가상환경만 활성화 시키면 된다.**
