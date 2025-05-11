# AI VIRTUAL Storyteller — Research Project

## Abstract
This research project explores the feasibility of integrating generative AI with the NAO humanoid robot to create a virtual storyteller designed for caregivers, educators, and professionals in assistive and therapeutic fields. Studies indicate that individuals with Autism Spectrum Disorder (ASD) often find robots more approachable and predictable than human partners, making robotic interaction a valuable tool for fostering communication and social skills. By leveraging the NAO robot’s built-in audio functionality as the primary mode of interaction, this project examines how robotics and generative AI can enhance interactive storytelling.

The project involves two main components: a sophisticated backend storyteller built with **Google Dialogflow CX** (utilizing Retrieval-Augmented Generation with a GCS Data Store) and **proof-of-concept scripts demonstrating NAO robot interaction** (listening via ASR, speaking via TTS, and calling a simpler webhook for story generation). While the Dialogflow CX system represents the advanced conversational and story generation logic, the direct integration of NAO with this specific Dialogflow CX agent is a key area for **future development** and is **not yet implemented**. Current NAO scripts showcase foundational capabilities with a more direct, simpler webhook.

Caregivers, educators, and professionals working with ASD may benefit from NAO-integrated storytelling as a tool for engagement and guided learning. By leveraging CoRAG (within the Dialogflow CX component), we aim to develop an accessible and contextually adaptive storytelling platform that fosters meaningful interaction within caregiver-supported environments. Looking ahead, we envision a future where the NAO robot’s mechanical expressiveness further enhances the storytelling experience through emotionally expressive movements, deepening engagement and immersion, potentially by connecting it to the full capabilities of the Dialogflow CX agent.

---

## Table of Contents

- [Abstract](#abstract)
- [Research](#research)
  - [Core Research](#core-research)
  - [Supplemental Research](#supplemental-research)
- [Other Resources](#other-resources)
- [How Our AI Storytelling System Works – Conceptual Overview](#how-our-ai-storytelling-system-works--conceptual-overview)
  - [How the Dialogflow CX Storytelling Backend Works (Explained for Everyone) :)](#how-the-dialogflow-cx-storytelling-backend-works-explained-for-everyone-)
  - [How the Current NAO Proof-of-Concept Works (Simplified Loop)](#how-the-current-nao-proof-of-concept-works-simplified-loop)
- [How Our AI Storytelling System Works – Technical Breakdown (CS Student)](#how-our-ai-storytelling-system-works--technical-breakdown-cs-student)
  - [🔹 Core Components:](#-core-components)
  - [🔹 System Flow A: Advanced Storytelling with Dialogflow CX (Conceptual)](#-system-flow-a-advanced-storytelling-with-dialogflow-cx-conceptual)
  - [🔹 System Flow B: NAO Proof-of-Concept (Current `test_asr.py` Implementation)](#-system-flow-b-nao-proof-of-concept-current-test_asrpy-implementation)
- [NAO Virtual Storyteller: Project Setup & Guide](#nao-virtual-storyteller-project-setup--guide)
  - [Project Objective (Clarified)](#project-objective-clarified)
- [Documentation & Downloads (NAO Specific)](#documentation--downloads-nao-specific)
- [Repository Structure Overview](#repository-structure-overview)
- [Section 1: NAO Robot Interaction Setup (Python 2 & NAOqi SDK)](#section-1-nao-robot-interaction-setup-python-2--naoqi-sdk)
  - [1.1. Network Setup for NAO Robot](#11-network-setup-for-nao-robot)
  - [1.2. Install Python 2.7 on Ubuntu 22.04 (using `pyenv`)](#12-install-python-27-on-ubuntu-2204-using-pyenv)
  - [1.3. Create a Python 2 Virtual Environment](#13-create-a-python-2-virtual-environment)
  - [1.4. Install the NAOqi Python 2 SDK](#14-install-the-naoqi-python-2-sdk)
  - [1.5. Install Python 2 Dependencies for NAO Scripts](#15-install-python-2-dependencies-for-nao-scripts)
  - [1.6. Troubleshooting NAO Setup](#16-troubleshooting-nao-setup)
- [Section 2: Dialogflow CX AI Storyteller Agent Setup](#section-2-dialogflow-cx-ai-storyteller-agent-setup)
  - [2.1. Project Overview (Dialogflow CX Agent)](#21-project-overview-dialogflow-cx-agent)
  - [2.2. Technology Stack (Dialogflow CX Agent)](#22-technology-stack-dialogflow-cx-agent)
  - [2.3. Core Concepts: RAG via GCS Data Store](#23-core-concepts-rag-via-gcs-data-store)
  - [2.4. Setup & Prerequisites (Dialogflow CX Start-to-Finish)](#24-setup--prerequisites-dialogflow-cx-start-to-finish)
  - [2.5. Agent Configuration Steps (Dialogflow CX Console)](#25-agent-configuration-steps-dialogflow-cx-console)
  - [2.6. How to Use/Test Dialogflow CX Agent](#26-how-to-usetest-dialogflow-cx-agent)
  - [2.7. Known Issues / Troubleshooting Context (Dialogflow CX)](#27-known-issues--troubleshooting-context-dialogflow-cx)
- [Section 3: Running Project Components & Demonstrations](#section-3-running-project-components--demonstrations)
  - [3.1. Configure OpenAI API Key (for `chatgpt_webhook.py`)](#31-configure-openai-api-key-for-chatgpt_webhookpy)
  - [3.2. Running the NAO Direct Interaction Scripts & PoC Loop (Python 2)](#32-running-the-nao-direct-interaction-scripts--poc-loop-python-2)
  - [3.3. Interacting with the Dialogflow CX AI Storyteller Agent (via Simulator)](#33-interacting-with-the-dialogflow-cx-ai-storyteller-agent-via-simulator)
- [Internals (NAO Interaction Scripts)](#internals-nao-interaction-scripts)
- [Scripts Overview Table](#scripts-overview-table)
- [Future Possibilities](#future-possibilities)
- [License](#license)
- [Questions or Contributions?](#questions-or-contributions)
- [🧾 Developer Reference (Doxygen)](#-developer-reference-doxygen)
  - [Entry Points (Python Scripts)](#entry-points-python-scripts)
  - [To Generate Doxygen Documentation](#to-generate-doxygen-documentation)

---

## Research

### Core Research

1. **[A Systematic Review of Artificial Intelligence Technologies Used for Story Writing](https://www.researchgate.net/publication/369799144_A_systematic_review_of_artificial_intelligence_technologies_used_for_story_writing)** *Fang, Xiaoxuan; Ng, Davy Tsz Kit; Leung, Jac; Chu, Samuel. (2023).* *Education and Information Technologies*. https://doi.org/10.1007/s10639-023-11741-5  

   - Validates AI-driven storytelling for engagement and creativity.  
   - Supports the CoRAG (Conversational Retrieval-Augmented Generation) approach.  
   - Highlights challenges in coherence, emotion, and user engagement.  
   - Encourages human-AI collaboration — AI assists rather than replaces.

2. **[Integrating GPT-Based AI into Virtual Patients](https://pmc.ncbi.nlm.nih.gov/articles/PMC11669881/)** *Gutiérrez Maquilón R, Uhl J, Schrom-Feiertag H, Tscheligi M. (2024).* *JMIR Form Res.* [https://doi.org/10.2196/58623](https://doi.org/10.2196/58623)  

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

5. **[Robots vs Humans: Social Interaction with ASD](https://www.mdpi.com/2076-328X/14/2/131)** *Dubois-Sage, M.; Jacquet, B.; Jamet, F.; Baratgin, J. (2024).* *Behavioral Sciences*, 14(2), 131. [https://doi.org/10.3390/bs14020131](https://doi.org/10.3390/bs14020131)  

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

## How Our AI Storytelling System Works – Conceptual Overview

This project explores creating an interactive storytelling experience. We have two main parts:
1.  **An Advanced Storytelling Backend:** Built using Google Dialogflow CX, this system can understand user preferences (like themes or characters) and use a knowledge base of stories (Retrieval-Augmented Generation - RAG) to craft new, unique tales. This is the sophisticated "brain" for story creation.
2.  **NAO Robot as an Interface (Proof of Concept):** We have scripts that allow the NAO robot to listen to simple keywords, send them to a basic story-generating service (a simpler OpenAI webhook detailed in `chatgpt_webhook.py`), and then speak the resulting story. This demonstrates NAO's potential as an engaging front-end.

**The Vision (Future Integration):** The ultimate goal is to connect the NAO robot to the advanced Dialogflow CX storytelling backend. This would allow users to have rich, interactive conversations with NAO, guiding the creation of complex, context-aware stories. The sections below describe how these components work individually and how they *could* work together.

### How the Dialogflow CX Storytelling Backend Works (Explained for Everyone) :)

Imagine an AI that's a master storyteller and also a great listener. This is what our Dialogflow CX system does:

#### 🔹 Step 1: Understanding Your Story Idea
You tell the system (through a chat interface or, hypothetically, through NAO) what kind of story you want:
🗣️ *“I’d like a fantasy story about a brave knight named Arthur who learns about courage.”*

#### 🔹 Step 2: Consulting the Archives & Crafting a New Tale
- The system looks up related ideas and story snippets from its knowledge base (like a library of story elements).
- Using these snippets for inspiration, and your specific requests (knight, Arthur, fantasy, courage), an AI (like Google's Gemini models) writes a *brand new* short story. It doesn't just copy; it creates something unique.

#### 🔹 Step 3: Presenting the Story
The newly crafted story is then presented to you. If NAO were connected to this system, it would be the one speaking the story.

### How the Current NAO Proof-of-Concept Works (Simplified Loop)

Our current NAO scripts (`test_asr.py`) demonstrate a simpler interaction:
1.  🗣️ **User speaks a keyword** (e.g., "dragon") to NAO.
2.  🤖 NAO recognizes the keyword.
3.  ➡️ NAO sends this single keyword to a basic local webhook (`chatgpt_webhook.py`).
4.  💡 This webhook uses OpenAI (e.g., GPT-4o-mini) to generate a very short story based *only* on that keyword.
5.  📢 NAO speaks the story.

This shows NAO can listen, trigger an AI, and tell a story. The next step would be to connect NAO to the more powerful Dialogflow CX backend described above for richer interactions.

---

## How Our AI Storytelling System Works – Technical Breakdown (CS Student)

This project integrates robotics (NAO) with two tiers of AI for storytelling: a sophisticated Dialogflow CX agent for advanced RAG-based narrative generation, and a simpler direct OpenAI webhook for NAO proof-of-concept interactions.

### 🔹 Core Components:
- **NAO Robot:** Captures voice input (ASR) and outputs speech (TTS) using the NAOqi SDK. (Proof-of-Concept Stage)
- **Dialogflow CX Agent:** The primary storytelling engine. Manages multi-turn conversations, extracts complex user preferences, and uses RAG with a GCS Data Store to generate context-aware stories. (Advanced Backend)
- **OpenAI API (via `chatgpt_webhook.py`):** Used by the current NAO ASR scripts for direct, keyword-based story generation as a proof-of-concept. (Simple Webhook for NAO PoC)

### 🔹 System Flow A: Advanced Storytelling with Dialogflow CX (Conceptual)
1.  **User Input:** User interacts with the Dialogflow CX agent (e.g., via text chat simulator or a future integrated interface).
2.  **Parameter Extraction:** Dialogflow CX extracts intents and parameters (protagonist, theme, moral).
3.  **RAG Process:**
    * The Dialogflow CX playbook queries a **GCS Data Store** (containing source stories) using the extracted parameters.
    * Relevant text snippets are retrieved.
4.  **Story Generation:** A generative model within Dialogflow CX (e.g., Gemini) uses the retrieved snippets and user parameters to craft a new story, adhering to instructions (e.g., "do not copy verbatim," "story length").
5.  **Response Delivery:** The story is presented to the user. *(Hypothetically, this could be sent to NAO for TTS output if fully integrated).*

### 🔹 System Flow B: NAO Proof-of-Concept (Current `test_asr.py` Implementation)
1.  **User Speaks Keyword to NAO:** e.g., "robot".
2.  **NAO ASR:** `ALSpeechRecognition` detects the keyword. `ALMemory` stores it.
3.  **Webhook Call:** `test_asr.py` sends the recognized keyword via an HTTP POST request to `chatgpt_webhook.py`.
4.  **Simple Story Generation:** `chatgpt_webhook.py` directly calls the OpenAI API (e.g., `gpt-4o-mini`) with a prompt based on the single keyword.
5.  **Webhook Response:** Returns the generated story snippet as JSON.
6.  **NAO TTS:** `test_asr.py` receives the story, and `ALTextToSpeech` makes NAO speak it.

The vision is to evolve System Flow B to integrate with a system like Flow A, where NAO becomes the voice/ears for the Dialogflow CX agent.

---

# NAO Virtual Storyteller: Project Setup & Guide

## Project Objective (Clarified)

This project demonstrates a **proof of concept** where a **NAO robot** serves as the expressive medium for a **virtual storyteller**. The current advanced core of the storytelling logic resides within a **Google Cloud Dialogflow CX agent**, which uses Retrieval-Augmented Generation (RAG) with a GCS Data Store.

The Python scripts included in this repository, primarily for Python 2 and NAOqi interaction, represent **foundational work and proof-of-concept implementations** (like direct NAO ASR to a simple OpenAI webhook and TTS output). While the Dialogflow CX system is functional as a standalone conversational agent, the direct, real-time integration of the **NAO robot with this specific Dialogflow CX agent is a key area for future development and is not yet implemented.**

This README provides setup instructions for both:
1.  The **NAO robot interaction components** (requiring Python 2.7 and the NAOqi SDK for proof-of-concept tests).
2.  The **Dialogflow CX AI Storyteller Agent** (requiring Google Cloud Platform setup, which functions independently).

---

## Documentation & Downloads (NAO Specific)

- **NAO Developer Documentation** [http://doc.aldebaran.com/2-8/home_nao.html](http://doc.aldebaran.com/2-8/home_nao.html)
- **NAO Software Downloads** [https://aldebaran.com/en/support/kb/nao6/downloads/nao6-software-downloads/](https://aldebaran.com/en/support/kb/nao6/downloads/nao6-software-downloads/)

---

## Repository Structure Overview

```
.
├── naoqi_tests/               # Scripts for NAO interaction (Python 2)
│   ├── chatgpt_webhook.py     # Flask webhook (can be run with Py2 for test_asr.py PoC)
│   ├── test_naoqi.py          # Basic NAO connectivity test
│   ├── test_tts.py            # Simple speech playback test
│   └── test_asr.py            # Full NAO ASR -> Webhook -> TTS loop (PoC)
├── docs/                      # Doxygen generated documentation (if built)
├── (other_python3_scripts/)   # Placeholder for Python 3 components (e.g., upload_stories.py for GCS)
├── naoqi_env/                 # Recommended name for Python 2.7 virtual environment
├── .env_example               # Example for environment variables
├── Doxyfile                   # Doxygen configuration file
└── README.md                  # This file
```
*(Note: Python 3 scripts like `upload_stories.py` or more complex webhooks for Dialogflow CX fulfillment should ideally be in their own Python 3 virtual environment, separate from `naoqi_env`.)*

---

## Section 1: NAO Robot Interaction Setup (Python 2 & NAOqi SDK)

This section details setting up your Ubuntu 22.04 system to run the Python 2 scripts that interact directly with the NAO robot. These scripts are primarily for testing NAO's capabilities and running the proof-of-concept ASR-Webhook-TTS loop.

### 1.1. Network Setup for NAO Robot

For your computer to communicate with the NAO robot, both must be on the same network.

#### 1.1.1. Connect NAO to the Network
* **Wi-Fi:** You can configure Wi-Fi on your NAO by connecting to its embedded web page. When NAO starts, it may announce its IP address or create its own Wi-Fi hotspot for initial configuration. Refer to your NAO's documentation for specific instructions.
* **Ethernet:** Connect an Ethernet cable from the NAO to your router or network switch.

#### 1.1.2. Find NAO's IP Address
* **Chest Button:** Press NAO's chest button once. It should say its IP address.
* **Router's DHCP Client List:** Check your router's administration page for a list of connected devices and find the NAO's IP address.
* **Network Scanning Tools:** Tools like `nmap` (e.g., `nmap -sP YOUR_NETWORK_CIDR` like `192.168.1.0/24`) can help discover devices on your network.

#### 1.1.3. Ensure Network Connectivity
* Once you have NAO's IP address (e.g., `192.168.1.120`), try to ping it from your Ubuntu machine:
    ```bash
    ping YOUR_NAO_IP_ADDRESS
    ```
* Ensure your PC and NAO are on the same subnet.

#### 1.1.4. Firewall Considerations
* The NAOqi SDK typically communicates on port `9559`. Ensure that no firewall on your Ubuntu machine or network is blocking TCP traffic on this port to or from the NAO's IP address.
    * You can temporarily disable `ufw` (if active) for testing: `sudo ufw disable` (remember to re-enable it later with `sudo ufw enable` and configure rules if necessary).

### 1.2. Install Python 2.7 on Ubuntu 22.04 (using `pyenv`)

Ubuntu 22.04 does not include Python 2 by default. Using `pyenv` is a clean way to install and manage Python 2.7 without interfering with the system's Python 3.

#### 1.2.1. Install `pyenv` Dependencies
These packages are needed to compile Python versions with `pyenv`:
```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev     libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm     libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

#### 1.2.2. Install `pyenv`
The recommended way to install `pyenv` is using the `pyenv-installer`:
```bash
curl https://pyenv.run | bash
```
This script will also show you how to set up your shell environment for `pyenv`.

#### 1.2.3. Configure Shell for `pyenv`
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

#### 1.2.4. Install Python 2.7.18 with `pyenv`
Python 2.7.18 was the final release of Python 2.
```bash
pyenv install 2.7.18
```
This might take some time as it compiles Python from source.

#### 1.2.5. (Optional) Set Python 2.7.18 as Local Default for Your Project
Navigate to your project directory (or the `naoqi_tests` subdirectory):
```bash
cd /path/to/your/nao_project # Or ./naoqi_tests
pyenv local 2.7.18
```
This creates a `.python-version` file, and `pyenv` will automatically use Python 2.7.18 here.

### 1.3. Create a Python 2 Virtual Environment

It's highly recommended to use a virtual environment. Let's name it `naoqi_env`.

#### 1.3.1. Ensure `pip` for Python 2.7 is Available
If `pyenv local 2.7.18` is active, `python` should point to Python 2.7.
Ensure `pip` is installed and up-to-date for this Python 2.7 version:
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel
```

#### 1.3.2. Install `virtualenv`
```bash
python -m pip install virtualenv
```

#### 1.3.3. Create and Activate the Virtual Environment
In your project directory (e.g., where `naoqi_tests` is located):
```bash
python -m virtualenv naoqi_env # Creates 'naoqi_env' folder
source naoqi_env/bin/activate   # Activates the environment
```
Your command prompt should now be prefixed with `(naoqi_env)`.

### 1.4. Install the NAOqi Python 2 SDK

This guide assumes you have downloaded the NAOqi Python 2 SDK for Linux (e.g., `pynaoqi-python2.7-X.X.X.X-linux64.tar.gz`).

#### 1.4.1. Extract the SDK
Extract the SDK archive to a known location, e.g., `~/naoqi_sdks/`.
The key library files (`naoqi.py`, `_naoqi.so`) are usually within a path like `pynaoqi-python2.7-X.X.X.X-linux64/lib/python2.7/site-packages/`.

#### 1.4.2. Make NAOqi SDK available to your Python 2 Environment
**Option A: Setting `PYTHONPATH` (Recommended)**
1.  Identify the full path to the SDK's `site-packages` directory (e.g., `~/naoqi_sdks/pynaoqi-python2.7-X.X.X.X-linux64/lib/python2.7/site-packages`). Let this be `NAOQI_PYTHON_LIB_DIR`.
2.  Add to your virtual environment's activation script:
    ```bash
    # (Ensure naoqi_env is activated)
    # (Replace /path/to/your/NAOQI_PYTHON_LIB_DIR with the actual, absolute path)
    echo 'export PYTHONPATH="${PYTHONPATH}:/path/to/your/NAOQI_PYTHON_LIB_DIR"' >> naoqi_env/bin/activate
    ```
    Deactivate and reactivate (`deactivate`, then `source naoqi_env/bin/activate`).

**Option B: Copying SDK files into Virtual Environment**
1.  Activate `naoqi_env`.
2.  Copy `naoqi.py`, `_naoqi.so`, and other relevant files (e.g., `motion_definitions.py`) from the SDK's `site-packages` to `naoqi_env/lib/python2.7/site-packages/`.
    ```bash
    # Example (replace with your actual SDK path):
    # SDK_LIB_PATH="~/naoqi_sdks/pynaoqi-python2.7-X.X.X.X-linux64/lib/python2.7/site-packages"
    # VENV_LIB_PATH="naoqi_env/lib/python2.7/site-packages"
    # cp "${SDK_LIB_PATH}/naoqi.py" "${VENV_LIB_PATH}/"; cp "${SDK_LIB_PATH}/_naoqi.so" "${VENV_LIB_PATH}/"
    ```

#### 1.4.3. Test NAOqi Import
With `naoqi_env` activated:
```bash
python -c "import naoqi; print 'NAOqi SDK imported successfully!'"
```

### 1.5. Install Python 2 Dependencies for NAO Scripts
The `test_asr.py` script calls a webhook and needs `requests`:
```bash
# (Ensure 'naoqi_env' is activated)
pip install requests
```
If running `chatgpt_webhook.py` under Python 2 for the PoC (not generally recommended for modern Flask/OpenAI usage), install Flask:
```bash
# pip install Flask
```

### 1.6. Troubleshooting NAO Setup
* **"ImportError: No module named naoqi"**: Check venv activation, `PYTHONPATH` (Option A) or file copy (Option B).
* **Connection Errors to NAO**: Verify IP, network, ping, firewall (port 9559 TCP).
* **SDK/OS Version:** Ensure NAOqi Python SDK and NAO's OS are compatible.

---

## Section 2: Dialogflow CX AI Storyteller Agent Setup

This section details the setup for the current core of the virtual storyteller, which uses Google Cloud Dialogflow CX with a GCS Data Store for Retrieval-Augmented Generation (RAG). This agent functions independently and represents the advanced storytelling backend.
*(This content is adapted from the README of the [ai-storyteller-agent-config](https://github.com/darthvandor13/ai-storyteller-agent-config) repository).*

### 2.1. Project Overview (Dialogflow CX Agent)

This component implements a conversational AI agent using **Google Cloud Dialogflow CX** designed to act as a virtual storyteller. The agent engages users in a conversation to gather preferences (protagonist name, story theme, moral) and then generates a unique short story (300-350 words).

The core mechanism is **Retrieval-Augmented Generation (RAG)**. The agent retrieves relevant context snippets from a predefined knowledge base of stories (hosted in Google Cloud Storage) and uses these snippets, along with the user's parameters, as strict inspiration to generate a new, original story. It is explicitly instructed *not* to use external knowledge or copy directly from the source material.

*(**Note on Initial Approach:** An earlier iteration attempted using ChromaDB via a webhook and parameter presets. This approach was paused due to platform issues encountered with parameter preset handling – specifically, the UI automatically adding quotes to `$webhookResponse` paths.)*

### 2.2. Technology Stack (Dialogflow CX Agent)

* **Conversational Platform:** Google Cloud Dialogflow CX
* **Knowledge Base Backend:** Google Cloud Storage (GCS)
* **Secrets Management:** Google Cloud Secret Manager
* **Version Control (for Agent Config):** GitHub (via Dialogflow CX Git Integration)

### 2.3. Core Concepts: RAG via GCS Data Store

1.  **Data Storage:** Source story texts (PDF, TXT, HTML formats supported) are stored in a GCS bucket.
2.  **Data Store Resource:** A Dialogflow "Data Store" resource is created within the Agent Builder environment, configured to point to the GCS bucket and index the unstructured content.
3.  **Data Store Tool:** A "Data Store Tool" is created within the agent and linked to the specific Data Store resource.
4.  **Retrieval:** The agent's playbook logic calls this Data Store Tool, sending a query based on user input.
5.  **Generation:** The tool returns relevant text snippets. These snippets, along with user parameters, are used within a generative prompt executed by the agent's playbook to create the final story.

### 2.4. Setup & Prerequisites (Dialogflow CX Start-to-Finish)

This guide assumes you have a Google Cloud project with billing enabled.

1.  **Enable APIs:**
    * In the Google Cloud Console, ensure the following APIs are enabled for your project:
        * Dialogflow API
        * Secret Manager API
        * Cloud Storage API
        * Vertex AI Agent Builder API (or Vertex AI Search and Conversation API)

2.  **Create GCS Bucket:**
    * Navigate to Cloud Storage -> Buckets. Click "Create".
    * Choose a unique **Bucket name** (e.g., `[YOUR_PROJECT_ID]-story-data`).
    * Select **Location type: Region** and choose the **SAME REGION** as your Dialogflow agent (e.g., `us-central1`). This is critical.
    * Select **Storage class: Standard**. Configure access control. Click "Create".

3.  **Upload Story Files:**
    * Upload your source story files (e.g., `.pdf`, `.txt`) to the GCS bucket.

4.  **Create GitHub Repository (for Agent Config Sync):**
    * Create a new, **dedicated repository** on GitHub (e.g., `ai-storyteller-agent-config`).
    * Ensure the primary branch (e.g., `main`) exists.

5.  **Create GitHub Personal Access Token (PAT):**
    * In GitHub: Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens.
    * Click "Generate new token". Name it (e.g., `dialogflow-cx-sync`), set Expiration.
    * Under "Repository access", select **"Only select repositories"** and choose the repo from step 4.
    * Under "Permissions" -> "Repository permissions", find **"Contents"** and set access to **"Read and write"**.
    * Click "Generate token". **COPY THE TOKEN IMMEDIATELY.**

6.  **Store PAT in Secret Manager:**
    * In Google Cloud Console -> Security -> Secret Manager. Click "+ Create Secret".
    * Enter a **Name** (e.g., `github-dialogflow-pat`). Paste the PAT into **Secret value**. Click "Create Secret".

7.  **Grant Dialogflow Access to Secret:**
    * In Secret Manager, open the secret. Go to "Permissions" tab. Click "+ Grant Access".
    * **New principals:** `service-[YOUR_PROJECT_NUMBER]@gcp-sa-dialogflow.iam.gserviceaccount.com` (Replace `[YOUR_PROJECT_NUMBER]`).
    * **Assign roles:** `Secret Manager Secret Accessor`. Click "Save".

8.  **Grant Dialogflow Access to GCS Bucket:**
    * Navigate to your story data GCS Bucket -> "Permissions" tab. Click "+ Grant Access".
    * **New principals:** `service-[YOUR_PROJECT_NUMBER]@gcp-sa-dialogflow.iam.gserviceaccount.com`.
    * **Assign roles:** `Storage Object Viewer`. Click "Save".

### 2.5. Agent Configuration Steps (Dialogflow CX Console)

1.  **Create Agent (if needed):**
    * Create a new agent ("Build your own"). Specify Agent Name, **Location/Region** (must match GCS bucket), Time zone, Default language.

2.  **Create Data Store Resource:**
    * Go to "Data Stores". Click "Create new data store".
    * Source: **"Cloud Storage"**. Select your GCS bucket/folder.
    * Data type: **"Unstructured documents"**.
    * Sync frequency: **"One time"** (workaround for potential UI issues). Click "Continue".
    * **Configure data connector:** Location (e.g., `us (multi-region)` for agent in `us-central1`), unique Connector name. Click "Create".
    * Wait for indexing ("Data Ingestion Activity" should show "Succeeded").

3.  **Create Data Store Tool:**
    * Go to "Tools". Click "+ Create".
    * **Tool Name:** e.g., `WorkspaceStoryContextTool-OneTime`.
    * **Tool Type:** `Data store`.
    * **Data stores:** Add the data store created above.
    * Add a Description. Click "Save".

4.  **Configure GitHub Integration (in Agent Settings):**
    * Go to Agent Settings (⚙️ icon) -> "Git integration". Click "+ Add Git integration".
    * **Display name:** e.g., `GitHub Sync - Storyteller Agent`.
    * **Git repository:** HTTPS URL of your dedicated GitHub repo for agent config.
    * **Branch:** e.g., `main`.
    * **Access token secret:** Full resource name of the Secret Manager secret version (e.g., `projects/[PROJECT_ID]/secrets/[SECRET_NAME]/versions/latest`).
    * Click "Connect", then "Save" agent settings.

5.  **Import/Configure Playbook:**
    * Import the playbook from the `ai-storyteller-agent-config` repository if you have one, or configure a new one.
    * Ensure you are working with the correct playbook (e.g., `Storyteller Playbook - GCS Test`).

6.  **Configure Playbook Instructions:**
    * Paste the playbook instructions (which define how the agent uses parameters and tool outputs to generate the story) into the "Instructions" field.

7.  **Configure Playbook Example:**
    * Edit/create an example demonstrating the successful path.
    * Tool Use step should call your Data Store Tool. Example Input JSON for the tool:
        ```json
        {
          "query": "Story about $session.params.theme with a moral of $session.params.moral",
          "filter": "",
          "userMetadata": {}
        }
        ```
    * Agent response step should contain the generative prompt, referencing user parameters (`$session.params.*`) and the tool output (e.g., `$tool.WorkspaceStoryContextTool-OneTime.snippets`). Example Prompt Text:
        ```text
        Okay, traveler! Using the inspiration found in our archives ($tool.WorkspaceStoryContextTool-OneTime.snippets), here is a new short story (300-350 words) about $session.params.protagonist in a $session.params.theme setting. The story must teach the moral '$session.params.moral'. Remember to base the story ONLY on the retrieved context from the archives, adapting creatively but not adding external information or copying verbatim. Make sure it has a beginning, middle, and end.

        Would you like me to craft another tale, traveler?
        ```
    * Configure "End example with output information". Save.

8.  **Configure Agent Generative Settings:**
    * Agent Settings -> Generative AI -> Playbook.
    * Select **Model** (e.g., `gemini-1.5-flash-001`), **Temperature**, **Token Limit**. Save.

9.  **Initial Git Push (from Dialogflow CX Agent Settings):**
    * Go to Agent Settings -> Git integration. Find your connection. Click **"Push"**.

### 2.6. How to Use/Test Dialogflow CX Agent

1.  Open Dialogflow CX console, select your agent.
2.  Open the **Simulator**.
3.  Simulator settings: Environment (`Draft`), Start Resource (`Playbook`), select your specific playbook.
4.  Interact by providing protagonist, theme, and moral when prompted.

### 2.7. Known Issues / Troubleshooting Context (Dialogflow CX)

* **Webhook Parameter Preset Bug (Historical):** Initial ChromaDB/Webhook approach using parameter presets failed due to a UI bug. This led to the GCS Data Store method.
* **GCS Data Store Visibility:** "One time" sync for Data Stores was found more reliable for immediate tool linking than "Periodic" sync during development.
* **GCS Permissions:** Ensure Dialogflow Service Agent has `Storage Object Viewer` on the GCS bucket.
* **Data Store Indexing:** Can take time. Check "DATA INGESTION ACTIVITY".

---

## Section 3: Running Project Components & Demonstrations

This section explains how to run the NAO interaction scripts (Python 2 PoC) and how to test the Dialogflow CX agent.

### 3.1. Configure OpenAI API Key (for `chatgpt_webhook.py`)
The `test_asr.py` script for NAO calls the `chatgpt_webhook.py` for its story generation proof-of-concept. Ensure the `AI_STORYTELLER_TEST_KEY_CV` environment variable is set in the shell environment where `chatgpt_webhook.py` will run:
```bash
export AI_STORYTELLER_TEST_KEY_CV="sk-...your API key..."
# Add to ~/.bashrc or ~/.zshrc for persistence and source the file
```

### 3.2. Running the NAO Direct Interaction Scripts & PoC Loop (Python 2)

These scripts test direct NAO functionalities and the proof-of-concept ASR -> Webhook -> TTS loop.

**A. Start the Local Story Generation Webhook (`chatgpt_webhook.py`)**
This webhook is called by `test_asr.py`. It's recommended to run this in a Python 3 environment if it uses modern libraries, but it can be run in the Python 2 `naoqi_env` if Flask is installed there and the script is Python 2 compatible.
1.  Open a *new terminal*.
2.  Activate the appropriate Python environment (Python 3 venv recommended, or `naoqi_env` if adapted for Py2).
3.  Run: `python /path/to/naoqi_tests/chatgpt_webhook.py`
4.  Keep this server running.

**B. Run the NAO Interaction Scripts**
Ensure your NAO robot is on, networked, and its IP is correctly set in the Python 2 scripts.
1.  Open a *new terminal*.
2.  Navigate to your project directory: `cd /path/to/your/nao_project`
3.  Activate the Python 2 virtual environment: `source naoqi_env/bin/activate`

4.  **Verify NAO Connectivity:**
    ```bash
    python naoqi_tests/test_naoqi.py
    ```

5.  **Confirm NAO Can Speak:**
    ```bash
    python naoqi_tests/test_tts.py
    ```

6.  **Run the Full Virtual Storyteller PoC Loop:**
    (Ensure `chatgpt_webhook.py` is running)
    ```bash
    python naoqi_tests/test_asr.py
    ```
    Speak one of the keywords (`hello`, `story`, `robot`) near NAO.

### 3.3. Interacting with the Dialogflow CX AI Storyteller Agent (via Simulator)
Refer to **Section 2.6. How to Use/Test Dialogflow CX Agent** above for instructions on using the Dialogflow CX simulator. This tests the advanced backend independently of NAO.

---

## Internals (NAO Interaction Scripts)

The Python 2 scripts for NAO interaction use:
- `ALSpeechRecognition` for listening.
- `ALMemory` for retrieving recognized words.
- `ALTextToSpeech` for playback.
- The `chatgpt_webhook.py` (Flask) serves `/generate_story` using OpenAI’s `chat/completions` API (model `gpt-4o-mini`) for the NAO PoC.

For a deeper dive into the script APIs, consult the Doxygen-generated documentation.

---

## Scripts Overview Table

| File                 | Purpose                                                     | Python Version Recommendation | Environment    |
|----------------------|-------------------------------------------------------------|-------------------------------|----------------|
| `test_naoqi.py`      | Verifies NAO connectivity (TTS subsystem)                   | Python 2.7                    | `naoqi_env`    |
| `test_tts.py`        | Simple NAO speech test                                      | Python 2.7                    | `naoqi_env`    |
| `test_asr.py`        | NAO ASR → Webhook → NAO TTS loop (PoC)                      | Python 2.7                    | `naoqi_env`    |
| `chatgpt_webhook.py` | Flask server for OpenAI story generation (called by ASR PoC)| Python 3 (recommended)        | Separate Py3 venv |
| `upload_stories.py`  | Bulk story uploader (e.g., for GCS or historical ChromaDB)  | Python 3                      | Separate Py3 venv |
| Dialogflow CX Agent  | Core storyteller logic, RAG with GCS Data Store             | N/A (Google Cloud Platform)   | GCP            |

---

## Future Possibilities

* **Direct NAO to Dialogflow CX Integration:** This is the primary envisioned next step. Adapt NAO scripts (or create new ones) to interact directly with the Dialogflow CX API (e.g., using the Dialogflow CX Python client library). This would allow NAO to leverage the advanced RAG capabilities and conversational management of the Dialogflow CX agent, replacing the simpler `chatgpt_webhook.py` flow.
* **Enhanced NAO Expressiveness:** Incorporate NAO's gestures and movements synchronized with storytelling.
* **Multi-turn Story Generation:** Fully utilize Dialogflow CX's capabilities for more interactive, choice-driven narratives guided by NAO's interaction.
* **Dynamic Vocabulary for NAO:** Allow NAO's recognized vocabulary to be updated dynamically, perhaps based on context from Dialogflow CX.
* **Cloud Deployment:** Host any intermediary webhooks or services (if needed for NAO-Dialogflow CX communication) on GCP Cloud Functions or Cloud Run for scalability.

---

## License

MIT License — See source files for copyright.

---

## Questions or Contributions?

Feel free to fork this repo, submit pull requests, or open an issue with suggestions for enhancements!

---

## 🧾 Developer Reference (Doxygen)

This repository includes full developer-level documentation using [Doxygen](https://www.doxygen.nl/) for the Python scripts. All Python source files are annotated with:

- `@file`, `@brief`, `@param`, `@return`, `@author`
- Function-level docstrings structured for auto-generation
- Mermaid diagrams (e.g., ASR → Webhook → TTS flowchart in `test_asr.py`)
- Module constants and environmental variable documentation

### Entry Points (Python Scripts)

| Script               | Purpose                                                |
|----------------------|--------------------------------------------------------|
| `test_asr.py`        | Speech input → OpenAI webhook → TTS output (PoC)      |
| `chatgpt_webhook.py` | Flask server to generate stories via OpenAI API (for PoC) |
| `test_naoqi.py`      | Connectivity check to NAO’s `ALTextToSpeech` proxy    |
| `test_tts.py`        | Basic smoke test of NAO’s speech output               |

### To Generate Doxygen Documentation

To build the Doxygen HTML output for the Python scripts:

```bash
doxygen Doxyfile
```

Then open the generated file (usually in a `docs/html/` subdirectory):

```bash
xdg-open docs/html/index.html
```

This will give you a full class/function reference, parameter table, call graphs, and links between modules for the Python code.

> **Note**: Ensure your `Doxyfile` is configured for Python (e.g., `OPTIMIZE_OUTPUT_FOR_C = NO`, `EXTENSION_MAPPING = py=Python`, correct `INPUT` path to your Python scripts).

ℹ️ **Browse the full project documentation (including Doxygen output if hosted) here →** [github.io/CSC212-Virtual-Storyteller](https://darthvandor13.github.io/CSC212-Virtual-Storyteller/)
