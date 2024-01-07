#include <stdint.h>

#ifndef MASKING_H
#define MASKING_H

void arithmetic_refresh(uint32_t* x, unsigned q);
void boolean_refresh(uint32_t* x, unsigned k);
uint32_t arith_unmask(uint32_t* x, unsigned q);
void arithm_masking(uint32_t* x, int a, unsigned q);
uint32_t bool_unmask(uint32_t* x);
uint32_t bool_unmask_n(uint32_t* x, uint32_t n);
void printf_mask(uint32_t* x, int n);

#endif