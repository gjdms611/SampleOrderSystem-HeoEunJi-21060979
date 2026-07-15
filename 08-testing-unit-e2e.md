# 미션2: 테스트 구축 (Unit / E2E)

## 목표
핵심 로직에 대한 Unit Test를 필수로 구축하고, 메인 메뉴 콘솔 흐름 전체를 검증하는 E2E Test를 권장 수준으로 구축한다.

## 배경
채점 주안점 중 하나로 Test(Unit 필수, E2E 권장)가 명시되어 있다. 특히 주문 상태전이 로직, 재고계산, 수율계산 등 핵심 비즈니스 로직은 반드시 Unit Test로 검증되어야 한다.

## 요구사항 상세
- Unit Test(필수): 상태전이 로직, 재고계산, 수율계산 등 핵심 로직 검증
- E2E Test(권장): 메인 메뉴 콘솔 흐름 전체 시나리오 검증
- 상태머신 전이 케이스별 테스트 정의(각각 필수 테스트 케이스로 작성):
  - RESERVED -> REJECTED
  - RESERVED -> CONFIRMED (재고 충분 경로)
  - RESERVED -> PRODUCING -> CONFIRMED (재고 부족 후 생산 완료 경로)
  - CONFIRMED -> RELEASE

## 완료 기준
- [ ] Unit Test가 SampleOrderSystem 레포에 존재하며 실행 시 통과함
- [ ] 위 4가지 상태전이 케이스에 대한 테스트 케이스가 각각 존재함
- [ ] (선택) E2E Test가 존재하며 실행 시 통과함

## 참고사항 및 확인 필요 사항
- 테스트 프레임워크 및 커버리지 기준: TBD (사용 언어 선택에 따름)
