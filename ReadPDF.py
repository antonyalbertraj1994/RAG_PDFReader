# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


# Read a PDF into LangChain Document objects
def ReadPDF(filename):

    #file_path = "../example_data/nke-10k-2023.pdf"
    loader = PyPDFLoader(filename)

    docs = loader.load()
    print(f"{docs[0].page_content[:201]}\n")
    print(docs[0].metadata)

    print(len(docs))
    return docs
#
def TextSplitter(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=100, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    print(f"Split:{len(all_splits)}\n")
    return all_splits

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     docs = ReadPDF('input.pdf')
#     splits = TextSplitter(docs)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
