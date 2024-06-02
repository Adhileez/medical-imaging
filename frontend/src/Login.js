import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Button, Input, Form, Segment } from 'semantic-ui-react';
import { useNavigate, Link } from 'react-router-dom';
import './App.css'; 

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const message = 'Welcome to the Medical Imaging Website. Please log in to continue.';
        speak(message);
    }, []);

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/login', { username, password });
            localStorage.setItem('token', response.data.access_token);
            navigate('/upload');
        } catch (error) {
            alert('Invalid credentials');
        }
    };

    const speak = (text) => {
        if ('speechSynthesis' in window) {
            const speech = new SpeechSynthesisUtterance(text);
            window.speechSynthesis.speak(speech);
        } else {
            console.error('Text-to-Speech is not supported in this browser.');
        }
    };

    return (
        <div className="login-page page-container">
            <Container className="auth-container">
                <h1 className="title">MEDICAL IMAGING WEBSITE</h1>
                <Segment>
                    <Form>
                        <Form.Field>
                            <label>Username</label>
                            <Input value={username} onChange={(e) => setUsername(e.target.value)} />
                        </Form.Field>
                        <Form.Field>
                            <label>Password</label>
                            <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                        </Form.Field>
                        <Button onClick={handleLogin}>Login</Button>
                    </Form>
                    <div>
                        <span>Don't have an account? </span>
                        <Link to="/register">Register here</Link>
                    </div>
                </Segment>
            </Container>
        </div>
    );
}

export default Login;















