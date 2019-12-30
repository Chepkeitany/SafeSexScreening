import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Recommendation from './pages/Recommendation';

export default function App() {
  return (
    <Router basename='/ss2frontend'>
        <Switch>
          <Route exact path="/" component={Login} />
          <Route path="/dashboard" component={Dashboard} />
          <Route path="/recommendation" component={Recommendation} />
        </Switch>
    </Router>
  );
}
