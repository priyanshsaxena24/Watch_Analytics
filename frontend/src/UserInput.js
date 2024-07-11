import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChartPage from './ChartPage';

function UserInputForm() {
const [username, setUsername] = useState('');
const [password, setPassword] = useState('');
const [authOption, setAuthOption] = useState('No');
const [message, setMessage] = useState('');
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
const [data, setData] = useState(null); 

const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true); 
    setError(null);
    try {
        const response = await axios.post('http://localhost:8000/start-selenium-task', {
        username,
        password,
        auth_option: authOption,
    });
    setMessage(response.data.message)

    pollStatus();

    } catch (error) {
    setError(error); 
    setLoading(false);
    }
};

const pollStatus = async () => {
    try {
    const interval = setInterval(async () => {
        const response = await axios.get('http://localhost:8000/status');
        if (response.data.processing_complete) {
        clearInterval(interval);
        fetchData(); 
        }
    }, 2000); // Poll every 2 seconds
    } catch (error) {
    setError(error);
    setLoading(false);
    }
};

const fetchData = async () => {
    try {
    
    const response = await axios.get('http://localhost:8000/data');
    setData(response.data); 
    setLoading(false);
    } catch (error) {
    setError(error); 
    setLoading(false);
    }
};

return (
    <div>
    <form onSubmit={handleSubmit}>
        <label>
        Username:
        <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
        />
        </label>
        <br />
        <label>
        Password:
        <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
        />
        </label>
        <br />
        <label>
        Two-Factor Authentication:
        <br />
        <label>
            <input
            type="radio"
            value="Yes"
            checked={authOption === 'Yes'}
            onChange={() => setAuthOption('Yes')}
            />
            Yes
        </label>
        <label>
            <input
            type="radio"
            value="No"
            checked={authOption === 'No'}
            onChange={() => setAuthOption('No')}
            />
            No
        </label>
        </label>
        <br />
        <button type="submit" disabled={loading}>Submit</button>
    </form>

    {loading && (
        <div className="loading-message">
        <p>Working on the backend...</p>
        </div>
    )}
    {message && <div>{message}</div>}
    {error && <div>Error: {error.message}</div>}
    {data && <ChartPage data={data} />}
    </div>
);
}

export default UserInputForm;
