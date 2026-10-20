#include "user.h"

#define T_ASSERT(cond) \
    do { \
        if (!(cond)) { \
            printf("Assertion failed at %s:%d: %s\n", __FILE__, __LINE__, #cond); \
            exit(1); \
        } \
    } while (0)


int N = 1000;

void sem_basic() {
    printf("[sem_basic] Initializing semaphore to 1...\n");
    int semid = sem_init(1);
    T_ASSERT(sem_getvalue(semid) == 1);

    printf("[sem_basic] Waiting (should decrement to 0)...\n");
    sem_wait(semid);
    T_ASSERT(sem_getvalue(semid) == 0);

    printf("[sem_basic] Posting (should increment to 1)...\n");
    sem_signal(semid);
    T_ASSERT(sem_getvalue(semid) == 1);

    sem_free(semid);
    printf("[sem_basic] PASS: Basic semaphore operations work.\n");
}

void do_work(int pid, int semid) {
    for (int i = 0; i < N; i++) {
        sem_wait(semid);
        int val = ucnt_get(0);
        ucnt_set(0, val + 1);
        sem_signal(semid);
    }
}

void race_test() {
    ucnt_set(0, 0);
    int semid = sem_init(1); // binary semaphore: mutual exclusion
    T_ASSERT(semid >= 0);

    int pid = fork();
    T_ASSERT(pid >= 0);
    if (pid == 0) { // child
        do_work(pid, semid);
        exit(0);
    } else { // parent
        do_work(getpid(), semid);
        wait(0);
        int final = ucnt_get(0);
        printf("[race_test] final counter=%d (expected %d)\n", final, 2*N);
        T_ASSERT(final == 2*N);
        printf("[race_test] PASS: consistent counter\n");
    }

    sem_free(semid);
}    

#define UBUF_SLOTS 16 // must match UBUF_SIZE in kernel/ubuf.c

struct buf_sem {
    int empty;   // counts free slots, initialised to UBUF_SLOTS
    int filled;  // counts filled slots, initialised to 0
    int mutex;   // binary semaphore protecting the buffer indices, initialised to 1
};

void consumer(struct buf_sem b, int loops, int valid[]) {
    char tmp;
    for(int i = 0; i < loops; i++) {
        sem_wait(b.filled);   // wait until a slot holds data
        sem_wait(b.mutex);    // enter the critical section
        tmp = ubuf_read();
        sem_signal(b.mutex);  // leave the critical section
        sem_signal(b.empty);  // one more slot is free
        T_ASSERT(valid[(unsigned char)tmp]);
    }
}

void producer(const char* msg, struct buf_sem b) {
    for (const char* p = msg; *p != '\0'; p++) {
        sem_wait(b.empty);    // wait until a slot is free
        sem_wait(b.mutex);    // enter the critical section
        ubuf_write(*p);
        sem_signal(b.mutex);  // leave the critical section
        sem_signal(b.filled); // one more slot holds data
    }
}

void producer_consumer() {
    #define MSG_SIZE 48
    const char msg[MSG_SIZE + 1] = "cafefacefacefacefacefacefacefacefacecafecafecafe";
    const int NUM_PROD = 2;
    int valid[256] = {0};
    for (const char* p = msg; *p != '\0'; p++) {
        unsigned char uc = (unsigned char)*p;
        valid[uc] = 1;
    }

    struct buf_sem b;
    b.empty = sem_init(UBUF_SLOTS); // buffer starts empty
    b.filled = sem_init(0);         // nothing to consume yet
    b.mutex = sem_init(1);          // unlocked
    T_ASSERT(b.empty >= 0 && b.filled >= 0 && b.mutex >= 0);

    for (int i = 0; i < NUM_PROD; i++) {
        int pid = fork();
        T_ASSERT(pid >= 0);
        if (pid == 0) { // child
            producer(msg, b);
            exit(0);
        }
    }

    consumer(b, MSG_SIZE * NUM_PROD, valid);
    for (int i = 0; i < NUM_PROD; i++) {
        wait(0);
    }
    printf("[producer_consumer] PASS: message delivered\n");
    sem_free(b.mutex);
    sem_free(b.filled);
    sem_free(b.empty);
}



int main() {
    sem_basic();
    
    race_test();

    producer_consumer();

    printf("ALL TESTS PASSED\n");

    exit(0);
}
