#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "cpucycles.h"
#include "random.h"
#include "convab.h"
#include "masking.h"

#ifndef ITER
#define ITER 10000
#endif

#ifdef COUNT
uint64_t count_rand = 0;
#endif

uint64_t start, stop;

void benchmark_SecA2B_RCA(){
   uint32_t y[MASKING_ORDER+1], x[MASKING_ORDER+1];
   uint32_t val;
   val = rand32()&MASK;
   arithm_masking(x, val, MASK);
  start = cpucycles();
  for(int i=0; i < ITER; i++) SecA2B_RCA(x,y,BIT_WIDTH,MASKING_ORDER+1);
  stop = cpucycles();
  printf("Avg speed CGV14 : %f cycles.\n", (double)(stop-start)/ITER);
}

void benchmark_SecA2B_KSA(){
   uint32_t y[MASKING_ORDER+1], x[MASKING_ORDER+1];
   uint32_t val;
   val = rand32()&MASK;
   arithm_masking(x, val, MASK);
  start = cpucycles();
  for(int i=0; i < ITER; i++) SecA2B_KSA(x,y,BIT_WIDTH,MASKING_ORDER+1);
  stop = cpucycles();
  printf("Avg speed CGV14 : %f cycles.\n", (double)(stop-start)/ITER);
}

void benchmark_SecA2B_CSA(){
   uint32_t y[MASKING_ORDER+1], x[MASKING_ORDER+1];
   uint32_t val;
   val = rand32()&MASK;
   arithm_masking(x, val, MASK);
  start = cpucycles();
  for(int i=0; i < ITER; i++) SecA2B_CSA(x,y,BIT_WIDTH,MASKING_ORDER+1);
  stop = cpucycles();
  printf("Avg speed CSA : %f cycles.\n", (double)(stop-start)/ITER);
}

void random_counting(){
#ifdef COUNT

  uint32_t y2[MASKING_ORDER+1], x2[MASKING_ORDER+1];
  
  count_rand = 0;
  SecA2B_RCA(x2,y2,BIT_WIDTH,MASKING_ORDER+1);
  printf("Number of shares: %i, bit width: %i\n",MASKING_ORDER+1,BIT_WIDTH);
  printf("Random usage SecA2B_RSA : %lu bits.\n", count_rand);
  count_rand = 0;
  SecA2B_KSA(x2,y2,BIT_WIDTH,MASKING_ORDER+1);
  printf("Number of shares: %i, bit width: %i\n",MASKING_ORDER+1,BIT_WIDTH);
  printf("Random usage SecA2B_KSA : %lu uint_32t.\n", count_rand);
  count_rand = 0;
  SecA2B_CSA(x2,y2,BIT_WIDTH,MASKING_ORDER+1);
  printf("Number of shares: %i, bit width: %i\n",MASKING_ORDER+1,BIT_WIDTH);
  printf("Random usage SecA2B_CSA : %lu uint_32t.\n", count_rand);

#else
  printf("COUNT mode not enabled\n");
#endif
}


int main(){


  #ifdef COUNT
  random_counting();

  printf("\n\nbenchmark_CGV14_RCA: \n");
  benchmark_SecA2B_RCA();

  printf("\n\nbenchmark_SecA2B_KSA: \n");
  benchmark_SecA2B_KSA();

  printf("\n\nbenchmark_SecA2B_CSA: \n");
  benchmark_SecA2B_CSA();
  
  printf("\n");
  
  #else
  printf("\n\nbenchmark_CGV14_RCA: \n");
  benchmark_SecA2B_RCA();

  printf("\n\nbenchmark_SecA2B_KSA: \n");
  benchmark_SecA2B_KSA();

  printf("\n\nbenchmark_SecA2B_CSA: \n");
  benchmark_SecA2B_CSA();
  
  printf("\n");
  #endif
  
  return 0;
}
