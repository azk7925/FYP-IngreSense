# IngreSense - run

This guide details how to run the IngreSense Cosmetic Ingredient Classification System.

## Project Structure

- **`backend/`**: FastAPI server, model logic, and knowledge base.
- **`frontend/`**: React + Vite application with Tailwind CSS.

## 1. Setting up the Backend

1.  Open a terminal in the root directory.
2.  Install python dependencies (if not already installed):
    ```bash
    pip install -r backend/requirements.txt
    ```
    *(Note: This installs torch, transformers, etc. It may take a while.)*

3.  Run the server:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

    > [!NOTE]
    > **Mock Mode**: If `backend/models/best_model.pt` is missing, the server will start in "Mock Mode". It will use keyword matching from the Knowledge Graph to simulate results, allowing you to test the UI immediately.

    > [!IMPORTANT]
    > **Enable AI Model**: To use the actual trained model, place your `best_model.pt` file inside `backend/models/`. Restart the backend server after adding the file.

## 2. Setting up the Frontend

1.  Open a new terminal and navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies (if you haven't already):
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
4.  Open the link shown (usually `http://localhost:5173`) in your browser.

## 3. Using the Application

1.  **Input**: Paste a list of ingredients into the text area.
    - *Example*: "Water, Glycerin, Niacinamide, Fragrance, Methylparaben"
2.  **Analyze**: Click the **Analyze Ingredients** button.
3.  **View Results**:
    - **Cards**: See the probability for Halal, Vegan, Allergen, and Eco-Friendly.
    - **Table**: View detailed breakdown for each ingredient, including its source and reasoning.

## 4. Features Implemented
- **Hybrid Backend**: Supports both AI model inference and Knowledge Graph lookups.
- **Resilient UI**: Handles errors gracefully and provides visual feedback (loading spinners, status badges).
- **Premium Design**: Glassmorphism effects, smooth animations, and a clean professional aesthetic.
