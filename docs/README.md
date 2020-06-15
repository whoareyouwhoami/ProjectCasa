
## Documentation

**Project Casa 디렉토리 구조**

    ProjectCasa
    ├── Crawling             --> 크롤링
    │   ├── SubwayCrawling   --> 지하철 크롤링
    │   └── WebCrawling      --> 웹 크롤링
    |
    ├── EDA                  --> 시각화
    |
    ├── Modeling             --> 모델링
    │   ├── data             --> 전처리된 데이터
    │   ├── model            --> 인코딩, 스케일링된 데이터
    │   ├── output           --> 결과
    │   ├── reference        --> 모델링 참고 문서
    │   └── trials           --> 시도된 모델링
    |
    ├── casa_src             --> 쉘에 필요한 소스
    │   └── data             --> 쉘에 필요한 데이터
    |
    └── docs                 --> 프로젝트 문서

**개별 문서**

  - [아키텍쳐](architecture.md)

  - [데이터베이스](database_structure.md)

  - [EDA](EDA.md)

  - [모델링](model.md)
