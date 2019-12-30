import React, { Component } from "react";
import CssBaseline from "@material-ui/core/CssBaseline";
import Container from "@material-ui/core/Container";
import { withStyles } from "@material-ui/core/styles";
import {
  FormControl,
  FormControlLabel,
  Input,
  InputBase,
  IconButton,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  CardHeader,
  Button,
  RadioGroup,
  Radio,
  FormLabel
} from "@material-ui/core";
import SearchIcon from "@material-ui/icons/Search";
import { apiGet, apiPost } from "../utils/api";
import TopBar from "./TopBar";

const styles = theme => ({
  card: {
    minWidth: 275,
    paddingBottom: 20
  },
  container: {
    display: "flex",
    flexWrap: "wrap"
  },
  history: {
    padding: 10
  },
  input: {
    marginLeft: theme.spacing(1),
    flex: 1
  },
  iconButton: {
    padding: 10
  },
  title: {
    fontSize: 14
  },
  paper: {
    color: theme.palette.text.secondary,
    paddingTop: 20
  },
  root: {
    padding: "2px 4px",
    display: "flex",
    alignItems: "center",
    minWidth: 275
  },
  margin: {
    margin:theme.spacing(1),
  },
  textField: {
    width: 200,
  }
});

class Dashboard extends Component {
  state = {
    name: ""
  };
  searchPatient = async () => {
    const response = await apiGet(`patients/${this.state.patientId}`);

    if (response) {
      this.setState({
        age: response.age,
        fhirid: response.id,
        name: response.name,
        gender: response.gender
      });
    }
  };

  yesNoValue = value => {
    if (value === 'yes') {
      return true;
    } else {
      return false;
    }
  }

  updateSexualHistory = async() => {
    const num_sexual_partners = this.state.noSexPartners || 0;
    const has_new_sex_partners = this.yesNoValue(this.state.hasNewSexPartners);
    const partner_has_std_symptoms = this.yesNoValue(this.state.sexWithInfectedPersons);
    const is_condom_user = this.yesNoValue(this.state.useCondoms);
    const is_drug_user = this.yesNoValue(this.state.isDrugUser);
    const is_sex_worker = this.yesNoValue(this.state.exchangeSexForDrugs);
    const is_sexually_active = this.yesNoValue(this.state.sexuallyActive);
    const last_screening = this.state.lastScreening || '2017-05-24';
    const has_dysuria = this.yesNoValue(this.state.painWhileUrinating);
    const has_rash = this.yesNoValue(this.state.hasRash);
    const has_fever = this.yesNoValue(this.state.hasFever);
    const has_pharyngeal_discomfort = this.yesNoValue(this.state.pharyngealDiscomfort);
    const is_pregnant = this.yesNoValue(this.state.expectant);
    const patient_id = this.state.patientId;

    const body = {
      has_dysuria,
      has_rash,
      has_fever,
      has_new_sex_partners,
      has_pharyngeal_discomfort,
      is_sexually_active,
      is_condom_user,
      is_drug_user,
      is_sex_worker,
      is_pregnant,
      last_screening,
      num_sexual_partners,
      partner_has_std_symptoms,
      patient_id
    };

    if (patient_id) {
      const response = await apiPost('recommendations', body);
      if (response) {
        // Redirect to recommendations page
        window.location = '/ss2frontend/recommendation';

      }
    } else {
      alert('Please search for a patient and fill their form!');
    }
  };
  render() {
    const { classes } = this.props;
    return (
      <Container>
        <CssBaseline />
        <TopBar />     
        <Paper className={classes.paper}>
          <Grid container justify="center" className={classes.history}>
            <Grid item xs={12} md={4}>
              <Paper className={classes.root}>
                <InputBase
                  className={classes.input}
                  placeholder="Search Patient ID"
                  inputProps={{ "aria-label": "search patient id" }}
                  onChange={e => this.setState({ patientId: e.target.value })}
                />
                <IconButton
                  className={classes.iconButton}
                  aria-label="search"
                  onClick={this.searchPatient}
                >
                  <SearchIcon />
                </IconButton>
              </Paper>
              <Card className={classes.card}>
                <CardHeader title={this.state.name}></CardHeader>
                <CardContent>
                  <Typography
                    className={classes.title}
                    color="textSecondary"
                    variant="h5"
                    gutterBottom
                  >
                    Age: {this.state.age}
                  </Typography>
                  <Typography
                    className={classes.title}
                    color="textSecondary"
                    variant="h5"
                    gutterBottom
                  >
                    Gender: {this.state.gender}
                  </Typography>
                  <Typography
                    className={classes.title}
                    color="textSecondary"
                    variant="h5"
                    gutterBottom
                  >
                    FHIR ID: {this.state.fhirid}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={8} className={classes.history}>
              <Paper>
                <Card className={classes.card}>
                  <CardHeader
                    title={`Sexual history for ${this.state.name}`}
                  ></CardHeader>
                  <CardContent>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="sexually-active">
                        1.Are you sexually active?
                      </FormLabel>
                      <RadioGroup
                        aria-label="sexually-active"
                        name="sexually-active"
                        onChange={e =>
                          this.setState({ sexuallyActive: e.target.value })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="use-condoms">
                        2.Do you use condoms always during intercourse?
                      </FormLabel>
                      <RadioGroup
                        aria-label="use-condoms"
                        name="use-condoms"
                        onChange={e =>
                          this.setState({ useCondoms: e.target.value })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="no-sex-partners">
                        3.How many sexual partners have you had in the past 3
                        months?
                      </FormLabel>
                      <Input
                        id="no-sex-partners"
                        className={classes.textField}
                        defaultValue='0'
                        type='number'
                        onChange={e =>
                          this.setState({ noSexPartners: e.target.value })
                        }
                      />
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="new-sex-partners">
                        4.Have you had new sex partners in last 3 months?
                      </FormLabel>
                      <RadioGroup
                        aria-label="new-sex-partners"
                        name="new-sex-partners"
                        onChange={e =>
                          this.setState({ hasNewSexPartners: e.target.value })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="no-new-sex-partners">
                        5.When was your last screening for Gonorrhea or
                        Chlamydia ?
                      </FormLabel>
                      <Input
                        className={classes.textField}
                        id="no-new-sex-partners"
                        type='date'
                        defaultValue="2017-05-24"
                        onChange={e =>
                          this.setState({ lastScreening: e.target.value })
                        }
                      />
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="use-drugs">
                        6.Have you used drugs since your last screening or in
                        the last year?
                      </FormLabel>
                      <RadioGroup
                        aria-label="use-drugs"
                        name="customized-radios"
                        onChange={e =>
                          this.setState({
                            isDrugUser: e.target.value
                          })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <FormControl
                      fullWidth
                      className={classes.margin}
                      component="fieldset"
                    >
                      <FormLabel htmlFor="exchange-sex-for-drugs">
                        7.Have you exchanged sex for money or drugs in the last
                        6 months?
                      </FormLabel>
                      <RadioGroup
                        aria-label="exchange-sex-for-drugs"
                        name="exchange-sex-for-drugs"
                        onChange={e =>
                          this.setState({ exchangeSexForDrugs: e.target.value })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="sex-with-infected-partner">
                        8.Have you had sex with a STD infected person?
                      </FormLabel>
                      <RadioGroup
                        aria-label="sex-with-infected-person"
                        name="customized-radios"
                        onChange={e =>
                          this.setState({
                            sexWithInfectedPersons: e.target.value
                          })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="has-rash">
                        9.Do you have a rash?
                      </FormLabel>
                      <RadioGroup
                        aria-label="has-rash"
                        name="has-rash"
                        onChange={e =>
                          this.setState({ hasRash: e.target.value })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="has-fever">
                        10.Do you have a fever?
                      </FormLabel>
                      <RadioGroup
                        aria-label="has-fever"
                        name="has-fever"
                        onChange={e =>
                          this.setState({ hasFever: e.target.value })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="pain-while-urinating">
                        11.Do you experience pain while urinating?
                      </FormLabel>
                      <RadioGroup
                        aria-label="pain-while-urinating"
                        name="pain-while-urinating"
                        onChange={e =>
                          this.setState({ painWhileUrinating: e.target.value })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="pain-in-throat">
                        12.Do you experience pain or discomfort in your throat?
                      </FormLabel>
                      <RadioGroup
                        aria-label="pain-during-throat"
                        name="pain-during-throat"
                        onChange={e =>
                          this.setState({
                            pharyngealDiscomfort: e.target.value
                          })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <FormControl fullWidth className={classes.margin}>
                      <FormLabel htmlFor="expectant">
                        13.Are you expectant?
                      </FormLabel>
                      <RadioGroup
                        aria-label="expectant"
                        name="expectant"
                        onChange={e =>
                          this.setState({ expectant: e.target.value })
                        }
                      >
                        <FormControlLabel
                          value="yes"
                          control={<Radio />}
                          label="Yes"
                        />
                        <FormControlLabel
                          value="no"
                          control={<Radio />}
                          label="No"
                        />
                      </RadioGroup>
                    </FormControl>
                    <Button
                      variant="contained"
                      color="primary"
                      className={classes.margin}
                      onClick={this.updateSexualHistory}
                    >
                      Update sexual history
                    </Button>
                  </CardContent>
                </Card>
              </Paper>
            </Grid>
          </Grid>
        </Paper>
      </Container>
    );
  }
}

export default withStyles(styles)(Dashboard);
