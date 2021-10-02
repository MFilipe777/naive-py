# naive-py

A python implementation of [naivecoin](https://github.com/lhartikk/naivecoin/tree/master). Uses [python-p2p-network](https://github.com/macsnoeren/python-p2p-network) for the p2p server. WIP; Made for fun :) .

## Dependencies

- Flask 
> pip install flask
- p2pnetwork
> pip install p2pnetwork

## Running

> python3 main.py

## Endpoints
- `/blocks` - Returns a list of every block mined so far. - GET
- `/mine_block` - Adds a block to the blockchain. - POST

| Name | Content  |  
|---| --- |
| data | < data : str > |  
  
- `/peers` - Returns a list of every connected peer. - GET
- `/add_peer` - Connects with peer; receives host and port of peer as body. - POST  

| Name |     Content     |  
|------|-----------------|  
| host | < host : str >  |  
| port | < port : int >  |  
