# Rate Limiter (Python)

This is a learning project which implements a rate limiter using the token bucket algorithm.

No AI tools were used in this project as it was meant to practice manual systems coding and design.

## Instructions (Windows OS)

1. Install dependencies
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

2. Run the test suite:
    ```bash
    pytest
    ```

3. Run the app:
    ```bash
    uvicorn src.main:app --reload
    ```

4. Test the rate limiter:
    ```bash
    # Run multiple single requests rapidly
    curl.exe http://127.0.0.1:8000/

    # Run loop of rapid requests
    1..5 | ForEach-Object { (curl.exe -s http://127.0.0.1:8000/) }
    ```

You can also test by using your browser to navigate to http://localhost:8000/ and refreshing repeatedly quickly.