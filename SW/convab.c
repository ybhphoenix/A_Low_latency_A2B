#include <stdint.h>
#include <stdio.h>
#include <assert.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include "masking.h"
#include "random.h"

#define MIN(a,b) ((a)<(b)? (a):(b))

void SecAnd_PINI1(uint32_t *x,uint32_t *y,uint32_t *c,int k,int n)
{
  int i,j;
  uint32_t r[MASKING_ORDER+1][MASKING_ORDER+1]={0};  
  uint32_t u[MASKING_ORDER+1][MASKING_ORDER+1]={0};  
  uint32_t v[MASKING_ORDER+1][MASKING_ORDER+1]={0};  
  uint32_t z[MASKING_ORDER+1][MASKING_ORDER+1]={0};
  uint32_t tmp;  
  uint32_t mask = (k==32)?0xffffffff:((1<<k)-1);
  for(i=0;i<n;i++)
  {
    for(j=i+1;j<n;j++)
    {  r[i][j]=rand32()&mask;
       r[j][i]=r[i][j];
    }
  }
    for(i=0;i<n;i++)
  {
    for(j=0;j<n;j++)
    {
      if(j!=i)
      {  
        u[i][j]=(~x[i])&r[i][j];
        v[i][j]=y[j]^r[i][j];
        v[i][j]=x[i]&v[i][j];
        z[i][j]=u[i][j]^v[i][j];
      }
    }
  }
  
  for(i=0;i<n;i++)
  {
    tmp = 0;
    for(j=0;j<n;j++)
    {
      if(j!=i)
      {
        tmp =tmp ^ z[i][j];
      }
    }  
    c[i]=(x[i]&y[i])^tmp;
  }
}

void SecCSA(uint32_t *x,uint32_t *y,uint32_t *cin, uint32_t* s, uint32_t* c, int k,int n)
{

  uint32_t a[MASKING_ORDER+1];
  uint32_t w[MASKING_ORDER+1];
  uint32_t v[MASKING_ORDER+1];
  int i;

  for(i=0;i<n;i++) a[i]=x[i]^y[i];
  
  for(i=0;i<n;i++) s[i]=a[i]^cin[i];
  
  for(i=0;i<n;i++) w[i]=x[i]^cin[i];

    SecAnd_PINI1(a,w,v,k,n);
  
  for(i=0;i<n;i++) c[i]=((x[i] ^ v[i])<<1) &MASK;
}

void SecCSAtree(uint32_t *x, uint32_t* s, uint32_t* c, int k,int n)
{

  uint32_t y1[MASKING_ORDER+1];
  uint32_t y2[MASKING_ORDER+1];
  uint32_t y3[MASKING_ORDER+1];

  int i;
  
  if(n==3){
    y1[0]= x[0];
    y1[1]= 0;
    y1[2]= 0;

    y2[0]= 0;
    y2[1]= x[1];
    y2[2]= 0;

    y3[0]= 0;
    y3[1]= 0;
    y3[2]= x[2];

    SecCSA(y1,y2,y3,s,c,k,3);
  }
  else{
    SecCSAtree(x,s,c,k,(n-1));
    for(i=0;i<n-1;i++) y1[i]=s[i];
    y1[n-1]=0;
    for(i=0;i<n-1;i++) y2[i]=c[i];
    y2[n-1]=0;
    for(i=0;i<n-1;i++) y3[i]=0;
    y3[n-1]=x[n-1];
    SecCSA(y1,y2,y3,s,c,k,n);
  }
}




void SecKSA(uint32_t *x,uint32_t *y,uint32_t *z,int k,int n)
{
    uint32_t W; 
    uint32_t p[MASKING_ORDER+1];
    uint32_t g[MASKING_ORDER+1];
    uint32_t tmp[MASKING_ORDER+1];
    uint32_t a[MASKING_ORDER+1];
    uint32_t pow;
    float kf=(float)k;
    int i,j;
    
    W = ceil(log(kf-1) / log(2))-1;

    for(i=0;i<n;i++) p[i]=x[i]^y[i];
    
    SecAnd_PINI1(x,y,g,k,n);
    
    if(W){
    for(j=0; j<W;j++){
        pow = 1<<j;
        for(i=0;i<n;i++) tmp[i]=(g[i]<<pow)&MASK;
        SecAnd_PINI1(p,tmp,a,k,n);
        for(i=0;i<n;i++) g[i]=g[i]^a[i];
        for(i=0;i<n;i++) tmp[i]=(p[i]<<pow)&MASK;
        SecAnd_PINI1(p,tmp,a,k,n);
        for(i=0;i<n;i++) p[i]=a[i];
    }
    for(i=0;i<n;i++) tmp[i]=(g[i]<<(1<<W))&MASK;
    SecAnd_PINI1(p,tmp,a,k,n);
    for(i=0;i<n;i++) g[i]=g[i]^a[i];
    for(i=0;i<n;i++) z[i]=(x[i]^y[i]^(g[i]<<1))&MASK;
    }
   
}

void Expand1(uint32_t *x,uint32_t *xp,int k,int n2,int n)
{ 
  int i;
  for(i=0;i<n2;i++)
  {
    xp[i]=x[i];
  }
  for(i=n2;i<n;i++)
  {
    xp[i]=0;
  }
  
}

void Expand2(uint32_t *x,uint32_t *xp,int k,int n2,int n)
{ 
  int i;
  for(i=0;i<(n-n2);i++)
  {
    xp[i]=0;
  }
  for(i=0;i<n2;i++)
  {
    xp[n-n2+i]=x[i];
  }
  
}

void SecRCA(uint32_t *x,uint32_t *y,uint32_t *z,int k,int n)
{
  uint32_t c[n];
  uint32_t c_j[n];
  uint32_t a[n];
  uint32_t a_j[n];
  uint32_t b[n];
  uint32_t tmp[n];
  
  for(int i=0;i<n;i++) c[i]=0;
  for(int i=0;i<n;i++) c_j[i]=0;
  for(int i=0;i<n;i++) a[i]=x[i] ^ y[i];
  

  for(int j=0;j<k-1;j++)
  {
    for(int i=0;i<n;i++) a_j[i]= (a[i]>>j) & (uint32_t)1 ;
    for(int i=0;i<n;i++) b[i] = ((x[i]>>j) & (uint32_t)1) ^ c_j[i];
    
    SecAnd_PINI1(b,a_j,tmp,1,n);
    for(int i=0;i<n;i++) c_j[i]=tmp[i] ^ ((x[i]>>j) & (uint32_t)1);
    
    for(int i=0;i<n;i++) c[i]=c[i]|(c_j[i] << (j+1));
  }
  for(int i=0;i<n;i++) z[i]=a[i] ^ c[i];
}


void SecA2B_RCA(uint32_t *A,uint32_t *z,int k,int n)
{ 
  if(n==1)
  {
    z[0]=A[0];
    return;
  }

  uint32_t x[n/2];
  SecA2B_RCA(A,x,k,n/2);
  uint32_t xp[n];
  Expand1(x,xp,k,n/2,n);
  
  uint32_t y[(n+1)/2];
  SecA2B_RCA(A+n/2,y,k,(n+1)/2);
  uint32_t yp[n];
  Expand2(y,yp,k,(n+1)/2,n);

  SecRCA(xp,yp,z,k,n);
 
}


void SecA2B_KSA(uint32_t *A,uint32_t *z,int k,int n)
{ 
  if(n==1)
  {
    z[0]=A[0];
    return;
  }

  uint32_t x[n/2];
  SecA2B_KSA(A,x,k,n/2);
  uint32_t xp[n];
  Expand1(x,xp,k,n/2,n);
  
  uint32_t y[(n+1)/2];
  SecA2B_KSA(A+n/2,y,k,(n+1)/2);
  uint32_t yp[n];
  Expand2(y,yp,k,(n+1)/2,n);

  SecKSA(xp,yp,z,k,n);
 
}


void SecA2B_CSA(uint32_t *A,uint32_t *z,int k,int n)
{ 

  uint32_t s[MASKING_ORDER+1];
  uint32_t c[MASKING_ORDER+1];

  if(n==1)
  {
    z[0]=A[0];
    return;
  }

  if(n==2)
  {
    s[0]=A[0];
    s[1]=0;
    c[0]=0;
    c[1]=A[1];
  }
  else{
  
  SecCSAtree(A,s,c,k,n);
  }

  SecKSA(s,c,z,k,n);
}



