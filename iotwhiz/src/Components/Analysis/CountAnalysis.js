import React from 'react';
import { Card, CardContent, Typography, makeStyles } from '@material-ui/core';

const useStyles = makeStyles({
      root: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        marginTop: '20px',
      },
      card: {
        width: '180px',
        height: '117px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f5f5f5',
        borderRadius: '8px',
        boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
        fontFamily: "'Kdam Thmor Pro', sans-serif",
        marginTop: '20px',
        textAlign: 'center', // Align text center
        transition: 'background-color 0.3s ease',
        '&:hover': {
          backgroundColor: '#007bff',
          '& $title': {
            color: '#f5f5f5', // Change value color on hover
          },
    },
      },
    title: {
      fontSize: '14px',
      fontWeight: '500',
      marginTop: '20px',
      marginBottom: '10px',
      fontFamily: "'Kdam Thmor Pro', sans-serif",
      color: '#0056b3', // White text color
      width: '100%', // Ensure title spans the entire width
      borderTopLeftRadius: '8px', // Rounded corners
      borderTopRightRadius: '8px', // Rounded corners
      padding: '10px', // Add padding for better appearance
    },
    value: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: 'darkslategrey',
      fontFamily: "'Kdam Thmor Pro', sans-serif",
      paddingBottom: '40px',
    },
    valueAlt: {
      fontSize: '20px',
      fontWeight: 'bold',
      color: 'darkslategrey',
      fontFamily: "'Kdam Thmor Pro', sans-serif",
      paddingBottom: '40px',
    },
  });  
  

const CountAnalysis = ({ lineAnalysis }) => {
  const classes = useStyles();
  const isIoTApp = lineAnalysis.iot_enabled;
  
  return (
    <div className={classes.root}>
      <Card className={classes.card}>
        <CardContent>
          <Typography className={classes.title}>Type</Typography>
          <Typography className={classes.valueAlt}>{isIoTApp ? 'IoT App' : 'Non-IoT App'}</Typography>
        </CardContent>
      </Card>
      <Card className={classes.card}>
        <CardContent>
          <Typography className={classes.title}>Lines of Code</Typography>
          <Typography className={classes.value}>{lineAnalysis.lines_of_code}</Typography>
        </CardContent>
      </Card>
      <Card className={classes.card}>
        <CardContent>
          <Typography className={classes.title}>Number of Classes</Typography>
          <Typography className={classes.value}>{lineAnalysis.number_of_classes}</Typography>
        </CardContent>
      </Card>
      <Card className={classes.card}>
        <CardContent>
          <Typography className={classes.title}>Number of Methods</Typography>
          <Typography className={classes.value}>{lineAnalysis.number_of_methods}</Typography>
        </CardContent>
      </Card>
    </div>
  );
};

export default CountAnalysis;
