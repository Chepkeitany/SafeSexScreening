import React, { Component } from "react";
import CssBaseline from "@material-ui/core/CssBaseline";
import Container from "@material-ui/core/Container";
import { withStyles } from "@material-ui/core/styles";
import {
  Card,
  CardContent,
  CardHeader,
  Link,
  Typography,
  Paper
} from "@material-ui/core";
import TopBar from "./TopBar";
import { apiGet } from "../utils/api";

const styles = theme => ({
  card: {
    minWidth: 275,
    paddingBottom: 20
  },
  title: {
    fontSize: 14
  },
  link: {
    margin: theme.spacing(1),
    paddingTop: 10,
  },
  red: {
    color:'red'
  },
  green: {
    color:'green'
  }
});

class Recommendation extends Component {
  state = {};

  getStyle(recommendation) {
    switch (recommendation) {
      case 'Urgently recommended': return 'red';
      case 'Highly recommended':   return 'yellow';
      default: return 'green';
    }
  }
  componentDidMount = async () => {
    const recommendations = await apiGet("recommendations");
    const patient_recommendations = [];
    for (let i = 0; i < recommendations.length; i++) {
      const recommendation = recommendations[i];
      const response = await apiGet(`patients/${recommendation.patient_id}`);
      patient_recommendations.push({
        age: response.age,
        name: response.name,
        gender: response.gender,
        days_since_last_screening: recommendation.days_since_last_screening,
        recommendation: recommendation.screening_recommendation
      });
    }

    this.setState({ patient_recommendations });
  };
  render() {
    const { classes } = this.props;
    const { patient_recommendations } = this.state;
    return (
      <Container>
        <CssBaseline />
        <TopBar />
        <Link href="/ss2frontend/dashboard" variant="button" className={classes.link}> Go Back </Link>
        <Typography variant="h6" className={classes.link}> Patient Recommendations </Typography>
        <Paper className={classes.paper}>
          {patient_recommendations &&
            patient_recommendations.map((recommendation,i) =>
              <Card className={classes.card} key={i}>
                <CardHeader title={recommendation.name}></CardHeader>
                <CardContent>
                  <Typography
                    className={classes.title}
                    color="textSecondary"
                    variant="h5"
                    gutterBottom
                  >
                    Age: {recommendation.age}
                  </Typography>
                  <Typography
                    className={classes.title}
                    color="textSecondary"
                    variant="h5"
                    gutterBottom
                  >
                    Gender: {recommendation.gender}
                  </Typography>
                  <Typography
                    className={classes.title}
                    color="textSecondary"
                    variant="h5"
                    gutterBottom
                  >
                    Days since last screening: {recommendation.days_since_last_screening}
                  </Typography>
                  <Typography
                    className={classes.title}
                    color="textSecondary"
                    variant="h5"
                    gutterBottom
                  >
                    Recommendation: <b style={{ color: this.getStyle(recommendation.recommendation) }}> { recommendation.recommendation} </b>
                  </Typography>
                </CardContent>
              </Card>
            )}
        </Paper>
      </Container>
    );
  }
}

export default withStyles(styles)(Recommendation);
