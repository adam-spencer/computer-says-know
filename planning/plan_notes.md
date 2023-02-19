# New Plan Notes


## Where I'm At

- I've moved away from the intended scope of the project
- The original plan was focused on creating a tool to enable semi-automated transcription
- My new plan moved towards altering Whisper but this was deemed too wide a scope for a dissertation to take - makes sense to me!
- To remedy this, JB has requested I consolidate a plan for the remainder of the project. 
- Another criticism of my work was that the plan I had produced already wasn't detailed enough (along with the rest of the project).


## What Now?

- Re-review literature, **shift focus away from elderly speakers and more towards automating transcription**
  - May still consider the elderly speaker part, though I don't see it being particularly useful for this new scope.
  - This is pretty urgent- if I can get work going on the lit review I won't have to consider it later.
- **Significantly increase the level of detail in the current lit review**
- Do small bits of writing regularly - I struggle with finding time to do large writings/get very bored. May be worth writing lots more notes!

- Modify Whisper to produce some *per-word confidence metric* - perhaps this is already somewhere within Whisper? (there is an `average logprob` score)

- Create GUI/TUI for semi-automated transcription
  1. **Design** - should I use GUI or TUI? I suppose this would require some assumption about who the intended user is (how familiar they are with a computer). Also need to factor in developing on MacOS for Windows users - I think TUI may be the way to go?
  2. **Workflow** - should Whisper run in-the-moment or be run in batch and then pass results to the tool?
  3. **UX** - how much information should be passed to the user? Do they see what the predicted output was?
  4. **Language** - What language should this be written in? *Rust* may be a good option?

- Demonstrate the benefit of semi-auto transcription
  - Compare speed of manual and semi-automated transcription
  - Compare accuracy of manual/semi-/automatic transcription


## What Shape Shall the Plan Take?

The project is due on **May 10th**, with a presentation on the **3rd**.

This gives me just about 11 weeks to finish. It'd be best if I could get this project rolling ASAP because, as seen in the analysis stage, rushing it ruins it.

With a stronger focus on creating a tool I should have more time for coding (yay) which should be way more fun :)

Again, however, I need to get this lit review out of the way. Just thinking about it is causing me a real ass pain right now. Maybe I should get that checked...
