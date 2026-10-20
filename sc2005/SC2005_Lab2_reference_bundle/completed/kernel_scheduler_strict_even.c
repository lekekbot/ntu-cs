void
scheduler(void)
{
  struct proc *p;
  struct cpu *c = mycpu();

  c->proc = 0;
  for(;;){
    // Keep the stock interrupt handling around the selection loop.
    intr_on();
    intr_off();

    int found = 0;

    /*
     * Strict class priority:
     * first try to select one RUNNABLE even-PID process.
     * Restart the whole selection loop after it returns so an odd PID
     * cannot be selected while an eligible even PID is runnable.
     */
    for(p = proc; p < &proc[NPROC]; p++) {
      acquire(&p->lock);

      if(p->state == RUNNABLE && (p->pid % 2) == 0) {
        p->state = RUNNING;
        c->proc = p;
        swtch(&c->context, &p->context);

        c->proc = 0;
        found = 1;
        release(&p->lock);
        break;
      }

      release(&p->lock);
    }

    if(found)
      continue;

    /*
     * No eligible even PID was found, so an odd RUNNABLE process
     * may be selected. Run one, then restart from the even-priority scan.
     */
    for(p = proc; p < &proc[NPROC]; p++) {
      acquire(&p->lock);

      if(p->state == RUNNABLE && (p->pid % 2) != 0) {
        p->state = RUNNING;
        c->proc = p;
        swtch(&c->context, &p->context);

        c->proc = 0;
        found = 1;
        release(&p->lock);
        break;
      }

      release(&p->lock);
    }

    if(found == 0) {
      asm volatile("wfi");
    }
  }
}
