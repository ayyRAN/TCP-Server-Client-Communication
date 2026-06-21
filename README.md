# TCP-Server-Client-Communication
A simple TCP based application created on Python using socket programming that allows for three concurrent users to connect and send messages to a server host.
### 5 Expected Functions:
1. Echo with uppercase ACK transformation
2. Sending `status` returns a valid JSON of connect/disconnect timestamps
3. Max clients = 3 (4th concurrent client is rejected)
4. Sending `exit` closes the connection cleanly and frees up a client slot
5. An abrupt disconnection without `exit` closes connection cleanly

`Pytest` is used to handle each of these tests on every Git push. If one of these tests fails, the workflow is marked as a fail. The `run_server.sh` script can be run manually to accomplish the same thing, but saves the result to a log file for easy debugging.

## CI Pipeline

Every push to `main` runs the full suite via GitHub Actions. The workflow:

1. Spins up a clean Ubuntu environment
2. Installs dependencies
3. Runs `pytest` 
4. Returns a pass/fail status depending on test results

