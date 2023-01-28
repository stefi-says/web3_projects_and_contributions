# Sybil  Checks Package 

`pip install SybilChecks`

` from SybilChecks import checks`

## Intro

This package was developed during ODC Data Builders Hackathon on Jan-2023, [OpenData Community](https://opendatacommunity.org/) . It intends to make it easier to do first basic checks on donors of public funds rounds. It can integrate systems of risk analysis as a ‘Lego’ for feature engineering or as a start for further data analysis on wallets. It cointans 5 functions, 4 of them tests behaviours and flags booleans outputs for the behaviour tested ,and 1 returns a dataset of historical transactional data till the current date. 

The functions were based on previous experience on web2 fraud detection and prevention, for example `account_age` analogue to `first_trx_during_round` function on this context, and exclusive on-chain feature peculiarities as in `wallet_initiated_by` to check close relations between different donors and grantees.

One principle that I kept in mind during the construction of this package  was  the ‘easy to use’  principle in an attempt that round owners, data analysts or people with little experience could run it and culminate in Sybil identification. 



## Why use it		

In the context for this package was developed, Sybil attack is a  kind of fraud in which the attacker seeks an ROI over each donation in a public funds round. To maximise that, the attackers create fake wallets to make donations, as the quadratic voting system used to distribute the funds, prioritise the distribution of funds due to majority preferences.  For more information, please check [ODC FAQs](https://opendatacommunity.org/docs/faq/) where you can find resources explaining this fraud. 

Giving attackers must split their funds through various accounts, the  benefits in using this package is to enhance the cost of forgery for fraudsters as, for example,  they will be forced to:			

- Initiate wallets and wait till rounds being announced as initiating wallets during the  round could flag them and indicate their presence. This could enhance their risk as money would be stuck in these wallets while markets fluctuates. 		
 - Enhance their ‘fake wallets layers’ as they will need to perform at least one transaction between the wallets that distribute the funds,  and the wallets that make donations. Forcing the wallets that distribute the funds to not make donations on the round otherwise it could be flagged too. 		
- Fraudsters' wallets that made donations would be forced to not transact between them otherwise they would be flagged too. 		

As fraudsters would try to avoid being flagged and good users would not, the cost of forgery would enhance, but not the current cost of making donations as a good user. 		

## When use it		

Round owners can elaborate on the moment to use the package giving their other algorithms and preventing systems. For example, they could run the `first_trx_during_round` and the `wallet_initiated` functions on every new wallet that makes donations to the round even in real time, and the `wallets_trx_during_round`  every x hours to verify suspicious interactions. 

They could  test too differents relations like confront transactions:		
- grantees x grantees 		
- donors x grantees 				
- grantees X donors 		

This could be done in different moments for different relations
 


## How it works

The package was created using [Covalent API](https://www.covalenthq.com/docs/api/#/0/0/USD/1), a decentrilized network of nodes, therefore it is imperative that the users get an [<api_key>](https://www.covalenthq.com/) , as it is a necessary  variable on every function. 

### Functions variables :   

`wallet_id` = type: ‘str’, wallet address that will be evaluated    
`api_key` = type: ‘str’, your covalent api_key   
`chain_id` = type: ‘str’, covalent id for the network you want the historical transactions    
`round_start` = type: ‘str’, format : ‘%Y-%m-%d’,  date of the round start or date when the round was announced. Example : ‘2022-12-05’   
 `round_finish` =  type: ‘str’, format : ‘%Y-%m-%d’,  date of the round end or date when donors were not able to make donations anymore. Example : ‘2022-12-31’    
 `list_for_testing` = type : ‘list’, present on the `wallet_initiated ` module, it should contain a list of unique wallet addresses of donors and grantees but not the wallet tested .     
 `wallets_lists` = type : ‘list’, present on the `wallet_historical_trx`  module, it should contains all wallets address that is intended to get the lifetime transactional data on the specified `chain_id`   



### Functions:     


`first_trx_during_round(wallet_id, api_key, chain_id, round_start, round_finish)`:      
	Function tests if the wallet was ‘initiated’ (tried its first transaction), on the specific chain tested,  during the period specified. This module does not distinguish between failed or successful transactions. Output: list['wallet_id', True/False]

`wallet_initiated_by(wallet_id, api_key, chain_id, list_for_testing)` :    
	Function tests if the first funds were received by one of the wallets in the <list_for_testing> variable . It returns ‘True’ only if the first successful and not ‘0’ value transaction was made by some of the wallets in the list. Output: list['wallet_id', True/False]

 Example:     
	Trx_1 : from x_wallet / successful : False / value: 1 (function will discart)     
	Trx_2 : from x_wallet / successful : True / value: 0 (function will discart)    
	Trx_3 : from n_wallet / successful : True / value: 10 (function will accept)    
	If  `list_for_testing` contains  'n_wallet' then module returns `True`    



`trx_between_wallets(wallet_id, api_key, chain_id, list_of_donors)` :    
	 Function tests if round donors have transitioned between themselves, there is not distinction between successful and failed transactions nor about when these transactions occurred.  In this module `wallet_id` must be in `list_of_donors`. Output: list['wallet_id', True/False]

`wallets_trx_during_round(wallet_id, api_key, chain_id, round_start, round_finish, list_of_donors)` :     
	 Function tests if round donors have transitioned between themselves during the period of grant round or announcement of the round, there is no distinction between successful and failed transactions.   wallet_id must be in list_of_donors. Output: list['wallet_id', True/False]

`wallet_historical_trx(wallets_list , api_key, chain_id)`:    
	This function was developed to make it easier to get historical transactional data from a list of wallets. It bridges the gap between the API usage and a final treated dataset. 


### Further development:    

The package has little study around time optimization due to hackathon time constraints. It can be slow when used to check a lot of wallets  owing to  making one API call for each function ‘check’. Further development would include:       

  * modules to import and treat a dataset and use it to retrieve the validations for the other modules.
  * One module that builds and processes networks algorithms and returns network metrics as degree of centrality, closeness and so on .. 


### Acknowledgements to:    

* Covalent Network, due to the service and support on their discord     
* Simon from [ 0x9simon ](https://twitter.com/csctgrace/status/1605835545040412673) due to his discussion around Gas Provision Network. It inspired the construction of the module ‘wallet_initiated’      

If you want to contribute, please contact Stefi :) 








