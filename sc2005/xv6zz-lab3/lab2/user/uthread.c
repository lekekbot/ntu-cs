#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

/* Possible states of a thread: */
#define FREE        0x0
#define RUNNING     0x1
#define RUNNABLE    0x2

#define STACK_SIZE  8192
#define MAX_THREAD  4


/* Saved context of a suspended thread.
   The field order must match the offsets in uthread_switch.S. */
struct context {
  uint64 ra;
  uint64 sp;

  // callee-saved
  uint64 s0;
  uint64 s1;
  uint64 s2;
  uint64 s3;
  uint64 s4;
  uint64 s5;
  uint64 s6;
  uint64 s7;
  uint64 s8;
  uint64 s9;
  uint64 s10;
  uint64 s11;
};

struct thread {
  char       stack[STACK_SIZE]; /* the thread's stack */
  int        state;             /* FREE, RUNNING, RUNNABLE */
  struct context *context;      /* saved context, at the top of stack[] */
};

// Slot where this thread's context is saved: the 16-byte-aligned top of its
// own stack, below the reserved context area nothing but the stack is used.
static struct context *
thread_context_slot(struct thread *t)
{
  uint64 top = (uint64)t->stack + STACK_SIZE - sizeof(struct context);
  return (struct context *)(top & ~(uint64)0xf);
}
struct thread all_thread[MAX_THREAD];
struct thread *current_thread;
extern void thread_switch(uint64, uint64);
              
void 
thread_init(void)
{
  // main() is thread 0, which will make the first invocation to
  // thread_schedule(). It needs a stack so that the first thread_switch() can
  // save thread 0's state.
  current_thread = &all_thread[0];
  current_thread->state = RUNNING;
  // Thread 0 runs on the process's own stack, but the first thread_switch()
  // still needs a writable place to save its context.
  current_thread->context = thread_context_slot(current_thread);
}

void 
thread_schedule(void)
{
  struct thread *t, *next_thread;

  /* Find another runnable thread. */
  next_thread = 0;
  t = current_thread + 1;
  for(int i = 0; i < MAX_THREAD; i++){
    if(t >= all_thread + MAX_THREAD)
      t = all_thread;
    if(t->state == RUNNABLE) {
      next_thread = t;
      break;
    }
    t = t + 1;
  }

  if (next_thread == 0) {
    printf("thread_schedule: no runnable threads\n");
    exit(-1);
  }

  if (current_thread != next_thread) {         /* switch threads?  */
    next_thread->state = RUNNING;
    t = current_thread;
    current_thread = next_thread;
    thread_switch((uint64)t->context, (uint64)next_thread->context);
  } else
    next_thread = 0;
}

void 
thread_create(void (*func)())
{
  struct thread *t;

  for (t = all_thread; t < all_thread + MAX_THREAD; t++) {
    if (t->state == FREE) break;
  }
  t->state = RUNNABLE;
  // A never-run thread has no saved state, so construct one: thread_switch()
  // restores ra and sp, and `ret` then starts func on this thread's own stack.
  t->context = thread_context_slot(t);
  memset(t->context, 0, sizeof(struct context));
  t->context->ra = (uint64)func;
  t->context->sp = (uint64)t->context;   // 16-byte aligned, grows down
}

void 
thread_yield(void)
{
  current_thread->state = RUNNABLE;
  thread_schedule();
}

void thread_exit(void) {
  current_thread->state = FREE;
  thread_schedule();
}
