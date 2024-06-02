import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { Container, Segment, Image, Grid } from 'semantic-ui-react';
import './App.css';

const DisplayPage = () => {
    const { filename } = useParams();
    const [imageSlices, setImageSlices] = useState([]);
    const [predictionSlices, setPredictionSlices] = useState([]);

    useEffect(() => {
        const token = localStorage.getItem('token');
        const config = {
            headers: { Authorization: `Bearer ${token}` },
        };

        axios.get(`http://127.0.0.1:5000/images_predictions/${filename}`, config)
            .then(response => {
                setImageSlices(response.data.image_slices);
                setPredictionSlices(response.data.prediction_slices);
            })
            .catch(error => console.error('Error fetching slices:', error));
    }, [filename]);

    const getPredictionSlice = (imageSlice) => {
        const sliceNumber = imageSlice.match(/slice(\d+)/)[1];
        const modalities = ['Background', 'Enhanced Tumor', 'Non-Enhanced Tumor', 'Swelling'];
        return modalities.map(modality => {
            const predSlice = predictionSlices.find(predSlice => predSlice.includes(`slice${sliceNumber}`) && predSlice.includes(modality));
            return { modality, sliceNumber, predSlice };
        }).filter(item => item.predSlice);
    };

    const combinedSlices = imageSlices.map((imageSlice) => {
        const sliceNumber = imageSlice.match(/slice(\d+)/)[1];
        const modality = imageSlice.match(/_(Flair|T1ce|T2)/)[1];
        return {
            imageSlice,
            sliceNumber,
            modality,
            predictionSlices: getPredictionSlice(imageSlice)
        };
    });

    return (
        <div className="display-page page-container">
            <Container>
                <Segment>
                    <h2>Original Image Slices and Prediction Masks</h2>
                    <div className="scroll-container">
                        <Grid columns={2} divided>
                            {combinedSlices.map((slicePair, index) => (
                                <Grid.Row key={index}>
                                    <Grid.Column>
                                        <h3>Original Image Slice (Slice {slicePair.sliceNumber} - {slicePair.modality})</h3>
                                        <Image src={`http://127.0.0.1:5000/static/images_png/${slicePair.imageSlice}`} alt={slicePair.imageSlice} />
                                    </Grid.Column>
                                    <Grid.Column>
                                        <h3>Prediction Mask Slices (Slice {slicePair.sliceNumber})</h3>
                                        {slicePair.predictionSlices.length > 0 ? (
                                            slicePair.predictionSlices.map((predSlice, predIndex) => (
                                                <div key={predIndex}>
                                                    <h4>{predSlice.modality} (Slice {predSlice.sliceNumber})</h4>
                                                    <Image src={`http://127.0.0.1:5000/static/predictions_png/${predSlice.predSlice}`} alt={predSlice.predSlice} />
                                                </div>
                                            ))
                                        ) : (
                                            <p>No prediction slice found for {slicePair.imageSlice}</p>
                                        )}
                                    </Grid.Column>
                                </Grid.Row>
                            ))}
                        </Grid>
                    </div>
                </Segment>
            </Container>
        </div>
    );
};

export default DisplayPage;

















