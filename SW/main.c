#include <stdint.h>
#include <time.h>

#include "random.h"


#ifdef COUNT
uint64_t count_rand = 0;
#endif

void tests();



int main(){
  srand(time(0));
  tests();

  return 0;
}