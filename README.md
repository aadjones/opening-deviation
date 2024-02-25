# How to Run

Follow these steps to set up and run the project.

## 1. Create a Virtual Environment

First, create a virtual environment for your Python in the project directory. This isolates your project dependencies.

```bash
python3 -m venv myenv
```

Activate the virtual environment:

- On Unix/Linux/macOS:
  ```bash
  source myenv/bin/activate
  ```
- On Windows:
  ```cmd
  myenv\Scripts\activate
  ```

## 2. Install Dependencies

Install the project dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## 3. Setup Streamlit Configuration

Streamlit expects a hidden directory named `.streamlit` at the top level of your project. Create this directory if it doesn't already exist:

```bash
mkdir -p .streamlit
```

Inside the `.streamlit` directory, create a file named `secrets.toml` and add your LICHESS API token:

```bash
cd .streamlit && touch secrets.toml 
```

```toml
LICHESS_API_TOKEN = "your_api_token"
```

Be sure to replace `"your_api_token"` with your actual API token.

## 4. Run the Streamlit App

With all requirements set up, run the Streamlit app from the top directory using the following command:

```bash
streamlit run opening-deviation.py
```