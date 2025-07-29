"""
title: LLM Markdown Document Store
author: adrian-bacon
author_url: https://github.com/adrian-bacon
git_url: https://github.com/adrian-bacon/llm-markdown-document-store
description: A set of functions to give an LLM a markdown document store via supported LLM tool calling or function calling.
version: 1.0.0
license: MIT
"""

import os
import json
from pydantic import BaseModel

# If this path does not work for you, modify it as needed.  This is initially
# set assuming open webui running in a docker container
DOCUMENTS_PATH = "/app/backend/data/.llm_markdown_document_store"


class Tools:
    class Valves(BaseModel):
        pass

    class UserValves(BaseModel):
        pass

    def __init__(self):
        self.valves = self.Valves()
        self.user_valves = self.UserValves()

        if not os.path.exists(DOCUMENTS_PATH):
            os.mkdir(DOCUMENTS_PATH)

    def save_markdown_document(self,
                               document_name: str,
                               document_contents: str) -> str:
        """
        Save a Markdown document with the given name to this Markdown document
        store.

        If the user does not give a document name or file name ask the user
        what document name they want to save the Markdown under.

        If the user tells you to generate a document name or file name, generate
        a document name that reflects the contents of the Markdown document to
        be saved.

        If generating a document name or file name, the name should end with a
        '.md' extension.

        If generating a document name or file name, the name should not have any
        spaces in it.  There should be underscores where there would normally
        be spaces, e.g. 'test_document.md'

        If the user gives you a document name that has spaces in it, replace the
        spaces with the underscore character for the user, e.g.
        'test document.md' would be converted to 'test_document.md'.

        If the user gives you a document name that does not end with a '.md'
        extension, then append a '.md' extension to the end of the name for the
        user.

        If automatically generating a document name or file name, to avoid
        overwriting any existing documents, do not generate a name that already
        exists.  You can check what document names already exist by running the
        `list_markdown_documents` function.  It will give you a list of document
        names that are already in use.

        If the user gives you a document name that already exists, they want to
        overwrite that document with the new contents.

        Example usage:
        "Save that as a markdown document with the name: yay.md"
        "Save that as a markdown document with the name yay.md"
        "Save that as markdown with the name: yay.md"
        "Save that as markdown"
        "Save that as markdown with a generated name"
        "Update test_document.md with this markdown"
        "Save this as a markdown document with the name: test_document.md"
        "Save this as a markdown document as test_document.md"

        :param document_name: The name of the Markdown document, can also be called the file name.
        :param document_contents: The full contents of the Markdown document to save.
        :return: A string indicating success or failure
        """
        if not document_name.lower().endswith(".md"):
            file_name = f"{document_name.lower()}.md".replace(" ", "_")
        else:
            file_name = document_name.lower().replace(" ", "_")

        full_path = os.path.join(DOCUMENTS_PATH, file_name)

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(document_contents)

            return f"Successfully saved {file_name}"

        except Exception as e:
            return (f"ERROR: Could not save {file_name}, an exception occurred:"
                    f" {str(e)}")

    def get_markdown_document(self, document_name: str) -> str:
        """
        Gets the contents of a Markdown document for the given document name.

        If the user asks you to get a Markdown document name or file name,
        get the contents of the Markdown document with this function and give
        the user the raw contents of the Markdown document with no
        modifications.

        If the user asks you show them the Markdown document on a given subject,
        use the `list_markdown_documents` function to get a list of documents
        and check if any document names are related to the requested subject,
        and if so, get that document's contents with this function and return
        the raw document contents to the user with no modifications.

        Example usage:
        "Show me the markdown document test_document.md"
        "Show me the markdown document on thomas edison"
        "Get the markdown document test_document.md"
        "Retrieve the markdown document test_document.md"

        :param document_name: The document name to get.  Can also be called the file name.
        :return: the contents of the Markdown document.
        """

        full_path = os.path.join(DOCUMENTS_PATH, document_name)
        if not os.path.exists(full_path):
            return 'ERROR: No document by that name exists'
        else:
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    return f.read()

            except Exception as e:
                return (f"ERROR: Could not read document {document_name}, "
                        f"an exception occurred: {str(e)}")

    def list_markdown_documents(self) -> str:
        """
        List all the Markdown document names currently saved to this Markdown
        document store.

        If a user is asking about a given subject, you can call this function to
        see if there are any Markdown documents that have a document name that
        might be related to the subject, and if so, use the
        `get_markdown_document` function to get the document's contents to help
        you give more information about the subject the user is asking about.

        Example usage:
        "Show me the list of Markdown documents"
        "What Markdown documents are available"

        :return: The list of Markdown documents in a string as a json array
        """
        documents = []
        for name in os.listdir(DOCUMENTS_PATH):
            if name.endswith(".md"):
                documents.append(name)

        return json.dumps(documents)

    def delete_markdown_document(self, document_name: str) -> str:
        """
        Delete a Markdown document from the Markdown document store.

        Do not use this function unless the user explicitly asks you to delete a
        Markdown document.

        Example usage:
        "Delete test_document.md"
        "Remove test_document.md"
        "Redact test_document.md"

        :param document_name: The Markdown document name to delete.
        :return: A string indicating success or failure.
        """
        full_path = os.path.join(DOCUMENTS_PATH, document_name)
        try:
            if os.path.exists(full_path):
                os.remove(full_path)
                return f"{document_name} successfully deleted"
            else:
                return f"{document_name} does not exist, could not delete"

        except Exception as e:
            return (f"ERROR: Could not delete {document_name}, and exception"
                    f" occurred: {str(e)}")
