
# Youtube Watch Analysis

This project analyzes YouTube watch data and presents it in a visual format using charts.

## Project Structure
```sh
.
├── backend
│   ├── data.json
│   ├── dataMerging.py
│   ├── main.py
│   ├── merged_data.json
│   ├── user_input.json
│   ├── vid_data.json
│   ├── video_data.json
│   ├── ytApi.py
│   └── ytLogging.py
├── public
│   ├── index.html
│   ├── manifest.json
│   └── robots.txt
├── src
│   ├── App.js
│   ├── ChartPage.css
│   ├── ChartPage.js
│   ├── index.js
│   ├── merged_data.json
│   ├── UserInput.css
│   └── UserInput.js
├── .gitignore
├── package.json
└── README.md
```

## Backend

The backend is implemented using FastAPI and Python scripts. It handles user input, runs Selenium tasks, fetches data from YouTube API, and merges the data.

### Endpoints

- `POST /start-selenium-task`: Starts the Selenium task with user input.
- `GET /status`: Checks the status of the processing.
- `GET /data`: Retrieves the processed data.

## Frontend

The frontend is implemented using React. It allows users to input their YouTube credentials and displays the processed data in charts.

## How to Run

1. Start the backend server:
    ```sh
    cd backend
    uvicorn main:app --reload
    ```

2. Start the frontend development server:
    ```sh
    npm start
    ```
    Runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Dependencies

- React
- Chart.js
- FastAPI
- Selenium
- Google API Client

## License

This project is licensed under the MIT License.