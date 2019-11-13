exepcted_results =[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811]

def fib(n):
    if n==0:return 0
    fib_list=[1]
    for i in range(1,n):
        last_term=fib_list[-1]
        last_index=fib_list.index(last_term)
        if len(fib_list)<2:
            fib_list.append(i)
        last_term2=fib_list[-2]
        current_term=last_term+last_term2
        fib_list.append(current_term)
    return  fib_list
n=int(input('fib n please : '))
print(fib(n))
print('Expected results ',exepcted_results[0:n+1])