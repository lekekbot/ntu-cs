#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int
main(int argc, char *argv[])
{
  int n = getproccount();
  printf("proccount: %d process-table entries in use\n", n);
  printf("proccount: pid %d (this process is one of them)\n", getpid());
  exit(0);
}
