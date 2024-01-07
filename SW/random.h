#ifndef RANDOM_H
#define RANDOM_H
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#ifndef MASKING_ORDER
#define MASKING_ORDER 3
#endif

#ifndef BIT_WIDTH
#define BIT_WIDTH (uint32_t)(32)
#endif

#ifndef MASK
#define MASK (uint32_t)((BIT_WIDTH==32)?0xffffffff:((uint32_t)(1<<BIT_WIDTH)-1))
#endif

#ifndef RNG_MODE
#define RNG_MODE 2
#endif

typedef struct Masked {int shares[MASKING_ORDER+1];} Masked;

//#define COUNT
#ifdef COUNT
extern uint64_t count_rand;
#endif

uint16_t rand16();
uint32_t rand32();
uint64_t rand64();
#endif