# RAG based chatbot
## Setup and execution
### Videos
*  [Demo](https://www.youtube.com/watch?v=FSou2DPo714)
*  [Architecture and code walkthorugh](https://www.youtube.com/watch?v=x5BxEr4s5_E)

### Description
This project aims to develop an interactive chat-based system leveraging the RAG (Retrieve, Aggregate, Generate) methodology to process data from demonstration indices. The system will allow users to interact with the data in a conversational manner.

### Setup instructions
We first need to install the correct version of python. One of the ways to do that is using **pyenv**
```
PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.11.8
```
Once we python installed we can create and activate our python virtual environment using
```
python -m venv venv
source venv/bin/activate
```
Dependencies can be installed using
```
pip install -r requirements.txt
```
We use Ollama to manage LLMs locally and it can be installed using the [installer](https://ollama.com/). Once installed, we can download LLama3 Instruct model using
```
ollama pull llama3:instruct
```
(Optional) We have our UI built using Elm and the compiled JS is already in the public/js folder. In case you wan to tinker with the Elm code base, then you can build client code using the below command after you have installed [Elm](https://guide.elm-lang.org/install/elm.html)
```
cd client
bash build.sh
```
### Running server
Make sure that you have the python virtual environment activated and then run following command
```
fastapi dev main.py
```
Once you see the line mentioned below in the console, head to [localhost:8000](http://localhost:8000) and start using the chatbot
```
INFO:     Application startup complete.
```
