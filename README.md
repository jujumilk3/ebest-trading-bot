# ebest_trading_bot

## description
1. 이베스트 API XING 기반으로 제작.
2. 전략 노출 우려로 관련 코드는 전부 제거함. 
   새 전략을 짜서 쓰려면 strategy의 example을 참고.
3. main processor 아래에 각 tr object별로 thread를 만들어서 
   각 TR의 aps(Action per second)에 맞춰서 요청을 보내게 설계.
   (각 전략에서 보내는 tr 요청으로 aps가 넘어 작동 안되는 걸 방지하기 위해)

