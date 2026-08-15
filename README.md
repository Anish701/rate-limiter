# Rate Limiter (Python)

This is a learning project which implements a rate limiter using the token bucket algorithm and Redis.

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

## Instructions (macOS)

1. Install dependencies
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. Run the test suite:
    ```bash
    pytest
    ```

3. If you are using the redis option, run redis on a separate terminal:
    ```bash
    brew install redis
    redis-server
    ```

4. Run the app:
    ```bash
    uvicorn src.main:app --reload
    ```

5. Test the rate limiter:
    ```bash
    # Run multiple single requests rapidly
    curl http://127.0.0.1:8000/

    # Run loop of rapid requests
    for i in {1..5}; do curl -s http://127.0.0.1:8000/; done
    ```

You can also test by using your browser to navigate to http://localhost:8000/ and refreshing repeatedly quickly.

## Test multiple IP handling

Windows OS:
```bash
# 1. Exhaust 3 tokens for IP 1.1.1.1 (Status: 200)
1..3 | ForEach-Object { curl.exe -i -H "X-Forwarded-For: 1.1.1.1" http://127.0.0.1:8000/ }

# 2. Try a 4th request for IP 1.1.1.1 (Status: 429)
curl.exe -i -H "X-Forwarded-For: 1.1.1.1" http://127.0.0.1:8000/

# 3. Prove IP 2.2.2.2 has its own fresh bucket (Status: 200)
curl.exe -i -H "X-Forwarded-For: 2.2.2.2" http://127.0.0.1:8000/
```

macOS:
```bash
# 1. Exhaust 3 tokens for IP 1.1.1.1 (Prints 200 responses)
for i in {1..3}; do
  curl -i -H "X-Forwarded-For: 1.1.1.1" http://127.0.0.1:8000/
done

# 2. Try a 4th request for IP 1.1.1.1 (Prints 429 response)
curl -i -H "X-Forwarded-For: 1.1.1.1" http://127.0.0.1:8000/

# 3. Prove IP 2.2.2.2 still works with its own fresh bucket (Prints 200 response)
curl -i -H "X-Forwarded-For: 2.2.2.2" http://127.0.0.1:8000/
```

## Formatting

python ruff formatting commands:
```bash
ruff format
ruff check --fix
```

output code to prompt if needed for AI review (we do not use AI for this project other than reviewing code):
```bash
files-to-prompt . -e py > code_prompt.txt
```