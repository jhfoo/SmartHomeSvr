import React, { Component } from 'react';
// import logo from './logo.svg';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import {List, ListItem} from 'material-ui/List';
import Subheader from 'material-ui/Subheader';
import Toggle from 'material-ui/Toggle';
import Paper from 'material-ui/Paper';

// custom
import './App.css';
import Header from './Header';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            BedroomLight: false
        };

        this.onToggleLight = this.onToggleLight.bind(this);
    }

    onToggleLight() {
        var NewLightState = !this.state.BedroomLight;
        console.debug('App.onToggleLight(): ' + NewLightState);

        if (NewLightState)
            window.socket.emit('DeviceAction', {
            ip:'192.168.1.18',
            state: 'ON'
            });
        else
            window.socket.emit('DeviceAction', {
            ip:'192.168.1.18',
            state: 'OFF'
            });

        this.setState({
            BedroomLight: NewLightState
        })
    }

  render() {
    return (
        <MuiThemeProvider>
            <div className="App">
                <Header/>
                <div className="grid-container">
                    <div className="grid-20 tablet-grid-25">
                        <span className="hide-on-mobile">Boo</span>
                    </div>
                    <div className="grid-60 tablet-grid-75">
                        <Paper zDepth={1}>
                            <List>
                                <Subheader>Home Controls</Subheader>
                                <ListItem primaryText="Bedroom lights" rightToggle={
                                    <Toggle onToggle={() => this.onToggleLight()} toggled={this.state.BedroomLight} />} />
                            </List>
                        </Paper>
                    </div>
                    <div className="grid-20 tablet-grid-25">
                        <span className="hide-on-mobile hide-on-tablet">Whitespace</span></div>
                </div>
            </div>
        </MuiThemeProvider>
    );
  }
}

export default App;
