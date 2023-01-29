# About This Repo

In this repo you will find a python notebook (.ipynb) that is a submission to  [The OpenData Community "DataBuilders" Hackathon](https://gitcoin.co/hackathon/DataBuilders?) . It aims to do a exploratory data analysis on the wallets that made donations  on the [Climate Solutions Round](https://grant-explorer.gitcoin.co/#/round/1/0x1b165fe4da6bc58ab8370ddc763d367d29f50ef0) of Gitcoin Grants Protocol. It will utilises SybilChecks python package, developed for the [Packaging Algorithms into Legos Bounty](https://github.com/opendataforweb3/jan2023hackathon/issues/2) to perform basics checks around suspicious behaviours of these voters. More information about the package can be found in [sybil start checks page](https://github.com/stefi-says/web3_projects_and_contributions/tree/main/sybil_start_checks_package/sybil_start_checks).

You will also find the datasets used to perform this analyses:  
`climate_grant_applications.csv` 
`climate_grant_votes.csv`

a dataset that contains the voters wallets and the answer for the checks made on them:    
`clima_solution_first_checks.csv`

 and finally a dataset produce with SybilChecks package function `checks.wallet_historical_trx()` , that contains all the historical transactional data of all the wallets involved on the round (voters and grantees) using the Ethereum Network:   
[clima_solution_wallets_trx.csv](https://drive.google.com/file/d/15_1bNhwM6pm_9nLujJGHjrcfdJiebBL5/view?usp=sharing)

Any feedback, please contact me :) 
