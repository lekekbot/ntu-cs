#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

/* Possible states of a thread: */
#define FREE        0x0
#define RUNNING     0x1
#define RUNNABLE    0x2

#define STACK_SIZE  8192
#define MAX_THREAD  4

/*
 * Saved state for a cooperative user-level context switch.
 *
 * The field order intentionally matches user/uthread_switch.S:
 *   ra  = 0
 *   sp  = 8
 *   s0  = 16
 *   ...
 *   s11 = 104
 *
 * This mirrors the register set used by kernel/swtch.S because a normal
 * function call only requires callee-saved registers plus ra/sp to survive
 * across the switch.
 */
struct thread_context {
  uint64 ra;
  uint64 sp;
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
  /*
   * RISC-V's standard ABI requires sp to be 16-byte aligned on function
   * entry. Giving the stack member 16-byte alignment also makes each
   * struct thread element 16-byte aligned.
   */
  char stack[STACK_SIZE] __attribute__((aligned(16)));
  int state;                        /* FREE, RUNNING, RUNNABLE */
  struct thread_context context;    /* saved cooperative-thread context */
};

struct thread all_thread[MAX_THREAD];
struct thread *current_thread;
extern void thread_switch(uint64, uint64);

void
thread_init(void)
{
  /*
   * all_thread[] is global, so it begins zero-filled (FREE).
   * main() becomes thread 0 and supplies the first outgoing context.
   */
  current_thread = &all_thread[0];
  current_thread->state = RUNNING;
}

void
thread_schedule(void)
{
  struct thread *t, *next_thread;

  /* Find the next runnable thread, wrapping around the table. */
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

  if(next_thread == 0) {
    printf("thread_schedule: no runnable threads\n");
    exit(-1);
  }

  /*
   * Mark the selected thread as running before transferring control.
   * If it happens to be the current thread, no register switch is needed.
   */
  next_thread->state = RUNNING;

  if(current_thread != next_thread) {
    t = current_thread;
    current_thread = next_thread;

    /*
     * a0 = outgoing saved context
     * a1 = incoming saved context
     */
    thread_switch((uint64)&t->context,
                  (uint64)&next_thread->context);
  }
}

void
thread_create(void (*func)())
{
  struct thread *t;

  for(t = all_thread; t < all_thread + MAX_THREAD; t++) {
    if(t->state == FREE)
      break;
  }

  if(t == all_thread + MAX_THREAD) {
    printf("thread_create: no free thread slots\n");
    exit(-1);
  }

  /*
   * A never-run thread has no previously saved context, so construct one.
   * thread_switch() will load ra and execute `ret`, which jumps to func.
   * The stack grows downward, so start sp at the aligned top of this
   * thread's private stack.
   *
   * The supplied test functions call thread_exit() themselves. If a thread
   * function simply returns, this minimal lab design has no normal caller
   * to return to.
   */
  memset(&t->context, 0, sizeof(t->context));
  t->context.ra = (uint64)func;
  t->context.sp = (uint64)(t->stack + STACK_SIZE);

  t->state = RUNNABLE;
}

void
thread_yield(void)
{
  current_thread->state = RUNNABLE;
  thread_schedule();
}

void
thread_exit(void)
{
  current_thread->state = FREE;
  thread_schedule();
}
