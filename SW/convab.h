#include <stdint.h>

#ifndef A2B_CSA
#define A2B_CSA

void SecAnd_PINI1(uint32_t *x,uint32_t *y,uint32_t *c,int k,int n);
void SecCSA(uint32_t *x,uint32_t *y,uint32_t *cin, uint32_t* c, uint32_t* s, int k,int n);
void SecKSA(uint32_t *x,uint32_t *y,uint32_t *z,int k,int n);

void Expand1(uint32_t *x,uint32_t *xp,int k,int n2,int n);
void Expand2(uint32_t *x,uint32_t *xp,int k,int n2,int n);
void SecRCA(uint32_t *x,uint32_t *y,uint32_t *z,int k,int n);

void SecA2B_RCA(uint32_t *A,uint32_t *z,int k,int n);
void SecA2B_KSA(uint32_t *A,uint32_t *z,int k,int n);
void SecA2B_CSA(uint32_t *A,uint32_t *z,int k,int n);


#endif
