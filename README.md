Strategy: 

1. Find most traded coin in pair with USDT
2. Purchase via strategy(15) for 15 USDT for example
3. Log growth if order ever grew
```
    print(f'Price {str(df.Close[-1])}')
    print(f'Target {str(buyprice * Target)}')
    print(f'Stop {str(buyprice * SL)}')
```

4. Log when price hits take profit
```
    print('SELLING: ', order)
```