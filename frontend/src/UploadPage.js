import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Button, Input, Segment } from 'semantic-ui-react';
import { useNavigate } from 'react-router-dom';
import './App.css'; 

const UploadPage = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const message = 'Upload your medical imaging files here.';
        speak(message);
    }, []);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const token = localStorage.getItem('token');
        const config = {
            headers: { Authorization: `Bearer ${token}` },
        };

        try {
            await axios.post('http://127.0.0.1:5000/upload', formData, config);
            alert('File uploaded successfully');
            navigate('/display/' + selectedFile.name);
        } catch (error) {
            alert('Failed to upload file');
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
        <div className="upload-page page-container">
            <Container className="auth-container">
                <Segment>
                    <Input type="file" onChange={handleFileChange} />
                    <Button onClick={handleSubmit}>Upload</Button>
                </Segment>
            </Container>
        </div>
    );
};

export default UploadPage;







