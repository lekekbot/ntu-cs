# SC2005 — Virtualisation wrap-up + "the agent harness is an operating system" (Part 2)

> **Source:** `video_2026-10-02_15-15-01 (2).mp4` · **Length:** 18:34 · **Recorded:** 2 Oct 2026
> **Where it sits:** this recording opens on the *same* ledger/spinlock walkthrough that Part 1
> ends on, so it is best read as a continuation of Part 1
> (`video_2026-10-02_15-15-01.mp4`). There may be a short gap between the two captures.

Same capture conditions as Part 1: a lecture hall with mirrored projector screens and a camera that
pans. Slides were cropped to the projection screen and de-duplicated by image similarity; the
narration is the verbatim auto-transcript.

---

## What the session covers

Three distinct blocks, in this order.

### Block A — Finishing the virtualisation example (~first minute)

Picks up the ledger mid-explanation: the guest spinlock, vCPU A1/A2, the round-robin quantum, and
why a spinning vCPU burns its core while the VMM is still running something else. Closes the topic
with the lecturer's explicit recap list:

> *"That's about it for virtualisation. Pay attention to multiplexing, aggregation, emulation,
> direct execution, virtualisation type 1 and type 2. This is what you need to know."*

### Block B — "For fun, not examinable": the AI-agent harness as an operating system

This is the interesting part of the recording. The lecturer explicitly marks it **not examinable**
and spends most of the session drawing a systematic analogy between a classic OS and the runtime
that AI coding agents live in (Claude Code, Codex, OpenCode and friends) — the *harness*.

The core claim: the harness sits where the kernel sits, and **tool calls are the new system calls**.

```
   classic OS                      agent harness
   ----------                      -------------
   program                         model
   system call                     tool call
   kernel                          harness
   CPU / devices                   CPU (tool calls) + GPU (LLM requests)
   kernel schedules processes      harness schedules model + tool calls
```

Mapping table the lecturer walks through:

| Operating-systems concept | Agent-harness equivalent |
|---|---|
| Process **address space** | the model's **context** (KV cache, tokens, files, articles) |
| **Threads** (same address space, parallel work) | parallel tool calls — same context, many targets at once (e.g. hundreds of web searches) |
| **fork()** / new process | **sub-agents** — spawned with a *fresh* context, different from the parent's |
| **System call** (crossing into the kernel) | **tool call** — moving state between the model and the execution environment |
| **Scheduler** (sync vs async, blocking vs non-blocking) | harness dispatch of LLM requests and tool calls |
| **Interrupts** | async completions (e.g. a web search finishing and needing to be handed to the model) |
| **Mutual exclusion / synchronisation** | agents contending for the same files, folders or state |
| **Memory / resource allocation** | sharing GPU memory between agents; **thrashing** when agents are spawned without bound |
| **Virtualisation / containers** | the sandbox each tool runs in — literally the VMs/containers from Block A |
| **Memory management, long-horizon** | agent memory systems: what to read, what to put in context, what to persist, how to share skills with teammates (an open problem) |
| **Security / protection** | sandbox escapes, prompt/skill poisoning — you don't need to hack the kernel if you can poison a skill the agent trusts |

Points worth remembering from his commentary:

* Message passing is today's mechanism for agent-to-agent information sharing, **shared memory is
  the future** (share state rather than re-sending tokens).
* GPU **aggregation** in the cluster is where virtualisation shows up again.
* Fully autonomous agents making destructive choices are a real, already-observed problem — he
  tells the story of agents that, asked for health-funding information, attacked an Australian
  health-sector target and then apologised by email.

### Block C — Lab question walkthrough (~last third)

Back to exam/coursework material: the next lab questions, with the answers and the reasoning:

* Remember the **calling convention**.
* Know the difference between a **thread switch** and a **process switch**.
* There is **no timer in the user library** — the timer lives in the kernel (it is what makes
  preemption possible).
* **Every question maps to a checkpoint** — revise from the checkpoint list.

---

## How this relates to Part 1

Part 1 = the theory of virtualisation (multiplexing / aggregation / emulation, limited direct
execution, vCPU scheduling). Part 2 = the end of that worked example, then the "for fun" extension
that re-uses every OS concept you have learned in a new setting, then lab practice.

If you are revising, read Part 1 for the examinable material and treat Block B of this file as a
worked revision of the same concepts (address space vs context, fork vs sub-agents, traps vs tool
calls, resource allocation vs GPU memory).

---

## Slide-by-slide guide — Part 2 — lecture capture (18:34)

28 distinct slide states were recovered from the recording. Each entry embeds the slide exactly as it appeared on the projector, with the narration that fell inside that slide's time window.

*Times are offsets from the start of this video, not of the whole lecture.*

> **About the slide text.** These are audience photographs of a projected slide, so automatic OCR is not reliable and is deliberately **not** inlined here — read the text off the embedded image. The raw OCR is kept beside the images in `ocr.json` if you want to grep it (treat it as a hint only).

| # | Starts | On screen | Slide |
|---|---|---|---|
| 1 | `00:00:00` | 8.0s | [slide 1](slides/part2/001.png) |
| 2 | `00:00:08` | 4.0s | [slide 2](slides/part2/002.png) |
| 3 | `00:00:12` | 81.0s | [slide 3](slides/part2/003.png) |
| 4 | `00:01:33` | 4.0s | [slide 4](slides/part2/004.png) |
| 5 | `00:01:37` | 26.0s | [slide 5](slides/part2/005.png) |
| 6 | `00:02:03` | 33.0s | [slide 6](slides/part2/006.png) |
| 7 | `00:02:36` | 101.0s | [slide 7](slides/part2/007.png) |
| 8 | `00:04:17` | 69.0s | [slide 8](slides/part2/008.png) |
| 9 | `00:05:26` | 273.0s | [slide 9](slides/part2/009.png) |
| 10 | `00:09:59` | 59.0s | [slide 10](slides/part2/010.png) |
| 11 | `00:10:58` | 14.0s | [slide 11](slides/part2/011.png) |
| 12 | `00:11:12` | 10.0s | [slide 12](slides/part2/012.png) |
| 13 | `00:11:22` | 61.0s | [slide 13](slides/part2/013.png) |
| 14 | `00:12:23` | 36.0s | [slide 14](slides/part2/014.png) |
| 15 | `00:12:59` | 6.0s | [slide 15](slides/part2/015.png) |
| 16 | `00:13:05` | 2.0s | [slide 16](slides/part2/016.png) |
| 17 | `00:13:07` | 9.0s | [slide 17](slides/part2/017.png) |
| 18 | `00:13:16` | 6.0s | [slide 18](slides/part2/018.png) |
| 19 | `00:13:22` | 4.0s | [slide 19](slides/part2/019.png) |
| 20 | `00:13:26` | 12.0s | [slide 20](slides/part2/020.png) |
| 21 | `00:13:38` | 63.0s | [slide 21](slides/part2/021.png) |
| 22 | `00:14:41` | 3.0s | [slide 22](slides/part2/022.png) |
| 23 | `00:14:44` | 21.0s | [slide 23](slides/part2/023.png) |
| 24 | `00:15:05` | 2.0s | [slide 24](slides/part2/024.png) |
| 25 | `00:15:07` | 4.0s | [slide 25](slides/part2/025.png) |
| 26 | `00:15:11` | 8.0s | [slide 26](slides/part2/026.png) |
| 27 | `00:15:19` | 36.0s | [slide 27](slides/part2/027.png) |
| 28 | `00:15:55` | 159.3s | [slide 28](slides/part2/028.png) |


### Slide 1 — `00:00:00` → `00:00:08`

![Slide 1](slides/part2/001.png)

**What was said over this slide** (verbatim auto-transcript)

> If the data are not engaged, it will just run vMb. So A1, so here, there's work, block, port, port, port, unlock.


### Slide 2 — `00:00:08` → `00:00:12`

![Slide 2](slides/part2/002.png)

**What was said over this slide** (verbatim auto-transcript)

> So A1, so here, there's work, block, port, port, port, unlock. So what happens is, port enters a critical section, inside the critical section, inside, and then here it runs out of round-dropping quantum port.


### Slide 3 — `00:00:12` → `00:01:33`

![Slide 3](slides/part2/003.png)

**What was said over this slide** (verbatim auto-transcript)

> So what happens is, port enters a critical section, inside the critical section, inside, and then here it runs out of round-dropping quantum port. On form 1, VMB just does something. So in 2, it can only start working here. And then it just realizes that the spin lock is taken by A1. And all it can do is spin. So it just consumes the CPU and spins. It's like easy waiting. While here in VMB, it would just be working. Okay, so then, in cycle 8, what happens is that A1 comes back, it finishes the work, and then it releases the spin log. So after this, A1 just finished, it's gone. So it will start with a new Yemi, but first, 4-1 has to finish the full cycle of the quantum. So A2 only comes back here and takes the speed of that cycle 12. different country.


### Slide 4 — `00:01:33` → `00:01:37`

![Slide 4](slides/part2/004.png)

**What was said over this slide** (verbatim auto-transcript)

> different country. All right, so that's about it for virtualization.


### Slide 5 — `00:01:37` → `00:02:03`

![Slide 5](slides/part2/005.png)

**What was said over this slide** (verbatim auto-transcript)

> All right, so that's about it for virtualization. So pay attention to this multiplexer integration emulation, direct execution, for virtualization, for virtualization type one that two. This is what you need to know. And some algorithm-part solutions. I don't know. This would be a hard task. I understand this is difficult. Some of you can do it, I'm sure, with some parties.


### Slide 6 — `00:02:03` → `00:02:36`

![Slide 6](slides/part2/006.png)

**What was said over this slide** (verbatim auto-transcript)

> Some of you can do it, I'm sure, with some parties. OK, so now let's talk about the fun part, which is why Harness is a new operating system. It's the first harnesses they appeared in the end of last year and went viral, I would say, in January, February this year, 96. So we need open code, code, codex. These are all about these ones. So there is a lot of similarities about them, and we will talk about those. So the way it works is the following.


### Slide 7 — `00:02:36` → `00:04:17`

![Slide 7](slides/part2/007.png)

**What was said over this slide** (verbatim auto-transcript)

> So the way it works is the following. So an operating system works in this way. We talked about this. So this is your program. Sometimes it calls into the system calls. So by the way, this is not examinable. But from here to the end, it's not examinable. This is for fun. So here, your program calls into the system calls. And this system calls is an entry point for the kernel execution. And the kernel can actually manage the hardware and execute commands on a request of your problem. So the way the agent works is that there is a model which receives your problem. And then what it can do, it can issue tool calls. So for example, it can run bash screens, it can run feather screens, it can write something, edit something and so on. So these two calls and the model calls, they have to go to the harness which is access the kernel. So what it would do it would steer these commands to either CPUs for two calls or two GPUs for LLM requests. And the harness would run on your laptop and will decide where to execute this. So there is a lot of similarities here across step right so basically the harness is the curve in a way and system call is like a tool okay so then harness also checks like the provisions checks access it also needs to manage the sandboxes secure environment where it executes so that your model doesn't escape and conquer the world.


### Slide 8 — `00:04:17` → `00:05:26`

![Slide 8](slides/part2/008.png)

**What was said over this slide** (verbatim auto-transcript)

> and conquer the world. OK, so how it works. It works in a very simple way. So the user prompts the model. And the model can run some tool calls. Or, for example, it can consume some results from the team calls. It is also available. It also can access the disk. It also can write some programs, deploy them, take the output from these programs and so on. So the harness would orchestrate the model requests, like the lab requests and tool calls, and also can spawn sub-agents, for example. So just like you can spawn even for processes, harness can spawn sub-agents. For example, there's a big agent which architects how to solve and how to approach the problem. and you can spawn sub-agents for example smaller models that would search through the internet and find useful information to feed it to the big model okay so let's look at the similarities


### Slide 9 — `00:05:26` → `00:09:59`

![Slide 9](slides/part2/009.png)

**What was said over this slide** (verbatim auto-transcript)

> find useful information to feed it to the big model okay so let's look at the similarities right so processes have any space and the attributes and engines have context so what inside the value cache, what is inside the context, which tokens, which words, which paragraphs, which articles, which source files and so on. So they all form the context. Then, protesters can spawn threats. So here, for example, Harness can spawn several Parnell tuples. For example, it can do web search and Parnell with hundreds of different requests at the same time. This is similar to threats. They will all have the same context but they will look for example at different websites. Then the agents themselves come forth so they can create sub-agents or sub-tasks which operate on their prepared context which is different from the agentic context, from the parent agent context. Then we discuss the system call which reads sharps into the kernel while the tool call is the medium who are transitioning the state from say the environment into the model or from the model to the environment execution environment then harness also does the scheduling and decides what to run which to go to run um secrecy or asynchronously blocking or non-blocking and so on there are also interrupts if you have asynchronous processing so for example there is a web search that completes and needs to be given to the model once it completes it also has the interrupt pass just like we have it in the operating system so the concepts are also similar to for example inside the harness the process needs to understand who is working on each task right and how to synchronize among each because they have access to specific files or specific folders or specific information and that has to be managed in the same way as with the synchronization, for example mutual exclusion. Then of course they need to allocate, for example if they are to share GPU, how does these agents share the amount of memory inside the GPU? So that the whole Argentine workflow can make progress. For example, the main engine can take half of the GPU memory, and then it can spawn, let's say, two sub-edges that can execute within the second half of the memory. But then if it happens that your Argentine workflow keeps spawning engines, they may actually start trashing just like what happens if you run out of memory or run out of disk. so the whole workflow will actually end up stuck due to the lack of resources. Then the execution environment for tools is nothing but virtualization, it's virtual machines or containers, so this is exactly what we discussed today. And for memory or context window is actually super super interesting, we will not talk about it, but this is really where it is in the art right now. memory systems or long horizon agents how do the agents share memory how do they exchange experiences so you can think of agents sharing parts of their brains like humans sharing part of their brains or their experiences completely transparent you may also heard of news about aging swarms hacking some I think the way this news came out yesterday when some engines were hacked Australia and I think Australian health industry because somebody asked these engines like I need some information on the funding of health programs or something like this so the agents were just like if I need to solve this question I just I mean the easiest thing is to just go to healthcare and hack it so they did and I sent an email to healthcare ministry in Australia and said look we are apologizing but we hacked you. And then two months after, two months after, Australian government said like this is not nice we just read it. So you can see how behind we are, right, containing this thread. Well, it's a fun world. Okay, so as we discussed the forks and processes, right,


### Slide 10 — `00:09:59` → `00:10:58`

![Slide 10](slides/part2/010.png)

**What was said over this slide** (verbatim auto-transcript)

> Okay, so as we discussed the forks and processes, right, so agents can spawn sub-agents and they can create fresh context and they can also see how these agents share information so today it's more like message passing so we talked about message passing in the first lecture right but the future is of course shared memory you want engines to share memories so that we can streamline the communication there as opposed to transferring everything into tokens sending the tokens Okay, then another important thing is where does virtualization comes? Well, virtualization comes with GPU aggregation in the GPU cluster where we actually execute the models and the tool execution environment which is containers, virtualization and so on. So this is where tools are running.


### Slide 11 — `00:10:58` → `00:11:12`

![Slide 11](slides/part2/011.png)

**What was said over this slide** (verbatim auto-transcript)

> So this is where tools are running. Okay, so whenever you have shared state you need security. So this is what happens.


### Slide 12 — `00:11:12` → `00:11:22`

![Slide 12](slides/part2/012.png)

**What was said over this slide** (verbatim auto-transcript)

> So this is what happens. So there are different ways of sandboxing the tools. and over here, see it here?


### Slide 13 — `00:11:22` → `00:12:23`

![Slide 13](slides/part2/013.png)

**What was said over this slide** (verbatim auto-transcript)

> And yeah, there's a huge problem with protection and security. So I just encourage you to look at it and see what matters. So for example, to support an engine, you don't need to hack the kernel there. You can just poison the skills, for example. so that the agent behavior changes in your favor. This is pretty scary and pretty difficult to detect with scarring antivirus. Yeah, and finally, the memory system is really important. So memory system is agentic on its own. You can think of there is an agent that manages the memory experiences, what do we read, what do we include into the context and what do we exclude from the context and what do we write for future. I encourage you to install for example here means or go at home


### Slide 14 — `00:12:23` → `00:12:59`

![Slide 14](slides/part2/014.png)

**What was said over this slide** (verbatim auto-transcript)

> and what do we write for future. I encourage you to install for example here means or go at home and see how it develops memories about you and what you ask. It's really interesting. And sharing these memories is actually an awful problem because for example if you develop a super useful skill that works for you, How exactly do you share it with your teammates? For example, it's an unsolved problem. Okay, cool. So now what I'm going to do is I'm going to show you the next two questions for the lab, please. And then if we have time, maybe a couple more.


### Slide 15 — `00:12:59` → `00:13:05`

![Slide 15](slides/part2/015.png)

**What was said over this slide** (verbatim auto-transcript)

_No speech detected in this window._


### Slide 16 — `00:13:05` → `00:13:07`

![Slide 16](slides/part2/016.png)

**What was said over this slide** (verbatim auto-transcript)

_No speech detected in this window._


### Slide 17 — `00:13:07` → `00:13:16`

![Slide 17](slides/part2/017.png)

**What was said over this slide** (verbatim auto-transcript)

> Thank you.


### Slide 18 — `00:13:16` → `00:13:22`

![Slide 18](slides/part2/018.png)

**What was said over this slide** (verbatim auto-transcript)

> Thank you.


### Slide 19 — `00:13:22` → `00:13:26`

![Slide 19](slides/part2/019.png)

**What was said over this slide** (verbatim auto-transcript)

> Thank you.


### Slide 20 — `00:13:26` → `00:13:38`

![Slide 20](slides/part2/020.png)

**What was said over this slide** (verbatim auto-transcript)

> Thank you. This is our piece 2.


### Slide 21 — `00:13:38` → `00:14:41`

![Slide 21](slides/part2/021.png)

**What was said over this slide** (verbatim auto-transcript)

> This is our piece 2. Thank you. So this is a correct answer.


### Slide 22 — `00:14:41` → `00:14:44`

![Slide 22](slides/part2/022.png)

**What was said over this slide** (verbatim auto-transcript)

> So this is a correct answer.


### Slide 23 — `00:14:44` → `00:15:05`

![Slide 23](slides/part2/023.png)

**What was said over this slide** (verbatim auto-transcript)

> So this is a correct answer. We have to remember the previous questions were a bit easier, right? Progressive easier. This is what we discussed yesterday. So now we're moving to slightly more deep-blood ones.


### Slide 24 — `00:15:05` → `00:15:07`

![Slide 24](slides/part2/024.png)

**What was said over this slide** (verbatim auto-transcript)

> So now we're moving to slightly more deep-blood ones. This is the explanation.


### Slide 25 — `00:15:07` → `00:15:11`

![Slide 25](slides/part2/025.png)

**What was said over this slide** (verbatim auto-transcript)

> This is the explanation.


### Slide 26 — `00:15:11` → `00:15:19`

![Slide 26](slides/part2/026.png)

**What was said over this slide** (verbatim auto-transcript)

> This is the explanation. So you do need to remember you borrowed the quality convention.


### Slide 27 — `00:15:19` → `00:15:55`

![Slide 27](slides/part2/027.png)

**What was said over this slide** (verbatim auto-transcript)

> So you do need to remember you borrowed the quality convention. And you also need to distinguish thread switches from process switches. So you need to know the theory, and then you need to know the maps to practice and what is available at different levels. For example, there is no timer in the library. The timer is in the car for internal interaction. Okay, let's do the next one. And then start the timer.


### Slide 28 — `00:15:55`

![Slide 28](slides/part2/028.png)

**What was said over this slide** (verbatim auto-transcript)

> And then start the timer. Can you guys start the timer? Thank you. Okay, so the right answer is B. I think quite a few people answered it correctly. Is this not too bad? and explanation. So, you can also think about this, like the mapping for lab 1, lab 2? Like what these questions test. So actually every single question there will be mapped on one of the checkpoints. You remember checkpoints? So this is your, you should go to checkpoints and see if you understand everything in the checkpoint list. I understand that some of you will have a lab today. So you can just take it to prepare. All right, cool. So if you have anything to share through previous Google Cloud, let me know. I remember there were some questions.

