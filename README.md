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


**TODO

1. Add mongo for analytics

1.1 Open price
1.2 Close price
1.3 Time elapsed
1.4 Position amount