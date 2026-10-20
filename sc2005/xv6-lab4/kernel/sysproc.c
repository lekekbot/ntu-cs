#include "types.h"
#include "riscv.h"
#include "defs.h"
#include "param.h"
#include "memlayout.h"
#include "spinlock.h"
#include "proc.h"

uint64
sys_exit(void)
{
  int n;
  argint(0, &n);
  exit(n);
  return 0;  // not reached
}

uint64
sys_getpid(void)
{
  return myproc()->pid;
}

uint64
sys_fork(void)
{
  return fork();
}

uint64
sys_wait(void)
{
  uint64 p;
  argaddr(0, &p);
  return wait(p);
}

uint64
sys_sbrk(void)
{
  uint64 addr;
  int n;

  argint(0, &n);
  addr = myproc()->sz;
  if(growproc(n) < 0)
    return -1;
  return addr;
}

// Number of virtual pages intersecting [0, p->sz): a partly used
// final page still counts as one.
uint64
sys_countvp(void)
{
  return PGROUNDUP(myproc()->sz) / PGSIZE;
}

// Number of physical frames backing [0, p->sz). Includes the stack guard
// page, whose PTE is valid but lacks PTE_U. Excludes page-table frames and
// the TRAMPOLINE/TRAPFRAME mappings, which lie above p->sz.
uint64
sys_countpp(void)
{
  struct proc *p = myproc();
  uint64 npages = PGROUNDUP(p->sz) / PGSIZE;
  uint64 n = 0;

  for(uint64 a = 0; a < npages * PGSIZE; a += PGSIZE){
    // alloc=0: inspect existing mappings only.
    pte_t *pte = walk(p->pagetable, a, 0);
    if(pte == 0 || (*pte & PTE_V) == 0)
      continue;
    if(PTE_FLAGS(*pte) == PTE_V){
      // points to a lower-level page table, not a data frame
      continue;
    }
    n++;
  }
  return n;
}

uint64
sys_sleep(void)
{
  int n;
  uint ticks0;

  argint(0, &n);
  if(n < 0)
    n = 0;
  acquire(&tickslock);
  ticks0 = ticks;
  while(ticks - ticks0 < n){
    if(killed(myproc())){
      release(&tickslock);
      return -1;
    }
    sleep(&ticks, &tickslock);
  }
  release(&tickslock);
  return 0;
}

uint64
sys_kill(void)
{
  int pid;

  argint(0, &pid);
  return kill(pid);
}

// return how many clock tick interrupts have occurred
// since start.
uint64
sys_uptime(void)
{
  uint xticks;

  acquire(&tickslock);
  xticks = ticks;
  release(&tickslock);
  return xticks;
}
