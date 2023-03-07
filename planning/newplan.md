# New Dissertation Plan

---

### Reasons to Change

To preface, there's approximately 11 weeks from now until hand-in. I'd like to have the project close to finished in 9, leaving the final 2 as 'ironing-out' time. 
I don't believe I can meet this deadline given the current direction and scope of my project.

While writing my *Survey and Analysis*, I had shifted the scope of the project to be looking at creating an improved ASR system specifically for elderly people. 
While I believe that this still provides some value for my final project, I've decided that the scope of this problem is much too large for me to comfortably produce a high-quality, comprehensive piece of work.

Instead, I believe that returning to my original plan and creating a semi-automated transcription tool would provide a much more concise and reasonable project scope, as well as being something I am *much* more comfortable working on.

---

## Plan

Feedback I received on my previous plan indicated an uneven allocation of workload across weeks; I've tried to keep this in mind when assigning tasks for each week, though I note that the workload of other modules is due to increase towards the end of the semester.
To ease my total workload for this semester, I have allocated important decisions (such as building a basic UI to build from) earlier.

As mentioned in the first section, I will be providing a strong plan for the only the first 9 weeks, leaving the 2 remaining weeks as time to refine the project and provide some leeway to deal with inevitible unforseen issues before hand-in.


### Work To Do

Before organising work into a weekly schedule, I've broken down what work I currently believe needs to be completed in no particular order;

- A Literature Review 
  * The current lit. review in the *Analysis* stage was incomplete and did not provide a suitable level of detail. 
  * The new project scope will require a different focus than what has already been produced, as well as some refinement which should result from a new review.
  * I have difficulty producing long written pieces so I will aim to keep a more comprehensive set of notes.
  * In the *Analysis* stage, I failed to keep a coherent flow of ideas, resulting in a total loss of the original aims I'd set out. To combat this, I shall commence my reviews of literature by setting out questions I need to answer, rather than just searching for information about a topic.

- UI Design
  * Decide on an appropriate workflow, e.g. what UI should be provided to allow a user to generate new Whisper transcriptions (and who is generating this?)
  * Should the UI be graphical or would a terminal-operated tool be suitable?
  * In what language shall this be programmed? All Whisper-related code will be in Python, but is this the best option for UI?
  * What information should be available to the user? Are low-confidence words highlighted or hidden?
  * Some review of existing tools may be worthwhile, though I'd obviously like to avoid plagiarism 

- Finding (or generating) a Confidence Metric
  * Is there already some confidence score within Whisper? (There is an `average logprob`, but can I extract some 'per-word' metric?)
  * Assuming I don't find a confidence score, how could I attempt to generate one? There is literature on this!

- Understand the Purpose of Semi-Automated Transcription
  * Benefits? Hinderances?
  * Versus fully-automatic (i.e. ASR)
  * Versus fully-manual
  * Temporal and financial costs compared with system accuracy
  * This may be aided by some kind of demonstration, perhaps testing my system using volunteers.

I'm sure that this won't be representative of every single task to complete or question to answer, but I believe that this list gives a reasonable place to start building a plan from.

---

### Week-by-week Breakdown

#### Week 1

- Re-review literature, fleshing out what has already been written and removing parts which no longer relate to the project (elderly speech, fine-tuning ASR).
- Begin surveying literature on semi-automated transcription and transcription in general, making sure to take notes. 

#### Week 2

- Decide on a language (Rails? Node.js? Rust?) to build a UI in. I currently believe that an in-browser app would be a good way to go because developing GUI across platforms seems like an unnecessary complexity for this project.
- Produce some user interface designs, perhaps following what Jon had described (differing levels of automation, would be a very interesting idea).

#### Week 3

- Produce some basic UI to be refined through the project. This will enable testing and a solid foundation to build from.

#### Week 4

- Search for literature relating to ASR confidence/intelligibility scoring. Is the `average logprob` that Whisper produces a potentially relevant metric?
- Use Whisper to transcribe some corpus data and try out confidence score techniques. Perhaps use WER to determine how well a technique has performed.

#### Week 5

- 

#### Week 6

- 

#### Week 7

- 

#### Week 8

- 

#### Week 9

- 

