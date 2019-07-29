/** @format */

import React from 'react';
import Speech from './components/Speech';
import sendRequest from './lib/request';
import { animalMap } from './lib/animals';

const animals = Object.keys(animalMap);

class App extends React.Component {
  state = {
    error: null,
    debug: false,
    animal: null,
    connected: false,
  };

  handleRecognized = result => {
    const animal = animalMap[result];
    sendRequest(`/animal/${animal}`, 'POST').then(
      response => {
        if (response.ok) {
          return this.setState({ animal });
        } else {
          switch (response.status) {
            case 404:
              this.setState({
                error: 'Der Endpunkt wurde nicht gefunden.',
                animal,
              });
              break;
            default:
              this.setState({
                error:
                  'Bei der Verbindung zum Server ist ein Fehler aufgetreten.',
                animal,
              });
          }
        }
      },
      error => {
        return this.setState({ error });
      }
    );
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Spracheingabe</h1>
        </header>
        <div className="container grid-lg">
          <div className="columns controls">
            <div className="column col-12">
              <Speech onRecognized={this.handleRecognized} targets={animals} />
            </div>
            <div className="column col-12">
              {this.state.animal && (
                <div className="toast toast-success">
                  <button
                    onClick={() => this.setState({ animal: null })}
                    class="btn btn-clear float-right"
                  />
                  {'Erkannt ' + this.state.animal}
                </div>
              )}
            </div>
            <div className="column col-12">
              {this.state.error && (
                <div className="toast toast-error">
                  <button
                    class="btn btn-clear float-right"
                    onClick={() => this.setState({ error: null })}
                  />
                  {this.state.error}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
