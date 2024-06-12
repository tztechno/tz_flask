
---
```
def main(N):
    ans = 0
    for i in range(1, N+1):
        if "7" not in str(i) and "7" not in str(oct(i)):
            ans += 1
    return ans

Result for input 1000000 = 253845
Time: 0.358 sec
```
---
```
def main(N):
    def to_base_n(decimal, base):
        result = ''
        while decimal > 0:
            remainder = decimal % base
            result = str(remainder) + result
            decimal = decimal // base
        return result if result else '0'
    ans=0
    for i in range(1,N+1):
        b_num = to_base_n(i,8)
        if '7' not in list(str(i)) and '7' not in list(str(b_num)):
            ans+=1
    return ans

Result for input 1000000 = 253845
Time: 2.572 sec
```
---
---
---
