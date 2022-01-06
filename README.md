# How to run
1. Clone this repo
2. Use existing aws profile or run `aws configure --profile <profile-name>` to create a new AWS profile
3. Add the aws profile <profile-name> to the `cdk.json` file under `profile` section
4. Create virtual environment: `python3 -m venv .venv` and activate it: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt` 
6. Run `cdk synth`
7. Run `cdk deploy --all`
# Test
The DNS name for the API-gateway will be output in the end of the stack deployment. 
It looks something like this in the terminal:

`Outputs:
CDK-API-STACK.APIGATEWAYEndpoint8F624808 = https://EXAMPLE.eu-west-2.amazonaws.com/prod/`

Head to that url. It will contain two sub-urls:

* https://EXAMPLE.eu-west-2.amazonaws.com/prod/hello-s3 (displaying index.html) 
* https://EXAMPLE.eu-west-2.amazonaws.com/prod/hello-fargate (displaying the nginx containers from the fargate service)

# Challenge 1: Automatically provisioning stacks
We want to introduce an API in a separate stack that owns the users and their properties.

Using Amazon CDK, please write a script that will provision a stack with needed components for this, like:

A Dynamo database

A container running on Fargate

A load balancer pointing at the containers

(optional) A setup with API Gateway

S3 buckets for storage of static objects


You can use any programming language you prefer. If you don’t care, we use Python.

## TODOs:
- :white_check_mark: Initial setup (cdk, libs, AWS account etc.)
- :white_check_mark: Deploy Dynamo table
- :white_check_mark: Fargate container running Nginx
- :white_check_mark: AWS Loadbalancer
- :white_check_mark: S3 bucket
- :white_check_mark: (optional) API Gateway
- :white_check_mark: (optional) Use API Gateway to display data (s3, dynamodb, fargate)

### Improvements
- Deletion of s3 bucket on `cdk destroy`
- Add data to Dynamodb table
- "Expose" Dynamodb table data
- Add tests

# Challenge 2: Case: Slow loading pages 
### The Problem
Imagine that CompanyA has player profile pages, where the individual player can see his video snippets and stats.
However, these pages have started loading quite slowly, with 5% of the pages taking over 20 seconds to load and display.

Try to describe the troubleshooting you would perform on this problem, and possible mitigations and solutions.

(It is recognized that nothing is known about the stack, so feel free to make assumptions wildly)


### Troubleshooting the problem/root-cause:
My initial and overall thoughts on this, is the problem can be one or more of:
1. Network (ex: large data)
2. Processing in the client/page (ex: filter/sorting of data)
3. Long backend request (ex: complex/slow database query)


1a. Using the browser's network tab, inspect the loading time and different requests that are made from the pages. This will potentially show if the issues are network related and what/which requests are the cause. 
Notice if the pages gets data from a single or multiple endpoints (API).

2a. If possible, obtain the code for the page and see if anything (obvious) stands-out. This could be some some form of processing (sorting/filtering) of some data. An example could be that the page is requesing all players video snippets and stats, and then filtering that list, to only show a single player (bad design).

Try to see if its possible to reproduce the problem locally to enable easier troubleshooting and debugging, and later on, to confirm that the proposed solution actually solves the problem. 

3a. Try to request the same endpoints as the client from another client, such as Postman, to inspect the loading times of each request. This will help narrow down the scope of the problem and determine if its backend or client/frontend related.


### Solutions:
Assumptions:
1. That the backend is well-done and serves the clients request quickly and is not considered part of the problem
2. The pages requests all data in single calls to the backend(s)
3. That the request is made synchronously with the rest of the page, which means that the load of the page is blocked, until this request completes, which causes the overall page to "hang" (loading slowly)

The troubleshooting has shown that the client receives all the data quickly from the backend, but displays the data slowly causing a high load time. To circumvent this, the following needs to be done:
1. Split the single request to the backend into multiple, and let the pages display data of each of these separate from the others and let the page load asynchronously, but display loading elements / spinners where data is taking a longer time to load. 
2. Consider if some of the requests that is taking a long time, can be loaded in the background before being needed (pre-rendered). Ie, if this data is displayed/needed on another page than the landing page, pre-render / load the data asynchronously in the background while loading the landing page, to have the data available on the subpages when the user navigates there. 


# Challenge 3: Prior code
Attach a piece of code you have written, that you are particularly proud of or is noteworthy, and describe why you chose this and what is particular about it.


## Code
[hydra_jobscheduler.py](hydra_jobscheduler.py)

## Reason
I have selected this piece of code which is class part of a Django app named Hydra. This is a service, which processes all our data using Kubernetes as the "batch job" engine, producing videos and matching GPS points to road segments.
Hydra is what produces business value of the incoming data (gps, gyroscope and photos) using Kubernetes. It runs entirely without user-intervention and users can easily add more Jobs using a Django webform 

The jobscheduler attached here, is responsible for conneting the Django app with the k8s cluster and dynamically creating a k8s Job based on some user-specified job arguments ([see image](hydra_jobspec.png))

Im more proud of the Hydra project and the value it creates, than of this specific class, but I did include this class as its a key component for Hydra.
