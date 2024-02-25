<div id="top"></div>

<br />
<div align="center">

<h2 align="center">IITK at SemEval-2024 Task 2: Exploring the Capabilities of LLMs for Safe Biomedical Natural Language Inference for Clinical Trials</h2>

  <p align="center">
    Official code implementation
    <br />
    <br />
    <a href="">View Paper</a>
    ·
    <a href="https://github.com/Shreyasi2002/NLI4CT/issues">Report Bug</a>
    ·
    <a href="https://github.com/Shreyasi2002/NLI4CT/pulls">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<summary><b>Table of Contents</b></summary>
<ol>
  <li>
    <a href="#about">About</a>
  </li>
  <li>
    <a href="#usage-instructions">Usage Instructions</a>
    <ul>
      <li><a href="#project-structure">Project Structure</a></li>
      <li><a href="#install-dependencies">Install Dependencies</a></li>
      <li><a href="#get-api-key">Get API Keys</a></li>
      <li><a href="#run-gemini">Run Gemini Pro</a></li>
    </ul>
  </li>
  <li>
    <a href="#results">Results</a>
  </li>
  <li>
    <a href="#citation">Citation</a>
  </li>
</ol>

## About
Large Language models (LLMs) have demonstrated state-of-the-art performance in various natural language processing (NLP) tasks across multiple domains, yet they are prone to shortcut learning and factual inconsistencies. This research investigates LLMs' robustness, consistency, and faithful reasoning when performing Natural Language Inference (NLI) on breast cancer Clinical Trial Reports (CTRs) in the context of SemEval 2024 Task 2: Safe Biomedical Natural Language Inference for Clinical Trials. We examine the reasoning capabilities of LLMs and their adeptness at logical problem-solving. A comparative analysis is conducted on pre-trained language models (PLMs), GPT-3.5, and Gemini Pro under zero-shot settings using Retrieval-Augmented Generation (RAG) framework, integrating various reasoning chains. The evaluation yields an F1 score of **0.69**, consistency of **0.71**, and a faithfulness score of **0.90** on the test dataset.

## Usage Instructions 

### Project Structure
```
📂 NLI4CT
|_📁 Gemini                   
  |_📄 run-gemini-chain.py   # Multi-turn conversation using Gemini Pro
  |_📄 prep_results.py       # Converting the labels to Entailment/Contradiction
  |_📄 Gemini_results.json   # Output of Gemini Pro - explanations and labels
  |_📄 results.json          # Final labels
|_📁 GPT-3.5                 # Experimentation with GPT-3.5
  |_📄 GPT3.5.py
  |_📄 ChatGPT_results.json
|_📁 training-data           # Training data - Clinical Trial Reports (CTRs)
|_📁 Experiments             # Experimentation with other models - Flan T5 and Pre-trained Language Models (PLMs)
  |_📄 flant5-label.ipynb
  |_📄 PLMs.ipynb
|_📄 Makefile                # Creating conda environment and installing dependencies
|_📄 LICENSE
|_📄 requirements.txt  
|_📄 .gitignore

```
