# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("---")
N = int(input()) #no. of squares
K = int(input()) #max allowed sum
A = []
C = []
for i in range(0,N):
    x = input()
    A.append(int(x))
for i in range(0,N):
    x = input()
    C.append(int(x))

Fin_flag = False
L = N-1
for l in range(1,N):
    print("L is now, ",l)
    bob_pos = 0
    S = A[0]
    while True:
        bob_pos = bob_pos + l  # Bob jumps
        if C[bob_pos] == C[bob_pos]:    #If squares are same colour
            break
        S = S + A[bob_pos]
        if S > K:               #If sum exceeds
            break
        print("Bob is now at, ", bob_pos)
        if (bob_pos == N-1):    #If bob reaches the end succesfully
            Fin_flag = True
            break
    if Fin_flag:
        L = l
        break
print("Final value of L is", L)