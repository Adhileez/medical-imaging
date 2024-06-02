import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Button, Input, Form, Segment } from 'semantic-ui-react';
import { useNavigate, Link } from 'react-router-dom';
import './App.css'; // Using absolute path

function Register() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const message = 'Register for a new account on the Medical Imaging Website.';
        speak(message);
    }, []);

    const handleRegister = async () => {
        try {
            await axios.post('http://127.0.0.1:5000/register', { username, password });
            alert('User registered successfully');
            navigate('/login');
        } catch (error) {
            alert('Error registering user');
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
        <div className="register-page page-container">
            <Container className="auth-container">
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
                        <Button onClick={handleRegister}>Register</Button>
                    </Form>
                    <div>
                        <span>Already have an account? </span>
                        <Link to="/login">Login here</Link>
                    </div>
                </Segment>
            </Container>
        </div>
    );
}

export default Register;










