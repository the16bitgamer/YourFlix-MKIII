import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import * as serviceWorker from './serviceWorker';
import 'core-js/stable';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import HomePage from './HomePage';
import ShowPage from './Show/ShowPage';

ReactDOM.render(
  <React.StrictMode>
    <Router>
        <Switch>
          <Route path="/home">
            <HomePage />
          </Route>
          <Route path="/show">
            <ShowPage />
          </Route>
          <Route path="/">
            <HomePage />
          </Route>
        </Switch>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);

serviceWorker.unregister();
