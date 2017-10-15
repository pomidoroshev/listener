import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';


const HOST = '127.0.0.1:8000'
const URL = `http://${HOST}/`
const WS_URL = `ws://${HOST}/ws`


class List extends Component {

  constructor(props) {
    super(props);
    this.state = {
      items: []
    }
  }
  

  openWebsocket(chatId) {
    let Socket = window.MozWebSocket || WebSocket;
    this.ws = new Socket(WS_URL);

    this.ws.onopen = () => {
      console.log('aaa')
      this.ws.send('open');
    };

    this.ws.onmessage = (e) => {
      let message = JSON.parse(e.data);
      if (message.item) {
        message.item.id = Number(message.item.id);
      }
      let items = this.state.items;
      
      if (message.action === 'insert') {
        items.push(message.item);
      } else if (message.action === 'update') {
        items = items.map(element => {
          if (element.id === message.item.id) {
            element.data = message.item.data;
          }
          return element;
        });
      } else if (message.action === 'delete') {
        items = items.filter(element => element.id !== message.item.id)
      }
      this.setState({
        items: items
      })
    };
  }

  componentDidMount() {
    fetch(URL, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(resp => {
      console.log(resp.status)
      if (resp.status === 200) {
        return resp.json();
      } else {
        throw resp.status;
      }
    }).then(items => {
      console.log(items)
      this.setState({
        items: items,
      });
    })

    this.openWebsocket();
  }

  render() {
    return (
      <ul className='list'>
        {this.state.items.map(item => (<li key={item.id}>{item.data}</li>))}
      </ul>
    );
  }
}


class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <List />
      </div>
    );
  }
}

export default App;
