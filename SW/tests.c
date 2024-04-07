/*This code contains mask test functions for different A2B schemes*/

#include <stdio.h>
#include "masking.h"
#include "convab.h"
#include "random.h"
#include "math.h"



#define NB_TESTS 1000


void initTab(uint32_t *a,int n)
{
  for(int i=0;i<n;i++)
    a[i]=0;
}


int testConvertAB_RCA(){

  uint32_t k = BIT_WIDTH;
  uint32_t val, val2,val_after_mask;
  uint32_t A[MASKING_ORDER+1],B[MASKING_ORDER+1];
  initTab(A,MASKING_ORDER+1);
  
  for(int i=0; i < NB_TESTS; ++i){
    val = rand32()&MASK;
    arithm_masking(A, val, MASK);
    val_after_mask=arith_unmask(A,MASK);
    SecA2B_RCA(A,B,k,MASKING_ORDER+1);
    val2 = bool_unmask(B);

    if (val != val2){
      printf("testConvertAB_RCA:Test %i failed ! Val: %i val_after_mask: %i Converted val: %i\n", i, val, val_after_mask, val2);
      printf_mask(A,MASKING_ORDER+1);
      printf_mask(B,MASKING_ORDER+1);
      return 0;
    }
  }
  printf("Number of shares: %i, bit width: %i\n",MASKING_ORDER+1,BIT_WIDTH);
  printf("Test convert A2B RCA: success\n");
  return 1;

}

int testConvertAB_KSA(){

  uint32_t k = BIT_WIDTH;
  uint32_t val, val2,val_after_mask;
  uint32_t A[MASKING_ORDER+1],B[MASKING_ORDER+1];
  initTab(A,MASKING_ORDER+1);
  
  for(int i=0; i < NB_TESTS; ++i){
    val = rand32()&MASK;
    arithm_masking(A, val, MASK);
    val_after_mask=arith_unmask(A,MASK);
    SecA2B_KSA(A,B,k,MASKING_ORDER+1);
    val2 = bool_unmask(B);

    if (val != val2){
      printf("testConvertAB_KSA:Test %i failed ! Val: %i val_after_mask: %i Converted val: %i\n", i, val, val_after_mask, val2);
      printf_mask(A,MASKING_ORDER+1);
      printf_mask(B,MASKING_ORDER+1);
      return 0;
    }
  }
  printf("Number of shares: %i, bit width: %i\n",MASKING_ORDER+1,BIT_WIDTH);
  printf("Test convert A2B KSA: success\n");
  return 1;

}

int testConvertAB_CSA(){

  int k = BIT_WIDTH;
  uint32_t val, val2,val_after_mask;
  uint32_t A[MASKING_ORDER+1],B[MASKING_ORDER+1];
  initTab(A,MASKING_ORDER+1);

  printf("k=%u\n",k);
  printf("MASK=%i\n",MASK);
  
  for(int i=0; i < NB_TESTS; ++i){
    val = rand32()&MASK;
    arithm_masking(A, val, MASK);
    val_after_mask=arith_unmask(A,MASK);
    SecA2B_CSA(A,B,k,MASKING_ORDER+1);
    val2 = bool_unmask(B);

    if (val != val2){
      printf("testConvertAB_CSA:Test %i failed ! Val: %i val_after_mask: %i Converted val: %i\n", i, val, val_after_mask, val2);
      printf_mask(A,MASKING_ORDER+1);
      printf_mask(B,MASKING_ORDER+1);
      return 0;
    }
  }
  printf("Number of shares: %i, bit width: %i\n",MASKING_ORDER+1,BIT_WIDTH);
  printf("Test convert A2B CSA: success\n");
  return 1;

}



void tests(){

  testConvertAB_RCA();
  testConvertAB_KSA();
  testConvertAB_CSA();

}