/* timestamp example */
#include <stdio.h>      /* printf */
#include <time.h>       /* time_t, time (for timestamp in second) */
#include <sys/timeb.h>  /* ftime, timeb (for timestamp in millisecond) */
#include <sys/time.h>   /* gettimeofday, timeval (for timestamp in microsecond) */
 
int main ()
{
  /* Example of timestamp in second. */
  time_t timestamp_sec; /* timestamp in second */
  time(&timestamp_sec);  /* get current time; same as: timestamp_sec = time(NULL)  */
  printf ("%ld seconds since epoch\n", timestamp_sec);
 
  /* Example of timestamp in millisecond. */
  struct timeb timer_msec;
  long int timestamp_msec; /* timestamp in millisecond. */
  if (!ftime(&timer_msec)) {
    timestamp_msec = ((long  int) timer_msec.time) * 1000ll + 
                        (long int) timer_msec.millitm;
  }
  else {
    timestamp_msec = -1;
  }
  printf("%ld milliseconds since epoch\n", timestamp_msec);
 
  /* Example of timestamp in microsecond. */
  struct timeval timer_usec; 
  long  int timestamp_usec; /* timestamp in microsecond */
  if (!gettimeofday(&timer_usec, NULL)) {
    timestamp_usec = ((long int) timer_usec.tv_sec) * 1000000ll + 
                        (long int) timer_usec.tv_usec;
  }
  else {
    timestamp_usec = -1;
  }
  printf("%ld microseconds since epoch\n", timestamp_usec);
 
  printf("epoch is 00:00 hours, Jan 1, 1970 UTC\n");
 
  return 0;
}