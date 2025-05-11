/*
 @licstart  The following is the entire license notice for the JavaScript code in this file.

 The MIT License (MIT)

 Copyright (C) 1997-2020 by Dimitri van Heesch

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 and associated documentation files (the "Software"), to deal in the Software without restriction,
 including without limitation the rights to use, copy, modify, merge, publish, distribute,
 sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or
 substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
 BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 @licend  The above is the entire license notice for the JavaScript code in this file
*/
var NAVTREE =
[
  [ "AI Storyteller", "index.html", [
    [ "NAO Virtual Storyteller — Research Project", "index.html", [
      [ "Abstract", "index.html#autotoc_md1", null ],
      [ "Table of Contents", "index.html#autotoc_md3", null ],
      [ "Research", "index.html#autotoc_md5", [
        [ "Core Research", "index.html#autotoc_md6", [
          [ "Supplemental Research", "index.html#autotoc_md7", null ]
        ] ]
      ] ],
      [ "Other Resources", "index.html#autotoc_md9", null ],
      [ "How Our AI Storytelling System Works – Conceptual Overview", "index.html#autotoc_md11", [
        [ "How the Dialogflow CX Storytelling Backend Works (Explained for Everyone) :)", "index.html#autotoc_md12", [
          [ "🔹 Step 1: Understanding Your Story Idea", "index.html#autotoc_md13", null ],
          [ "🔹 Step 2: Consulting the Archives & Crafting a New Tale", "index.html#autotoc_md14", null ],
          [ "🔹 Step 3: Presenting the Story", "index.html#autotoc_md15", null ]
        ] ],
        [ "How the Current NAO Proof-of-Concept Works (Simplified Loop)", "index.html#autotoc_md16", null ]
      ] ],
      [ "How Our AI Storytelling System Works – Technical Breakdown (CS Student)", "index.html#autotoc_md18", [
        [ "🔹 Core Components:", "index.html#autotoc_md19", null ],
        [ "🔹 System Flow A: Advanced Storytelling with Dialogflow CX (Conceptual)", "index.html#autotoc_md20", null ],
        [ "🔹 System Flow B: NAO Proof-of-Concept (Current <tt>test_asr.py</tt> Implementation)", "index.html#autotoc_md21", null ]
      ] ],
      [ "NAO Virtual Storyteller: Project Setup & Guide", "index.html#autotoc_md23", [
        [ "Project Objective (Clarified)", "index.html#autotoc_md24", null ],
        [ "Documentation & Downloads (NAO Specific)", "index.html#autotoc_md26", null ],
        [ "Repository Structure Overview", "index.html#autotoc_md28", null ],
        [ "Section 1: NAO Robot Interaction Setup (Python 2 & NAOqi SDK)", "index.html#autotoc_md30", [
          [ "1.1. Network Setup for NAO Robot", "index.html#autotoc_md31", [
            [ "1.1.1. Connect NAO to the Network", "index.html#autotoc_md32", null ],
            [ "1.1.2. Find NAO's IP Address", "index.html#autotoc_md33", null ],
            [ "1.1.3. Ensure Network Connectivity", "index.html#autotoc_md34", null ],
            [ "1.1.4. Firewall Considerations", "index.html#autotoc_md35", null ]
          ] ],
          [ "1.2. Install Python 2.7 on Ubuntu 22.04 (using <tt>pyenv</tt>)", "index.html#autotoc_md36", [
            [ "1.2.1. Install <tt>pyenv</tt> Dependencies", "index.html#autotoc_md37", null ],
            [ "1.2.2. Install <tt>pyenv</tt>", "index.html#autotoc_md38", null ],
            [ "1.2.3. Configure Shell for <tt>pyenv</tt>", "index.html#autotoc_md39", null ],
            [ "1.2.4. Install Python 2.7.18 with <tt>pyenv</tt>", "index.html#autotoc_md40", null ],
            [ "1.2.5. (Optional) Set Python 2.7.18 as Local Default for Your Project", "index.html#autotoc_md41", null ]
          ] ],
          [ "1.3. Create a Python 2 Virtual Environment", "index.html#autotoc_md42", [
            [ "1.3.1. Ensure <tt>pip</tt> for Python 2.7 is Available", "index.html#autotoc_md43", null ],
            [ "1.3.2. Install <tt>virtualenv</tt>", "index.html#autotoc_md44", null ],
            [ "1.3.3. Create and Activate the Virtual Environment", "index.html#autotoc_md45", null ]
          ] ],
          [ "1.4. Install the NAOqi Python 2 SDK", "index.html#autotoc_md46", [
            [ "1.4.1. Extract the SDK", "index.html#autotoc_md47", null ],
            [ "1.4.2. Make NAOqi SDK available to your Python 2 Environment", "index.html#autotoc_md48", null ]
          ] ]
        ] ]
      ] ],
      [ "(Ensure naoqi_env is activated)", "index.html#autotoc_md49", null ],
      [ "(Replace /path/to/your/NAOQI_PYTHON_LIB_DIR with the actual, absolute path)", "index.html#autotoc_md50", null ],
      [ "Example (replace with your actual SDK path):", "index.html#autotoc_md51", null ],
      [ "SDK_LIB_PATH=\"~/naoqi_sdks/pynaoqi-python2.7-X.X.X.X-linux64/lib/python2.7/site-packages\"", "index.html#autotoc_md52", null ],
      [ "VENV_LIB_PATH=\"naoqi_env/lib/python2.7/site-packages\"", "index.html#autotoc_md53", null ],
      [ "cp \"${SDK_LIB_PATH}/naoqi.py\" \"${VENV_LIB_PATH}/\"; cp \"${SDK_LIB_PATH}/_naoqi.so\" \"${VENV_LIB_PATH}/\"", "index.html#autotoc_md54", [
        [ "Section 2: Dialogflow CX AI Storyteller Agent Setup", "index.html#autotoc_md59", [
          [ "1.5. Install Python 2 Dependencies for NAO Scripts", "index.html#autotoc_md56", null ],
          [ "1.6. Troubleshooting NAO Setup", "index.html#autotoc_md57", null ],
          [ "2.1. Project Overview (Dialogflow CX Agent)", "index.html#autotoc_md60", null ],
          [ "2.2. Technology Stack (Dialogflow CX Agent)", "index.html#autotoc_md61", null ],
          [ "2.3. Core Concepts: RAG via GCS Data Store", "index.html#autotoc_md62", null ],
          [ "2.4. Setup & Prerequisites (Dialogflow CX Start-to-Finish)", "index.html#autotoc_md63", null ],
          [ "2.5. Agent Configuration Steps (Dialogflow CX Console)", "index.html#autotoc_md64", null ],
          [ "2.6. How to Use/Test Dialogflow CX Agent", "index.html#autotoc_md65", null ],
          [ "2.7. Known Issues / Troubleshooting Context (Dialogflow CX)", "index.html#autotoc_md66", null ]
        ] ],
        [ "Section 3: Running Project Components & Demonstrations", "index.html#autotoc_md68", [
          [ "3.1. Configure OpenAI API Key (for <tt>chatgpt_webhook.py</tt>)", "index.html#autotoc_md69", null ],
          [ "3.2. Running the NAO Direct Interaction Scripts & PoC Loop (Python 2)", "index.html#autotoc_md70", null ],
          [ "3.3. Interacting with the Dialogflow CX AI Storyteller Agent (via Simulator)", "index.html#autotoc_md71", null ]
        ] ],
        [ "Internals (NAO Interaction Scripts)", "index.html#autotoc_md73", null ],
        [ "Scripts Overview Table", "index.html#autotoc_md75", null ],
        [ "Future Possibilities", "index.html#autotoc_md77", null ],
        [ "License", "index.html#autotoc_md79", null ],
        [ "Questions or Contributions?", "index.html#autotoc_md81", null ],
        [ "🧾 Developer Reference (Doxygen)", "index.html#autotoc_md83", [
          [ "Entry Points (Python Scripts)", "index.html#autotoc_md84", null ],
          [ "To Generate Doxygen Documentation", "index.html#autotoc_md85", null ]
        ] ]
      ] ]
    ] ],
    [ "Namespaces", "namespaces.html", [
      [ "Namespace List", "namespaces.html", "namespaces_dup" ],
      [ "Namespace Members", "namespacemembers.html", [
        [ "All", "namespacemembers.html", null ],
        [ "Functions", "namespacemembers_func.html", null ],
        [ "Variables", "namespacemembers_vars.html", null ]
      ] ]
    ] ],
    [ "Classes", "annotated.html", [
      [ "Class List", "annotated.html", "annotated_dup" ],
      [ "Class Index", "classes.html", null ],
      [ "Class Hierarchy", "hierarchy.html", "hierarchy" ],
      [ "Class Members", "functions.html", [
        [ "All", "functions.html", null ],
        [ "Variables", "functions_vars.html", null ]
      ] ]
    ] ],
    [ "Files", "files.html", [
      [ "File List", "files.html", "files_dup" ]
    ] ]
  ] ]
];

var NAVTREEINDEX =
[
"annotated.html",
"index.html#autotoc_md69"
];

var SYNCONMSG = 'click to disable panel synchronisation';
var SYNCOFFMSG = 'click to enable panel synchronisation';