# NAO Virtual Storyteller — Research Project

## Abstract
This research project explores the feasibility of integrating generative AI with the NAO humanoid robot to create a virtual storyteller designed for caregivers, educators, and professionals in assistive and therapeutic fields. Studies indicate that individuals with Autism Spectrum Disorder (ASD) often find robots more approachable and predictable than human partners, making robotic interaction a valuable tool for fostering communication and social skills. By leveraging the NAO robot’s built-in audio functionality as the primary mode of interaction, this project examines how robotics and generative AI can enhance interactive storytelling.

The system implementation will utilize Google Dialogflow CX to manage conversational flow and process user input, working in conjunction with a Conversational Retrieval-Augmented Generation (CoRAG) model. CoRAG enhances storytelling continuity by adapting to user choices and thematic preferences over multiple interactions. Instead of generating isolated responses, CoRAG enables the storyteller to retain user preferences and past interactions, ensuring context-aware, progressively enriching narratives. The storyteller will process verbal input—such as user choices, questions, and themes—to generate personalized stories set in engaging fictional worlds, including space adventures and fantasy realms.

Caregivers, educators, and professionals working with ASD may benefit from NAO-integrated storytelling as a tool for engagement and guided learning. By leveraging CoRAG, we aim to develop an accessible and contextually adaptive storytelling platform that fosters meaningful interaction within caregiver-supported environments. Looking ahead, we envision a future where the NAO robot’s mechanical expressiveness further enhances the storytelling experience through emotionally expressive movements, deepening engagement and immersion.

---

## Research

### Core Research

1. **[A Systematic Review of Artificial Intelligence Technologies Used for Story Writing](https://www.researchgate.net/publication/369799144_A_systematic_review_of_artificial_intelligence_technologies_used_for_story_writing)**  
   *Fang, Xiaoxuan; Ng, Davy Tsz Kit; Leung, Jac; Chu, Samuel. (2023).*  
   *Education and Information Technologies*. https://doi.org/10.1007/s10639-023-11741-5  

   - Validates AI-driven storytelling for engagement and creativity.  
   - Supports the CoRAG (Conversational Retrieval-Augmented Generation) approach.  
   - Highlights challenges in coherence, emotion, and user engagement.  
   - Encourages human-AI collaboration — AI assists rather than replaces.

2. **[Integrating GPT-Based AI into Virtual Patients](https://pmc.ncbi.nlm.nih.gov/articles/PMC11669881/)**  
   *Gutiérrez Maquilón R, Uhl J, Schrom-Feiertag H, Tscheligi M. (2024).*  
   *JMIR Form Res.* https://doi.org/10.2196/58623  

   - Demonstrates GPT in real-time verbal interactions.  
   - Emphasizes reducing AI response latency for better usability.  
   - Aligns with CoRAG and prompt engineering techniques.  
   - Notes the role of expressive speech and gestures.

3. **[Designing AI-Enabled Games for Children with Autism](https://arxiv.org/abs/2404.15576)**  
   *Lyu, Y.; An, P.; Zhang, H.; Katsuragawa, K.; Zhao, J. (2024).*  
   *CHI 2024 Workshop*. arXiv:2404.15576  

   - Applies adaptive storytelling for emotional development.  
   - Suggests multimodal feedback via NAO’s movements.  
   - Highlights robotic integration potential.

4. **[Human-Mediated LLMs for Robotic Intervention](https://arxiv.org/abs/2402.00260)**  
   *Mishra, R.; Welch, K. C.; Popa, D. O. (2024).*  
   arXiv:2402.00260  

   - LLMs generate meaningful real-time dialogue.  
   - Human-mediated AI ensures appropriateness.  
   - Discusses NAO’s speech recognition limitations and therapy potential.

5. **[Robots vs Humans: Social Interaction with ASD](https://www.mdpi.com/2076-328X/14/2/131)**  
   *Dubois-Sage, M.; Jacquet, B.; Jamet, F.; Baratgin, J. (2024).*  
   *Behavioral Sciences*, 14(2), 131. https://doi.org/10.3390/bs14020131  

   - Validates robotic storytelling for ASD engagement.  
   - Suggests CoRAG enhances structured interaction.  
   - Notes ethical concerns like dependency.

#### Supplemental Research

- **[Narrative Ability in Autism](https://doi.org/10.1016/j.rasd.2022.102092)** – Greco et al. (2022)  
- **[Can AI Tell Good Stories?](https://doi.org/10.1093/joc/jqae029)** – Chu & Liu (2024)  
- **[LLMs & NAO for Education](https://doi.org/10.20944/preprints202501.2278.v1)** – Fragakis et al. (2025)  
- **[AI in Creative Writing](https://doi.org/10.5772/intechopen.1008429)** – Suchy (2024)  
- **[A Story of Robots and Autism (YouTube)](https://www.youtube.com/watch?v=nwJsxLOilcc)** – 2024  
- **[Robots Teach Communication (YouTube)](https://www.youtube.com/watch?v=lm3vE7YFsGM)** – 2024  

---

## Other Resources

- **[gptars YouTube Channel](https://www.youtube.com/@gptars)**  
- **[Conversational Agents (Dialogflow CX) documentation](https://cloud.google.com/dialogflow/cx/docs)** – Google Cloud  

---

## How Our AI Storytelling Robot Works – ChatGPT Version (Explained for Everyone) :)

Imagine a robot storyteller that listens to you, understands what kind of story you want, and then tells you an engaging, AI-generated tale—all in real-time. Our project is about making that happen using a humanoid robot (NAO), AI storytelling technology (ChatGPT), and a system that connects them.

### 🔹 Step 1: The User Talks to the Robot
The interaction starts when a person speaks to the NAO robot—just like talking to a smart assistant (e.g., Siri, Alexa). They might say:

🗣️ *“Tell me a story about a brave astronaut!”*

#### 🔹 What Happens Next?
- The robot listens using its built-in microphone.  
- The speech is converted into text (so the AI can understand it).  
- The request is sent to our AI-powered storytelling system for processing.  

### 🔹 Step 2: Processing the Story Request
Once the user’s request is received, the system figures out what kind of story to generate.

#### 🔹 How It Works Behind the Scenes:
- The request is sent to ChatGPT, an advanced AI model that can generate human-like text.  
- ChatGPT creates a unique story based on the input.  
- The AI structures the story so it makes sense, ensuring it’s engaging and fun.  
- The finished story is sent back to the robot to be spoken aloud.  

#### 🔹 For Example:
If the user asked for a space adventure, ChatGPT might generate a story about: 🚀 *“Captain Luna, a brave astronaut, who embarks on a journey to find a lost alien civilization.”*

### 🔹 Step 3: The Robot Tells the Story
Now that the story has been created, the robot brings it to life!

#### 🔹 What Happens Now?
- The AI-generated story is converted back into speech using the robot’s built-in voice.  
- The robot reads the story aloud, just like a human storyteller would.  
- If time allows, we might also make the robot move its arms, nod, or react during the story.  

### 🔹 Step 4: User Interaction (Optional Future Feature)
Instead of just telling one long story, the system could allow for interactive choices, where the listener gets to decide what happens next.

#### 🔹 For Example:
🗣️ *"Should Captain Luna explore the dark cave or send a drone first?"* 🤖 The robot waits for an answer and then continues the story based on the choice.

*(This would take extra time to implement, so we may stick to straightforward storytelling for now!)*

### 🔹 What’s Needed to Make This Work?
Building this system requires connecting three main components:  
1️⃣ **The NAO Robot** – The physical device that listens, speaks, and interacts.  
2️⃣ **Conversational Agents (Dialogflow CX)** – A system that helps manage the conversation flow and decides what should happen next.  
3️⃣ **ChatGPT API** – The AI that generates the actual story.  

To make them work together, we need a **bridge**—a small program called a **webhook** that connects Conversational Agents (Dialogflow CX) to ChatGPT.

### 🔹 How Long Will This Take?
Since we’re working under a deadline, we’re focusing on the core goal: ✅ Make the robot listen, generate, and tell a story smoothly. 🚀 If time allows, we’ll explore adding extra features, like gestures or interactive choices.

### 🔹 Why This Matters
This AI-powered storytelling system could be useful for **educators, therapists, and caregivers**, helping them introduce engaging, AI-generated stories in an interactive way. It also provides a hands-free, voice-activated experience, making it easy to use.

While this is a technical research project, it’s also about **bringing storytelling to life** using AI and robotics!

### 🔹 Summary: The Big Picture
🔹 User speaks to the robot → 🗣️ NAO listens  
🔹 Request is sent to ChatGPT → 💡 AI generates a unique story  
🔹 Story is sent back to the robot → 🤖 NAO reads the story aloud  
🔹 Potential future expansion → 🔄 Interactive choices  

---

## How Our AI Storytelling System Works – ChatGPT Version (Explained for a CS Student)

This project is about integrating **robotics and AI** to create an interactive storytelling system where a humanoid robot (NAO) listens to user input, processes the request using AI (ChatGPT), and narrates a dynamically generated story.

### 🔹 Core Components:
- **NAO Robot** → Captures voice input and outputs speech.  
- **Conversational Agents (Dialogflow CX)** → Manages the conversation and processes user input.  
- **ChatGPT API** → Generates the story dynamically based on user preferences.  

A **webhook** is developed to **bridge** Conversational Agents (Dialogflow CX) and ChatGPT.

### 🔹 Step 1: User Input & Speech Processing
The interaction begins when the user talks to NAO:

🗣️ *Example: “Tell me a story about a brave astronaut.”*

#### 🔹 How This Works Technically:
1. NAO records the user’s voice and converts speech to text.  
2. The text is sent to Conversational Agents (Dialogflow CX), which classifies the intent (e.g., “Story Request”) and extracts parameters (e.g., “astronaut theme”).  
3. Conversational Agents (Dialogflow CX) forwards this request to our custom webhook, which will call ChatGPT.

### 🔹 Step 2: Webhook & AI Story Generation
The webhook is a simple backend service (**Python/Flask** or **Node.js**) that processes Conversational Agents' (Dialogflow CX) structured request and queries **ChatGPT’s API**.

#### 🔹 Technical Breakdown:
- Webhook receives a **JSON request** from Conversational Agents (Dialogflow CX).  
- Extracts the user’s theme preference (e.g., “astronaut adventure”).  
- Formats the request and sends it to **ChatGPT’s API**.  
- ChatGPT generates a structured response, returning a **short story**.  
- Webhook parses the response and sends it back to **Dialogflow CX**.

##### Example API Call to ChatGPT
```python
import openai

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "system", "content": "Tell a short astronaut adventure story."}]
)
print(response["choices"][0]["message"]["content"])
```

### 🔹 Step 3: NAO Reads the Story Aloud
Once the AI-generated story is returned, it’s sent back to **NAO for speech synthesis**.

#### 🔹 How This Works:
- The **formatted story text** is sent back to **Conversational Agents (Dialogflow CX)**.  
- Conversational Agents (Dialogflow CX) forwards the response to **NAO**.  
- NAO’s **Text-to-Speech (TTS)** engine converts the text to spoken words.

##### Example NAO TTS Code
```python
from naoqi import ALProxy

tts = ALProxy("ALTextToSpeech", "<NAO_IP>", 9559)
story_text = "Captain Luna soared through space on a mission to find the lost alien civilization."
tts.say(story_text)
```

### 🔹 Summary of the System Flow:
🔹 **User speaks to NAO** → Speech converted to text  
🔹 **Conversational Agents (Dialogflow CX) processes request** → Extracts story parameters  
🔹 **Webhook sends request to ChatGPT** → AI generates a custom story  
🔹 **Webhook returns the story to Conversational Agents (Dialogflow CX)**  
🔹 **NAO reads the story aloud** using TTS


# NAO Virtual Storyteller

## Project Objective

This project demonstrates a **proof of concept** where a **NAO robot** serves as the expressive medium for a **virtual storyteller** powered by **generative AI**. The robot listens for spoken keywords, sends them to an OpenAI-powered story generation service, and narrates the resulting story using its onboard Text-to-Speech (TTS) engine.

The system is designed to be easily extensible. While this version uses keyword recognition and a simple webhook, the architecture could integrate with more robust conversation engines such as **Google Conversational Agents (Dialogflow CX)** for richer, multi-turn dialogue.

---

## Documentation & Downloads

- **NAO Developer Documentation**  
  [http://doc.aldebaran.com/2-8/home_nao.html](http://doc.aldebaran.com/2-8/home_nao.html)

- **NAO Software Downloads**  
  [https://aldebaran.com/en/support/kb/nao6/downloads/nao6-software-downloads/](https://aldebaran.com/en/support/kb/nao6/downloads/nao6-software-downloads/)

---

## Directory Structure

```
naoqi_tests/
├── chatgpt_webhook.py     # Flask-based story generation API
├── test_naoqi.py          # Basic NAO connectivity test
├── test_tts.py            # Simple speech playback test
├── test_asr.py            # Full storyteller integration loop
├── venv/                  # Python 2.7 virtual environment
└── README.md              # (this file)
```

---

## Network Requirements

To communicate with the NAO robot:
- Ensure both your computer and the robot are on the **same local subnet** (e.g., `192.168.1.X`).
- Find the NAO robot’s IP via its touchscreen or audio prompt after boot.
- Update the `NAO_IP` variable in your scripts (e.g., `test_asr.py`) to match the robot's IP.

---

## ⚙️ Setup Instructions

### 1. Set Up a Python 2.7 Virtual Environment

```bash
sudo apt install python2.7 python2.7-venv
mkdir -p ~/naoqi_env
cd ~/naoqi_env
virtualenv -p python2.7 venv
source venv/bin/activate
```

---

### 2. Install Required Packages

```bash
pip install flask requests
```

---

### 3. Configure Your OpenAI API Key

Add the following to your `~/.bashrc`:
```bash
export AI_STORYTELLER_TEST_KEY_CV="sk-...your API key..."
```

Apply it in your current shell:
```bash
source ~/.bashrc
```

---

### 4. Run Tests

#### 🔸 Verify NAO Connectivity
```bash
python2 test_naoqi.py
```

#### 🔸 Confirm NAO Can Speak
```bash
python2 test_tts.py
```

#### 🔸 Start the Flask Story Generator Webhook
```bash
python2 chatgpt_webhook.py
```

Then, test it with:

```bash
curl -X POST http://localhost:5000/generate_story \
     -H "Content-Type: application/json" \
     -d '{"word": "robot"}'
```

---

### 5. Run the Virtual Storyteller

```bash
python2 test_asr.py
```

Then speak one of the following words near NAO:
- `hello`
- `story`
- `robot`

The system will:
1. Recognize your spoken keyword using NAO’s ASR.
2. Send it to the Flask server.
3. Generate a short story using the OpenAI API.
4. Speak the story aloud using NAO’s built-in speakers.

---

## Internals

This project uses:
- `ALSpeechRecognition` for listening
- `ALMemory` for retrieving recognized words
- `ALTextToSpeech` for playback
- Flask (`chatgpt_webhook.py`) to serve `/generate_story`
- OpenAI’s `chat/completions` API with the model `gpt-4o-mini`

For technical reference, all scripts have been refactored for [Doxygen](https://www.doxygen.nl/) compatibility with documented parameters, types, and call graphs.

---

## Scripts Overview

| File               | Purpose                                                  |
|--------------------|----------------------------------------------------------|
| `test_naoqi.py`    | Verifies connection to the NAO robot and TTS subsystem   |
| `test_tts.py`      | Sends a single test sentence to the NAO for speech       |
| `chatgpt_webhook.py` | Flask server that generates stories using OpenAI       |
| `test_asr.py`      | End-to-end: speech → story generation → TTS playback     |

---

## Future Possibilities

This setup validates the feasibility of **using NAO as a front-end for a generative AI-based virtual storyteller**. With this foundation, the following enhancements are possible:
- Integrating **Conversational Agents (Dialogflow CX)** to manage conversation logic.
- Adding **multi-turn story generation** with memory of previous interactions.
- Expanding vocabulary dynamically via the web interface.
- Hosting the webhook on a public domain via `ngrok` or GCP/AWS.

---

## License

MIT License — See source files for copyright.

---

## Questions or Contributions?

Feel free to fork this repo, submit pull requests, or open an issue with suggestions for enhancements!
```

