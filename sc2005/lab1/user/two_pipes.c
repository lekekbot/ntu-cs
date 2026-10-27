#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

#define MSGLEN 4
#define BUFSZ  (MSGLEN + 1)

// Write the whole string or report failure.
static int
sendmsg(int fd, const char *s)
{
  int len = strlen(s);

  if(write(fd, s, len) != len){
    fprintf(2, "two_pipes: write of %s failed\n", s);
    return -1;
  }
  return 0;
}

int
main(int argc, char *argv[])
{
  int p2c[2];  // parent -> child
  int c2p[2];  // child  -> parent
  char buf[BUFSZ];
  int n;

  if(pipe(p2c) < 0 || pipe(c2p) < 0){
    fprintf(2, "two_pipes: pipe failed\n");
    exit(1);
  }

  int pid = fork();
  if(pid < 0){
    fprintf(2, "two_pipes: fork failed\n");
    exit(1);
  }

  if(pid == 0){
    // Child: read ping from p2c[0], reply pong on c2p[1].
    close(p2c[1]);   // child never writes to p2c
    close(c2p[0]);   // child never reads from c2p

    if((n = read(p2c[0], buf, MSGLEN)) != MSGLEN){
      fprintf(2, "two_pipes: child read %d bytes, expected %d\n", n, MSGLEN);
      exit(1);
    }
    buf[n] = '\0';
    printf("%d: received %s\n", getpid(), buf);

    if(sendmsg(c2p[1], "pong") < 0)
      exit(1);

    close(p2c[0]);
    close(c2p[1]);
    exit(0);
  }

  // Parent: send ping on p2c[1], read pong from c2p[0].
  close(p2c[0]);     // parent never reads from p2c
  close(c2p[1]);     // parent never writes to c2p

  if(sendmsg(p2c[1], "ping") < 0){
    close(p2c[1]);
    close(c2p[0]);
    exit(1);
  }
  close(p2c[1]);     // let the child see EOF once the byte is consumed

  if((n = read(c2p[0], buf, MSGLEN)) != MSGLEN){
    fprintf(2, "two_pipes: parent read %d bytes, expected %d\n", n, MSGLEN);
    exit(1);
  }
  buf[n] = '\0';
  printf("%d: received %s\n", getpid(), buf);

  close(c2p[0]);
  wait(0);
  exit(0);
}
