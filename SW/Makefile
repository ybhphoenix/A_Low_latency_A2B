ORDER = 1
RUNS = 10000
WIDTH = 32
RNG = 2

MACRO = -D MASKING_ORDER=$(ORDER) -D ITER=$(RUNS) -D BIT_WIDTH=$(WIDTH) 
MACROB = -D MASKING_ORDER=$(ORDER) -D ITER=$(RUNS) -D BIT_WIDTH=$(WIDTH) -D RNG_MODE=$(RNG) -D COUNT
SOURCES = random.c  tests.c convab.c masking.c
HEADERS = random.h
SOURCES_BENCH = benchmarks.c cpucycles.c 

main: $(SOURCES) $(HEADERS) main.c
	gcc  -Wall  main.c  $(SOURCES) $(MACRO) -lm -o main  

bench: $(SOURCES) $(HEADERS) $(SOURCES_BENCH)
	gcc  -Wall -O0 -march=native $(SOURCES) $(SOURCES_BENCH) $(MACROB) -lm -o bench 

clean:
	rm -f main bench