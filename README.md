# **LLM Markdown Document Store**

A Python library to give an LLM a markdown document store via supported LLM tool calling or function calling to Large Language Models (LLMs) through Open WebUI's (or similar clients) tools feature.

----
**Table of Contents**

* [Overview](#overview)
* [Features](#features)
* [Installing](#installing)
* [Usage](#usage)
* [License](#license)

----
**Overview**

This library is designed to provide a simple way for Open WebUI users (or users of similar LLM clients that support tool calling or function calling) to access and manipulate Markdown Documents through the tool calling feature.

----
**Features**

* Save a Markdown document in the document store
* Get the contents of a Markdown document in the document store
* List the Markdown documents currently saved in the document store
* Delete a Markdown document in the document store

----
**Installing**

To install this toolset, simply add it to your Open WebUI tools list:

1. Navigate to the `Tools` tab under the `Workspaces` section.
2. Click the plus (+) button to add a new tool.
3. Copy/Paste the contents of [`llm_markdown_document_store.py`](llm_markdown_document_store.py) into the code window
4. Fill in the tool name and description fields and click save, then confirm.

----
**Usage**

* In Open WebUI, in the prompt field, you can now select the tool and prompt the LLM to save all or part of the current context as a markdown document with a given name.
* The LLM can also look at documents in the document store to see if any of them can augment it's training data, sort of like a port man's RAG, though, that is not the intent of this feature.

----
**License**

This library is released under the MIT License. See [`LICENSE`](./LICENSE) for details.
