# NAO Virtual Storyteller — Research Project

## Abstract
This research project explores the feasibility of integrating generative AI with the NAO humanoid robot to create a virtual storyteller designed for caregivers, educators, and professionals in assistive and therapeutic fields. Studies indicate that individuals with Autism Spectrum Disorder (ASD) often find robots more approachable and predictable than human partners, making robotic interaction a valuable tool for fostering communication and social skills. By leveraging the NAO robot’s built-in audio functionality as the primary mode of interaction, this project examines how robotics and generative AI can enhance interactive storytelling.

The system implementation will utilize Google Dialogflow CX to manage conversational flow and process user input, working in conjunction with a Conversational Retrieval-Augmented Generation (CoRAG) model. CoRAG enhances storytelling continuity by adapting to user choices and thematic preferences over multiple interactions. Instead of generating isolated responses, CoRAG enables the storyteller to retain user preferences and past interactions, ensuring context-aware, progressively enriching narratives. The storyteller will process verbal input—such as user choices, questions, and themes—to generate personalized stories set in engaging fictional worlds, including space adventures and fantasy realms.

Caregivers, educators, and professionals working with ASD may benefit from NAO-integrated storytelling as a tool for engagement and guided learning. By leveraging CoRAG, we aim to develop an accessible and contextually adaptive storytelling platform that fosters meaningful interaction within caregiver-supported environments. Looking ahead, we envision a future where the NAO robot’s mechanical expressiveness further enhances the storytelling experience through emotionally expressive movements, deepening engagement and immersion.

---

## Research

### Core Research

1. **[A Systematic Review of Artificial Intelligence Technologies Used for Story Writing](https://www.researchgate.net/publication/369799144_A_systematic_review_of_artificial_intelligence_technologies_used_for_story_writing)** *Fang, Xiaoxuan; Ng, Davy Tsz Kit; Leung, Jac; Chu, Samuel. (2023).* *Education and Information Technologies*. https://doi.org/10.1007/s10639-023-11741-5  

   - Validates AI-driven storytelling for engagement and creativity.  
   - Supports the CoRAG (Conversational Retrieval-Augmented Generation) approach.  
   - Highlights challenges in coherence, emotion, and user engagement.  
   - Encourages human-AI collaboration — AI assists rather than replaces.

2. **[Integrating GPT-Based AI into Virtual Patients](https://pmc.ncbi.nlm.nih.gov/articles/PMC11669881/)** *Gutiérrez Maquilón R, Uhl J, Schrom-Feiertag H, Tscheligi M. (2024).* *JMIR Form Res.* https://doi.org/10.2196/58623  

   - Demonstrates GPT in real-time verbal interactions.  
   - Emphasizes reducing AI response latency for better usability.  
   - Aligns with CoRAG and prompt engineering techniques.  
   - Notes the role of expressive speech and gestures.

3. **[Designing AI-Enabled Games for Children with Autism](https://arxiv.org/abs/2404.15576)** *Lyu, Y.; An, P.; Zhang, H.; Katsuragawa, K.; Zhao, J. (2024).* *CHI 2024 Workshop*. arXiv:2404.15576  

   - Applies adaptive storytelling for emotional development.  
   - Suggests multimodal feedback via NAO’s movements.  
   - Highlights robotic integration potential.

4. **[Human-Mediated LLMs for Robotic Intervention](https://arxiv.org/abs/2402.00260)** *Mishra, R.; Welch, K. C.; Popa, D. O. (2024).* arXiv:2402.00260  

   - LLMs generate meaningful real-time dialogue.  
   - Human-mediated AI ensures appropriateness.  
   - Discusses NAO’s speech recognition limitations and therapy potential.

5. **[Robots vs Humans: Social Interaction with ASD](https://www.mdpi.com/2076-328X/14/2/131)** *Dubois-Sage, M.; Jacquet, B.; Jamet, F.; Baratgin, J. (2024).* *Behavioral Sciences*, 14(2), 131. https://doi.org/10.3390/bs14020131  

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

- **[gptars YouTube Channel](https://www.youtube.com/@gptars)** - **[Conversational Agents (Dialogflow CX) documentation](https://cloud.google.com/dialogflow/cx/docs)** – Google Cloud  

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
🔹 **Webhook returns the story to Conversational Agents (Dialogflow CX)** 🔹 **NAO reads the story aloud** using TTS

---

# NAO Virtual Storyteller

## Project Objective

This project demonstrates a **proof of concept** where a **NAO robot** serves as the expressive medium for a **virtual storyteller** powered by **generative AI**. The robot listens for spoken keywords, sends them to an OpenAI-powered story generation service, and narrates the resulting story using its onboard Text-to-Speech (TTS) engine.

The system is designed to be easily extensible. While this version uses keyword recognition and a simple webhook, the architecture could integrate with more robust conversation engines such as **Google Conversational Agents (Dialogflow CX)** for richer, multi-turn dialogue.

---

## Documentation & Downloads

- **NAO Developer Documentation** [http://doc.aldebaran.com/2-8/home_nao.html](http://doc.aldebaran.com/2-8/home_nao.html)

- **NAO Software Downloads** [https://aldebaran.com/en/support/kb/nao6/downloads/nao6-software-downloads/](https://aldebaran.com/en/support/kb/nao6/downloads/nao6-software-downloads/)

---

## Directory Structure

```
naoqi_tests/
├── chatgpt_webhook.py     # Flask-based story generation API
├── test_naoqi.py          # Basic NAO connectivity test
├── test_tts.py            # Simple speech playback test
├── test_asr.py            # Full storyteller integration loop
├── naoqi_env/             # Python 2.7 virtual environment (as per new guide)
└── README.md              # (this file)
```

*(Note: The Python 2.7 virtual environment directory is named `naoqi_env` as per the detailed setup guide below).*

---

## Network Setup for NAO Robot

For your computer to communicate with the NAO robot, both must be on the same network.

### 1.1. Connect NAO to the Network
* **Wi-Fi:** You can configure Wi-Fi on your NAO by connecting to its embedded web page. When NAO starts, it may announce its IP address or create its own Wi-Fi hotspot for initial configuration. Refer to your NAO's documentation for specific instructions.
* **Ethernet:** Connect an Ethernet cable from the NAO to your router or network switch.

### 1.2. Find NAO's IP Address
* **Chest Button:** Press NAO's chest button once. It should say its IP address.
* **Router's DHCP Client List:** Check your router's administration page for a list of connected devices and find the NAO's IP address.
* **Network Scanning Tools:** Tools like `nmap` (e.g., `nmap -sP YOUR_NETWORK_CIDR` like `192.168.1.0/24`) can help discover devices on your network.

### 1.3. Ensure Network Connectivity
* Once you have NAO's IP address (e.g., `192.168.1.120`), try to ping it from your Ubuntu machine:
    ```bash
    ping YOUR_NAO_IP_ADDRESS
    ```
* Ensure your PC and NAO are on the same subnet.

### 1.4. Firewall Considerations
* The NAOqi SDK typically communicates on port `9559`. Ensure that no firewall on your Ubuntu machine or network is blocking TCP traffic on this port to or from the NAO's IP address.
    * You can temporarily disable `ufw` (if active) for testing: `sudo ufw disable` (remember to re-enable it later with `sudo ufw enable` and configure rules if necessary).

---

## ⚙️ Setup Instructions

The following steps will guide you through setting up the Python 2 environment required for interacting with the NAO robot using the `naoqi` SDK on an **Ubuntu 22.04 system**. For other parts of this project that might use Python 3 (e.g., webhooks if they use modern libraries, advanced data processing), please manage a separate Python 3 environment.

**Important Note on Python Versions:** The NAOqi SDK historically relies on **Python 2.7**. Ubuntu 22.04 does not include Python 2 by default. The instructions below use `pyenv` for a clean installation of Python 2.7.

### 1. Install Python 2.7 on Ubuntu 22.04 (using `pyenv`)

Using `pyenv` is a clean way to install and manage different Python versions without interfering with the system's Python 3.

#### 1.1. Install `pyenv` Dependencies
These packages are needed to compile Python versions with `pyenv`:
```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev     libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm     libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

#### 1.2. Install `pyenv`
The recommended way to install `pyenv` is using the `pyenv-installer`:
```bash
curl https://pyenv.run | bash
```
This script will also show you how to set up your shell environment for `pyenv`.

#### 1.3. Configure Shell for `pyenv`
After installation, add the following lines to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`):
```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init --path)"
  eval "$(pyenv init -)"
fi
```
Then, apply the changes by sourcing the file (e.g., `source ~/.bashrc`) or opening a new terminal session.

#### 1.4. Install Python 2.7.18 with `pyenv`
Python 2.7.18 was the final release of Python 2.
```bash
pyenv install 2.7.18
```
This might take some time as it compiles Python from source.

#### 1.5. (Optional) Set Python 2.7.18 as Local Default for Your Project
Navigate to your project directory where you'll keep the NAO scripts:
```bash
cd /path/to/your/nao_project # Adjust to your project path
pyenv local 2.7.18
```
This creates a `.python-version` file in your project directory, and `pyenv` will automatically use Python 2.7.18 when you are in this directory. Now, running `python --version` in this directory should show Python 2.7.18.

---

### 2. Create a Python 2 Virtual Environment

It's highly recommended to use a virtual environment for your project to manage dependencies cleanly. Let's name it `naoqi_env`.

#### 2.1. Ensure `pip` for Python 2.7 is Available
If you used `pyenv local 2.7.18`, the `python` command in your project directory should point to Python 2.7.
Ensure `pip` is installed and up-to-date for this Python 2.7 version:
```bash
# (Ensure you are in your project directory where pyenv local 2.7.18 is set)
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel
```

#### 2.2. Install `virtualenv`
```bash
python -m pip install virtualenv
```

#### 2.3. Create and Activate the Virtual Environment
In your project directory:
```bash
python -m virtualenv naoqi_env # Creates a folder named 'naoqi_env'
source naoqi_env/bin/activate   # Activates the environment
```
Your command prompt should now be prefixed with `(naoqi_env)`. Running `python --version` inside this activated environment should show Python 2.7.18.

---

### 3. Install the NAOqi Python 2 SDK

This guide assumes you have downloaded the NAOqi Python 2 SDK for Linux (e.g., `pynaoqi-python2.7-X.X.X.X-linux64.tar.gz`).

#### 3.1. Extract the SDK
Extract the SDK archive to a known location. For example:
```bash
mkdir -p ~/naoqi_sdks # Or any other location you prefer
tar -xzf /path/to/your/pynaoqi-python2.7-sdk.tar.gz -C ~/naoqi_sdks/
```
This will create a directory structure, often containing a `pynaoqi` folder or similar. The key library files (`naoqi.py`, `_naoqi.so`, etc.) are usually found within a path like `pynaoqi-python2.7-X.X.X.X-linux64/lib/python2.7/site-packages/`.

#### 3.2. Make NAOqi SDK available to your Python 2 Environment
You have two main options:

**Option A: Setting `PYTHONPATH` (Recommended for flexibility)**
1.  Identify the full path to the directory *inside* your extracted SDK that contains `naoqi.py` and `_naoqi.so`. (e.g., `~/naoqi_sdks/pynaoqi-python2.7-X.X.X.X-linux64/lib/python2.7/site-packages`). Let's call this `NAOQI_PYTHON_LIB_DIR`.
2.  For a more permanent solution *within your virtual environment*, add this `export` line to your virtual environment's activation script:
    ```bash
    # (Make sure your naoqi_env is activated: source naoqi_env/bin/activate)
    # (Replace /path/to/your/NAOQI_PYTHON_LIB_DIR with the actual, absolute path)
    echo 'export PYTHONPATH="${PYTHONPATH}:/path/to/your/NAOQI_PYTHON_LIB_DIR"' >> naoqi_env/bin/activate
    ```
    You'll need to deactivate and reactivate your environment (`deactivate`, then `source naoqi_env/bin/activate`) for this change to take effect.

**Option B: Copying SDK files into Virtual Environment (Simpler for self-contained venvs)**
1.  Activate your virtual environment: `source naoqi_env/bin/activate`
2.  Identify your virtual environment's `site-packages` directory (usually `naoqi_env/lib/python2.7/site-packages/`).
3.  Copy `naoqi.py`, `_naoqi.so`, and any other relevant `.py` or `.so` files (like `vision_definitions.py`, `motion_definitions.py`) from the SDK's Python library directory directly into your virtual environment's `site-packages` directory.
    ```bash
    # Example (replace with your actual SDK path and ensure paths are correct):
    # SDK_LIB_PATH="~/naoqi_sdks/pynaoqi-python2.7-X.X.X.X-linux64/lib/python2.7/site-packages"
    # VENV_LIB_PATH="naoqi_env/lib/python2.7/site-packages"
    # cp "${SDK_LIB_PATH}/naoqi.py" "${VENV_LIB_PATH}/"
    # cp "${SDK_LIB_PATH}/_naoqi.so" "${VENV_LIB_PATH}/"
    # cp "${SDK_LIB_PATH}/motion_definitions.py" "${VENV_LIB_PATH}/" # If it exists and is needed
    # cp "${SDK_LIB_PATH}/vision_definitions.py" "${VENV_LIB_PATH}/" # If it exists and is needed
    ```
    Please ensure the source path (`SDK_LIB_PATH`) is correct and exists before running copy commands.

#### 3.3. Test NAOqi Import
With your `naoqi_env` virtual environment activated:
```bash
python -c "import naoqi; print 'NAOqi SDK imported successfully!'"
```
If this runs without errors, your SDK is likely set up correctly.

---

### 4. Install Python 2 Dependencies for NAO Scripts

The NAO interaction scripts might require a few external Python 2 compatible libraries. Install them into your **activated `naoqi_env` virtual environment**.

The `test_asr.py` script, for example, calls a webhook and needs the `requests` library:
```bash
# (Ensure 'naoqi_env' is activated: source naoqi_env/bin/activate)
pip install requests
```
If your `chatgpt_webhook.py` is intended to run under Python 2 (which is less common for modern Flask/OpenAI usage but possible for simpler versions), you would also install Flask here:
```bash
# pip install Flask  # Uncomment if running chatgpt_webhook.py in this Python 2 env
```

---

### 5. Configure Your OpenAI API Key

(This step is relevant for the `chatgpt_webhook.py` script, which `test_asr.py` interacts with.)

Add the following to your `~/.bashrc` (or `~/.zshrc`):
```bash
export AI_STORYTELLER_TEST_KEY_CV="sk-...your API key..."
```

Apply it in your current shell:
```bash
source ~/.bashrc
```
Ensure the `chatgpt_webhook.py` script (or whichever environment it runs in) can access this environment variable.

---

### 6. Running Tests and the Virtual Storyteller

Ensure your NAO robot is on, connected to the network, and you have updated the `NAO_IP` variable in scripts like `test_naoqi.py`, `test_tts.py`, and `test_asr.py` to match your robot's actual IP address.

**Activate your Python 2 virtual environment in each new terminal session:**
```bash
cd /path/to/your/nao_project # Adjust to your project path
source naoqi_env/bin/activate
```

#### 6.1. Verify NAO Connectivity
```bash
python test_naoqi.py
```

#### 6.2. Confirm NAO Can Speak
```bash
python test_tts.py
```

#### 6.3. Start the Flask Story Generator Webhook
This webhook (`chatgpt_webhook.py`) generates stories using OpenAI.
**Recommendation:** Run modern web services and AI library interactions (like OpenAI API calls) in a **Python 3 environment**.
If you have `chatgpt_webhook.py` configured for Python 3:
1. Open a *new terminal*.
2. Activate your Python 3 virtual environment for that script.
3. Run `python /path/to/chatgpt_webhook.py`.

If you have adapted `chatgpt_webhook.py` to run under Python 2 (and installed Flask in `naoqi_env`):
```bash
# In a separate terminal, ensure naoqi_env is activated if running webhook under Python 2
# source naoqi_env/bin/activate 
python chatgpt_webhook.py
```
Keep this webhook server running.

Then, test the webhook from another terminal:
```bash
curl -X POST http://localhost:5000/generate_story          -H "Content-Type: application/json"          -d '{"word": "robot"}'
```

#### 6.4. Run the Virtual Storyteller
Ensure the `chatgpt_webhook.py` server is running. In your terminal with the `naoqi_env` (Python 2) activated:
```bash
python test_asr.py
```

Then speak one of the following words near NAO:
- `hello`
- `story`
- `robot`

---

## 7. Troubleshooting Tips

* **"ImportError: No module named naoqi"**:
    * Ensure your Python 2 virtual environment (`naoqi_env`) is activated.
    * Verify `PYTHONPATH` is correct (Option 4.2.A) OR SDK files are in venv's `site-packages` (Option 4.2.B).
    * Confirm you're using the Python interpreter from `naoqi_env`.
* **Connection Errors ("Connection refused", "Host not found", Timeout to NAO):**
    * Double-check NAO's IP in the scripts.
    * Ensure NAO is on and on the same network.
    * Ping NAO's IP.
    * Check firewalls (port 9559 TCP).
* **SDK Version Compatibility:** Match NAOqi Python SDK version with NAO's OS version.
* **Python 2 Quirks:** Remember `print` syntax (unless `from __future__ import print_function` is used), string/unicode differences from Python 3.
* **Webhook Issues:**
    * Ensure `chatgpt_webhook.py` is running and accessible (check its console output for errors).
    * Verify `AI_STORYTELLER_TEST_KEY_CV` is set correctly and accessible by the webhook script.
    * Test the webhook with `curl` first to isolate issues.

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

| File               | Purpose                                                  | Python Version Recommendation |
|--------------------|----------------------------------------------------------|-------------------------------|
| `test_naoqi.py`    | Verifies connection to the NAO robot and TTS subsystem   | Python 2.7 (via `naoqi_env`)  |
| `test_tts.py`      | Sends a single test sentence to the NAO for speech       | Python 2.7 (via `naoqi_env`)  |
| `chatgpt_webhook.py` | Flask server that generates stories using OpenAI       | Python 3 (in a separate venv) |
| `test_asr.py`      | End-to-end: speech → story generation → TTS playback     | Python 2.7 (via `naoqi_env`)  |

*(Other scripts like `upload_stories.py` or FastAPI webhooks for ChromaDB would typically require Python 3 and their own setup.)*

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


---

## 🧾 Developer Reference (Doxygen)

This repository includes full developer-level documentation using [Doxygen](https://www.doxygen.nl/). All Python source files are annotated with:

- `@file`, `@brief`, `@param`, `@return`, `@author`
- Function-level docstrings structured for auto-generation
- Mermaid diagrams (e.g., ASR → Webhook → TTS flowchart in `test_asr.py`)
- Module constants and environmental variable documentation

### Entry Points

| Script               | Purpose                                                |
|----------------------|--------------------------------------------------------|
| `test_asr.py`        | Speech input → OpenAI webhook → TTS output            |
| `chatgpt_webhook.py` | Flask server to generate stories via OpenAI API       |
| `test_naoqi.py`      | Connectivity check to NAO’s `ALTextToSpeech` proxy    |
| `test_tts.py`        | Basic smoke test of NAO’s speech output               |

### To Generate Documentation

To build the Doxygen HTML output:

```bash
doxygen Doxyfile
```

Then open the generated file:

```bash
xdg-open docs/html/index.html
```

This will give you a full class/function reference, parameter table, call graphs, and links between modules.

> **Note**: Ensure your `Doxyfile` is configured for Python with `OPTIMIZE_OUTPUT_FOR_C = NO` and `EXTENSION_MAPPING = py=Python`.

ℹ️ **Browse the full documentation here →** [github.io/CSC212-Virtual-Storyteller](https://darthvandor13.github.io/CSC212-Virtual-Storyteller/)
