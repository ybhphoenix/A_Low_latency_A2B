/*This code contains generation function, refresh function, remove function, print function for Boolean masking and arithmetic masking.*/

#include <stdint.h>
#include <stdio.h>
#include <assert.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

#include "random.h"




void arithmetic_refresh(uint32_t* x, unsigned mask){
  uint32_t r;
  for(int i=0; i< MASKING_ORDER+1; i++){
    r = (uint32_t) rand32()&mask;     
    x[i] = (x[i] + r)&mask;
    x[MASKING_ORDER] = (x[MASKING_ORDER] - r + mask+1)&mask;
  }
}

void boolean_refresh(uint32_t* x, unsigned k){
  uint32_t r;
  for(int i=0; i< MASKING_ORDER; ++i){
    r = (uint32_t) rand32() & ((1<<k)-1);
    x[i] = (x[i] ^ r);
    x[MASKING_ORDER] = (x[MASKING_ORDER] ^ r);
  }
}

uint32_t arith_unmask(uint32_t* x, unsigned mask){
  uint32_t res = 0;
  for(int i=0;i<MASKING_ORDER+1;++i)
  res = (res+x[i])&mask;
  return res;
}

void arithm_masking(uint32_t* x, int a, unsigned mask){
  x[0] = a;
  for(int i=1; i < (MASKING_ORDER+1); i++) x[i] = 0;
  arithmetic_refresh(x, mask);

}


uint32_t bool_unmask(uint32_t* x){
  uint32_t res = 0;
  for(int i=0;i<MASKING_ORDER+1;i++)
    res = (res^x[i]);
  return res;
}

uint32_t bool_unmask_n(uint32_t* x, uint32_t n){
  uint32_t res = 0;
  for(int i=0;i<n;i++)
    res = (res^x[i]);
  return res;
}

void printf_mask(uint32_t* x, int n){
  for(int i=0;i<n;i++)
  printf("share%i=%02x\n",i,x[i]);
}