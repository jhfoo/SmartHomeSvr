import React, { Component } from 'react';
// import logo from './logo.svg';
// import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="ui grid container">
           <div className="four wide column"></div>
           <div className="eight wide column">
           Select an action<br/><br/>
            <div className="ui raised segment">
              <div className="ui middle aligned animated selection divided list">
                <div className="item">
                  <div className="right floated content">
                    <i className="icon chevron right"></i>
                  </div>
                  <div className="content">
                    <div className="header">Bedroom</div>
                    <div className="description">Turn lights ON</div>
                  </div>
                </div>
                <div className="item">
                  <div className="right floated content">
                    <i className="icon chevron right"></i>
                  </div>
                  <div className="content">
                    <div className="header">Bedroom</div>
                    <div className="description">Turn lights OFF</div>
                  </div>
                </div>
              </div>
            </div>
           </div>
           <div className="four wide column"></div>
        </div>
      </div>
    );
  }
}

export default App;
