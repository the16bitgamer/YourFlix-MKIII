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
import NewPage from './NewPage/NewPage';
import ProgramPage from './ProgramPage/ProgramPage';
import SearchPage from './Search/SearchPage';
import ShowPage from './Show/ShowPage';
import VideoPage from './Video/VideoPage';

ReactDOM.render(
  <React.StrictMode>
    <Router>
        <Switch>
          <Route path="/Programs">
            <ProgramPage />
          </Route>
          <Route path="/New">
            <NewPage />
          </Route>
          <Route path="/Search">
            <SearchPage />
          </Route>
          <Route path="/Show">
            <ShowPage />
          </Route>
          <Route path="/Video">
            <VideoPage />
          </Route>
          <Route path="/">
            <ProgramPage />
          </Route>
        </Switch>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);

serviceWorker.unregister();
