import React, {useState} from 'react';
import { Card, CardContent, Typography, makeStyles, Modal, Box } from '@material-ui/core';
import './Analysis.css'

const useStyles = makeStyles({
      root: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        marginTop: '20px',
        marginLeft: "90px",
      },
      card: {
        width: '300px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f5f5f5',
        borderRadius: '8px',
        boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
        fontFamily: "'Kdam Thmor Pro', sans-serif",
        marginTop: '20px',
        textAlign: 'left', 
      },
    title: {
      fontSize: '16px',
      fontWeight: '500',
      marginBottom: '30px',
      fontFamily: "'Kdam Thmor Pro', sans-serif",
      color: '#0056b3', // White text color
      width: '100%', // Ensure title spans the entire width
      borderTopLeftRadius: '8px', // Rounded corners
      borderTopRightRadius: '8px', // Rounded corners
    },
    spanValue: {
        color: '#f5f5f5', // Default color for span
        paddingLeft: '5px',
      },
      spanValueDetails: {
        color: '#D4DFC7', // Default color for span
      },
      spanValueFilePath: {
        color: '#333', // Default color for span
      },
      list: {
        listStyle: 'none',
        padding: 0,
        textAlign: 'left',
      },
      listItem: {
        color: '#333',
        display: 'flex',
        alignItems: 'center',
        marginBottom: '5px',
      },
      icon: {
        marginRight: '5px',
        color: '#0056b3',
      },
      button: {
        padding: '5px 10px',
        cursor: 'pointer',
        backgroundColor: '#007bff',
        color: '#fff',
        borderRadius: '5px',
        border: '1px solid #007bff',
        '&:hover': {
            backgroundColor: '#0056b3',
        }
      }
  });  
  

// Your imports...

const ReflectionAnalysis = ({ lineAnalysis }) => {
    const classes = useStyles();
    const reflections = Object.entries(lineAnalysis).filter(([key, value]) => key !== 'Total_Reflections');
    const [selectedReflection, setSelectedReflection] = useState(null);
  
    const openModal = (type) => {
      setSelectedReflection(type);
    };
  
    const closeModal = () => {
      setSelectedReflection(null);
    };
  
    return (
      <div className={classes.root}>
        <Card className={classes.card}>
        <CardContent>
            <Typography className={classes.title}>
            Reflection Usage: <span className={classes.spanValue}>{lineAnalysis.Total_Reflections}</span>
            </Typography>
            <ul className={classes.list}>
            {reflections
                .filter(([type, info]) => info.count !== 0) // Filter out entries with count 0
                .map(([type, info]) => (
                <li key={type} className={classes.listItem}>
                    <button className={classes.button} onClick={() => openModal(type)}>
                    <span className={classes.spanValueDetails}>{type.replace(/_/g, ' ')}:</span>
                    <span className={classes.spanValue}>{info.count}</span>
                    </button>
                </li>
                ))}
            </ul>
        </CardContent>
        </Card>

        {selectedReflection && (
        <Modal open={Boolean(selectedReflection)} onClose={closeModal}>
          <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: 800, bgcolor: 'background.paper', boxShadow: 24, p: 4 }}>
            <Typography variant="h6">{selectedReflection}</Typography>
            <span className="close" onClick={closeModal}>
                &times;
            </span>            
            <ul style={{ maxHeight: '500px', overflow: 'auto', listStyleType: 'none', padding: 0 }}>
              {lineAnalysis[selectedReflection].occurrences.map((occurrence, index) => (
                <li key={index} style={{ color: '#333' }}>
                    <span className='filePath'>File Path: </span><span className={classes.spanValueFilePath}>{occurrence.file_path}, </span>
                    <span className='lineNumber'>Line Number: </span><span className={classes.spanValueFilePath}>{occurrence.line_number}</span><br></br>
                    <span className={classes.spanValueFilePath}>{occurrence.line_content}</span>
                </li>
              ))}
            </ul>
          </Box>
        </Modal>
      )}
      </div>
    );
  };
  
  export default ReflectionAnalysis;