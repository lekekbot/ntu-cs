# SC2005 — Virtualisation, Part 1 (lecture recording)

> **Source:** `video_2026-10-02_15-15-01.mp4` · **Length:** 23:01 · **Recorded:** 2 Oct 2026
> **Where it sits:** the capture starts mid-topic (a lecturer mid-sentence about running x86/ARM binaries)
> and ends just as the lecturer is about to walk through the CPU-scheduling "ledger" example.
> The walkthrough itself is in **Part 2** (`..._15-15-01 (2).mp4`), which opens on the same example.

This is a photograph-style audio/video capture of a lecture hall: three projectors, all mirroring the
same deck, with the camera panning between framings. The slides below were recovered from the video
(cropped to the projection screen and de-duplicated by image similarity). The narration is the
automatically transcribed audio for each slide's time window, kept verbatim so nothing is lost.

The deck displaying these slides identifies itself as **"Virtualization Overview"** (about 32 pages),
so this session is a walkthrough of that deck plus live Wooclap questions.

---

## What the lecture covers

The whole session is about **virtualisation**: how one physical machine is made to look like several
(or like a different machine), and what the operating-system consequences are.

### 1. Emulation vs. virtualisation — the motivating examples

* Apple switched Macs from Intel to ARM (2020+): Intel programs still run, but only because of a
  translation/emulation layer.
* Old Nintendo games running in an emulator on a PC: the emulator *is* the interface.
* These matter because they set up the central distinction used for the rest of the lecture:
  **emulation changes the *kind*** of machine you present, while **multiplexing and aggregation
  change the *count*** (how many of the real resources are visible). This one-liner is worth
  memorising — the Wooclap questions test exactly this.

### 2. The three mechanisms, with the "real world" analogies

The lecturer uses everyday Singaporean examples as a memory hook:

| Mechanism | What it does | Real-world analogy used in class |
|---|---|---|
| **Multiplexing** | many users share one resource, one at a time (in time) | 5 courses sharing one lecture slot — one course at a time, not five at once |
| **Aggregation** | many resources are hidden behind a single interface | campus Wi-Fi: dozens of access points, one SSID, seamless switching |
| **Emulation** | one thing is made to behave as something else | using your phone as a hotspot — the phone *becomes* a router |

### 3. vCPUs are just processes (on the host)

* The **guest OS** sees its vCPUs as *real* CPUs: it maintains its own ready queues, its own
  scheduler, its own process state machines.
* The **host** sees only vCPUs (one per virtual CPU per VM) and schedules them with the *same*
  machinery it uses for processes — the host ready queue holds **vCPUs, not processes**.
* Consequence: **two decoupled state machines**. Every process inside a VM has a state machine;
  every vCPU outside has its own, on the host. They progress independently, and the guest has no
  guarantees about when its vCPU actually runs.
* Worked numbers from the lecture: 8 VMs × 2 vCPUs = **16 vCPUs to schedule on 4 physical cores**.
  That is only possible because vCPUs are not always runnable; a *partitioned* scheduler can pin
  4 vCPUs to one core and swap them there.
* The hypervisor **does not pause VMs** — it schedules each vCPU separately. And, exactly as with
  ordinary processes, there is **no fairness guarantee**.

### 4. The layered model (formal definition)

```
  application(s)
  guest operating system          <- real interface to its processes
  virtual hardware                <- what the VMM exposes
  virtual machine monitor (VMM) / hypervisor
  physical hardware
```

The VMM/ hypervisor owns the physical hardware and decides how to expose it: cores, memory and
network can be **multiplexed in time or partitioned in space**; disks and NICs can be
**aggregated** (many logical drives for many VMs) or handed to a specific VM; and some devices are
**emulated** (legacy NICs, legacy keyboard abstractions). Two goals: **efficiency** and
**isolation** — no VM should notice it is virtual or that it shares hardware.

### 5. Limited direct execution (the key mechanism)

You cannot translate every instruction executed inside a guest; instead, the interesting
instructions **trap** from the guest into the VMM, which emulates the effect and returns. This is
*limited direct execution*: run guest code natively, but trap on the privileged/sensitive subset.

### 6. Worked example: a spinlock across two vCPUs

The last stretch of the recording is the setup for the "ledger" exercise — two vCPUs (A1, A2) on
two cores, a guest spinlock, a time quantum, and the question of what each core actually runs in
each cycle. The lecturer stresses two failure modes:

* assuming **one** state machine when there are two (guest-side and host-side),
* forgetting that a spinning vCPU is *running* (burning its core) while a blocked one is not.

Fixes discussed: a **blocking mutex** (the vCPU halts and yields the core) and
**para-virtualisation** (the guest tells the VMM "I hold this lock").

---

## Lecturer's "make sure you know this" list

* "The three — aggregation, multiplexing, emulation — **and direct execution** is very, very
  important."
* **Virtualisation type 1 vs type 2** (bare-metal vs hosted hypervisor).
* Distinguish **emulation (changes the kind)** from **multiplexing/aggregation (change the count)**.
* vCPU scheduling: host ready queue holds vCPUs; guest ready queue holds processes.
* The lecturer points at the **pre-recorded lectures** for the theory that this session practises.

## How to revise from this file

1. Read the summary above.
2. Skim the slide table to see the deck order, then work through the slide-by-slide entries.
3. Use each slide image to re-read the diagram — the OCR text loses the layout, and several slides
   are diagrams (layered model, VM/VMM boxes, the ledger table).
4. The narration under each slide is the raw transcript; it is noisy (ASR), but it is faithful to
   what was said, including which Wooclap options students picked wrong and why.

---

## Slide-by-slide guide — Part 1 — lecture capture (23:01)

23 distinct slide states were recovered from the recording. Each entry embeds the slide exactly as it appeared on the projector, with the narration that fell inside that slide's time window.

*Times are offsets from the start of this video, not of the whole lecture.*

> **About the slide text.** These are audience photographs of a projected slide, so automatic OCR is not reliable and is deliberately **not** inlined here — read the text off the embedded image. The raw OCR is kept beside the images in `ocr.json` if you want to grep it (treat it as a hint only).

| # | Starts | On screen | Slide |
|---|---|---|---|
| 1 | `00:00:07` | 58.0s | [slide 1](slides/part1/001.png) |
| 2 | `00:01:05` | 25.0s | [slide 2](slides/part1/002.png) |
| 3 | `00:01:30` | 3.0s | [slide 3](slides/part1/003.png) |
| 4 | `00:01:33` | 6.0s | [slide 4](slides/part1/004.png) |
| 5 | `00:01:39` | 83.0s | [slide 5](slides/part1/005.png) |
| 6 | `00:03:02` | 17.0s | [slide 6](slides/part1/006.png) |
| 7 | `00:03:19` | 27.0s | [slide 7](slides/part1/007.png) |
| 8 | `00:03:46` | 30.0s | [slide 8](slides/part1/008.png) |
| 9 | `00:04:16` | 7.0s | [slide 9](slides/part1/009.png) |
| 10 | `00:04:23` | 138.0s | [slide 10](slides/part1/010.png) |
| 11 | `00:06:41` | 77.0s | [slide 11](slides/part1/011.png) |
| 12 | `00:07:58` | 95.0s | [slide 12](slides/part1/012.png) |
| 13 | `00:09:33` | 4.0s | [slide 13](slides/part1/013.png) |
| 14 | `00:09:37` | 2.0s | [slide 14](slides/part1/014.png) |
| 15 | `00:09:39` | 3.0s | [slide 15](slides/part1/015.png) |
| 16 | `00:09:42` | 306.0s | [slide 16](slides/part1/016.png) |
| 17 | `00:14:48` | 109.0s | [slide 17](slides/part1/017.png) |
| 18 | `00:16:37` | 54.0s | [slide 18](slides/part1/018.png) |
| 19 | `00:17:31` | 7.0s | [slide 19](slides/part1/019.png) |
| 20 | `00:17:38` | 181.0s | [slide 20](slides/part1/020.png) |
| 21 | `00:20:39` | 109.0s | [slide 21](slides/part1/021.png) |
| 22 | `00:22:28` | 5.0s | [slide 22](slides/part1/022.png) |
| 23 | `00:22:33` | 20.4s | [slide 23](slides/part1/023.png) |


### Slide 1 — `00:00:07` → `00:01:05`

![Slide 1](slides/part1/001.png)

**What was said over this slide** (verbatim auto-transcript)

> So, programs written for Intel smoothly, even though Apple at some point swapped the chip from Intel to ARM that they developed themselves. So, if you are using Apple Mac produced after 2020, it's very likely that you are using ARM, but you can still run xv6 programs. Another idea of it is, for example, if anyone plays old computer games from Nintendo or from something like this on the PC, this works through the emulator. So you have the emulator of Nintendo running on your computer, and then you can run many different programs with it. Okay, so this is the most important theory of how virtualization actually works. You should definitely find more details in the pre-recorded lectures, but let us now go directly into the practice.


### Slide 2 — `00:01:05` → `00:01:30`

![Slide 2](slides/part1/002.png)

**What was said over this slide** (verbatim auto-transcript)

> So let's take a look and also see what we can do.


### Slide 3 — `00:01:30` → `00:01:33`

![Slide 3](slides/part1/003.png)

**What was said over this slide** (verbatim auto-transcript)

> So let's take a look and also see what we can do.


### Slide 4 — `00:01:33` → `00:01:39`

![Slide 4](slides/part1/004.png)

**What was said over this slide** (verbatim auto-transcript)

> So let's take a look and also see what we can do. So here we are talking about the real world analogy for all these three concepts.


### Slide 5 — `00:01:39` → `00:03:02`

![Slide 5](slides/part1/005.png)

**What was said over this slide** (verbatim auto-transcript)

> So here we are talking about the real world analogy for all these three concepts. So one lecture better in five courses. it means that courses one by one will be given into the lecture credit. So we will not have five courses in one lecture credit, we will have one at a time. So that's multiplication, that's not application. So people who voted B, they confused this point, but here for example, there is a lot of access points on campus. So for example, there are so many routers and you go anywhere and there is the same Wi-Fi network, you don't need to enter your password. Again, you don't need to choose another network. How does it work? That works through aggregation. So actually, as you move through the campus, your phone smoothly reconnects from one point to another point, always chooses the closest point and just keeps going without bothering you. So you don't need to reconnect to Wi-Fi. This is a classic example of aggregation. Yeah, and emulation is for example when you just try to access internet with your phone. So for your browser it actually doesn't matter at all, maybe it's a router, maybe it's your phone, it doesn't matter. So your phone becomes a router. Emulates a router.


### Slide 6 — `00:03:02` → `00:03:19`

![Slide 6](slides/part1/006.png)

**What was said over this slide** (verbatim auto-transcript)

> Emulates a router. Let's get it through. Okay, let's move to the next one.


### Slide 7 — `00:03:19` → `00:03:46`

![Slide 7](slides/part1/007.png)

**What was said over this slide** (verbatim auto-transcript)

> Okay, let's move to the next one. And switch from the book on. So most of you did answer right, but some of you missed this part.


### Slide 8 — `00:03:46` → `00:04:16`

![Slide 8](slides/part1/008.png)

**What was said over this slide** (verbatim auto-transcript)

> So most of you did answer right, but some of you missed this part. And here there is still confusion with the 100 cars shared by 8 PMs. That means multiplexing connection. So 8 EMs would multiplex to access the same network card. This is the classic example for obligation, we mentioned, when two links can be connected to one. OK.


### Slide 9 — `00:04:16` → `00:04:23`

![Slide 9](slides/part1/009.png)

**What was said over this slide** (verbatim auto-transcript)

_No speech detected in this window._


### Slide 10 — `00:04:23` → `00:06:41`

![Slide 10](slides/part1/010.png)

**What was said over this slide** (verbatim auto-transcript)

> Okay, let's keep going. So let's talk a little bit more about multiplexing. So I told you that there are vCPUs which are scheduled as processes on the host, but inside the guest OS they are regarded as real CPU. So they are a real course for the guest OS kit. So what the guest OS kit there does, it manages the RdQ, it sends the process, it's assigned the process to virtual CPUs and those processes would kind of clog that CPU for a while. But at the same time, the host site, what's called hypervisor, or the host OS, it only sees the ECP. So it knows that there are two VMs, and each of these VMs, for example, have, or for example, here, eight VMs, each one of them has two ECPUs. That means there are 16 ECPUs to schedule on the host. So that would be equivalent to scheduling 16 processes on the host. Moreover, some of these vCPUs can be inactive because maybe the guest has nothing to run and that is why you can actually map these 16 vCPUs on 4 cores How? Because for example you have a partition scheduler, you map 4 vCPUs to 1 core and then they will just swap on that core So that would mean that the host OS would also, for the hypervisor, would also have a ready queue in the host, but in that ready queue there will be vCPUs, not processes. While in the guest OS there will be ready queue in front of each vCPU owned by that virtual machine. So the state machine in that case would be replicated. There is a state machine for each process inside each virtual machine, and there is also a state machine for each of the VCPUs outside on the host. Okay, let's do another example.


### Slide 11 — `00:06:41` → `00:07:58`

![Slide 11](slides/part1/011.png)

**What was said over this slide** (verbatim auto-transcript)

> Okay, let's do another example. And I started with a... Thank you. I can sense some confusion in the ear, but most people did get it right and I actually


### Slide 12 — `00:07:58` → `00:09:33`

![Slide 12](slides/part1/012.png)

**What was said over this slide** (verbatim auto-transcript)

> I can sense some confusion in the ear, but most people did get it right and I actually encourage people to participate more actively. If you are here, please walk. That's why you are practicing. Okay, so again, let's think about it. Each vCPU is like a process on the host. So in that regard, that means each of these processes can be scheduled independently. so at most four BCPUs can execute because you have four real physical cores right so all others would be in the ready state while this core would be in the right state. At the same time the state machine is completely decoupled so the guest OS will have processes in the ready cubes And some of them will be in the running state, some of them will be in the ready state. This is based on how the guest OS assigns them to the VCPUs. So it's independent from the host side. So here, and here, these are managing confusions here. So for the hypervisor doesn't pause VMs because it doesn't manage VMs. It manages each VCPU separately. And here, there is no guarantees, right? Just like there is no guarantees for processes to share the CPUs equally, there is no guarantees for the hypervisor to do it.


### Slide 13 — `00:09:33` → `00:09:37`

![Slide 13](slides/part1/013.png)

**What was said over this slide** (verbatim auto-transcript)

_No speech detected in this window._


### Slide 14 — `00:09:37` → `00:09:39`

![Slide 14](slides/part1/014.png)

**What was said over this slide** (verbatim auto-transcript)

_No speech detected in this window._


### Slide 15 — `00:09:39` → `00:09:42`

![Slide 15](slides/part1/015.png)

**What was said over this slide** (verbatim auto-transcript)

_No speech detected in this window._


### Slide 16 — `00:09:42` → `00:14:48`

![Slide 16](slides/part1/016.png)

**What was said over this slide** (verbatim auto-transcript)

> Okay, that's one more. So, the next is the formal definition of these layers. So we talked about the approaches. So we talked about multiplexing, aggregation, and emulation. So now let's talk about layers. So here, the guest OS is just like we learned before. So there is application, there is an operating system here, there is emulate virtual hardware here. But then there is another layer called virtual machine monitor or monitor or hypervisor, which emulates these virtual devices by multiplexing, aggregating, or emulating the real hardware for those fields. So it does so that the programs can run efficiently, but also so that they are isolated from each other, so that none of them actually is aware that it's virtual, not real, and it actually shares real hardware with someone else. So the hypervisor here is in control of the real hardware and decides how to expose this hardware to each of these virtual machines. For example, cores can be multiplexed, memory can be multiplexed, network can be also multiplexed, or maybe like either in space or in time, for example assigning network cards to a specific VM, or assigning NGPU to a specific VM. can be both multiplexed and aggregated, so there could be many disks exposed to many VMs as separate logical drives or same logical drives, and then some of the hardware can be emulated because maybe some of the virtual machines they use some old network card or old keyboard abstractions. Okay, so how does it actually work? The key here is what's called limited direct execution and this is really really important for you to understand. So the three aggregation multi-boxed emulation and direct execution is very very important. So we cannot really emulate every single instruction that runs inside the virtual machine so that it translates into the instruction in the host so instead we separate the instructions which require trap into the guest to us and the guest to us may trap into the heart provider right and finally there is this vector so most of the instructions will still be just arithmetic and it actually doesn't matter which of these three layers issues this arithmetics, it doesn't matter. So that's what's called direct execution. For example, if it's just arithmetics, it doesn't matter whether it's an application layer or the guest source. But if this is a previous instruction, then the application first needs to trap into the guest OS. For example, when it issues the system hold, hold process and interrupt. And then sometimes when the guest operating system needs to access real hardware, it has to trap into the DMM as well. So what's important to understand here is that each of these layers can either execute directly if it's like a harmless execution, but there is no privileged, no sensitive instructions here, or it will trap into the next layer. But in the system, the application layer cannot directly access the VMM, or for example, the hardware cannot be directly accessed by the application or the guest OS, except for direct execution. Okay. So just remember that adjusting the layers can talk to each other, but the layer is cannot be skipped. So for example, the application will never know that the hypervisor is there. Okay. So let's do another.


### Slide 17 — `00:14:48` → `00:16:37`

![Slide 17](slides/part1/017.png)

**What was said over this slide** (verbatim auto-transcript)

> Okay. So let's do another. Thank you. Thank you. milligram So the correct answers are A and C but some of you will also choose B


### Slide 18 — `00:16:37` → `00:17:31`

![Slide 18](slides/part1/018.png)

**What was said over this slide** (verbatim auto-transcript)

> but the app system call goes to the guest server it doesn't really go to the hypervisor because the application cannot access hypervisor so it's the guest OS that needs to mitigate which is captured Okay. Okay, so another thing that is important for lecture quizzes, for concept quizzes, is the types of improvisers. So for this, I will just show you this thing. And I encourage you all to spend more time understanding what is type 1 versus type 2 and so on. thing is that important for this practice so let's capture this information and this is the


### Slide 19 — `00:17:31` → `00:17:38`

![Slide 19](slides/part1/019.png)

**What was said over this slide** (verbatim auto-transcript)

> thing is that important for this practice so let's capture this information and this is the the past and this is the explanation


### Slide 20 — `00:17:38` → `00:20:39`

![Slide 20](slides/part1/020.png)

**What was said over this slide** (verbatim auto-transcript)

> the past and this is the explanation so this I just encourage you to look into the pre-recorded lectures pretty easy it's more fun you just need to remember what is type 1, type 2, or Okay, so now let's consider a complex problem, which we need to consider two scanners and two stick machines. So here we have a round-roaming over two PCPUs, where each VM would get four units, four cycles, per turn. So if PCPU doesn't execute, then there is nothing happening, and if there is a spin-lock, then it works like a regular spin-lock. That's all. Nothing is different. So what you need to understand is how processes and VNs swap each other on the cores. cores. So let's take a look. So here for example what you see is there are two cores and there are two VMs. VM-A owns BCPUs A0 and A1. So basically there are two processes. There are two BCPUs A0 and A1. and BMP has P0 and P1 ECPUs, and BMA has two processes, A1, like small A1, small A2, which actually have some synchronization between them. So you can see how this A1 and A2 are implemented. So you can see that first cycle there is work, second cycle there is lock then followed by warp then there's two cycles of warp and then finally there is a warp ending up in unlock and warp and exit here so this is a per cycle distribution of what these And then we have the round-robin here. So for 4.0, it will execute vCPU easier, then vCPU easier, then vCPU easier. So this is a partitioned scheduler here on the host. so it would take one BCBU from BMA and one BCBU from BMP. So you will see it B1, A1, B1, B1, B1, the multiplex and core 1. So they don't really jump from one core to another. So your goal here is to understand how does it work and show on the ledger.


### Slide 21 — `00:20:39` → `00:22:28`

![Slide 21](slides/part1/021.png)

**What was said over this slide** (verbatim auto-transcript)

> It's not difficult, just think about two cores independently on the host and who gets scheduled on that core. Start the web. Thank you. Okay, so the correct answer is B. So let's see what happens.


### Slide 22 — `00:22:28` → `00:22:33`

![Slide 22](slides/part1/022.png)

**What was said over this slide** (verbatim auto-transcript)

> Okay, so the correct answer is B. So let's see what happens.


### Slide 23 — `00:22:33`

![Slide 23](slides/part1/023.png)

**What was said over this slide** (verbatim auto-transcript)

> Okay, so the correct answer is B. So let's see what happens. before we see what happens, let's do another one. Then I'll show you the core ledger. Or maybe you just capture this one, and I'll show you the ledger directly. Just capture it, okay? This way of practice.

