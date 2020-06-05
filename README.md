# Goals
- Long term goals: unclear 
- Short term goals: 
  - Set up ESP-based environment monitors
  - Set up Prometheus exports to key data
  - (Optional) Set up Grafana to visualise Prometheus data

# Installation

```
git clone https://github.com/jhfoo/SmartHomeSvr
npm install
npm start
```

# Defaults
- Starts up server listening on port 8080
- Uses Supervisor to auto restart on code change
- Edit config.json to override defaults

# Supported devices
- [Edimax SP2101W](https://github.com/mwittig/edimax-smartplug)


# Todos
Where does one begin? There's so much to do!
- Tests!
- Production npm startup
- Feature parity between REST API and Websocket
- Document APIs
