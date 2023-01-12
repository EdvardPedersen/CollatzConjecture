import os

new_options = '''
-falign-functions  -falign-jumps 
-falign-labels  -falign-loops 
-fcaller-saves 
-fcode-hoisting 
-fcrossjumping 
-fcse-follow-jumps  -fcse-skip-blocks 
-fdelete-null-pointer-checks 
-fdevirtualize  -fdevirtualize-speculatively 
-fexpensive-optimizations 
-ffinite-loops 
-fgcse  -fgcse-lm  
-fhoist-adjacent-loads 
-finline-functions 
-finline-small-functions 
-findirect-inlining 
-fipa-bit-cp  -fipa-cp  -fipa-icf 
-fipa-ra  -fipa-sra  -fipa-vrp 
-fisolate-erroneous-paths-dereference 
-flra-remat 
-foptimize-sibling-calls 
-foptimize-strlen 
-fpartial-inlining 
-fpeephole2 
-freorder-blocks-algorithm=stc 
-freorder-blocks-and-partition  -freorder-functions 
-frerun-cse-after-loop  
-fschedule-insns  -fschedule-insns2 
-fsched-interblock  -fsched-spec 
-fstore-merging 
-fstrict-aliasing 
-fthread-jumps 
-ftree-builtin-call-dce 
-ftree-loop-vectorize 
-ftree-pre 
-ftree-slp-vectorize 
-ftree-switch-conversion  -ftree-tail-merge 
-ftree-vrp 
-fvect-cost-model=very-cheap
'''

if __name__ == "__main__":
    options = []
    for option in new_options.split():
        if option.strip():
            options.append(option.strip())

    commands = []

    for opt in options:
        print(f"Testing with {opt}")
        os.system(f"gcc -O1 {opt} collatz.c && ./a.out")
