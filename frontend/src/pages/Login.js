import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import { withStyles } from "@material-ui/core/styles";
import Container from '@material-ui/core/Container';
import logo from '../images/logo.png';
import { apiGet } from '../utils/api';

const styles = theme => ({
  '@global': {
    body: {
      backgroundColor: theme.palette.common.white,
    },
  },
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
});

class Login extends Component {
  state = {};
  submitLogin = async() => {
    const username = this.state.username;
    const password = this.state.password;

    const response = await apiGet('users');

    const user = response.filter(user => user.username === username);

    if(user.length) {
      // Add some validation here
      let dbPassword =  user[0].password;

      console.log(dbPassword);
      if (password === dbPassword) {
        // Redirect to Dashboard
        window.location = '/ss2frontend/dashboard';
      } else {
        alert("Invalid password");
      }
    } else {
      alert("Invalid username or password");
      // Add a fancy error handler later
      }

  }
  render() {
    const { classes } = this.props;
    return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
        <img src={logo} style={{ width:300, height:300}} className="App-logo" alt="logo" />
        </div>
        <div className={classes.paper}>
          <form className={classes.form} noValidate>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="id"
              label="Clinician Username"
              name="username"
              autoComplete="username"
              autoFocus
              onChange={(e) =>
                this.setState({ username: e.target.value})
              }
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={(e) =>
                this.setState({ password: e.target.value})
              }
            />
            <Button
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
              onClick={this.submitLogin}
            >
              Login
            </Button>
          </form>
        </div>
      </Container>
    );
  }
}

export default withStyles(styles)(Login);
